import streamlit as st
import base64
import os

# 1. PAGE CONFIGURATION
st.set_page_config(
    page_title="Biological Waste - RecycLens",
    page_icon="🍂",
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
        return "https://via.placeholder.com/400x300?text=Image+Not+Found"

# 3. CSS STYLING
st.markdown("""
<style>
    /* Global Styles */
    .stApp {
        background-color: #FFFFFF;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        color: #000000;
    }

    /* --- RESPONSIVE CONTAINER --- */
    .block-container {
        max-width: 1200px !important;
        padding-top: 100px !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        padding-bottom: 2rem !important;
        margin: auto !important;
    }

    /* Hide Default Elements */
    [data-testid="stHeader"] { display: none; }
    [data-testid="stSidebar"] { display: none; }
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }

    /* --- FIXED HEADER STYLING --- */
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

    /* --- TITLE SECTION WITH CLOSE BUTTON --- */
    .title-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
    }

    .main-page-title {
        font-size: 48px;
        font-weight: 900;
        color: #000000;
        text-transform: uppercase;
        margin: 0;
    }

    /* Close Button Image Style */
    .page-close-btn {
        width: 40px;
        height: 40px;
        cursor: pointer;
        opacity: 0.6;
        transition: opacity 0.2s, transform 0.2s;
    }
    .page-close-btn:hover {
        opacity: 1;
        transform: scale(1.1);
    }

    /* --- HERO SECTION --- */
    .hero-container {
        background-color: #C8E6C9; 
        padding: 40px;
        border-radius: 15px; 
        margin-bottom: 40px;
        color: black;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
    
    .hero-subtitle {
        font-size: 24px;
        font-weight: 700;
        margin-bottom: 30px;
    }

    /* --- IMAGE GRID --- */
    .image-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 20px;
        margin-bottom: 30px;
    }
    .image-grid img {
        width: 100%; 
        height: 220px; 
        object-fit: cover; 
        border-radius: 8px;
        background-color: #FFF; 
        border: 2px solid rgba(0,0,0,0.1);
    }

    /* --- CONTENT BOXES --- */
    .content-box {
        padding: 30px;
        border-radius: 12px;
        margin-bottom: 30px;
        color: black;
        box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        height: 100%;
    }

    .box-title {
        font-size: 22px;
        font-weight: 800;
        margin-bottom: 15px;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .box-yellow {
        background-color: #FFF3E0;
        border-left: 8px solid #FF9800;
    }

    .box-green {
        background-color: #E8F5E9;
        border-left: 8px solid #4CAF50;
    }

    .box-text {
        font-size: 18px;
        line-height: 1.6;
    }
    
    ul { margin-top: 10px; margin-bottom: 10px; }
    li { margin-bottom: 8px; font-size: 18px; }
</style>
""", unsafe_allow_html=True)


# 4. FIXED HEADER
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


# 5. MAIN CONTENT

close_icon_src = get_img_base64("images/xicon.png") 

st.markdown(f"""
<div class="title-container">
    <div class="main-page-title">BIOLOGICAL WASTE</div>
    <a href="/about" target="_self">
        <img src="{close_icon_src}" class="page-close-btn" title="Close">
    </a>
</div>
""", unsafe_allow_html=True)

# Image Loading 
img1 = get_img_base64("images/biologicalpage/bio1.jpeg") 
img2 = get_img_base64("images/biologicalpage/bio2.jpeg") 
img3 = get_img_base64("images/biologicalpage/bio3.jpg") 
img4 = get_img_base64("images/biologicalpage/bio4.jpg") 

# HERO SECTION
st.markdown(f"""
<div class="hero-container">
    <div class="hero-subtitle">Organic Waste That Needs the Right Treatment</div>
    <div class="image-grid">
        <img src="{img1}">
        <img src="{img2}">
        <img src="{img3}">
        <img src="{img4}">
    </div>
    <div style="font-size: 20px; font-weight: 500;">
        Biological waste, also known as organic waste, includes natural materials that come from plants 
        or animals. This type of waste can decompose naturally and is commonly produced in households, 
        markets, and restaurants.
    </div>
</div>
""", unsafe_allow_html=True)

# 6. INFO BOXES
# Box 1 (Yellow) - Problem
st.markdown("""
<div class="content-box box-yellow">
    <div class="box-title">⚠️ Why Is Biological Waste a Problem?</div>
    <div class="box-text">
        When biological waste is mixed with general trash and sent to landfills, it decomposes 
        without oxygen and produces methane gas, a powerful greenhouse gas that contributes to 
        climate change. Poor management of biological waste can also cause:
        <ul>
            <li>Unpleasant odors</li>
            <li>Attraction of pests and insects</li>
            <li>Water and soil contamination</li>
        </ul>
    </div>
</div>
""", unsafe_allow_html=True)

# Grid for Green Boxes
col_left, col_right = st.columns(2)

with col_left:
    # Box 2 - How to Manage
    st.markdown("""
<div class="content-box box-green">
    <div class="box-title">♻️ How to Manage Biological Waste Properly</div>
    <div class="box-text">
        <ul>
            <li>Separate organic waste from other trash</li>
            <li>Compost food and garden waste at home</li>
            <li>Use community composting or organic waste bins</li>
            <li>Avoid mixing biological waste with plastics or metals</li>
        </ul>
    </div>
</div>
    """, unsafe_allow_html=True)

with col_right:
    # Box 3 - Benefits
    st.markdown("""
<div class="content-box box-green">
    <div class="box-title">🌱 Benefits of Proper Biological Waste Management</div>
    <div class="box-text">
        <ul>
            <li>Reduces landfill waste</li>
            <li>Produces compost for soil enrichment</li>
            <li>Lowers greenhouse gas emissions</li>
            <li>Supports sustainable agriculture</li>
        </ul>
    </div>
</div>
    """, unsafe_allow_html=True)