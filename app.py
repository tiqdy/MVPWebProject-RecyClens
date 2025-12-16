import streamlit as st
from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np
from datetime import datetime
import base64 
import pandas as pd
import os
import streamlit.components.v1 as components

# 1. PAGE CONFIGURATION
st.set_page_config(
    page_title="RecycLens",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. HELPER FUNCTION FOR CLICKABLE IMAGE
def get_base64_of_bin_file(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except Exception:
        return ""

# 3. CSS STYLING
st.markdown("""
    <style>
    .stApp {
        background-color: #FFFFFF;
        color: #000000; 
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }

    .block-container {
        max-width: 1200px !important;
        padding-top: 70px !important; 
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        margin: auto !important;
    }

    [data-testid="stHeader"] { display: none; }
    [data-testid="stSidebar"] { display: none; }
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    
    .fixed-header {
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 90px;
        background-color: #FFFFFF;
        z-index: 9999;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        display: flex;
        justify-content: space-between; 
        align-items: center;
        padding: 0 40px; 
        box-sizing: border-box;
    }

    .header-left {
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .header-logo {
        height: 50px;
        width: auto;
        object-fit: contain;
    }
    .header-tagline {
        font-size: 14px;
        color: #000000;
        font-weight: 500;
        margin-top: 2px;
    }

    .header-right {
        display: flex;
        gap: 30px; 
        align-items: center;
    }
    
    .nav-link {
        color: #000000;      
        text-decoration: none !important;
        font-weight: 600;    
        font-size: 18px;
        transition: color 0.2s ease;
        background: transparent;
        border: none;
    }
    .nav-link:hover {
        color: #1B5E20;      
        text-decoration: none !important;
        cursor: pointer;
    }

    .main-desc {
        text-align: center;
        font-size: 22px;
        color: #000000;
        max-width: 900px;
        margin: 0 auto 40px auto; 
        line-height: 1.6;
        font-weight: 500;
    }
    .section-header {
        text-align: center;
        font-size: 24px; 
        font-weight: 700;
        color: #000000;
        margin-bottom: 20px;
    }

    [data-testid="stCameraInput"] {
        width: 100% !important;
        margin: 0 auto;
    }
    
    [data-testid="stCameraInput"] > div:first-child {
        width: 100% !important;
        height: auto !important; 
        background-color: transparent !important;
        border-radius: 12px;
        border: 2px solid #000000;
        overflow: hidden;
    }

    [data-testid="stCameraInput"] video, 
    [data-testid="stCameraInput"] img {
        width: 100% !important;
        height: auto !important; 
        object-fit: cover; 
    }

    [data-testid="stCameraInput"] button {
        color: #FFFFFF !important;
        background-color: #2E7D32 !important;
        border: none !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        padding: 12px 16px !important; 
        width: 100%; 
        border-radius: 8px !important; 
        margin-top: 15px !important; 
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }
    [data-testid="stCameraInput"] button:hover {
        background-color: #000000 !important;
        color: #FFFFFF !important;
    }

    
    /* SUCCESS (Green) */
    .result-card-success {
        background-color: #F1F8E9; 
        border: 2px solid #2E7D32; 
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        margin-top: 20px; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        width: 100%; 
    }
    .result-card-success .result-title {
        color: #1B5E20;
        font-size: 16px;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    /* ERROR (Red) */
    .result-card-error {
        background-color: #FFEBEE; /* Light Red */
        border: 2px solid #C62828; /* Dark Red */
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        margin-top: 20px; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        width: 100%; 
    }
    .result-card-error .result-title {
        color: #C62828;
        font-size: 16px;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .result-value {
        font-size: 36px; 
        font-weight: 900;
        color: #000000;
        margin: 0;
    }
    .result-conf {
        font-size: 16px;
        color: #000000;
        font-weight: 600;
        margin-top: 5px;
    }

    div.stButton > button {
        background-color: #2E7D32;
        color: white;
        border: none;
        padding: 10px 20px;
        font-size: 16px;
        font-weight: 700;
        border-radius: 6px;
        transition: background-color 0.2s;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }
    div.stButton > button:hover {
        background-color: #000000;
        color: white;
    }
    
    @media only screen and (max-width: 768px) {
        .fixed-header {
            padding: 0 15px; 
            height: 70px;    
        }
        .header-logo {
            height: 35px;    
        }
        .header-tagline {
            display: none;   
        }
        
        .nav-link {
            font-size: 14px;
            margin-left: 5px;
        }
        .header-right {
            gap: 15px;       
        }

        .block-container {
            padding-top: 80px !important; 
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }

        .main-desc {
            font-size: 18px;
            margin-bottom: 30px;
        }
        .section-header {
            font-size: 20px;
        }
        .result-value {
            font-size: 28px; 
        }
    }
    </style>
    """, unsafe_allow_html=True)

# 4. MODEL LOADING
@st.cache_resource
def load_waste_model():
    return load_model("keras_model.h5", compile=False)

@st.cache_data
def load_labels():
    with open("labels.txt", "r") as f:
        return [line.strip() for line in f.readlines()]


# 5. FIXED HEADER LAYOUT
try:
    logo_path = "images/recyclenslogo.png"
    img_base64 = get_base64_of_bin_file(logo_path)
    logo_src = f"data:image/png;base64,{img_base64}"
except Exception:
    logo_src = ""

st.markdown(f"""
    <div class="fixed-header">
        <div class="header-left">
            <a href="/" target="_self">
                <img src="{logo_src}" class="header-logo" alt="RecycLens">
            </a>
            <div class="header-tagline">Smart Vision for Smarter Recycling</div>
        </div>
        <div class="header-right">
            <a href="/" target="_self" class="nav-link">Home</a>
            <a href="/about" target="_self" class="nav-link">About</a>
            <a href="/history" target="_self" class="nav-link">History</a>
        </div>
    </div>
""", unsafe_allow_html=True)

# 6. MAIN CONTENT
st.markdown("""
<div class="main-desc">
    AI-powered waste classification that helps you identify and sort waste correctly, 
    instantly and accurately.
</div>
""", unsafe_allow_html=True)

# 7. CAMERA & PROCESSING

c1, c2, c3 = st.columns([1, 6, 1]) 

with c2:
    st.markdown('<div class="section-header">Ready to recycle smarter?</div>', unsafe_allow_html=True)

    camera_image = st.camera_input(label="Scan Now", label_visibility="collapsed")

    if camera_image:
        model = load_waste_model()
        class_names = load_labels()
        
        image = Image.open(camera_image)
        image = ImageOps.fit(image, (224, 224), Image.Resampling.LANCZOS)
        image_array = np.asarray(image)
        normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
        data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
        data[0] = normalized_image_array
        
        with st.spinner("Analyzing..."):
            prediction = model.predict(data, verbose=0)
            index = np.argmax(prediction)
            class_name = class_names[index]
            confidence_score = prediction[0][index]
            clean_label = class_name.split(" ", 1)[-1].strip()

        st.markdown('<div id="result-anchor"></div>', unsafe_allow_html=True)

        if confidence_score < 0.80:
            st.markdown(f"""
            <div class="result-card-error">
                <div class="result-title">⚠️ Cannot Identify</div>
                <div class="result-value">UNKNOWN ITEM</div>
                <div class="result-conf">Confidence: {confidence_score*100:.1f}%</div>
                <div style="margin-top:10px; font-size:14px;">Please try scanning closer or with better lighting.</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="result-card-success">
                <div class="result-title">Detected Material</div>
                <div class="result-value">{clean_label.upper()}</div>
                <div class="result-conf">Confidence: {confidence_score*100:.1f}%</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            csv_file = "history.csv"
            
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
            new_entry = {"item": clean_label, "conf": confidence_score, "time": timestamp}

            if os.path.exists(csv_file):
                df = pd.read_csv(csv_file)
            else:
                df = pd.DataFrame(columns=["item", "conf", "time"])

            if df.empty or df.iloc[-1]['time'] != timestamp:
                new_df = pd.DataFrame([new_entry])
                df = pd.concat([df, new_df], ignore_index=True)
                df.to_csv(csv_file, index=False)
                
            btn_col1, btn_col2, btn_col3 = st.columns([1, 2, 1])
            with btn_col2:
                page_link = f"pages/{clean_label.lower()}.py"
                
                if st.button(f"Read More", use_container_width=True):
                    try:
                        st.switch_page(page_link)
                    except:
                        st.switch_page("pages/about.py")

        components.html(
            """
            <script>
                const anchor = window.parent.document.getElementById('result-anchor');
                if (anchor) {
                    anchor.scrollIntoView({behavior: 'smooth', block: 'start'});
                }
            </script>
            """,
            height=0
        )
        
