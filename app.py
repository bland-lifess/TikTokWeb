import streamlit as st
import requests
from bs4 import BeautifulSoup
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
    img {border-radius: 8px;}
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'last_search' not in st.session_state:
    st.session_state.last_search = ""
if 'last_results' not in st.session_state:
    st.session_state.last_results = []

def search_google_images(query, max_results=30):
    """
    Search Google Images - better quality results than Bing
    """
    try:
        # Google Images search URL
        search_url = f"https://www.google.com/search?q={requests.utils.quote(query)}&tbm=isch&hl=en"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'none',
            'Cache-Control': 'max-age=0'
        }
        
        response = requests.get(search_url, headers=headers, timeout=15)
        
        if response.status_code != 200:
            return [], f"Search failed with status {response.status_code}"
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        results = []
        
        # Find all script tags that contain image data
        scripts = soup.find_all('script')
        
        for script in scripts:
            if script.string and 'AF_initDataCallback' in script.string:
                # Extract JSON data from Google's JavaScript
                try:
                    # Find image URLs in the script
                    text = script.string
                    
                    # Look for image URLs (https URLs ending in common image formats)
                    import re
                    urls = re.findall(r'https://[^"]+?\.(?:jpg|jpeg|png|gif|webp)', text)
                    
                    # Filter out small icons and thumbnails
                    for url in urls:
                        if len(results) >= max_results:
                            break
                        
                        # Skip tiny thumbnails and icons
                        if any(skip in url.lower() for skip in ['gstatic', 'favicon', 'logo', 'icon', '1x1']):
                            continue
                        
                        # Skip encrypted/encoded Google URLs
                        if 'encrypted' in url or 'ggpht' in url:
                            continue
                            
                        if url not in [r['image'] for r in results]:
                            results.append({
                                'image': url,
                                'title': 'Image',
                                'url': url
                            })
                except:
                    continue
        
        return results[:max_results], None
        
    except Exception as e:
        return [], f"Error: {str(e)}"

def verify_image_url(url):
    """
    Quick check if image URL is accessible
    """
    try:
        response = requests.head(url, timeout=3, allow_redirects=True)
        return response.status_code == 200
    except:
        return False

# Main app
st.title("🔍 Image Search Engine")

# Search input
search_query = st.text_input(
    "",
    placeholder="Search for any images... (try: 'thinking monkey tiktok' or 'cat meme')",
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
            results, error = search_google_images(search_query, max_results=30)
            
            if error:
                st.error(f"⚠️ {error}")
                st.info("💡 Tip: If search fails, try being more specific (e.g., add 'meme' or 'tiktok' to your search)")
            elif results:
                st.session_state.last_search = search_query
                st.session_state.last_results = results
                st.success(f"✅ Found {len(results)} images")
            else:
                st.warning("No images found. Try adding keywords like 'meme', 'tiktok', 'viral', or 'funny'")
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
                        # Display the actual image
                        st.image(
                            img['image'],
                            use_container_width=True,
                            output_format='auto'
                        )
                        # Add download link below image
                        st.markdown(
                            f"<a href='{img['image']}' target='_blank' style='text-decoration:none;'>⬇️ Download</a>",
                            unsafe_allow_html=True
                        )
                    except Exception as e:
                        # If image fails to load, show clickable link
                        st.markdown(
                            f"<a href='{img['image']}' target='_blank'>🖼️ View Image (click here)</a>",
                            unsafe_allow_html=True
                        )

# Tips section
with st.expander("💡 Search Tips"):
    st.markdown("""
    **To get better, more relevant results:**
    - For memes: Add "meme" to your search (e.g., "thinking monkey meme")
    - For TikTok content: Add "tiktok" (e.g., "thinking monkey tiktok")
    - For viral content: Add "viral" or "trending"
    - Be specific: "cute cat meme" works better than just "cat"
    
    **Examples:**
    - "thinking monkey tiktok meme"
    - "drip goku meme"
    - "sigma male gif"
    - "funny dog tiktok"
    """)

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>Powered by Google Images | Built with Streamlit</p>", unsafe_allow_html=True)
