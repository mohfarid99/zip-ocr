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

