import streamlit as st
from keras.models import load_model
from PIL import Image, ImageOps
import numpy as np
from datetime import datetime
import base64 
import pandas as pd
import os
import streamlit.components.v1 as components
import google.generativeai as genai

# 1. PAGE CONFIGURATION
st.set_page_config(
    page_title="RecycLens",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. HELPER FUNCTION
def get_base64_of_bin_file(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except Exception:
        return ""

# --- IMAGE LOADING ---
# 1. Main Logo
logo_src = ""
try:
    logo_path = "images/recyclenslogo.png"
    img_base64 = get_base64_of_bin_file(logo_path)
    if img_base64:
        logo_src = f"data:image/png;base64,{img_base64}"
except:
    pass

# 2. Chatbot Icon (Local Only)
chat_icon_url = ""
try:
    chat_icon_path = "images/chatbot.png"
    chat_b64 = get_base64_of_bin_file(chat_icon_path)
    if chat_b64:
        chat_icon_url = f"data:image/png;base64,{chat_b64}"
except:
    pass

# 3. CSS STYLING
st.markdown(f"""
<style>
    /* --- GLOBAL STYLES --- */
    .stApp {{ 
        background-color: #FFFFFF; 
        color: #000000; 
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; 
    }}
    
    p, li, div {{ 
        color: #000000; 
    }}

    .block-container {{ 
        max-width: 1200px !important; 
        padding-top: 70px !important; 
        padding-left: 2rem !important; 
        padding-right: 2rem !important; 
        margin: auto !important; 
    }}

    /* Hide Default Elements */
    [data-testid="stHeader"], 
    [data-testid="stSidebar"], 
    #MainMenu, 
    footer {{ 
        display: none; 
    }}
    
    /* --- FIXED HEADER --- */
    .fixed-header {{ 
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
    }}

    .header-left {{ 
        display: flex; 
        flex-direction: column; 
        justify-content: center; 
    }}

    .header-logo {{ 
        height: 50px; 
        width: auto; 
        object-fit: contain; 
    }}

    .header-tagline {{ 
        font-size: 14px; 
        color: #000000; 
        font-weight: 500; 
        margin-top: 2px; 
    }}

    .header-right {{ 
        display: flex; 
        gap: 30px; 
        align-items: center; 
    }}

    .nav-link {{ 
        color: #000000; 
        text-decoration: none !important; 
        font-weight: 600; 
        font-size: 18px; 
        background: transparent; 
        border: none; 
    }}

    .nav-link:hover {{ 
        color: #1B5E20; 
        cursor: pointer; 
    }}
    
    /* --- MAIN CONTENT --- */
    .main-desc {{ 
        text-align: center; 
        font-size: 22px; 
        color: #000000; 
        max-width: 900px; 
        margin: 0 auto 40px auto; 
        line-height: 1.6; 
        font-weight: 500; 
    }}

    .section-header {{ 
        text-align: center; 
        font-size: 24px; 
        font-weight: 700; 
        color: #000000; 
        margin-bottom: 20px; 
    }}
    
    /* --- CAMERA STYLING --- */
    [data-testid="stCameraInput"] {{ 
        width: 100% !important; 
        margin: 0 auto; 
    }}

    [data-testid="stCameraInput"] > div:first-child {{ 
        border-radius: 12px; 
        border: 2px solid #000000; 
    }}

    [data-testid="stCameraInput"] button {{ 
        background-color: #2E7D32 !important; 
        color: #FFFFFF !important; 
        border-radius: 8px !important; 
        margin-top: 20px !important; 
    }}

    /* --- RESULT CARDS --- */
    .result-card-success {{ 
        background-color: #F1F8E9; 
        border: 2px solid #2E7D32; 
        border-radius: 12px; 
        padding: 20px; 
        text-align: center; 
        margin-top: 20px; 
        color: black; 
    }}

    .result-card-error {{ 
        background-color: #FFEBEE; 
        border: 2px solid #C62828; 
        border-radius: 12px; 
        padding: 20px; 
        text-align: center; 
        margin-top: 20px; 
        color: black; 
    }}

    .result-value {{ 
        font-size: 36px; 
        font-weight: 900; 
        color: #000000; 
        margin: 0; 
    }}

    /* --- BUTTONS ("Read More") --- */
    div.stButton > button {{
        background-color: #2E7D32 !important; 
        border: none;
        padding: 10px 20px;
        font-size: 16px;
        font-weight: 700;
        border-radius: 6px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.2);
    }}
    
    div.stButton > button p {{
        color: #FFFFFF !important;
    }}
    
    div.stButton > button:hover {{
        background-color: #1B5E20 !important; 
        border: none;
    }}
    
    /* Force text white on hover too */
    div.stButton > button:hover p {{
        color: #FFFFFF !important;
    }}
    
    
    /* --- CHATBOT CSS --- */
    
    /* 1. Container Positioning */
    div[data-testid="stExpander"] {{
        position: fixed;
        bottom: 30px;
        right: 30px;
        width: auto;
        z-index: 999999;
        background: transparent;
        border: none;
    }}

    /* 2. The Open Chat Window */
    div[data-testid="stExpander"] > details[open] {{
        background-color: white;
        width: 380px;
        max-height: 550px;
        border-radius: 16px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.15);
        border: 1px solid #e0e0e0;
        padding: 0;
        display: flex;
        flex-direction: column;
        overflow: hidden;
    }}
    
    div[data-testid="stExpander"] > details[open] > div {{
        overflow-y: auto;
        max-height: 400px; 
        padding: 15px;
        padding-bottom: 0px;
    }}

    /* 3. The Circular Button (Summary) */
    div[data-testid="stExpander"] > details > summary {{
        list-style: none;
        display: block;
        width: 65px;
        height: 65px;
        border-radius: 50%;
        background-color: #2E7D32; 
        
        background-image: url('{chat_icon_url}'); 
        background-size: 35px; 
        background-repeat: no-repeat;
        background-position: center;
        
        color: transparent !important; 
        font-size: 0px !important;    
        
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
        cursor: pointer;
        transition: transform 0.2s, background-color 0.2s;
        margin-left: auto; 
        overflow: hidden;
    }}

    div[data-testid="stExpander"] > details > summary:hover {{
        transform: scale(1.1);
        background-color: #1B5E20;
    }}
    

    div[data-testid="stExpander"] > details > summary::-webkit-details-marker {{ display: none; }}
    div[data-testid="stExpander"] > details > summary > svg {{ display: none !important; }}

    /* 4. Chat Input Styling */
    div[data-testid="stForm"] {{
        border: none;
        padding: 10px;
        background-color: #f7f7f7;
        border-top: 1px solid #eee;
    }}

    div[data-testid="stForm"] input[type="text"] {{
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 1px solid #ccc !important;
        border-radius: 8px !important;
    }}
    
    div[data-testid="stForm"] button {{
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 1px solid #ccc !important;
        border-radius: 8px !important;
    }}
    div[data-testid="stForm"] button:hover {{
        background-color: #f0f0f0 !important;
        border: 1px solid #bbb !important;
    }}

    @media only screen and (max-width: 768px) {{
        .fixed-header {{ padding: 0 15px; height: 70px; }}
        .header-logo {{ height: 35px; }}
        .header-tagline {{ display: none; }}
        .header-right {{ gap: 15px; }}
        div[data-testid="stExpander"] > details[open] {{ width: 300px; right: 10px; bottom: 80px; }}
        div[data-testid="stExpander"] {{ bottom: 20px; right: 20px; }}
    }}
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

# 5. FIXED HEADER
st.markdown(f"""
    <div class="fixed-header">
        <div class="header-left">
            <a href="/" target="_self"><img src="{logo_src}" class="header-logo" alt="RecycLens"></a>
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
                    try: st.switch_page(page_link)
                    except: st.switch_page("pages/about.py")

        components.html("""<script>
            const anchor = window.parent.document.getElementById('result-anchor');
            if (anchor) { anchor.scrollIntoView({behavior: 'smooth', block: 'start'}); }
        </script>""", height=0)

# 8. CHATBOT LOGIC
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hi! I am RecycLens AI. Ask me how to recycle!"}
    ]

gemini_ready = False
try:
    if "GOOGLE_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
        gemini_ready = True
except:
    pass

if gemini_ready:
    # Use empty string label to avoid text artifacts
    with st.expander(" "): 
        
        # 1. Message History
        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])
        
        # 2. Input Form
        with st.form(key='chat_form', clear_on_submit=True):
            user_input = st.text_input("Type your question here...", key="user_input_val")
            
            cols = st.columns([4,1])
            with cols[1]:
                submit_button = st.form_submit_button("➤")
            
        # 3. Handle Logic
        if submit_button and user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            st.rerun() 

        # 4. Generate AI Response
        if st.session_state.messages[-1]["role"] == "user":
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    try:
                        gemini_history = []
                        for m in st.session_state.messages:
                            role = "user" if m["role"] == "user" else "model"
                            gemini_history.append({"role": role, "parts": [m["content"]]})
                        
                        model = genai.GenerativeModel("gemini-2.5-flash")
                        response = model.generate_content(gemini_history)
                        
                        st.session_state.messages.append({"role": "assistant", "content": response.text})
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")

    # --- CLICK OUTSIDE TO CLOSE (JS) ---
    components.html("""
        <script>
        const parentDoc = window.parent.document;
        if (!parentDoc.hasOwnProperty('chatListenerAttached')) {
            parentDoc.addEventListener('click', function(e) {
                const expander = parentDoc.querySelector('div[data-testid="stExpander"] details');
                if (expander && expander.hasAttribute('open')) {
                    if (!expander.contains(e.target)) {
                        expander.removeAttribute('open');
                    }
                }
            });
            parentDoc.chatListenerAttached = true;
        }
        </script>
        """, height=0)

else:
    pass


