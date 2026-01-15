import streamlit as st
import streamlit.components.v1 as components

# MUST be first
st.set_page_config(
    page_title="Nebula Proxy",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Full screen CSS
st.markdown("""
<style>
/* Hide ALL Streamlit elements */
#MainMenu, footer, header, .stDeployButton {display: none !important;}
.stApp > header {display: none !important;}

/* Remove all padding */
.main .block-container {
    padding: 0 !important;
    max-width: 100% !important;
}
.main {padding: 0 !important;}

/* Modern gradient background */
.stApp {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

/* Navigation bar */
.nav-bar {
    background: rgba(255,255,255,0.95);
    backdrop-filter: blur(10px);
    padding: 12px 16px;
    display: flex;
    gap: 10px;
    align-items: center;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

/* Iframe container */
.proxy-frame {
    width: 100%;
    height: calc(100vh - 70px);
    background: white;
}

iframe {
    width: 100% !important;
    height: 100% !important;
    border: none !important;
}

/* Input styling */
.stTextInput input {
    border-radius: 20px !important;
    border: 2px solid #e0e0e0 !important;
    padding: 10px 20px !important;
    font-size: 14px !important;
}

.stTextInput input:focus {
    border-color: #667eea !important;
    box-shadow: 0 0 0 2px rgba(102,126,234,0.2) !important;
}

/* Button styling */
.stButton button {
    background: linear-gradient(135deg, #667eea, #764ba2) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 10px 20px !important;
    font-weight: 600 !important;
    transition: transform 0.2s !important;
}

.stButton button:hover {
    transform: scale(1.05) !important;
}

/* Home page */
.home-hero {
    padding: 60px 20px;
    text-align: center;
    color: white;
}

.hero-title {
    font-size: 4rem;
    font-weight: 800;
    margin-bottom: 20px;
    text-shadow: 0 4px 20px rgba(0,0,0,0.3);
}

.hero-subtitle {
    font-size: 1.5rem;
    opacity: 0.95;
    margin-bottom: 40px;
}

@media (max-width: 768px) {
    .hero-title {font-size: 2.5rem;}
    .hero-subtitle {font-size: 1.2rem;}
}
</style>
""", unsafe_allow_html=True)

# Session state
if 'url' not in st.session_state:
    st.session_state.url = ""

# Navigation
col1, col2, col3 = st.columns([0.4, 7, 0.6])

with col1:
    if st.button("🏠", key="home"):
        st.session_state.url = ""
        st.rerun()

with col2:
    url = st.text_input("", placeholder="Enter URL or search...", label_visibility="collapsed", key="url_input")

with col3:
    go = st.button("Go", key="go")

# Handle input
if url and (go or url != st.session_state.get('last', '')):
    st.session_state.last = url
    
    # Parse input
    from urllib.parse import quote
    if url.startswith('http'):
        final_url = url
    elif '.' in url and ' ' not in url:
        final_url = f"https://{url}"
    else:
        final_url = f"https://www.google.com/search?q={quote(url)}"
    
    st.session_state.url = final_url
    st.rerun()

# Display
if st.session_state.url:
    # Embed using full HTML component
    html_code = f"""
    <!DOCTYPE html>
    <html style="margin:0;padding:0;height:100vh;overflow:hidden;">
    <head>
        <style>
            body, html {{margin:0;padding:0;width:100%;height:100%;overflow:hidden;}}
            iframe {{width:100%;height:100%;border:none;display:block;}}
        </style>
    </head>
    <body>
        <iframe src="{st.session_state.url}" 
                sandbox="allow-same-origin allow-scripts allow-popups allow-forms allow-top-navigation allow-modals"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                allowfullscreen>
        </iframe>
    </body>
    </html>
    """
    components.html(html_code, height=800)
    
else:
    # Home page
    st.markdown("""
    <div class="home-hero">
        <div class="hero-title">🌌 Nebula Proxy</div>
        <div class="hero-subtitle">Browse freely and securely</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<h3 style='color:white;text-align:center;margin-bottom:30px;'>Quick Links</h3>", unsafe_allow_html=True)
    
    c1, c2, c3, c4 = st.columns(4)
    
    links = [
        ("Google", "google.com"),
        ("YouTube", "youtube.com"),
        ("Reddit", "reddit.com"),
        ("Twitter", "twitter.com"),
        ("Discord", "discord.com"),
        ("Wikipedia", "wikipedia.org"),
        ("GitHub", "github.com"),
        ("Spotify", "spotify.com")
    ]
    
    for i, (name, url) in enumerate(links):
        with [c1,c2,c3,c4][i%4]:
            if st.button(f"🔗 {name}", key=f"l{i}", use_container_width=True):
                st.session_state.url = f"https://{url}"
                st.rerun()
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    with st.expander("ℹ️ About"):
        st.markdown("""
        **How to use:**
        - Type a URL: `youtube.com`
        - Or search: `funny videos`
        - Press Enter or click Go
        
        **Note:** Some sites block iframe embedding for security. If a site shows blank:
        - Try the official Holy Unblocker: [holyunblocker.org](https://holyunblocker.org)
        - Or use Incognito: [incog.dev](https://incog.dev)
        
        These are dedicated Ultraviolet proxies that work better than embedded iframes.
        """)
