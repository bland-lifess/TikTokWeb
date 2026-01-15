import streamlit as st
import streamlit.components.v1 as components
from urllib.parse import quote

# Page configuration
st.set_page_config(
    page_title="Nebula Proxy",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Modern UI CSS
st.markdown("""
    <style>
    /* Hide Streamlit UI */
    #MainMenu, footer, header, .stDeployButton, .stToolbar {visibility: hidden;}
    
    /* Full screen layout */
    .main .block-container {
        padding: 0 !important;
        max-width: 100% !important;
    }
    
    /* Modern gradient background */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Glassmorphism browser bar */
    .browser-header {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 16px;
        padding: 16px;
        margin: 12px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    
    /* URL input styling */
    .stTextInput > div > div > input {
        background: rgba(255, 255, 255, 0.9) !important;
        border: 2px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 24px !important;
        padding: 14px 20px !important;
        font-size: 15px !important;
        color: #2d3748 !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
    }
    
    .stTextInput > div > div > input:focus {
        background: white !important;
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px 24px !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6) !important;
    }
    
    /* Content area */
    .content-frame {
        background: white;
        border-radius: 16px;
        margin: 0 12px 12px 12px;
        overflow: hidden;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
    }
    
    /* Home page styling */
    .home-container {
        padding: 60px 20px;
        text-align: center;
        color: white;
    }
    
    .home-title {
        font-size: 4rem;
        font-weight: 800;
        margin-bottom: 16px;
        background: linear-gradient(135deg, #fff 0%, #f0f0f0 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: 0 2px 10px rgba(0,0,0,0.1);
    }
    
    .home-subtitle {
        font-size: 1.4rem;
        opacity: 0.9;
        margin-bottom: 40px;
        font-weight: 300;
    }
    
    /* Quick links cards */
    .quick-link-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.2);
        border-radius: 12px;
        padding: 20px;
        margin: 10px;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    .quick-link-card:hover {
        background: rgba(255, 255, 255, 0.2);
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
    }
    
    /* Mobile responsive */
    @media (max-width: 768px) {
        .home-title {font-size: 2.5rem;}
        .home-subtitle {font-size: 1.1rem;}
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'proxy_url' not in st.session_state:
    st.session_state.proxy_url = ""
if 'input_value' not in st.session_state:
    st.session_state.input_value = ""

# Browser header
col1, col2, col3 = st.columns([0.3, 7, 0.5])

with col1:
    if st.button("🏠 Home", key="home_btn"):
        st.session_state.proxy_url = ""
        st.session_state.input_value = ""
        st.rerun()

with col2:
    url_input = st.text_input(
        "url",
        value=st.session_state.input_value,
        placeholder="🔍 Search or enter URL... (youtube.com, reddit.com)",
        label_visibility="collapsed",
        key="url_input_field"
    )

with col3:
    go_clicked = st.button("Go →", key="go_button")

# Handle navigation
if url_input and (go_clicked or url_input != st.session_state.input_value):
    st.session_state.input_value = url_input
    
    # Determine if search or URL
    if ' ' in url_input or (not '.' in url_input and not url_input.startswith('http')):
        # Search query
        final_url = f"https://www.google.com/search?q={quote(url_input)}"
    else:
        # Direct URL
        if not url_input.startswith('http'):
            final_url = f"https://{url_input}"
        else:
            final_url = url_input
    
    # Use Holy Unblocker proxy - simpler URL format
    st.session_state.proxy_url = f"https://holyubofficial.net/?url={quote(final_url)}"
    st.rerun()

# Display content
if st.session_state.proxy_url:
    # Show loading indicator
    st.markdown(f'<div style="color: white; padding: 8px 20px; font-size: 13px;">🌐 Loading via proxy...</div>', unsafe_allow_html=True)
    
    # Full screen iframe
    components.iframe(
        st.session_state.proxy_url,
        height=780,
        scrolling=True
    )
else:
    # Modern home page
    st.markdown("""
        <div class="home-container">
            <div class="home-title">🌌 Nebula Proxy</div>
            <div class="home-subtitle">Browse the web without limits</div>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<h3 style='color: white; text-align: center; margin: 30px 0 20px 0;'>⚡ Quick Access</h3>", unsafe_allow_html=True)
    
    # Quick links
    col1, col2, col3, col4 = st.columns(4)
    
    quick_sites = [
        ("🔍", "Google", "google.com"),
        ("📺", "YouTube", "youtube.com"),
        ("🐦", "Twitter", "twitter.com"),
        ("💬", "Reddit", "reddit.com"),
        ("🎮", "Discord", "discord.com"),
        ("📱", "TikTok", "tiktok.com"),
        ("📖", "Wikipedia", "wikipedia.org"),
        ("🎬", "Twitch", "twitch.tv"),
    ]
    
    cols = [col1, col2, col3, col4]
    for idx, (emoji, name, url) in enumerate(quick_sites):
        with cols[idx % 4]:
            if st.button(f"{emoji}\n\n**{name}**", key=f"quick_{idx}", use_container_width=True):
                st.session_state.input_value = url
                st.session_state.proxy_url = f"https://holyubofficial.net/?url={quote(f'https://{url}')}"
                st.rerun()
    
    # Features section
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    feat1, feat2, feat3, feat4 = st.columns(4)
    
    with feat1:
        st.markdown("""
            <div style='text-align: center; color: white; padding: 20px;'>
                <div style='font-size: 2.5rem; margin-bottom: 10px;'>🚀</div>
                <div style='font-weight: 600; margin-bottom: 5px;'>Ultra Fast</div>
                <div style='font-size: 0.9rem; opacity: 0.8;'>Optimized proxy speed</div>
            </div>
        """, unsafe_allow_html=True)
    
    with feat2:
        st.markdown("""
            <div style='text-align: center; color: white; padding: 20px;'>
                <div style='font-size: 2.5rem; margin-bottom: 10px;'>🔒</div>
                <div style='font-weight: 600; margin-bottom: 5px;'>Secure</div>
                <div style='font-size: 0.9rem; opacity: 0.8;'>Encrypted connection</div>
            </div>
        """, unsafe_allow_html=True)
    
    with feat3:
        st.markdown("""
            <div style='text-align: center; color: white; padding: 20px;'>
                <div style='font-size: 2.5rem; margin-bottom: 10px;'>🌍</div>
                <div style='font-weight: 600; margin-bottom: 5px;'>No Limits</div>
                <div style='font-size: 0.9rem; opacity: 0.8;'>Access any website</div>
            </div>
        """, unsafe_allow_html=True)
    
    with feat4:
        st.markdown("""
            <div style='text-align: center; color: white; padding: 20px;'>
                <div style='font-size: 2.5rem; margin-bottom: 10px;'>📱</div>
                <div style='font-weight: 600; margin-bottom: 5px;'>Mobile Ready</div>
                <div style='font-size: 0.9rem; opacity: 0.8;'>Works everywhere</div>
            </div>
        """, unsafe_allow_html=True)
    
    # Tips
    st.markdown("<br>", unsafe_allow_html=True)
    with st.expander("💡 How to Use Nebula Proxy"):
        st.markdown("""
        **Quick Start:**
        - Type any website: `youtube.com`, `reddit.com`, `discord.com`
        - Or search: `funny videos`, `news today`
        - Press Enter or click "Go →"
        
        **Features:**
        - ✅ Unblock YouTube, Discord, Reddit, TikTok
        - ✅ Watch videos and use social media
        - ✅ Full JavaScript support
        - ✅ Mobile-friendly interface
        - ✅ No registration needed
        
        **Powered by:** Holy Unblocker (Ultraviolet Proxy)
        """)
