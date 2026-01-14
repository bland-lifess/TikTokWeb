import streamlit as st
from duckduckgo_search import DDGS
import time
import random

# Page configuration
st.set_page_config(
    page_title="Image Search Engine",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for mobile-friendly design
st.markdown("""
    <style>
    .main {
        padding: 1rem;
    }
    .stTextInput > div > div > input {
        font-size: 16px;
        padding: 12px;
    }
    h1 {
        font-size: 2rem;
        margin-bottom: 1.5rem;
        text-align: center;
    }
    @media (max-width: 768px) {
        h1 {
            font-size: 1.5rem;
        }
    }
    .stButton button {
        width: 100%;
        background-color: #FF4B4B;
        color: white;
        border: none;
        padding: 10px;
        font-size: 16px;
        border-radius: 5px;
    }
    img {
        border-radius: 8px;
        object-fit: cover;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state for caching
if 'last_search' not in st.session_state:
    st.session_state.last_search = ""
if 'last_results' not in st.session_state:
    st.session_state.last_results = []
if 'search_count' not in st.session_state:
    st.session_state.search_count = 0

# Search function with better error handling
@st.cache_data(ttl=3600, show_spinner=False)
def search_images_cached(query, search_id):
    """
    Cached search function to avoid repeated API calls
    """
    return search_images(query)

def search_images(query, max_results=24):
    """
    Search for images using DuckDuckGo with improved error handling
    """
    try:
        # Add random delay to avoid rate limiting
        time.sleep(random.uniform(1, 2))
        
        # Use DDGS with headers to avoid 403
        with DDGS(headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }, timeout=30) as ddgs:
            
            results = []
            for r in ddgs.images(
                keywords=query,
                region='wt-wt',
                safesearch='moderate',
                max_results=max_results
            ):
                results.append(r)
                if len(results) >= max_results:
                    break
            
            # Filter valid results
            valid_results = [r for r in results if r.get('image') and r['image'].startswith('http')]
            
            return valid_results, None
            
    except Exception as e:
        error_msg = str(e)
        if '403' in error_msg:
            return [], "DuckDuckGo blocked the request. Please wait 10-15 seconds and try again."
        elif 'Ratelimit' in error_msg:
            return [], "Rate limit reached. Please wait 10-15 seconds before searching again."
        else:
            return [], f"Search error: {error_msg}"

# Main app
st.title("🔍 Image Search Engine")

# Search input
search_query = st.text_input(
    "",
    placeholder="Search for any images...",
    label_visibility="collapsed",
    key="search_input"
)

# Search button
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    search_button = st.button("🔎 Search", use_container_width=True)

# Perform search
if search_button and search_query:
    if search_query != st.session_state.last_search:
        st.session_state.search_count += 1
        
        with st.spinner("Searching for images..."):
            # Use cached function with unique ID to force new search
            results, error = search_images_cached(search_query, st.session_state.search_count)
            
            if error:
                st.error(f"⚠️ {error}")
                st.info("**Quick fix**: Wait 10-15 seconds between searches to avoid rate limits.")
            elif results:
                st.session_state.last_search = search_query
                st.session_state.last_results = results
                st.success(f"✅ Found {len(results)} images")
            else:
                st.warning("No images found. Try a different search term.")
    else:
        results = st.session_state.last_results
        if results:
            st.success(f"✅ Found {len(results)} images (cached)")

# Display results
if st.session_state.last_results and search_query == st.session_state.last_search:
    results = st.session_state.last_results
    
    # Display images in a responsive grid
    cols_per_row = 3
    for idx in range(0, len(results), cols_per_row):
        cols = st.columns(cols_per_row)
        for col_idx, col in enumerate(cols):
            result_idx = idx + col_idx
            if result_idx < len(results):
                img = results[result_idx]
                with col:
                    try:
                        st.image(
                            img['image'],
                            use_container_width=True,
                            caption=img.get('title', '')[:60]
                        )
                        st.markdown(
                            f"[🔗 Source]({img.get('url', img['image'])}) | "
                            f"[⬇️ Download]({img['image']})",
                            unsafe_allow_html=True
                        )
                    except:
                        st.markdown(
                            f"[🖼️ View Image]({img['image']})",
                            unsafe_allow_html=True
                        )

# Instructions
with st.expander("ℹ️ Tips to avoid errors"):
    st.markdown("""
    **If you get a 403 or rate limit error:**
    1. Wait 10-15 seconds before searching again
    2. DuckDuckGo limits how many searches you can do quickly
    3. The app caches results, so searching the same thing twice won't trigger errors
    
    **How to use:**
    - Type anything and hit Search
    - Click Download to save images
    - Click Source to see where the image came from
    """)

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray;'>Powered by DuckDuckGo | Built with Streamlit</p>",
    unsafe_allow_html=True
)
