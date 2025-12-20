import streamlit as st
import base64
from datetime import datetime

# 1. PAGE CONFIGURATION
st.set_page_config(
    page_title="My Account",
    page_icon="👤",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# SESSION RECOVERY & SECURITY
if "user" in st.query_params:
    st.session_state.logged_in = True
    st.session_state.username = st.query_params["user"]

if "logged_in" not in st.session_state or not st.session_state.logged_in:
    st.switch_page("app.py")

current_user = st.session_state.username if "username" in st.session_state else "Guest"

# 2. HELPER FUNCTION
def get_base64_of_bin_file(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except Exception:
        return ""

# --- LOAD IMAGES ---
logo_src = ""
try:
    logo_path = "images/recyclenslogo.png" 
    img_base64 = get_base64_of_bin_file(logo_path)
    if img_base64:
        logo_src = f"data:image/png;base64,{img_base64}"
except:
    pass

# 3. CSS STYLING
st.markdown(f"""
<style>
    /* --- GLOBAL STYLES --- */
    .stApp {{ 
        background-color: #FFFFFF !important; 
        color: #000000; 
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; 
    }}
    
    [data-testid="stHeader"], footer, [data-testid="stSidebar"] {{ display: none !important; }}
    
    /* --- FIXED HEADER STYLING --- */
    .fixed-header {{
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100px;
        background-color: #FFFFFF;
        z-index: 10000;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0 40px;
        box-sizing: border-box;
    }}

    .header-left {{
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: flex-start;
    }}

    .header-logo {{
        height: 50px;
        object-fit: contain;
        margin-bottom: 2px;
    }}

    .header-quote {{
        font-size: 13px;
        color: #555555;
        font-weight: 500;
        font-style: italic;
        margin: 0;
        white-space: nowrap;
    }}

    .header-right {{
        display: flex;
        gap: 35px;
        align-items: center;
    }}

    .nav-link {{
        color: #000000;
        text-decoration: none !important;
        font-weight: 700;
        font-size: 18px;
        background: transparent;
        border: none;
        transition: color 0.2s ease;
    }}

    .nav-link:hover {{
        color: #2E7D32;
        cursor: pointer;
    }}
    
    /* --- PROFILE CARD STYLING --- */
    .profile-container {{
        margin-top: 20px !important;
        background-color: #F9F9F9;
        border: 1px solid #E0E0E0;
        border-radius: 20px;
        padding: 40px;
        max-width: 500px;
        margin: 150px auto 20px auto; 
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
    }}
    
    .profile-pic {{
        width: 120px;
        height: 120px;
        border-radius: 50%;
        background-color: #E0E0E0;
        object-fit: cover;
        margin-bottom: 20px;
        border: 4px solid #2E7D32; 
    }}
    
    .user-name {{
        font-size: 28px;
        font-weight: 700;
        color: #2E7D32;
        margin-bottom: 5px;
    }}
    
    .user-role {{
        font-size: 16px;
        color: #666;
        margin-bottom: 30px;
    }}
    
    .info-row {{
        display: flex;
        justify-content: space-between;
        padding: 15px 0;
        border-bottom: 1px solid #eee;
        font-size: 16px;
    }}
    
    .info-label {{ font-weight: 600; color: #333; }}
    .info-value {{ color: #666; }}
    
    /* Logout Button Styling */
    div.stButton > button {{
        background-color: #C62828 !important; 
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        padding: 10px 30px !important;
        margin-left: 60px !important;
        margin-right: 50px !important;
        margin-top: 20px !important;
        width: 100%;
        box-shadow: 0 2px 5px rgba(0,0,0,0.2);
    }}
    div.stButton > button:hover {{
        background-color: #B71C1C !important;
    }}
    
    /* Responsive */
    @media only screen and (max-width: 768px) {{
        .fixed-header {{ 
            padding: 0 20px; 
            height: 80px; 
        }}
        .header-logo {{ height: 40px; }}
        .header-quote {{ display: none; }}
        
        .header-right {{ gap: 15px; }}
        
        /* HIDE HOME NAV ON MOBILE */
        .header-right a:nth-child(1) {{
            display: none;
        }}
        
        .nav-link {{ font-size: 14px; }}
        
        .block-container {{
            padding-top: 100px !important;
        }}
        
        .profile-container {{ 
            padding: 25px; 
        }}
        
        /* Full width button on mobile */
        div.stButton {{margin-left: 10px !important; margin-right: 15px !important;}}
    }}
</style>
""", unsafe_allow_html=True)

# 4. FIXED HEADER
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
<a href="/history?user={current_user}" target="_self" class="nav-link">History</a>
<a href="/account?user={current_user}" target="_self" class="nav-link" style="font-size: 24px;">👤</a>
</div>
</div>
""", unsafe_allow_html=True)

# 5. PROFILE CONTENT
avatar_url = "https://cdn-icons-png.flaticon.com/512/3135/3135715.png"
username = current_user
email = f"{username.lower().replace(' ', '')}@recyclens.com"
join_date = datetime.now().strftime("%B %Y")

st.markdown(f"""
<div class="profile-container">
<img src="{avatar_url}" class="profile-pic">
<div class="user-name">{username}</div>
<div class="user-role">RecycLens Member</div>
<div class="info-row">
<span class="info-label">Email</span>
<span class="info-value">{email}</span>
</div>
<div class="info-row">
<span class="info-label">Member Since</span>
<span class="info-value">{join_date}</span>
</div>
<div class="info-row" style="border-bottom: none;">
<span class="info-label">Status</span>
<span class="info-value" style="color: #2E7D32; font-weight: bold;">Active</span>
</div>
</div>
""", unsafe_allow_html=True)

# Logout Button
c1, c2, c3 = st.columns([3, 2, 3])
with c2:
    if st.button("Log Out"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.switch_page("app.py")