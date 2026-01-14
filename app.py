import streamlit as st
import requests
import re
import json

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

def search_serpapi_images(query, max_results=30):
    """
    Use SerpApi free tier to search Google Images
    Free tier: 100 searches/month
    """
    try:
        # SerpApi endpoint (you'll need to get a free API key from serpapi.com)
        api_key = st.secrets.get("SERPAPI_KEY", "")
        
        if not api_key:
            # Try without API key using direct scraping
            return search_imgur(query, max_results)
        
        url = "https://serpapi.com/search"
        params = {
            "q": query,
            "tbm": "isch",  # Image search
            "api_key": api_key,
            "num": max_results
        }
        
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        results = []
        for img in data.get('images_results', [])[:max_results]:
            results.append({
                'image': img.get('original'),
                'thumbnail': img.get('thumbnail'),
                'title': img.get('title', 'Image'),
                'url': img.get('source', img.get('original'))
            })
        
        return results, None
        
    except Exception as e:
        # Fallback to Imgur
        return search_imgur(query, max_results)

def search_imgur(query, max_results=30):
    """
    Search Imgur - tons of memes, no API key needed
    """
    try:
        # Imgur gallery search
        search_url = f"https://imgur.com/search?q={requests.utils.quote(query)}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        }
        
        response = requests.get(search_url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            # Extract image data from page
            results = []
            
            # Find imgur image IDs in the HTML
            image_ids = re.findall(r'"hash":"([a-zA-Z0-9]+)"', response.text)
            titles = re.findall(r'"title":"([^"]*)"', response.text)
            
            for idx, img_id in enumerate(image_ids[:max_results]):
                # Construct direct image URL
                img_url = f"https://i.imgur.com/{img_id}.jpg"
                title = titles[idx] if idx < len(titles) else "Image"
                
                results.append({
                    'image': img_url,
                    'thumbnail': img_url,
                    'title': title,
                    'url': f"https://imgur.com/{img_id}"
                })
            
            if results:
                return results, None
        
        # If Imgur fails, try Giphy for GIFs/memes
        return search_giphy(query, max_results)
        
    except Exception as e:
        return search_giphy(query, max_results)

def search_giphy(query, max_results=30):
    """
    Search Giphy - great for memes and reactions
    Free API key: dc6zaTOxFJmzC (public beta key)
    """
    try:
        url = "https://api.giphy.com/v1/gifs/search"
        params = {
            'api_key': 'dc6zaTOxFJmzC',  # Giphy's public beta key
            'q': query,
            'limit': max_results,
            'rating': 'pg-13'
        }
        
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        results = []
        for item in data.get('data', []):
            results.append({
                'image': item['images']['fixed_height']['url'],
                'thumbnail': item['images']['fixed_height_small']['url'],
                'title': item.get('title', 'GIF'),
                'url': item.get('url', item['images']['fixed_height']['url'])
            })
        
        return results, None
        
    except Exception as e:
        return [], f"All search methods failed: {str(e)}"

# Main app
st.title("🔍 Meme & Image Search")
st.caption("Search Imgur, Giphy & more for memes, GIFs, and viral content")

# Search input
search_query = st.text_input(
    "",
    placeholder="Search for memes, GIFs, viral content... (e.g., thinking monkey, cat meme)",
    label_visibility="collapsed"
)

# Search button
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    search_button = st.button("🔎 Search", use_container_width=True)

# Perform search
if search_button and search_query:
    if search_query != st.session_state.last_search:
        with st.spinner("Searching for images..."):
            results, error = search_serpapi_images(search_query, max_results=30)
            
            if error:
                st.error(f"⚠️ {error}")
            elif results:
                st.session_state.last_search = search_query
                st.session_state.last_results = results
                st.success(f"✅ Found {len(results)} images")
            else:
                st.warning("No images found. Try different keywords!")
    else:
        results = st.session_state.last_results
        if results:
            st.info(f"Showing {len(results)} cached results")

# Display results
if st.session_state.last_results and search_query == st.session_state.last_search:
    results = st.session_state.last_results
    
    # Display images in grid - 3 columns
    cols_per_row = 3
    for idx in range(0, len(results), cols_per_row):
        cols = st.columns(cols_per_row)
        for col_idx, col in enumerate(cols):
            result_idx = idx + col_idx
            if result_idx < len(results):
                img = results[result_idx]
                with col:
                    # Display image
                    st.image(img['image'], use_container_width=True, caption=img.get('title', '')[:50])
                    # Download link
                    st.markdown(f"[⬇️ Download]({img['image']}) | [🔗 Source]({img.get('url', img['image'])})")

# Setup instructions
with st.expander("🔧 Optional: Add SerpApi for Google Images (100 free/month)"):
    st.markdown("""
    **To search Google Images:**
    1. Go to [serpapi.com](https://serpapi.com) and sign up (free)
    2. Get your API key from the dashboard
    3. In Streamlit Cloud, go to your app settings → Secrets
    4. Add: `SERPAPI_KEY = "your_key_here"`
    5. Restart the app
    
    **Without SerpApi:** The app searches Imgur and Giphy (still great for memes!)
    """)

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>Searches Imgur, Giphy & more | Built with Streamlit</p>", unsafe_allow_html=True)
