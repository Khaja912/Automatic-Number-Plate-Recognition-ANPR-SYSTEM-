import streamlit as st
import pandas as pd
import easyocr
from PIL import Image
import cv2
import numpy as np
import re
from difflib import SequenceMatcher
import tempfile
import time

st.set_page_config(page_title="🚘 Indian ANPR Pro", layout="wide")

@st.cache_data
def load_database():
    """✅ YOUR EXACT 8 columns[file:113]"""
    data = pd.read_csv("indian_vehicle_database.csv")
    data['license_plate'] = data['license_plate'].astype(str).str.strip().str.upper()
    return data

@st.cache_resource
def load_ocr():
    return easyocr.Reader(['en'])

@st.cache_data
def find_vehicle(plate_text, data):
    """Exact + fuzzy match for YOUR 8-column CSV[file:113]"""
    exact = data[data['license_plate'] == plate_text]
    if not exact.empty:
        return exact.iloc[0]
    
    best_match = None
    best_score = 0
    sample_data = data.sample(min(5000, len(data))).reset_index(drop=True)
    
    for _, row in sample_data.iterrows():
        score = SequenceMatcher(None, plate_text, row['license_plate']).ratio()
        if score > best_score and score >= 0.85:
            best_score = score
            best_match = row
    
    return best_match

# ✅ Load FIRST
data = load_database()
reader = load_ocr()

st.title("🚘 Indian ANPR Pro")
st.markdown(f"✅ **{len(data):,} vehicles loaded** | Ready to scan!")

# 🔥 4 TABS: Clean UI - NO sidebar clutter
tab1, tab2, tab3, tab4 = st.tabs(["📷 Camera", "🖼️ Photo", "🎥 Video", "⌨️ Search"])

# 🔥 TAB 1: Camera
with tab1:
    st.header("📷 Take Photo of License Plate")
    camera_img = st.camera_input("Point at license plate")
    
    if camera_img:
        image = Image.open(camera_img)
        st.image(image, caption="📸 Captured", use_column_width=True)
        
        frame = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        results = reader.readtext(gray)
        
        plate = None
        for (_, text, conf) in results:
            clean = re.sub(r'[^\w]', '', text.upper())
            if len(clean) >= 8 and conf > 0.4:
                plate = clean
                break
        
        if plate:
            match = find_vehicle(plate, data)
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.success(f"**Detected**: `{plate}`")
                if match is not None:
                    st.balloons()
            
            with col2:
                if match is not None:
                    st.metric("🆔 Plate", match['license_plate'])
                    st.metric("🏛️ State", f"{match['state_name']} ({match['state_code']})")
                    st.metric("🚗 Vehicle", f"{match['make']} {match['model']}")
                    st.metric("👤 Owner", match['owner_name'])
                    st.metric("📞 Phone", match['phone'])
                else:
                    st.warning(f"❌ `{plate}` not in database")

# 🔥 TAB 2: Photo
with tab2:
    st.header("🖼️ Upload Photo")
    uploaded_file = st.file_uploader("Upload vehicle photo", type=['jpg','png','jpeg'])
    
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="🖼️ Photo", use_column_width=True)
        
        frame = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        results = reader.readtext(gray)
        
        plate = None
        for (_, text, conf) in results:
            clean = re.sub(r'[^\w]', '', text.upper())
            if len(clean) >= 8 and conf > 0.4:
                plate = clean
                break
        
        if plate:
            match = find_vehicle(plate, data)
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.success(f"**Detected**: `{plate}`")
                if match is not None:
                    st.balloons()
            
            with col2:
                if match is not None:
                    st.metric("🆔 Plate", match['license_plate'])
                    st.metric("🏛️ State", f"{match['state_name']} ({match['state_code']})")
                    st.metric("🚗 Vehicle", f"{match['make']} {match['model']}")
                    st.metric("👤 Owner", match['owner_name'])
                    st.metric("📞 Phone", match['phone'])
                else:
                    st.warning(f"❌ `{plate}` not in database")

# 🔥 TAB 3: Video
with tab3:
    st.header("🎥 Upload Video")
    uploaded_video = st.file_uploader("Upload MP4 video", type=['mp4'])
    
    if uploaded_video:
        st.video(uploaded_video)
        
        if st.button("🎬 Analyze Video", type="primary"):
            with st.spinner("Analyzing video frames..."):
                tfile = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
                tfile.write(uploaded_video.getvalue())
                tfile.close()
                
                cap = cv2.VideoCapture(tfile.name)
                plates_found = []
                frame_count = 0
                
                progress_bar = st.progress(0)
                
                while cap.isOpened():
                    ret, frame = cap.read()
                    if not ret:
                        break
                    
                    if frame_count % 30 == 0:  # Every 30th frame
                        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                        results = reader.readtext(gray)
                        
                        for (_, text, conf) in results:
                            clean = re.sub(r'[^\w]', '', text.upper())
                            if len(clean) >= 8 and conf > 0.4:
                                match = find_vehicle(clean, data)
                                if match is not None and match['license_plate'] not in plates_found:
                                    plates_found.append(match['license_plate'])
                                    st.success(f"🎥 Found: **{match['license_plate']}**")
                                    st.metric("State", match['state_name'])
                                    st.metric("Vehicle", f"{match['make']} {match['model']}")
                    
                    frame_count += 1
                    if frame_count > 300:  # Limit to 10 seconds
                        break
                    progress_bar.progress(min(frame_count / 300, 1.0))
                
                cap.release()
                import os
                os.unlink(tfile.name)
                
                st.success(f"✅ **{len(plates_found)} unique plates found!**")

# 🔥 TAB 4: Manual Search
with tab4:
    st.header("⌨️ Manual Search")
    col1, col2 = st.columns([2, 1])
    
    with col1:
        search_plate = st.text_input("Enter license plate number")
    
    with col2:
        if st.button("🔍 Search", type="primary") and search_plate:
            clean_plate = re.sub(r'[^\w]', '', search_plate.upper())
            match = find_vehicle(clean_plate, data)
            
            if match is not None:
                st.success("✅ **VEHICLE FOUND!**")
                st.balloons()
                col_a, col_b = st.columns(2)
                
                with col_a:
                    st.metric("🆔 Plate", match['license_plate'])
                    st.metric("🏛️ State", f"{match['state_name']} ({match['state_code']})")
                    st.metric("🚗 Vehicle", f"{match['make']} {match['model']}")
                
                with col_b:
                    st.metric("👤 Owner", match['owner_name'])
                    st.metric("📞 Phone", match['phone'])
                
                # Clean JSON output
                with st.expander("📋 Full Details"):
                    st.json({
                        "license_plate": match['license_plate'],
                        "state_code": match['state_code'],
                        "state_name": match['state_name'],
                        "make": match['make'],
                        "model": match['model'],
                        "owner_name": match['owner_name'],
                        "phone": match['phone'],
                        "synthetic_id": match['synthetic_id']
                    })
            else:
                st.error("❌ No vehicle found")

st.markdown("---")
st.caption("🚀 Clean ANPR Pro | Camera + Photo + Video + Search")
