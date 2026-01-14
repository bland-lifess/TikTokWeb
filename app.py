import streamlit as st
from duckduckgo_search import DDGS
import base64
from io import BytesIO
import requests
import time

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
    .image-grid {
        display: grid;
        grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
        gap: 15px;
        margin-top: 20px;
    }
    @media (max-width: 768px) {
        .image-grid {
            grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
            gap: 10px;
        }
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

# Search function with retry logic
def search_images(query, max_results=30):
    """
    Search for images using DuckDuckGo with retry logic and error handling
    """
    max_retries = 3
    retry_delay = 2
    
    for attempt in range(max_retries):
        try:
            # Create a new DDGS instance for each search
            ddgs = DDGS(timeout=20)
            
            results = list(ddgs.images(
                keywords=query,
                max_results=max_results,
                safesearch='moderate',
                region='wt-wt',
                type_image=None
            ))
            
            # Filter out broken image URLs
            valid_results = []
            for result in results:
                if result.get('image') and result['image'].startswith('http'):
                    valid_results.append(result)
            
            return valid_results, None
            
        except Exception as e:
            error_msg = str(e)
            if attempt < max_retries - 1:
                if 'Ratelimit' in error_msg:
                    time.sleep(retry_delay * (attempt + 1))
                    continue
                else:
                    time.sleep(1)
                    continue
            else:
                return [], f"Search failed after {max_retries} attempts: {error_msg}"
    
    return [], "Search failed: Unknown error"

# Function to verify image URL
def is_valid_image_url(url):
    """
    Check if URL is accessible and returns an image
    """
    try:
        response = requests.head(url, timeout=3, allow_redirects=True)
        content_type = response.headers.get('content-type', '')
        return response.status_code == 200 and 'image' in content_type
    except:
        return True  # Assume valid if can't verify, let browser handle it

# Main app
st.title("🔍 Image Search Engine")

# Search input
search_query = st.text_input(
    "",
    placeholder="Search for any images...",
    label_visibility="collapsed"
)

# Search button
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    search_button = st.button("🔎 Search", use_container_width=True)

# Perform search
if search_button and search_query:
    # Check if this is a new search or same as last
    if search_query != st.session_state.last_search:
        with st.spinner("Searching for images..."):
            results, error = search_images(search_query, max_results=30)
            
            if error:
                st.error(f"⚠️ {error}")
                st.info("💡 Try again in a few seconds. DuckDuckGo may be rate limiting requests.")
            elif results:
                # Cache results
                st.session_state.last_search = search_query
                st.session_state.last_results = results
                
                st.success(f"Found {len(results)} images")
            else:
                st.warning("No images found. Try a different search term.")
    else:
        # Use cached results
        results = st.session_state.last_results
        st.success(f"Found {len(results)} images")

# Display cached results
if st.session_state.last_results and (search_query == st.session_state.last_search or search_button):
    results = st.session_state.last_results
    
    # Display images in a grid
    cols_per_row = 3
    for idx in range(0, len(results), cols_per_row):
        cols = st.columns(cols_per_row)
        for col_idx, col in enumerate(cols):
            result_idx = idx + col_idx
            if result_idx < len(results):
                img = results[result_idx]
                with col:
                    try:
                        # Display image with error handling
                        st.image(
                            img['image'],
                            use_container_width=True,
                            caption=img.get('title', '')[:60]
                        )
                        # Links
                        st.markdown(
                            f"[🔗 Source]({img.get('url', img['image'])}) | "
                            f"[⬇️ Download]({img['image']})",
                            unsafe_allow_html=True
                        )
                    except Exception as e:
                        # Fallback: show as a link if image fails to load
                        st.markdown(
                            f"**{img.get('title', 'Image')[:50]}**  \n"
                            f"[🖼️ View Image]({img['image']})",
                            unsafe_allow_html=True
                        )

# Instructions
with st.expander("ℹ️ How to use"):
    st.markdown("""
    - **Search freely** - Just type what you're looking for (e.g., "sunset", "cute cats", "vintage cars")
    - **Download images** - Click the Download link under any image
    - **View source** - Click Source to see the original webpage
    - **Rate limiting** - If you get an error, wait 5-10 seconds and try again
    """)

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray;'>Powered by DuckDuckGo | "
    "Built with Streamlit</p>",
    unsafe_allow_html=True
)
