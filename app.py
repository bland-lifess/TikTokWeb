import streamlit as st
import requests
from bs4 import BeautifulSoup
import json
import re

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
    img {border-radius: 8px; object-fit: cover;}
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'last_search' not in st.session_state:
    st.session_state.last_search = ""
if 'last_results' not in st.session_state:
    st.session_state.last_results = []

def search_images_alternative(query, max_results=24):
    """
    Alternative image search using direct web scraping
    """
    try:
        # Use Bing Image Search (more reliable than DuckDuckGo)
        search_url = f"https://www.bing.com/images/search?q={requests.utils.quote(query)}&first=1"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Referer': 'https://www.bing.com/',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        
        response = requests.get(search_url, headers=headers, timeout=10)
        
        if response.status_code != 200:
            return [], f"Search failed with status code: {response.status_code}"
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract image data from Bing's page
        results = []
        
        # Method 1: Find image containers
        image_containers = soup.find_all('a', class_='iusc')
        
        for container in image_containers[:max_results]:
            try:
                m = container.get('m')
                if m:
                    metadata = json.loads(m)
                    image_url = metadata.get('murl') or metadata.get('turl')
                    title = metadata.get('t', 'Image')
                    source_url = metadata.get('purl', image_url)
                    
                    if image_url:
                        results.append({
                            'image': image_url,
                            'title': title,
                            'url': source_url
                        })
            except:
                continue
        
        # Method 2: Fallback - find img tags
        if len(results) < 5:
            img_tags = soup.find_all('img', src=True)
            for img in img_tags[:max_results]:
                src = img.get('src')
                if src and src.startswith('http') and 'data:' not in src:
                    results.append({
                        'image': src,
                        'title': img.get('alt', 'Image'),
                        'url': src
                    })
        
        # Remove duplicates
        seen = set()
        unique_results = []
        for r in results:
            if r['image'] not in seen:
                seen.add(r['image'])
                unique_results.append(r)
        
        return unique_results[:max_results], None
        
    except Exception as e:
        return [], f"Error: {str(e)}"

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
    if search_query != st.session_state.last_search:
        with st.spinner("Searching for images..."):
            results, error = search_images_alternative(search_query, max_results=30)
            
            if error:
                st.error(f"⚠️ {error}")
            elif results:
                st.session_state.last_search = search_query
                st.session_state.last_results = results
                st.success(f"✅ Found {len(results)} images")
            else:
                st.warning("No images found. Try a different search term.")
    else:
        results = st.session_state.last_results
        if results:
            st.success(f"✅ Showing {len(results)} images")

# Display results
if st.session_state.last_results and search_query == st.session_state.last_search:
    results = st.session_state.last_results
    
    # Display images in grid
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
                        st.markdown(f"[🖼️ View]({img['image']})")

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>Powered by Bing Images | Built with Streamlit</p>", unsafe_allow_html=True)
