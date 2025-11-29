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

os.environ["USE_TORCH"] = "1"

from doctr.models import ocr_predictor

# -------------------------------------------------
# FastAPI
# -------------------------------------------------
app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Load docTR once
ocr_model = ocr_predictor(pretrained=True)

CSV_PATH = "output.csv"


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
def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "results": None,
            "query": "",
            "error": "",
            "upload_msg": ""
        }
    )


# ======================================================
# 1. UPLOAD ZIP → OCR → SAVE CSV
# ======================================================
@app.post("/upload_zip", response_class=HTMLResponse)
async def upload_zip(
    request: Request,
    zip_file: UploadFile = File(...)
):
    if not zip_file.filename.lower().endswith(".zip"):
        return templates.TemplateResponse("index.html", {
            "request": request,
            "results": None,
            "query": "",
            "error": "",
            "upload_msg": "Please upload a ZIP file."
        })

    zip_bytes = await zip_file.read()
    extracted_rows = []

    try:
        with zipfile.ZipFile(io.BytesIO(zip_bytes)) as z:
            for fname in z.namelist():
                if fname.lower().endswith((".png", ".jpg", ".jpeg", ".bmp")):
                    with z.open(fname) as img_file:
                        image = Image.open(io.BytesIO(img_file.read()))
                        text = extract_text_with_doctr(image)
                        extracted_rows.append([fname, text])
    except Exception as e:
        return templates.TemplateResponse("index.html", {
            "request": request,
            "results": None,
            "query": "",
            "error": "",
            "upload_msg": f"Error: {e}"
        })

    # Write CSV
    with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
        csv.writer(f).writerows([["filename", "text"]] + extracted_rows)

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "results": None,
            "query": "",
            "error": "",
            "upload_msg": f"ZIP extracted successfully. {len(extracted_rows)} images processed."
        }
    )


# ======================================================
# 2. SEARCH TEXT USING CSV ONLY
# ======================================================
@app.post("/search_text", response_class=HTMLResponse)
def search_text(
    request: Request,
    query: str = Form(...)
):
    if not os.path.exists(CSV_PATH):
        return templates.TemplateResponse("index.html", {
            "request": request,
            "results": None,
            "query": query,
            "error": "CSV does not exist. Upload ZIP first.",
            "upload_msg": ""
        })

    results = []
    query_lower = query.lower().strip()

    with open(CSV_PATH, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if query_lower in row["text"].lower():
                results.append(row["filename"])

    return templates.TemplateResponse("index.html", {
        "request": request,
        "results": results,
        "query": query,
        "error": "",
        "upload_msg": ""
    })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
