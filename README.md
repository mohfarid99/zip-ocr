# ZIP OCR Search (FastAPI + docTR)

A lightweight prototype for an **“image scan extraction”** system.

This project allows you to:

1. **Upload a ZIP file** containing images  
2. **Extract text** from all images using **docTR (deep-learning OCR)**  
3. Save all results into **output.csv** (`filename`, `text`)  
4. **Search any keyword** against the CSV without re-uploading the ZIP  

---

## ✨ Features

- 🔤 OCR using **docTR** (Deep Learning, PyTorch backend)
- 📦 Upload ZIP with images: `.png`, `.jpg`, `.jpeg`, `.bmp`
- 🧾 Automatically generates `output.csv` containing OCR results
- 🔍 Search text multiple times after extraction without re-uploading ZIP
- 🌐 Simple UI using FastAPI + Jinja2 templates

---

## 📁 Project Structure

```text
.
├── images/          # (optional) sample images
├── templates/
│   └── index.html   # Web UI
├── main.py          # FastAPI backend
├── output.csv       # Generated OCR results (auto-created)
├── images.zip       # Example ZIP (optional)
├── requirements.txt
└── .gitattributes

# 🚀 Step-by-Step Setup & Usage

Follow these instructions to run the project locally.

---

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/<your-username>/zip-ocr.git
cd zip-ocr
Replace <your-username> with your GitHub username.

2️⃣ Create & Activate Python Environment
Option A — Using Conda (recommended)
bash
Copy code
conda create -n zip-ocr python=3.10 -y
conda activate zip-ocr
Option B — Using venv
bash
Copy code
python -m venv venv
Windows:

bash
Copy code
venv\Scripts\activate
Linux / macOS:

bash
Copy code
source venv/bin/activate
3️⃣ Install Dependencies
bash
Copy code
pip install -r requirements.txt
⚠️ The first run may download docTR OCR models — this can take a few minutes.

4️⃣ Run the FastAPI Server
Option A — Run main.py directly
bash
Copy code
python main.py
Option B — Use Uvicorn manually
bash
Copy code
uvicorn main:app --reload
You should see:

nginx
Copy code
Uvicorn running on http://0.0.0.0:8000
5️⃣ Open the Web Application
Open your browser and go to:

cpp
Copy code
http://127.0.0.1:8000/
You will see two sections:

🧾 Step 1 — Upload ZIP & Extract Text (One Time Per ZIP)
In Section 1, click Choose File and select a .zip that contains images.

Click Upload & Extract.

The system will:

Extract all images

Run OCR using docTR

Save results to output.csv

You will see a message like:

ZIP extracted successfully. 14 images processed.

Note: Every new upload overwrites the previous output.csv.

🔍 Step 2 — Search Text (Can Be Repeated Unlimited Times)
In Section 2, type any keyword or phrase.

Click Search.

The system will:

Load output.csv

Perform a case-insensitive search

List all image filenames where the OCR text matches

If no CSV exists:

CSV does not exist. Upload ZIP first.

🧠 How It Works Internally
➤ Upload ZIP (POST /upload_zip)
Unzip images

Run docTR OCR

Save results to output.csv

➤ Search Text (POST /search_text)
Load CSV

Search text (case-insensitive)

Return matching filenames

🔧 Possible Future Improvements
Add download button for the CSV

Display extracted text per image in UI

Show image thumbnails

Highlight matched text

Use SQLite instead of CSV

Add authentication for production use
