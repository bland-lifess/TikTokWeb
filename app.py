import streamlit as st
import streamlit.components.v1 as components

# Page configuration - MUST be first Streamlit command
st.set_page_config(
    page_title="Web Browser",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
    <style>
    /* Hide all Streamlit UI */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {visibility: hidden;}
    
    /* Remove padding */
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 0rem;
        max-width: 100%;
    }
    
    /* Browser styling */
    .browser-bar {
        background: #f1f3f4;
        padding: 10px 15px;
        border-radius: 8px;
        margin-bottom: 10px;
        display: flex;
        gap: 10px;
        align-items: center;
    }
    
    .nav-btn {
        background: white;
        border: 1px solid #dadce0;
        border-radius: 4px;
        padding: 6px 12px;
        cursor: pointer;
        font-size: 16px;
    }
    
    .nav-btn:hover {
        background: #f8f9fa;
    }
    
    input[type="text"] {
        flex: 1;
        padding: 8px 15px;
        border: 1px solid #dadce0;
        border-radius: 20px;
        font-size: 14px;
    }
    
    .stTextInput > div > div {
        background: white !important;
    }
    
    .stTextInput input {
        border-radius: 20px !important;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'current_url' not in st.session_state:
    st.session_state.current_url = ""
if 'search_query' not in st.session_state:
    st.session_state.search_query = ""

# Browser bar
col1, col2, col3, col4 = st.columns([0.4, 0.4, 6, 0.5])

with col1:
    if st.button("◀", key="back", help="Back"):
        pass

with col2:
    if st.button("⟳", key="reload", help="Reload"):
        st.rerun()

with col3:
    user_input = st.text_input(
        "url",
        value=st.session_state.search_query,
        placeholder="Search Google or enter URL...",
        label_visibility="collapsed",
        key="url_bar"
    )

with col4:
    if st.button("Go", key="go_btn"):
        st.session_state.search_query = user_input
        if user_input:
            # Check if URL or search
            if user_input.startswith('http://') or user_input.startswith('https://'):
                st.session_state.current_url = user_input
            elif '.' in user_input and ' ' not in user_input:
                st.session_state.current_url = f"https://{user_input}"
            else:
                # It's a search query
                from urllib.parse import quote
                st.session_state.current_url = f"https://www.google.com/search?igu=1&q={quote(user_input)}"
        st.rerun()

# Handle Enter key in text input
if user_input != st.session_state.search_query:
    st.session_state.search_query = user_input
    if user_input:
        if user_input.startswith('http://') or user_input.startswith('https://'):
            st.session_state.current_url = user_input
        elif '.' in user_input and ' ' not in user_input:
            st.session_state.current_url = f"https://{user_input}"
        else:
            from urllib.parse import quote
            st.session_state.current_url = f"https://www.google.com/search?igu=1&q={quote(user_input)}"
        st.rerun()

# Display the webpage
if st.session_state.current_url:
    # Use components.iframe for full page embedding
    components.iframe(st.session_state.current_url, height=800, scrolling=True)
else:
    # Welcome screen with quick links
    st.markdown("### 🌐 Web Browser")
    st.markdown("Enter a URL or search term above to get started")
    
    st.markdown("#### Quick Links")
    
    col1, col2, col3, col4 = st.columns(4)
    
    links = [
        ("Google", "https://www.google.com"),
        ("YouTube", "https://www.youtube.com"),
        ("Reddit", "https://www.reddit.com"),
        ("Wikipedia", "https://www.wikipedia.org"),
        ("Twitter", "https://www.twitter.com"),
        ("GitHub", "https://www.github.com"),
        ("Stack Overflow", "https://stackoverflow.com"),
        ("CNN", "https://www.cnn.com")
    ]
    
    for idx, (name, url) in enumerate(links):
        col = [col1, col2, col3, col4][idx % 4]
        with col:
            if st.button(f"🔗 {name}", key=f"link_{idx}", use_container_width=True):
                st.session_state.current_url = url
                st.session_state.search_query = url
                st.rerun()
    
    st.markdown("---")
    st.info("""
    **How to use:**
    - Type a URL: `youtube.com`, `reddit.com`, `twitter.com`
    - Or search: `funny cat videos`, `news today`
    - Press Enter or click Go
    
    **Note:** Some sites (like Google) may show blank due to iframe restrictions. Try the direct URL instead (e.g., `reddit.com` works great!)
    """)
