import streamlit as st
import base64
import pandas as pd
import os

# 1. PAGE CONFIGURATION
st.set_page_config(
    page_title="History - RecycLens",
    page_icon="🕒",
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
        return "https://via.placeholder.com/150?text=Logo"


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

    /* --- HISTORY TABLE STYLING --- */
    .history-card {
        background-color: #F9F9F9;
        border-left: 6px solid #2E7D32;
        padding: 20px;
        margin-bottom: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        display: flex;
        justify-content: space-between;
        align-items: center;
        transition: transform 0.2s;
    }
    .history-card:hover {
        transform: translateX(5px);
        background-color: #F1F8E9;
    }
    
    .h-item {
        font-size: 20px;
        font-weight: 800;
        color: #000000;
        text-transform: uppercase;
    }
    
    .h-time {
        font-size: 14px;
        color: #666666;
        margin-top: 4px;
    }
    
    .h-conf {
        font-size: 16px;
        font-weight: 600;
        color: #2E7D32;
        background-color: #E8F5E9;
        padding: 5px 12px;
        border-radius: 20px;
    }
    
    .no-history {
        text-align: center;
        margin-top: 50px;
        color: #888;
        font-size: 18px;
        font-style: italic;
    }

    /* Clear Button Styling */
    div.stButton > button {
        background-color: #C62828; 
        color: white;
        border: none;
        padding: 8px 16px;
        font-weight: 600;
        border-radius: 6px;
        font-size: 14px;
        float: right; 
    }
    div.stButton > button:hover {
        background-color: #B71C1C;
        color: white;
    }
    

    @media only screen and (max-width: 768px) {
        
        
        .fixed-header {
            height: 60px;
            padding: 0 15px;
        }
        .header-logo {
            height: 35px;
        }
        .header-tagline {
            display: none;
        }
        .header-right {
            gap: 15px;
        }
        .nav-link {
            font-size: 14px;
        }

    
        .block-container {
            padding-top: 80px !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }

        .history-card {
            padding: 15px;       
            margin-bottom: 10px;
        }
        
        .h-item {
            font-size: 16px;     
        }
        
        .h-time {
            font-size: 12px;    
        }
        
        .h-conf {
            font-size: 12px;     
            padding: 4px 8px;
        }

        div.stButton > button {
            width: 100%;
            margin-top: 5px;
        }
        
        h1 {
            font-size: 28px !important; 
        }
    }
    
    
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
        <a href="/history" target="_self" class="nav-link" style="color:#1B5E20; text-decoration: underline;">History</a>
    </div>
</div>
""", unsafe_allow_html=True)


# 5. MAIN CONTENT
csv_file = "history.csv"
history_exists = False
df = pd.DataFrame()

# Pre-load data to check existence
if os.path.exists(csv_file):
    df = pd.read_csv(csv_file)
    if not df.empty:
        history_exists = True
        df = df.iloc[::-1] # Reverse order

# --- MAIN TITLE ---
st.markdown("<h1 style='text-align: center; margin-bottom: 20px;'>Scan History</h1>", unsafe_allow_html=True)

# --- CONTAINER FOR CONTENT (Controls Width) ---
c_left, c_main, c_right = st.columns([1, 2, 1])

with c_main:
    
    if history_exists:
        top_c1, top_c2 = st.columns([3, 1], vertical_alignment="bottom")
        
        with top_c1:
            # Show count
            st.markdown(f"**Total Scans:** {len(df)}")
            
        with top_c2:
            if st.button("Clear History", key="clear_btn", use_container_width=True):
                if os.path.exists(csv_file):
                    os.remove(csv_file)
                st.rerun()
                
        st.markdown("<hr style='margin: 10px 0px 20px 0px; border-color: #eee;'>", unsafe_allow_html=True)

    # --- HISTORY LIST ---
    if not history_exists:
        st.markdown("""
        <div class="no-history">
            <div style="font-size: 50px; margin-bottom: 20px;">📜</div>
            No scans yet.<br>Go to the Home page to start scanning waste items!
        </div>
        """, unsafe_allow_html=True)
    else:
        # Display Cards
        for index, row in df.iterrows():
            name = row['item']
            conf = float(row['conf']) * 100
            time = row['time']
            
            st.markdown(f"""
            <div class="history-card">
                <div>
                    <div class="h-item">{name}</div>
                    <div class="h-time">{time}</div>
                </div>
                <div class="h-conf">{conf:.1f}% Confidence</div>
            </div>
            """, unsafe_allow_html=True)


