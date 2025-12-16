import streamlit as st
import base64
import os

# 1. PAGE CONFIGURATION
st.set_page_config(
    page_title="About - RecycLens",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# 2. HELPER FUNCTION (IMAGE TO BASE64)
def get_img_base64(file_path):
    try:
        with open(file_path, "rb") as f:
            data = f.read()
            return f"data:image/png;base64,{base64.b64encode(data).decode()}"
    except FileNotFoundError:
        return "https://via.placeholder.com/150?text=Image+Not+Found"

# 3. CSS STYLING (MERGED: HEADER + CONTENT)
st.markdown("""
    <style>
    /* Global Styles */
    .stApp {
        background-color: #FFFFFF;
        color: #000000; 
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
    }


    .block-container {
        max-width: 1200px !important;
        padding-top: 100px !important; 
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        padding-bottom: 2rem !important;
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
    
    /* Nav Links */
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

    /* --- SDG SECTION STYLES --- */
    .sdg-container {
        background-color: #E69F00; /* SDG 12 Orange */
        color: black;
        border-radius: 15px;
        padding: 40px;
        display: flex;
        align-items: center;
        gap: 40px;
        margin-bottom: 50px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
    .sdg-image-box {
        flex: 0 0 200px;
    }
    .sdg-image-box img {
        width: 100%;
        border-radius: 8px;
    }
    .sdg-text {
        flex: 1; 
    }
    .sdg-title {
        font-size: 22px;
        font-weight: 800;
        margin-bottom: 15px;
        text-transform: uppercase;
        color: #FFFFFF;
    }
    .sdg-body {
        font-size: 18px;
        line-height: 1.6;
        font-weight: 500;
        color: #FFFFFF;
    }

    /* --- CLASSIFICATION GRID STYLES --- */
    .grid-container {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 30px;
        margin-bottom: 50px;
    }
    
    .class-card {
        display: block; 
        text-decoration: none !important;
        color: black !important;
        border-radius: 15px;
        overflow: hidden;
        transition: transform 0.2s, box-shadow 0.2s;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        position: relative;
        height: 320px; 
    }
    
    .class-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0,0,0,0.2);
    }

    .card-image-area {
        height: 70%;
        width: 100%;
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: rgba(255,255,255,0.3); 
    }
    
    .card-image-area img {
        max-width: 60%;
        max-height: 60%;
        object-fit: contain;
    }

    .card-label {
        height: 30%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 20px;
        font-weight: 700;
        color: black; 
        background-color: rgba(0,0,0,0.05); 
    }
    </style>
""", unsafe_allow_html=True)

# 4. RENDER FUNCTION FOR CARDS
def render_card(name, color, base64_img, link_page):
    html = f"""
    <a href="{link_page}" target="_self" class="class-card" style="background-color: {color};">
        <div class="card-image-area">
             <img src="{base64_img}" alt="{name}">
        </div>
        <div class="card-label">
            {name}
        </div>
    </a>
    """
    return html

# 5. FIXED HEADER 
try:
    logo_path = "images/recyclenslogo.png"
    img_base64 = get_img_base64(logo_path)
    logo_src = img_base64
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

# 6. CONTENT

# SDG BANNER 
sdg_image_path = "images/sdg12.png" 
sdg_img_src = get_img_base64(sdg_image_path)

st.markdown(f"""
    <div class="sdg-container">
        <div class="sdg-image-box">
            <img src="{sdg_img_src}">
        </div>
        <div class="sdg-text">
            <div class="sdg-title">SDG 12: Responsible Consumption and Production</div>
            <div class="sdg-body">
                Incorrect waste sorting leads to pollution, recycling failure, and long-term environmental damage. 
                When waste is not properly classified, recyclable materials often end up in landfills, contributing 
                to resource loss and environmental harm.
                <br><br>
                RecycLens leverages computer vision and artificial intelligence to help individuals and communities 
                make smarter, more responsible waste decisions – one photo at a time. By providing instant and accurate 
                waste classification, RecycLens encourages better recycling practices and supports sustainable 
                consumption patterns.
            </div>
        </div>
    </div>
""", unsafe_allow_html=True)


# CLASSIFICATION GRID 
st.markdown("<h2 style='color: black; font-weight: 700; margin-bottom: 20px;'>Waste Classification</h2>", unsafe_allow_html=True)

items = [
    {"name": "Battery",          "color": "#ECEC0B", "link": "battery",    "file": "images/battery.png"},
    {"name": "Biological Waste", "color": "#C8E6C9", "link": "biological", "file": "images/biological.png"},
    {"name": "Cardboard",        "color": "#D7CCC8", "link": "cardboard",  "file": "images/cardboard.png"},
    {"name": "Paper",            "color": "#F5F5F5", "link": "paper",      "file": "images/paper.png"},
    {"name": "Glass",            "color": "#BBDEFB", "link": "glass",      "file": "images/glass.png"},
    {"name": "Metal",            "color": "#CFD8DC", "link": "metal",      "file": "images/metal.png"},
    {"name": "Plastic",          "color": "#FFF9C4", "link": "plastic",    "file": "images/plastic.png"},
]

cols = st.columns(4) 

for i, item in enumerate(items):
    col_index = i % 4
    with cols[col_index]:
        b64_img = get_img_base64(item['file'])
        card_html = render_card(item['name'], item['color'], b64_img, item['link'])
        st.markdown(card_html, unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)