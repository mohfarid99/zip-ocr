# ZIP OCR Search (FastAPI + docTR)

A lightweight prototype for an “image scan extraction” system.

This project allows you to:
1. Upload a ZIP file containing images
2. Extract text from all images using docTR (deep-learning OCR)
3. Save all results into output.csv (filename, text)
4. Search any keyword against the CSV without re-uploading the ZIP

------------------------------------------------------------
## ✨ Features
------------------------------------------------------------
- Deep-learning OCR using docTR (PyTorch backend)
- Upload ZIP containing images: .png, .jpg, .jpeg, .bmp
- Automatically creates output.csv with extracted text
- Search text multiple times without re-uploading ZIP
- Simple UI using FastAPI + Jinja2 templates

------------------------------------------------------------
## 📁 Project Structure
------------------------------------------------------------
.
├── images/             (optional)
├── templates/
│   └── index.html
├── main.py
├── output.csv          (auto-created)
├── images.zip          (optional)
├── requirements.txt
└── .gitattributes

------------------------------------------------------------
# 🚀 Step-by-Step Setup & Usage
------------------------------------------------------------
Follow these instructions to run the project locally.

------------------------------------------------------------
## 1️⃣ Clone the Repository
------------------------------------------------------------
git clone https://github.com/<your-username>/zip-ocr.git
cd zip-ocr

(Replace <your-username> with your GitHub username.)

------------------------------------------------------------
## 2️⃣ Create & Activate Python Environment
------------------------------------------------------------

Option A — Conda:
    conda create -n zip-ocr python=3.10 -y
    conda activate zip-ocr

Option B — venv:
    python -m venv venv

Windows:
    venv\Scripts\activate

macOS / Linux:
    source venv/bin/activate

------------------------------------------------------------
## 3️⃣ Install Dependencies
------------------------------------------------------------
pip install -r requirements.txt

Note: The first run may download docTR model files (takes a few minutes).

------------------------------------------------------------
## 4️⃣ Run the FastAPI Server
------------------------------------------------------------

Option A — Run main.py:
    python main.py

Option B — Use Uvicorn:
    uvicorn main:app --reload

If successful, you will see:
    Uvicorn running on http://0.0.0.0:8000

------------------------------------------------------------
## 5️⃣ Open the Web Application
------------------------------------------------------------
Open this in your browser:
    http://127.0.0.1:8000/

You will see two main sections.

------------------------------------------------------------
# 🧾 Step 1 — Upload ZIP & Extract Text (One Time Per ZIP)
------------------------------------------------------------
1. Click “Choose File” and select a .zip containing images.
2. Click “Upload & Extract”.

The system will:
- Extract all images
- Run OCR using docTR
- Save results into output.csv

You will see:
    ZIP extracted successfully. X images processed.

IMPORTANT:
Every new upload overwrites the previous output.csv.

------------------------------------------------------------
# 🔍 Step 2 — Search Text (Unlimited Times)
------------------------------------------------------------
1. Enter any keyword or phrase.
2. Click “Search”.

The system will:
- Load output.csv
- Perform case-insensitive search
- Display image filenames containing the keyword

If no CSV exists:
    CSV does not exist. Upload ZIP first.

------------------------------------------------------------
# 🧠 How It Works Internally
------------------------------------------------------------

Upload ZIP (POST /upload_zip):
- Unzip input file
- Extract images
- Run OCR with docTR
- Save (filename, text) to output.csv

Search Text (POST /search_text):
- Load output.csv
- Perform case-insensitive matching
- Return matching filenames

------------------------------------------------------------
# 🔧 Possible Future Improvements
------------------------------------------------------------
- Add Download CSV button
- Show extracted OCR text per image
- Display image thumbnails
- Highlight matched text
- Use SQLite instead of CSV
- Add authentication (for production use)

------------------------------------------------------------
## 📄 License
------------------------------------------------------------
This project is a prototype for demonstration and portfolio purposes.
Feel free to modify and extend it as needed.
