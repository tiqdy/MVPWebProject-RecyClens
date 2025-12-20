import streamlit as st
import base64

st.set_page_config(
    page_title="RecycLens Login",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

def get_base64_of_bin_file(bin_file):
    try:
        with open(bin_file, "rb") as f:
            return base64.b64encode(f.read()).decode()
    except:
        return ""

logo_src = ""
try:
    logo_path = "images/recyclenslogo.png"
    img_base64 = get_base64_of_bin_file(logo_path)
    if img_base64:
        logo_src = f"data:image/png;base64,{img_base64}"
except:
    pass

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if st.session_state.logged_in:
    st.switch_page("pages/home.py")

st.markdown("""
<style>
[data-testid="stHeader"], [data-testid="stSidebar"], footer {
    display: none !important;
}

.stApp {
    background-color: #FFFFFF !important;
}

.main .block-container {
    padding-top: 20vh !important;
}

[data-testid="stForm"] {
    background-color: #FFFFFF !important;
    border: 1px solid #FFFFFF !important;
    border-radius: 12px;
    padding: 40px 30px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.05);
}

.login-logo {
    width: 250px;
    margin-bottom: 20px;
    display: block;
    margin-left: auto;
    margin-right: auto;
}

div[data-baseweb="base-input"] {
    background-color: #FFFFFF !important;
    border: 1px solid #FFFFFF !important;
    border-radius: 8px !important;
    padding: 5px 10px !important;
    box-shadow: none !important;
}

div[data-baseweb="base-input"] * {
    background-color: transparent !important;
    color: #000000 !important;
}


input[type="text"], input[type="password"] {
    font-weight: 500 !important;
    font-size: 16px !important;
}

input::placeholder {
    color: #FFFFFF !important;
}

div[data-baseweb="base-input"]:focus-within {
    border: 1px solid #2E7D32 !important;
    box-shadow: 0 0 0 1px #2E7D32 !important;
}

button[aria-label="Password visibility"] {
    display: none !important;
}

.stFormSubmitButton {
    width: 100%;
}

.stFormSubmitButton button {
    display: block !important;
    margin-left: 160px !important;
    margin-right: 160px  !important;
    margin-top: 20px !important;
    width: 150px !important;
    padding: 10px 0 !important;
    background-color: #2E7D32 !important;
    color: #FFFFFF !important;
    font-weight: 700 !important;
    font-size: 16px !important;
    border-radius: 8px !important;
    border: none !important;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
}

.stFormSubmitButton button:hover {
    background-color: #1B5E20 !important;
}

.stFormSubmitButton button:focus,
.stFormSubmitButton button:active {
    background-color: #1B5E20 !important;
    outline: none !important;
}

[data-testid="stForm"] > div {
    gap: 15px;
}

@media only screen and (max-width: 768px) {
    .main .block-container {
        padding-top: 5vh !important; 
    }
    
    .stFormSubmitButton button {
        margin-left: 80px !important;
        margin-right: 80px !important;
        margin-top: 16px !important;
        width: 100% !important;
        max-width: 280px !important;
        padding: 12px 0 !important;
        font-size: 15px !important;
        border-radius: 10px !important;
    }
    
    [data-testid="stForm"] {
        padding: 20px 15px; 
    }
    
    .login-logo {
        width: 200px; 
    }
}

</style>
""", unsafe_allow_html=True)

c1, c2, c3 = st.columns([3, 4, 3])

with c2:
    if logo_src:
        st.markdown(f'<img src="{logo_src}" class="login-logo">', unsafe_allow_html=True)

    with st.form("login_form"):
        st.markdown('<h3 style="text-align:center; color:#2E7D32; margin-bottom:20px; font-family:Helvetica, sans-serif;">Welcome! Let’s Recycle Smarter.</h3>', unsafe_allow_html=True)

        username = st.text_input("Username", placeholder="Username", label_visibility="collapsed")
        password = st.text_input("Password", type="password", placeholder="Password", label_visibility="collapsed")

        submitted = st.form_submit_button("Login")

        if submitted:
            if username.strip() and password == "1234":
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Success!")
                st.switch_page("pages/home.py")
            else:
                st.error("Invalid username or password")
