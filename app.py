import streamlit as st
import streamlit.components.v1 as components
from urllib.parse import quote
import base64

# Page configuration
st.set_page_config(
    page_title="Web Proxy",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS - Full screen mode
st.markdown("""
    <style>
    /* Hide ALL Streamlit UI elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {visibility: hidden;}
    .stToolbar {visibility: hidden;}
    
    /* Remove all padding and margins */
    .main .block-container {
        padding: 0 !important;
        margin: 0 !important;
        max-width: 100% !important;
    }
    
    .main {
        padding: 0 !important;
    }
    
    /* Browser bar styling */
    .browser-bar {
        background: #202124;
        padding: 8px 12px;
        display: flex;
        gap: 8px;
        align-items: center;
        position: sticky;
        top: 0;
        z-index: 1000;
    }
    
    .stTextInput > div > div > input {
        background: #303134 !important;
        color: #e8eaed !important;
        border: 1px solid #5f6368 !important;
        border-radius: 24px !important;
        padding: 8px 16px !important;
        font-size: 14px !important;
    }
    
    .stTextInput > div > div > input:focus {
        background: #303134 !important;
        border-color: #8ab4f8 !important;
    }
    
    .stButton > button {
        background: #8ab4f8 !important;
        color: #202124 !important;
        border: none !important;
        border-radius: 4px !important;
        padding: 8px 16px !important;
        font-weight: 500 !important;
    }
    
    .stButton > button:hover {
        background: #aecbfa !important;
    }
    
    /* Hide Streamlit's default spacing */
    .element-container {
        margin: 0 !important;
        padding: 0 !important;
    }
    
    div[data-testid="column"] {
        padding: 0 !important;
    }
    
    /* Full screen iframe */
    .stIframe {
        border: none !important;
    }
    
    iframe {
        border: none !important;
        display: block !important;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'current_url' not in st.session_state:
    st.session_state.current_url = ""
if 'encoded_url' not in st.session_state:
    st.session_state.encoded_url = ""

def encode_url_for_proxy(url):
    """
    Encode URL for Holy Unblocker's Ultraviolet proxy
    """
    if not url:
        return ""
    
    # Add https:// if needed
    if not url.startswith('http://') and not url.startswith('https://'):
        url = f"https://{url}"
    
    # Holy Unblocker uses base64 encoding in the URL path
    # Format: https://holyubofficial.net/service/hvtrs8%2F-[encoded_url]
    
    # Their encoding scheme: https:// becomes hvtrs8%2F-
    encoded = url.replace('https://', 'hvtrs8%2F-').replace('http://', 'hvtr8%2F-')
    encoded = encoded.replace('.', ',').replace('/', '%2F')
    
    return f"https://holyubofficial.net/service/{encoded}"

# Browser navigation bar
col1, col2, col3 = st.columns([0.2, 8, 0.4])

with col1:
    if st.button("🏠", key="home", help="Home"):
        st.session_state.current_url = ""
        st.session_state.encoded_url = ""
        st.rerun()

with col2:
    url_input = st.text_input(
        "url",
        value=st.session_state.current_url,
        placeholder="Search or enter website (e.g., youtube.com, reddit.com)",
        label_visibility="collapsed",
        key="url_bar"
    )

with col3:
    go_button = st.button("Go", key="go_btn")

# Handle URL submission
if url_input and (go_button or url_input != st.session_state.current_url):
    st.session_state.current_url = url_input
    
    # Check if it's a search or URL
    if ' ' in url_input or (not '.' in url_input and not url_input.startswith('http')):
        # It's a search - use Google
        search_url = f"https://www.google.com/search?q={quote(url_input)}"
        st.session_state.encoded_url = encode_url_for_proxy(search_url)
    else:
        # It's a URL
        st.session_state.encoded_url = encode_url_for_proxy(url_input)
    
    st.rerun()

# Display proxy content
if st.session_state.encoded_url:
    # Use full viewport height minus the nav bar
    components.iframe(
        st.session_state.encoded_url,
        height=850,
        scrolling=True
    )
else:
    # Home page with quick links
    st.markdown("""
        <div style='padding: 40px; text-align: center; background: #202124; color: #e8eaed; min-height: 80vh;'>
            <h1 style='font-size: 3rem; margin-bottom: 20px;'>🌐 Web Proxy</h1>
            <p style='font-size: 1.2rem; color: #9aa0a6; margin-bottom: 40px;'>
                Browse any website unblocked
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### 🚀 Quick Access")
    
    col1, col2, col3, col4 = st.columns(4)
    
    sites = [
        ("🔍 Google", "google.com"),
        ("📺 YouTube", "youtube.com"),
        ("🐦 Twitter", "twitter.com"),
        ("📰 Reddit", "reddit.com"),
        ("💬 Discord", "discord.com"),
        ("📱 TikTok", "tiktok.com"),
        ("📖 Wikipedia", "wikipedia.org"),
        ("🎮 Twitch", "twitch.tv"),
    ]
    
    cols = [col1, col2, col3, col4]
    for idx, (name, url) in enumerate(sites):
        with cols[idx % 4]:
            if st.button(name, key=f"site_{idx}", use_container_width=True):
                st.session_state.current_url = url
                st.session_state.encoded_url = encode_url_for_proxy(url)
                st.rerun()
    
    st.markdown("---")
    
    with st.expander("ℹ️ How to Use"):
        st.markdown("""
        **Getting Started:**
        1. Type any website in the search bar (e.g., `youtube.com`)
        2. Press Enter or click "Go"
        3. The site loads through the proxy!
        
        **Search:**
        - Type anything with spaces to search Google
        - Example: "funny cat videos" → Google search
        
        **Direct URLs:**
        - Type: `youtube.com` → YouTube
        - Type: `reddit.com` → Reddit
        - Type: `twitter.com` → Twitter
        
        **Features:**
        - ✅ Bypass all blocks and restrictions
        - ✅ Works with YouTube, Discord, Reddit, etc.
        - ✅ Full JavaScript support
        - ✅ Mobile friendly
        
        **Note:** Uses Holy Unblocker's Ultraviolet proxy service
        """)
