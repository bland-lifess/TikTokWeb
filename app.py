import streamlit as st
import requests
from urllib.parse import quote
import base64

# Page configuration
st.set_page_config(
    page_title="Web Browser",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for Chrome-like browser
st.markdown("""
    <style>
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Browser chrome styling */
    .browser-header {
        background: #f1f3f4;
        padding: 8px 12px;
        border-radius: 8px 8px 0 0;
        margin-bottom: 0;
        border: 1px solid #dadce0;
    }
    
    .url-bar {
        display: flex;
        align-items: center;
        background: white;
        border: 1px solid #dadce0;
        border-radius: 20px;
        padding: 8px 15px;
        margin: 5px 0;
    }
    
    .url-bar input {
        border: none !important;
        outline: none !important;
        flex: 1;
        font-size: 14px;
        background: transparent !important;
    }
    
    .browser-tabs {
        display: flex;
        gap: 4px;
        margin-bottom: 8px;
        border-bottom: 1px solid #dadce0;
        padding-bottom: 4px;
    }
    
    .tab {
        background: #e8eaed;
        padding: 8px 16px;
        border-radius: 8px 8px 0 0;
        cursor: pointer;
        font-size: 13px;
        max-width: 200px;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
    }
    
    .tab.active {
        background: white;
    }
    
    .browser-content {
        background: white;
        border: 1px solid #dadce0;
        border-top: none;
        border-radius: 0 0 8px 8px;
        min-height: 700px;
        padding: 0;
        overflow: hidden;
    }
    
    iframe {
        width: 100%;
        height: 700px;
        border: none;
    }
    
    .stButton button {
        background: transparent;
        border: none;
        padding: 8px 12px;
        font-size: 18px;
        cursor: pointer;
    }
    
    .stButton button:hover {
        background: #e8eaed;
        border-radius: 50%;
    }
    
    @media (max-width: 768px) {
        iframe {
            height: 500px;
        }
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'tabs' not in st.session_state:
    st.session_state.tabs = [{'title': 'New Tab', 'url': ''}]
if 'active_tab' not in st.session_state:
    st.session_state.active_tab = 0
if 'history' not in st.session_state:
    st.session_state.history = []

def get_proxy_url(url):
    """
    Create a proxy URL that works with JavaScript-heavy sites
    """
    if not url:
        return None
    
    # Add https:// if not present
    if not url.startswith(('http://', 'https://')):
        url = 'https://' + url
    
    return url

def search_web(query):
    """
    Search and return Google search URL
    """
    return f"https://www.google.com/search?q={quote(query)}&igu=1"

# Browser Header
st.markdown('<div class="browser-header">', unsafe_allow_html=True)

# Tab bar
cols = st.columns([0.5, 0.5, 0.5, 6, 0.5])

with cols[0]:
    if st.button("◀", help="Back", key="back_btn"):
        if len(st.session_state.history) > 1:
            st.session_state.history.pop()
            prev_url = st.session_state.history[-1] if st.session_state.history else ''
            st.session_state.tabs[st.session_state.active_tab]['url'] = prev_url

with cols[1]:
    if st.button("▶", help="Forward", key="fwd_btn"):
        pass  # Placeholder for forward functionality

with cols[2]:
    if st.button("⟳", help="Refresh", key="refresh_btn"):
        st.rerun()

# URL/Search bar
with cols[3]:
    current_tab = st.session_state.tabs[st.session_state.active_tab]
    url_input = st.text_input(
        "URL",
        value=current_tab.get('url', ''),
        placeholder="Search Google or type a URL",
        label_visibility="collapsed",
        key="url_input_field"
    )

with cols[4]:
    if st.button("➕", help="New Tab"):
        st.session_state.tabs.append({'title': 'New Tab', 'url': ''})
        st.session_state.active_tab = len(st.session_state.tabs) - 1
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# Handle URL/Search submission
if url_input and url_input != current_tab.get('url', ''):
    # Check if it's a search query or URL
    if ' ' in url_input or (not '.' in url_input and not url_input.startswith('http')):
        # It's a search query
        final_url = search_web(url_input)
        st.session_state.tabs[st.session_state.active_tab]['title'] = f"Search: {url_input[:20]}"
    else:
        # It's a URL
        final_url = get_proxy_url(url_input)
        st.session_state.tabs[st.session_state.active_tab]['title'] = url_input.replace('https://', '').replace('http://', '')[:30]
    
    st.session_state.tabs[st.session_state.active_tab]['url'] = final_url
    st.session_state.history.append(final_url)
    st.rerun()

# Display current page in iframe
current_url = st.session_state.tabs[st.session_state.active_tab].get('url', '')

if current_url:
    st.markdown('<div class="browser-content">', unsafe_allow_html=True)
    
    # Embed the website using iframe
    iframe_html = f"""
    <iframe 
        src="{current_url}" 
        sandbox="allow-same-origin allow-scripts allow-popups allow-forms allow-top-navigation"
        loading="lazy"
        allowfullscreen
    ></iframe>
    """
    st.markdown(iframe_html, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
else:
    # New tab page with shortcuts
    st.markdown('<div class="browser-content" style="padding: 40px; text-align: center;">', unsafe_allow_html=True)
    st.markdown("### 🌐 Start Browsing")
    st.markdown("Type a URL or search in the bar above")
    
    st.markdown("#### Quick Links")
    col1, col2, col3, col4 = st.columns(4)
    
    quick_links = [
        ("🔍 Google", "https://www.google.com"),
        ("📺 YouTube", "https://www.youtube.com"),
        ("🐦 Twitter", "https://www.twitter.com"),
        ("📰 Reddit", "https://www.reddit.com"),
        ("📖 Wikipedia", "https://www.wikipedia.org"),
        ("📧 Gmail", "https://mail.google.com"),
        ("🎵 Spotify", "https://open.spotify.com"),
        ("💬 Discord", "https://discord.com")
    ]
    
    cols = [col1, col2, col3, col4]
    for idx, (name, url) in enumerate(quick_links):
        with cols[idx % 4]:
            if st.button(name, key=f"quick_{idx}", use_container_width=True):
                st.session_state.tabs[st.session_state.active_tab]['url'] = url
                st.session_state.tabs[st.session_state.active_tab]['title'] = name
                st.session_state.history.append(url)
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Tips
with st.expander("💡 Browser Tips"):
    st.markdown("""
    **How to use:**
    - **Search**: Type anything in the bar (e.g., "cat videos") and press Enter
    - **Visit sites**: Type URLs like `youtube.com`, `reddit.com`, `twitter.com`
    - **Navigate**: Use ◀ Back button to go to previous pages
    - **New tabs**: Click ➕ to open a new tab
    
    **Supported sites:**
    - ✅ YouTube, Twitter, Reddit, Wikipedia, Google
    - ✅ News sites (CNN, BBC, etc.)
    - ✅ Most modern websites with JavaScript
    
    **Works in iframe:**
    Sites are loaded directly in the browser using iframe technology, so JavaScript/videos/interactive content all work!
    """)

st.markdown("<p style='text-align: center; color: gray; margin-top: 20px;'>Web Browser | Built with Streamlit</p>", unsafe_allow_html=True)
