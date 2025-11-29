# ZIP OCR Search (FastAPI + docTR)

A lightweight prototype for an “image scan extraction” system.

This project allows you to:
1. Upload a ZIP file containing images
2. Extract text from all images using docTR (deep-learning OCR)
3. Save all results into output.csv (filename, text)
4. Search any keyword against the CSV without re-uploading the ZIP

---

## Features

- Deep-learning OCR using docTR (PyTorch backend)
- Upload ZIP containing images: .png, .jpg, .jpeg, .bmp
- Automatically creates output.csv with extracted text
- Search text multiple times without re-uploading ZIP
- Simple UI using FastAPI + Jinja2 templates

---

## Project Structure

\`\`\`
.
├── images/             
├── templates/
│   └── index.html      
├── main.py             
├── output.csv          
├── images.zip          
├── requirements.txt
└── .gitattributes
\`\`\`

---

# Step-by-Step Setup & Usage

Follow these instructions to run the project locally.

---

## 1 Clone the Repository

```bash
git clone https://github.com/<your-username>/zip-ocr.git
cd zip-ocr
```

Replace <your-username> with your GitHub username.

---

## 2️ Create & Activate Python Environment

### Option A — Conda
```bash
conda create -n zip-ocr python=3.10 -y
conda activate zip-ocr
```

### Option B — venv
```bash
python -m venv venv
```

Windows:
```bash
venv\Scripts\activate
```

macOS / Linux:
```bash
source venv/bin/activate
```

---

## 3️ Install Dependencies

```bash
pip install -r requirements.txt
```

⚠️ First run may download docTR model files (takes a few minutes).

---

## 4️ Run the FastAPI Server

### Option A — Run main.py
```bash
python main.py
```

### Option B — Use Uvicorn
```bash
uvicorn main:app --reload
```

You should see:
```
Uvicorn running on http://0.0.0.0:8000
```

---

## 5️5 Open the Web Application

Open your browser at:
```
http://127.0.0.1:8000/
```

---

# 🧾 Step 1 — Upload ZIP & Extract Text

1. Click "Choose File" and select a ZIP containing images  
2. Click "Upload & Extract"

The system will:
- Extract all images  
- Run OCR using docTR  
- Save results into output.csv  

You will see:
> ZIP extracted successfully. XX images processed.

⚠️ Every new upload overwrites the previous output.csv.

---

## Search Text

1. Enter any keyword  
2. Click "Search"

The system will:
- Load output.csv  
- Search text (case-insensitive)  
- Show filenames containing the keyword  

If output.csv doesn't exist:
> CSV does not exist. Upload ZIP first.

---

## How It Works Internally

### Upload ZIP (POST /upload_zip)
- Unzip ZIP contents  
- Run docTR OCR on each image  
- Save results to output.csv  

### Search Text (POST /search_text)
- Read output.csv  
- Case-insensitive matching  
- Return matching filenames  

---

## License
This project is a prototype for demonstration and portfolio usage.
Feel free to modify and extend it.
