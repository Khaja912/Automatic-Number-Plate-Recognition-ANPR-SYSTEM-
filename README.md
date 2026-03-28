
# 🚘 Indian ANPR Pro (Streamlit-Based)

## 📌 Overview

**Indian ANPR Pro** is a modern **Automatic Number Plate Recognition (ANPR) web application** built using **Streamlit**, **EasyOCR**, and **OpenCV**.

It allows users to:

* 📷 Capture license plates using camera
* 🖼️ Upload images
* 🎥 Analyze videos
* ⌨️ Manually search vehicle details

The system detects number plates and matches them with a **vehicle database (CSV)** using **exact + fuzzy matching**.

---

## ✨ Features

* 📷 Real-time camera capture
* 🖼️ Image upload detection
* 🎥 Video frame analysis (every 30th frame)
* 🔍 Manual license plate search
* 🧠 OCR using EasyOCR
* 🔎 Fuzzy matching using SequenceMatcher
* 🎯 Supports Indian vehicle format
* 🎉 Visual feedback (balloons, metrics, progress bar)

---

## 🛠️ Tech Stack

* **Frontend/UI:** Streamlit
* **Backend:** Python
* **OCR Engine:** EasyOCR
* **Computer Vision:** OpenCV
* **Data Handling:** Pandas
* **Image Processing:** PIL, NumPy

---

## 📂 Project Structure

```
Indian-ANPR-Pro/
│
├── app.py                         # Main Streamlit app (your code)
├── indian_vehicle_database.csv   # Vehicle database (8 columns)
├── requirements.txt              # Dependencies
└── README.md                     # Documentation
```

---

## 📊 Dataset Format (IMPORTANT)

Your CSV must contain **exactly these 8 columns**:

```
license_plate
state_code
state_name
make
model
owner_name
phone
synthetic_id
```

---

## ⚙️ Installation

### 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/indian-anpr-pro.git
cd indian-anpr-pro
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Install Required System Packages

#### EasyOCR dependencies:

```bash
pip install easyocr opencv-python-headless
```

---

## ▶️ Run the App

```bash
streamlit run app.py
```

App will open in browser:

```
http://localhost:8501
```

---

## 🔍 How It Works

### 📷 Camera / 🖼️ Photo

1. Capture/upload image
2. Convert to grayscale
3. Apply OCR using EasyOCR
4. Clean text using regex
5. Validate plate format
6. Search in database

---

### 🎥 Video Processing

* Extracts frames every **30 frames**
* Limits processing to **~10 seconds (300 frames)**
* Detects multiple vehicles
* Displays unique matches

---

### 🔎 Matching Logic

* ✅ Exact match first
* 🔁 Fuzzy match (≥ 85% similarity)
* Uses `SequenceMatcher`

---

## 📸 UI Tabs

| Tab       | Function           |
| --------- | ------------------ |
| 📷 Camera | Capture live plate |
| 🖼️ Photo | Upload image       |
| 🎥 Video  | Analyze video      |
| ⌨️ Search | Manual lookup      |

---

## 📊 Example Output

```
Detected Plate: TS09AB1234

State: Telangana (TS)
Vehicle: Hyundai Creta
Owner: Ramesh Kumar
Phone: 9876543210
```

---

## 💡 Author

**Khaja Siddique Ahmed**

