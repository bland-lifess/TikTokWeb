import streamlit as st
from duckduckgo_search import DDGS
import base64
from io import BytesIO
import requests

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
    </style>
""", unsafe_allow_html=True)

# AI-powered query enhancement
def enhance_query(query):
    """
    Intelligently enhance search queries for better image results
    """
    query_lower = query.lower()
    
    # Meme detection
    meme_keywords = {
        'thinking monkey': 'thinking monkey meme tiktok',
        'monkey': 'monkey meme',
        'cat': 'cat meme funny',
        'dog': 'dog meme funny',
        'pepe': 'pepe the frog meme',
        'wojak': 'wojak meme',
        'doge': 'doge meme',
        'distracted boyfriend': 'distracted boyfriend meme',
        'drake': 'drake meme template',
        'stonks': 'stonks meme',
        'galaxy brain': 'galaxy brain meme',
    }
    
    # Check for exact meme matches
    for key, enhanced in meme_keywords.items():
        if key in query_lower:
            return enhanced
    
    # Trend detection - add trending platform keywords
    trend_words = ['dance', 'trend', 'viral', 'challenge', 'reaction']
    if any(word in query_lower for word in trend_words):
        if 'tiktok' not in query_lower:
            query += ' tiktok viral'
    
    # Art/aesthetic queries
    art_words = ['aesthetic', 'wallpaper', 'art', 'drawing', 'painting']
    if any(word in query_lower for word in art_words):
        query += ' high quality hd'
    
    # Default: add quality keywords for better results
    if len(query.split()) <= 2:
        query += ' hd quality'
    
    return query

# Search function
def search_images(query, max_results=20):
    """
    Search for images using DuckDuckGo
    """
    try:
        enhanced_query = enhance_query(query)
        
        with DDGS() as ddgs:
            results = list(ddgs.images(
                keywords=enhanced_query,
                max_results=max_results,
                safesearch='moderate'
            ))
        
        return results, enhanced_query
    except Exception as e:
        st.error(f"Search error: {str(e)}")
        return [], query

# Function to create download link
def get_image_download_link(img_url, filename):
    """
    Generate a download link for images
    """
    try:
        response = requests.get(img_url, timeout=5)
        b64 = base64.b64encode(response.content).decode()
        return f'<a href="data:image/jpeg;base64,{b64}" download="{filename}">Download</a>'
    except:
        return f'<a href="{img_url}" target="_blank">Open</a>'

# Main app
st.title("🔍 Image Search Engine")

# Search input
search_query = st.text_input(
    "",
    placeholder="Search for images... (e.g., thinking monkey, aesthetic sunset)",
    label_visibility="collapsed"
)

# Search button
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    search_button = st.button("🔎 Search", use_container_width=True)

# Perform search
if search_button and search_query:
    with st.spinner("Searching for images..."):
        results, enhanced_query = search_images(search_query, max_results=24)
        
        if results:
            # Show enhanced query info
            if enhanced_query != search_query:
                st.info(f"💡 Searching for: **{enhanced_query}**")
            
            st.success(f"Found {len(results)} images")
            
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
                                st.image(
                                    img['image'],
                                    use_container_width=True,
                                    caption=img.get('title', '')[:50]
                                )
                                # Download button
                                st.markdown(
                                    f"[🔗 Open]({img['image']}) | [⬇️ Download]({img['image']})",
                                    unsafe_allow_html=True
                                )
                            except Exception as e:
                                st.error(f"Error loading image")
        else:
            st.warning("No images found. Try a different search term.")

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: gray;'>Powered by DuckDuckGo | "
    "Built with Streamlit</p>",
    unsafe_allow_html=True
)
