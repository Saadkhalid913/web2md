import html_parser as html2text
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re

def convert_relative_urls_to_absolute(html_content: str, base_url: str) -> str:
    """Convert all relative URLs in the HTML to absolute URLs."""
    soup = BeautifulSoup(html_content, 'html.parser')
    
    # Get the base domain for the URL
    parsed_base = urlparse(base_url)
    base_domain = f"{parsed_base.scheme}://{parsed_base.netloc}"
    
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
    
    # Convert to markdown
    converter = get_html2text_converter()
    # write the html_with_absolute_urls to a file
    with open("html_with_absolute_urls.html", "w") as file:
        file.write(html_with_absolute_urls)
    markdown_text = converter.handle(html_with_absolute_urls)
    
    # Clean up the markdown
    return clean_markdown(markdown_text) 