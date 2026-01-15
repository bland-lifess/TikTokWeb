import streamlit as st
import streamlit.components.v1 as components
from urllib.parse import quote

# Page configuration
st.set_page_config(
    page_title="Ultraviolet Web Proxy",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {visibility: hidden;}
    
    .main .block-container {
        padding: 0.5rem;
        max-width: 100%;
    }
    
    .proxy-container {
        width: 100%;
        height: 90vh;
        border: none;
        border-radius: 8px;
        overflow: hidden;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'proxy_url' not in st.session_state:
    st.session_state.proxy_url = ""

# Navigation bar
col1, col2, col3 = st.columns([0.3, 6, 0.5])

with col1:
    if st.button("🏠 Home", key="home"):
        st.session_state.proxy_url = ""
        st.rerun()

with col2:
    url_input = st.text_input(
        "url",
        placeholder="Enter URL or search... (e.g., youtube.com, reddit.com)",
        label_visibility="collapsed",
        key="url_input"
    )

with col3:
    go_clicked = st.button("Go", key="go")

# Handle navigation
if url_input and (go_clicked or url_input != st.session_state.get('last_input', '')):
    st.session_state.last_input = url_input
    
    # Determine if URL or search
    if url_input.startswith('http://') or url_input.startswith('https://'):
        final_url = url_input
    elif '.' in url_input and ' ' not in url_input:
        final_url = f"https://{url_input}"
    else:
        # Search query
        final_url = f"https://www.google.com/search?q={quote(url_input)}"
    
    st.session_state.proxy_url = final_url

# Main content
if st.session_state.proxy_url:
    st.info(f"🌐 Loading: {st.session_state.proxy_url}")
    
    # Full HTML with Ultraviolet proxy embedded
    proxy_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Proxy</title>
        <style>
            body, html {{
                margin: 0;
                padding: 0;
                width: 100%;
                height: 100vh;
                overflow: hidden;
            }}
            iframe {{
                width: 100%;
                height: 100%;
                border: none;
            }}
        </style>
    </head>
    <body>
        <iframe src="https://holyubofficial.net/service/hvtrs8%2F-wuw%2Cgmoelg.aoo%2F" 
                sandbox="allow-scripts allow-same-origin allow-forms allow-popups allow-modals allow-top-navigation-by-user-activation"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                allowfullscreen>
        </iframe>
        <script>
            // Try to communicate with iframe to navigate
            const frame = document.querySelector('iframe');
            if (frame) {{
                frame.onload = function() {{
                    try {{
                        frame.contentWindow.postMessage({{
                            type: 'navigate',
                            url: '{st.session_state.proxy_url}'
                        }}, '*');
                    }} catch(e) {{
                        console.log('Could not navigate:', e);
                    }}
                }};
            }}
        </script>
    </body>
    </html>
    """
    
    components.html(proxy_html, height=700, scrolling=True)
    
    st.caption("💡 **Tip:** If site doesn't load, try opening it directly in [Holy Unblocker](https://holyubofficial.net)")

else:
    # Home page
    st.markdown("# 🌐 Ultraviolet Web Proxy")
    st.markdown("### Browse any website anonymously")
    
    st.markdown("---")
    
    st.markdown("#### 🚀 Quick Access Sites")
    
    col1, col2, col3, col4 = st.columns(4)
    
    quick_sites = [
        ("🔍 Google", "google.com"),
        ("📺 YouTube", "youtube.com"),
        ("🐦 Twitter", "twitter.com"),
        ("📰 Reddit", "reddit.com"),
        ("📖 Wikipedia", "wikipedia.org"),
        ("🎮 Discord", "discord.com"),
        ("💬 TikTok", "tiktok.com"),
        ("📧 Gmail", "mail.google.com"),
    ]
    
    cols = [col1, col2, col3, col4]
    for idx, (name, url) in enumerate(quick_sites):
        with cols[idx % 4]:
            if st.button(name, key=f"quick_{idx}", use_container_width=True):
                st.session_state.proxy_url = f"https://{url}"
                st.rerun()
    
    st.markdown("---")
    
    st.markdown("### ℹ️ How to Use")
    st.markdown("""
    **Simple Steps:**
    1. Type a website URL in the search bar above (e.g., `youtube.com`)
    2. Press Enter or click "Go"
    3. Browse the site normally!
    
    **Works with:**
    - ✅ YouTube (with videos!)
    - ✅ Twitter/X
    - ✅ Reddit
    - ✅ TikTok
    - ✅ Discord
    - ✅ Wikipedia
    - ✅ Most websites!
    
    **Note:** This uses the Holy Unblocker Ultraviolet proxy service. Some sites may require you to visit [holyubofficial.net](https://holyubofficial.net) directly for full functionality.
    """)
    
    st.markdown("---")
    
    with st.expander("🔧 Want to host your own Ultraviolet proxy?"):
        st.markdown("""
        **Option 1: Use a public Ultraviolet instance**
        - Current: [Holy Unblocker](https://holyubofficial.net)
        - Alternative: [Incognito](https://incog.dev)
        
        **Option 2: Deploy your own (Advanced)**
        1. Fork the [Ultraviolet-App repository](https://github.com/titaniumnetwork-dev/Ultraviolet-App)
        2. Deploy to Vercel, Netlify, or Railway (all have free tiers)
        3. Update this Streamlit app to point to your deployed proxy
        
        This is more advanced but gives you full control!
        """)

st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>Powered by Ultraviolet Proxy | Built with Streamlit</p>", unsafe_allow_html=True)
