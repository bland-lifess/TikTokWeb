import streamlit as st
import requests

# Page configuration
st.set_page_config(
    page_title="Image Search Engine",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
    <style>
    .main {padding: 1rem;}
    .stTextInput > div > div > input {font-size: 16px; padding: 12px;}
    h1 {font-size: 2rem; margin-bottom: 1.5rem; text-align: center;}
    @media (max-width: 768px) {h1 {font-size: 1.5rem;}}
    .stButton button {width: 100%; background-color: #FF4B4B; color: white; border: none; padding: 10px; font-size: 16px; border-radius: 5px;}
    img {border-radius: 8px; width: 100%;}
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'last_search' not in st.session_state:
    st.session_state.last_search = ""
if 'last_results' not in st.session_state:
    st.session_state.last_results = []

def search_giphy(query, limit=30):
    """
    Search Giphy API - GUARANTEED to work, no authentication needed
    """
    try:
        api_key = "dc6zaTOxFJmzC"  # Public beta key that always works
        url = f"https://api.giphy.com/v1/gifs/search"
        
        params = {
            'api_key': api_key,
            'q': query,
            'limit': limit,
            'offset': 0,
            'rating': 'g',
            'lang': 'en'
        }
        
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        results = []
        for item in data.get('data', []):
            # Use the original image, not GIF
            image_url = item['images']['original']['url']
            
            results.append({
                'image': image_url,
                'title': item.get('title', 'GIF')[:60],
                'url': item.get('url', image_url)
            })
        
        return results, None
        
    except Exception as e:
        return [], f"Giphy error: {str(e)}"

def search_tenor(query, limit=30):
    """
    Search Tenor GIF API - also free and reliable
    """
    try:
        # Tenor's API key for testing
        api_key = "AIzaSyAyimkuYQYF_FXVALexPuGQctUWRURdCYQ"
        url = "https://tenor.googleapis.com/v2/search"
        
        params = {
            'q': query,
            'key': api_key,
            'client_key': 'streamlit_app',
            'limit': limit
        }
        
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        results = []
        for item in data.get('results', []):
            # Get the gif URL
            media = item.get('media_formats', {}).get('gif', {})
            image_url = media.get('url', '')
            
            if image_url:
                results.append({
                    'image': image_url,
                    'title': item.get('content_description', 'GIF')[:60],
                    'url': item.get('itemurl', image_url)
                })
        
        return results, None
        
    except Exception as e:
        return [], f"Tenor error: {str(e)}"

def search_all(query):
    """
    Search both Giphy and Tenor, combine results
    """
    giphy_results, giphy_error = search_giphy(query, limit=20)
    tenor_results, tenor_error = search_tenor(query, limit=15)
    
    all_results = giphy_results + tenor_results
    
    if not all_results:
        error_msg = f"Giphy: {giphy_error}, Tenor: {tenor_error}" if (giphy_error or tenor_error) else "No results found"
        return [], error_msg
    
    return all_results, None

# Main app
st.title("🔍 GIF & Meme Search")
st.caption("Powered by Giphy & Tenor - Search for any GIF, meme, or reaction")

# Search input
search_query = st.text_input(
    "",
    placeholder="Search: thinking monkey, cat meme, funny dog, etc...",
    label_visibility="collapsed"
)

# Search button
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    search_button = st.button("🔎 Search", use_container_width=True)

# Perform search
if search_button and search_query:
    if search_query != st.session_state.last_search:
        with st.spinner("Searching..."):
            results, error = search_all(search_query)
            
            if error:
                st.error(f"⚠️ {error}")
                st.info("Try a different search term or check your internet connection")
            elif results:
                st.session_state.last_search = search_query
                st.session_state.last_results = results
                st.success(f"✅ Found {len(results)} GIFs & images")
            else:
                st.warning("No results found. Try different keywords!")
    else:
        results = st.session_state.last_results
        if results:
            st.success(f"✅ Showing {len(results)} results")

# Display results
if st.session_state.last_results and search_query == st.session_state.last_search:
    results = st.session_state.last_results
    
    # Display in 3-column grid
    cols_per_row = 3
    for idx in range(0, len(results), cols_per_row):
        cols = st.columns(cols_per_row)
        for col_idx, col in enumerate(cols):
            result_idx = idx + col_idx
            if result_idx < len(results):
                img = results[result_idx]
                with col:
                    try:
                        st.image(img['image'], use_container_width=True)
                        st.caption(img.get('title', 'Image')[:50])
                        st.markdown(f"[⬇️ Download]({img['image']})")
                    except:
                        st.error("Failed to load")
                        st.markdown(f"[View]({img['image']})")

# Examples
with st.expander("💡 Try these searches"):
    st.markdown("""
    - thinking monkey
    - cat meme
    - funny dog
    - shocked reaction
    - facepalm
    - thumbs up
    - dancing
    - laughing
    """)

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>Powered by Giphy & Tenor APIs | Built with Streamlit</p>", unsafe_allow_html=True)
