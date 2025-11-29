import io
import zipfile
import csv
from typing import List

from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from PIL import Image
import numpy as np
import os

# docTR uses PyTorch by default
os.environ["USE_TORCH"] = "1"

from doctr.models import ocr_predictor

# -------------------------------------------------
# FastAPI initialization
# -------------------------------------------------
app = FastAPI()
templates = Jinja2Templates(directory="templates")

# -------------------------------------------------
# Load docTR OCR model globally (only once)
# -------------------------------------------------
print("Loading docTR OCR model...")
ocr_model = ocr_predictor(pretrained=True)
print("docTR model loaded!")


# -------------------------------------------------
# DOC TR OCR function
# -------------------------------------------------
def extract_text_with_doctr(pil_image: Image.Image) -> str:
    img_rgb = pil_image.convert("RGB")
    img_np = np.array(img_rgb)

    result = ocr_model([img_np])
    output = result.export()

    words = []
    for page in output.get("pages", []):
        for block in page.get("blocks", []):
            for line in block.get("lines", []):
                for word in line.get("words", []):
                    value = word.get("value", "")
                    if value:
                        words.append(value)

    return " ".join(words)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "results": None, "query": "", "error": ""}
    )


# -------------------------------------------------
# MAIN SEARCH & CSV GENERATION LOGIC
# -------------------------------------------------
@app.post("/search", response_class=HTMLResponse)
async def search_in_zip(
    request: Request,
    zip_file: UploadFile = File(...),
    query: str = Form(...)
):

    if not zip_file.filename.lower().endswith(".zip"):
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "results": None, "query": query,
             "error": "Please upload a .zip file."}
        )

    # Read zip into memory
    zip_bytes = await zip_file.read()

    extracted_rows = []     # for csv
    matched_files = []      # search results
    error_msg = ""

    print("\n========== NEW REQUEST ==========")
    print(f"Query: {query!r}")

    # -----------------------------------------
    # Extract ZIP & OCR all images
    # -----------------------------------------
    try:
        with zipfile.ZipFile(io.BytesIO(zip_bytes)) as z:
            names = z.namelist()
            print("Files inside zip:", names)

            image_ext = (".png", ".jpg", ".jpeg", ".tiff", ".bmp", ".gif")

            for fname in names:
                if not fname.lower().endswith(image_ext):
                    print("Skipping (not image):", fname)
                    continue

                print("\n--- OCR image:", fname)
                try:
                    with z.open(fname) as img_file:
                        image_data = img_file.read()

                    img = Image.open(io.BytesIO(image_data))
                    text = extract_text_with_doctr(img)

                    print("OCR text:", text[:100], "...")

                    # Save row for CSV
                    extracted_rows.append([fname, text])

                except Exception as e:
                    print("OCR ERROR:", e)

    except zipfile.BadZipFile:
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "results": None, "query": query,
             "error": "Invalid ZIP file."}
        )

    # ------------------------------------------------
    # Write CSV file (output.csv)
    # ------------------------------------------------
    csv_path = "output.csv"
    print("Saving CSV to:", csv_path)

    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["filename", "extracted_text"])
        writer.writerows(extracted_rows)

    print("CSV saved successfully.")

    # ------------------------------------------------
    # SEARCH in the generated CSV instead of raw OCR
    # ------------------------------------------------
    print("\nSearching for:", query)

    query_lower = query.lower().strip()

    for fname, text in extracted_rows:
        if query_lower in text.lower():
            matched_files.append(fname)

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "results": matched_files,
            "query": query,
            "error": error_msg,
        },
    )


# Run using: python main.py
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
