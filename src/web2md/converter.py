import html2text
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re
from .user_agents import DEFAULT_USER_AGENT, BROWSER_HEADERS
import requests
import random
from typing import Dict

def get_browser_headers(user_agent: str = DEFAULT_USER_AGENT) -> Dict[str, str]:
    """Get a complete set of browser headers to mimic a real browser."""
    headers = BROWSER_HEADERS.copy()
    headers["User-Agent"] = user_agent
    
    languages = ["en-US,en;q=0.9", "en-GB,en;q=0.8", "en;q=0.7"]
    random.shuffle(languages)
    headers["Accept-Language"] = ",".join(languages)
    
    return headers

def convert_relative_urls_to_absolute(html_content: str, base_url: str) -> str:
    """Convert all relative URLs in the HTML to absolute URLs."""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Get the base domain for the URL
    parsed_base = urlparse(base_url)
    
    # Convert relative URLs in various attributes
    for tag in soup.find_all(['a', 'img', 'link', 'script']):
        # Handle href attributes
        if tag.has_attr('href'):
            href = tag['href']
            if href and not href.startswith(('http://', 'https://', 'mailto:', 'tel:', '#')):
                tag['href'] = urljoin(base_url, href)
                
        # Handle src attributes
        if tag.has_attr('src'):
            src = tag['src']
            if src and not src.startswith(('http://', 'https://', 'data:', '//')):
                tag['src'] = urljoin(base_url, src)
    
    return str(soup)

def clean_markdown(markdown_text: str) -> str:
    # Only remove excessive blank lines (more than 2 consecutive blank lines)
    markdown_text = re.sub(r'\n\s*\n\s*\n\s*\n+', '\n\n\n', markdown_text)
    
    # Remove any remaining HTML comments
    markdown_text = re.sub(r'<!--.*?-->', '', markdown_text, flags=re.DOTALL)

    return markdown_text.strip()

def get_html2text_converter() -> html2text.HTML2Text:
    """Configure and return an HTML2Text converter instance."""
    converter = html2text.HTML2Text()
    converter.ignore_links = False
    converter.ignore_images = False
    converter.ignore_tables = False
    converter.body_width = 0  # Don't wrap text
    converter.ignore_emphasis = False
    converter.single_line_break = False
    converter.wrap_links = False
    converter.unicode_snob = True
    converter.pad_tables = True
    converter.inline_links = True
    converter.protect_links = True
    converter.use_automatic_links = True
    converter.mark_code = True
    return converter

def convert_html_to_markdown(html_content: str, base_url: str) -> str:
    """Convert HTML content to markdown with proper URL handling."""
    # Convert relative URLs to absolute
    html_with_absolute_urls = convert_relative_urls_to_absolute(html_content, base_url)
    converter = get_html2text_converter()
    markdown_text = converter.handle(html_with_absolute_urls)
    return clean_markdown(markdown_text) 


def convert_url_to_markdown(url: str, user_agent: str = DEFAULT_USER_AGENT, session: requests.Session | None = None) -> str:
    """
    Convert a URL to markdown with browser-like behavior.
    """
    headers = get_browser_headers(user_agent)
    if session is None:
        session = requests.Session()
    
    # First request to get cookies
    session.get(url, headers=headers)
    
    # Main request
    response = session.get(
        url,
        headers=headers,
        timeout=10,
        allow_redirects=True
    )
    response.raise_for_status()
    
    html_content = response.text
    return convert_html_to_markdown(html_content, url)


def convert_urls_to_markdown(urls: list[str], user_agent: str = DEFAULT_USER_AGENT) -> list[str]:
    return [convert_url_to_markdown(url, user_agent) for url in urls]
