import streamlit as st
import base64
import pandas as pd
import os
import random

# 1. PAGE CONFIGURATION
st.set_page_config(
    page_title="History - RecycLens",
    page_icon="🕒",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --------------------------------------------------
# SESSION RECOVERY & SECURITY
# --------------------------------------------------
if "user" in st.query_params:
    st.session_state.logged_in = True
    st.session_state.username = st.query_params["user"]

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.switch_page("app.py")

current_user = st.session_state.username if "username" in st.session_state else "Guest"

# 2. HELPER FUNCTIONS
def get_img_base64(file_path):
    try:
        with open(file_path, "rb") as f:
            data = f.read()
            return f"data:image/png;base64,{base64.b64encode(data).decode()}"
    except FileNotFoundError:
        return "https://via.placeholder.com/150?text=Logo"

# --- IMPACT CALCULATOR ---
def calculate_impact(df):
    impact_map = {
        "plastic": {"co2": 0.09, "energy": 50},
        "metal":   {"co2": 0.15, "energy": 100},
        "glass":   {"co2": 0.05, "energy": 30},
        "paper":   {"co2": 0.03, "energy": 20},
        "cardboard": {"co2": 0.04, "energy": 25},
        "battery": {"co2": 0.00, "energy": 0}
    }
    
    total_co2 = 0
    total_energy = 0
    item_counts = {}
    
    for item in df['item']:
        key = item.lower().strip()
        found = False
        for k in impact_map:
            if k in key:
                total_co2 += impact_map[k]['co2']
                total_energy += impact_map[k]['energy']
                found = True
                break
        if not found:
            total_co2 += 0.05
            total_energy += 30
            
        item_counts[key] = item_counts.get(key, 0) + 1
            
    return total_co2, total_energy, item_counts

# --- EDUCATIONAL FACT ---
def get_educational_fact(most_common_item):
    facts = {
        "plastic": "Did you know? Recycling just one plastic bottle saves enough energy to power a 60W light bulb for 3 hours!",
        "metal": "Fun Fact: Aluminum cans can be recycled indefinitely without losing quality. It's one of the most sustainable materials!",
        "glass": "Glass Fact: Glass takes over 1 million years to decompose in a landfill. Recycling it makes a huge difference!",
        "paper": "Eco Tip: Recycling one ton of paper saves 17 trees, 7,000 gallons of water, and 463 gallons of oil.",
        "cardboard": "Did you know? Over 90% of all products shipped in the US are packaged in corrugated cardboard, most of which is recyclable.",
        "battery": "Safety First: Batteries contain toxic chemicals like lead and mercury. Never throw them in the trash—take them to e-waste centers!",
        "general": "General Fact: The average person generates over 4 pounds of trash every day and about 1.5 tons of solid waste per year."
    }
    for key in facts:
        if most_common_item and key in most_common_item:
            return facts[key]
    return facts["general"]

# 3. CSS STYLING
st.markdown("""
<style>
    /* GLOBAL */
    .stApp {
        background-color: #FFFFFF;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        color: #000000;
    }

    [data-testid="stHeader"], [data-testid="stSidebar"], footer { display: none !important; }

    /* Padding just enough to clear the fixed Nav Header (100px) */
    .block-container {
        max-width: 1200px !important;
        padding-top: 130px !important; 
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        padding-bottom: 2rem !important;
        margin: auto !important;
    }

    /* --- FIXED HEADER (NAV ONLY) --- */
    .fixed-header {
        position: fixed; top: 0; left: 0; width: 100%; height: 100px;
        background-color: #FFFFFF; z-index: 10002;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        display: flex; justify-content: space-between; align-items: center;
        padding: 0 40px; box-sizing: border-box;
    }

    /* --- HEADER ELEMENTS --- */
    .header-logo { height: 50px; object-fit: contain; margin-bottom: 2px; }
    .header-quote { font-size: 13px; color: #555; font-weight: 500; font-style: italic; margin: 0; }
    .header-right { display: flex; gap: 35px; align-items: center; }
    .nav-link { color: #000; text-decoration: none !important; font-weight: 700; font-size: 18px; transition: color 0.2s; }
    .nav-link:hover { color: #2E7D32; cursor: pointer; }

    /* --- IMPACT CARD --- */
    .impact-card {
        background: linear-gradient(135deg, #2E7D32 0%, #43A047 100%);
        color: white;
        padding: 20px;
        border-radius: 12px;
        margin-bottom: 30px; /* Space before history list */
        box-shadow: 0 4px 15px rgba(46, 125, 50, 0.2);
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .impact-stats { text-align: left; }
    .impact-fact { 
        text-align: right; font-size: 14px; font-style: italic; 
        max-width: 50%; opacity: 0.9; border-left: 1px solid rgba(255,255,255,0.3);
        padding-left: 20px;
    }
    .big-stat { font-size: 24px; font-weight: 800; }
    .small-stat { font-size: 14px; opacity: 0.9; }

    /* --- HISTORY LIST --- */
    .history-card {
        background-color: #F9F9F9;
        border-left: 6px solid #2E7D32;
        padding: 20px; margin-bottom: 15px; border-radius: 8px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        display: flex; justify-content: space-between; align-items: center;
        transition: transform 0.2s;
    }
    .history-card:hover { transform: translateX(5px); background-color: #F1F8E9; }
    .h-item { font-size: 20px; font-weight: 800; color: #000; text-transform: uppercase; }
    .h-time { font-size: 14px; color: #666; margin-top: 4px; }
    .h-conf { font-size: 16px; font-weight: 600; color: #2E7D32; background-color: #E8F5E9; padding: 5px 12px; border-radius: 20px; }
    .no-history { text-align: center; margin-top: 50px; color: #888; font-size: 18px; font-style: italic; }

    /* --- CLEAR BUTTON STYLING --- */
    div.stButton > button {
        background-color: #C62828 !important; color: white !important;
        border: none !important; padding: 8px 16px !important;
        font-weight: 600 !important; border-radius: 6px !important;
        font-size: 14px !important; float: right;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2) !important;
    }
    div.stButton > button:hover { background-color: #B71C1C !important; }

    /* RESPONSIVE */
    @media only screen and (max-width: 768px) {
        .fixed-header { height: 80px; padding: 0 20px; }
        .header-logo { height: 40px; }
        .header-quote { display: none; }
        
        .header-right { gap: 15px; }
        
        .header-right a:nth-child(1) {
            display: none;
        }
        
        .nav-link { font-size: 14px; }
        
        .block-container { padding-top: 100px !important; }
        
        .impact-card { flex-direction: column; text-align: center; gap: 15px; }
        .impact-stats, .impact-fact { text-align: center; max-width: 100%; border: none; padding: 0; }
        
        div.stButton > button { width: 100%; margin-top: 10px; }
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
        <a href="/home?user={current_user}" target="_self">
            <img src="{logo_src}" class="header-logo" alt="RecycLens">
        </a>
        <div class="header-quote">Smart Vision for Smarter Recycling</div>
    </div>
    <div class="header-right">
        <a href="/home?user={current_user}" target="_self" class="nav-link">Home</a>
        <a href="/about?user={current_user}" target="_self" class="nav-link">About</a>
        <a href="/history?user={current_user}" target="_self" class="nav-link" style="color:#2E7D32; text-decoration: underline;">History</a>
        <a href="/account?user={current_user}" target="_self" class="nav-link" style="font-size: 24px;">👤</a>
    </div>
</div>
""", unsafe_allow_html=True)

# 5. DATA LOADING
csv_file = "history.csv"
history_exists = False
df = pd.DataFrame()

if os.path.exists(csv_file):
    df_all = pd.read_csv(csv_file)
    if "username" in df_all.columns:
        df = df_all[df_all["username"] == current_user]
    else:
        df = df_all 
    if not df.empty:
        history_exists = True
        df = df.iloc[::-1]

# --- MAIN TITLE ---
st.markdown("<h1 style='text-align: center; margin-bottom: 20px; color: #000;'>Scan History</h1>", unsafe_allow_html=True)

# 6. MAIN CONTENT
c_left, c_main, c_right = st.columns([1, 2, 1])

with c_main:
    
    if history_exists:
        # --- TOP CONTROLS (SCROLLABLE) ---
        top_c1, top_c2 = st.columns([3, 1], vertical_alignment="bottom")
        
        with top_c1:
            st.markdown(f"**Total Scans for {current_user}:** {len(df)}")
            
        with top_c2:
            if st.button("Clear History"):
                if os.path.exists(csv_file):
                    df_full = pd.read_csv(csv_file)
                    if "username" in df_full.columns:
                        df_remaining = df_full[df_full["username"] != current_user]
                        df_remaining.to_csv(csv_file, index=False)
                    else:
                        os.remove(csv_file)
                st.rerun()
        
        st.markdown("<hr style='margin: 10px 0px 20px 0px; border-color: #eee;'>", unsafe_allow_html=True)

        # --- IMPACT CARD (SCROLLABLE) ---
        total_co2, total_energy, item_counts = calculate_impact(df)
        most_common_item = max(item_counts, key=item_counts.get) if item_counts else "general"
        fact = get_educational_fact(most_common_item)
        
        st.markdown(f"""
        <div class="impact-card">
            <div class="impact-stats">
                <div style="font-size: 18px; font-weight: 700; margin-bottom: 5px;">🌍 Your Eco-Impact</div>
                <div class="big-stat">{total_co2:.2f} kg</div>
                <div class="small-stat">Estimated CO₂ Savings</div>
                <div class="small-stat" style="margin-top:5px;">⚡ {int(total_energy)} Wh Energy Conserved</div>
            </div>
            <div class="impact-fact">
                "{fact}"
            </div>
        </div>
        """, unsafe_allow_html=True)

        # --- HISTORY LIST (SCROLLABLE) ---
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
            
    else:
        st.markdown("""
        <div class="no-history">
            <div style="font-size: 50px; margin-bottom: 20px;">📜</div>
            No scans yet.<br>Go to the Home page to start scanning waste items!
        </div>
        """, unsafe_allow_html=True)