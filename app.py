import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, quote
import re

# Page configuration
st.set_page_config(
    page_title="Web Proxy Browser",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
    <style>
    .main {padding: 0.5rem;}
    .stTextInput > div > div > input {font-size: 16px; padding: 12px;}
    h1 {font-size: 1.8rem; margin-bottom: 1rem; text-align: center;}
    .proxy-frame {
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 20px;
        background: white;
        min-height: 600px;
    }
    .url-bar {
        background: #f0f0f0;
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 15px;
    }
    @media (max-width: 768px) {
        h1 {font-size: 1.3rem;}
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'current_url' not in st.session_state:
    st.session_state.current_url = ""
if 'page_content' not in st.session_state:
    st.session_state.page_content = ""
if 'history' not in st.session_state:
    st.session_state.history = []

def fetch_page(url):
    """
    Fetch and parse a webpage
    """
    try:
        # Add https:// if not present
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        
        response = requests.get(url, headers=headers, timeout=15, allow_redirects=True)
        
        if response.status_code == 200:
            # Parse HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Remove scripts and styles for cleaner display
            for tag in soup(['script', 'style', 'iframe', 'noscript']):
                tag.decompose()
            
            # Get page title
            title = soup.find('title')
            title_text = title.string if title else "Webpage"
            
            # Get main content
            content = soup.find('body')
            
            if content:
                # Convert relative URLs to absolute
                for tag in content.find_all(['a', 'img']):
                    if tag.name == 'a' and tag.get('href'):
                        tag['href'] = urljoin(url, tag['href'])
                        tag['target'] = '_blank'
                    elif tag.name == 'img' and tag.get('src'):
                        tag['src'] = urljoin(url, tag['src'])
                
                html_content = str(content)
                return html_content, title_text, None
            
            return response.text, title_text, None
        else:
            return None, None, f"HTTP Error {response.status_code}"
            
    except requests.exceptions.Timeout:
        return None, None, "Request timed out - site took too long to respond"
    except requests.exceptions.ConnectionError:
        return None, None, "Connection error - couldn't reach the website"
    except Exception as e:
        return None, None, f"Error: {str(e)}"

def search_web(query):
    """
    Perform a web search and return results
    """
    try:
        # Use DuckDuckGo HTML search (lite version)
        search_url = f"https://lite.duckduckgo.com/lite/?q={quote(query)}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        response = requests.get(search_url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        results = []
        
        # Parse search results
        for result in soup.find_all('tr')[:15]:
            link = result.find('a')
            if link and link.get('href'):
                url = link['href']
                # Skip DuckDuckGo internal links
                if url.startswith('http') and 'duckduckgo.com' not in url:
                    title = link.get_text(strip=True)
                    snippet = result.get_text(strip=True)
                    results.append({
                        'title': title,
                        'url': url,
                        'snippet': snippet[:200]
                    })
        
        return results, None
        
    except Exception as e:
        return [], f"Search error: {str(e)}"

# Main app
st.title("🌐 Web Proxy Browser")
st.caption("Browse the web or search for anything")

# Input mode selection
tab1, tab2 = st.tabs(["🔗 Direct URL", "🔍 Search Web"])

with tab1:
    url_input = st.text_input(
        "Enter website URL:",
        placeholder="example.com or https://example.com",
        key="url_input"
    )
    
    col1, col2 = st.columns([3, 1])
    with col1:
        go_button = st.button("🚀 Go to Site", use_container_width=True, key="go_btn")
    with col2:
        if st.button("🔄 Refresh", use_container_width=True):
            if st.session_state.current_url:
                go_button = True
                url_input = st.session_state.current_url

with tab2:
    search_query = st.text_input(
        "Search the web:",
        placeholder="Search for anything...",
        key="search_input"
    )
    search_button = st.button("🔎 Search", use_container_width=True)

# Handle URL navigation
if go_button and url_input:
    with st.spinner(f"Loading {url_input}..."):
        content, title, error = fetch_page(url_input)
        
        if error:
            st.error(f"❌ {error}")
        elif content:
            st.session_state.current_url = url_input
            st.session_state.page_content = content
            if url_input not in st.session_state.history:
                st.session_state.history.append(url_input)
            st.success(f"✅ Loaded: {title}")
            st.rerun()

# Handle search
if search_button and search_query:
    with st.spinner("Searching..."):
        results, error = search_web(search_query)
        
        if error:
            st.error(f"❌ {error}")
        elif results:
            st.success(f"✅ Found {len(results)} results")
            
            for idx, result in enumerate(results, 1):
                with st.container():
                    st.markdown(f"**{idx}. {result['title']}**")
                    st.caption(result['snippet'])
                    col1, col2 = st.columns([1, 4])
                    with col1:
                        if st.button(f"Visit →", key=f"visit_{idx}"):
                            st.session_state.current_url = result['url']
                            with st.spinner("Loading..."):
                                content, title, error = fetch_page(result['url'])
                                if not error and content:
                                    st.session_state.page_content = content
                                    st.rerun()
                    with col2:
                        st.caption(f"🔗 {result['url'][:60]}...")
                    st.divider()
        else:
            st.warning("No results found. Try different keywords.")

# Display current page
if st.session_state.page_content:
    st.markdown("---")
    
    # URL bar
    st.markdown(f"**Current URL:** {st.session_state.current_url}")
    
    # Display content in frame
    st.markdown('<div class="proxy-frame">', unsafe_allow_html=True)
    st.markdown(st.session_state.page_content, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# History sidebar
if st.session_state.history:
    with st.expander("📜 Browsing History"):
        for url in reversed(st.session_state.history[-10:]):
            if st.button(url, key=f"hist_{url}"):
                st.session_state.current_url = url
                content, title, error = fetch_page(url)
                if not error and content:
                    st.session_state.page_content = content
                    st.rerun()

# Instructions
with st.expander("ℹ️ How to use"):
    st.markdown("""
    **Direct URL Mode:**
    - Enter any website (e.g., `wikipedia.org`, `reddit.com`)
    - Click "Go to Site" to load it
    
    **Search Mode:**
    - Type your search query
    - Click "Search" to find websites
    - Click "Visit →" on any result to load it
    
    **Features:**
    - Browse any public website
    - Search the web via DuckDuckGo
    - View browsing history
    - Mobile-friendly design
    
    **Note:** Some sites may block proxy access or require JavaScript
    """)

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>Web Proxy | Built with Streamlit</p>", unsafe_allow_html=True)
