import html2text
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import re
from .user_agents import DEFAULT_USER_AGENT, BROWSER_HEADERS
import aiohttp
import asyncio
from typing import List, Dict, Union, Any, TypeVar, Callable, Awaitable, Tuple
import random
import time
from asyncio import Semaphore
import requests


T = TypeVar("T")

# Global rate limiter
MAX_CONCURRENT_REQUESTS = 100
rate_limiter = Semaphore(MAX_CONCURRENT_REQUESTS)

def get_browser_headers(user_agent: str = DEFAULT_USER_AGENT) -> Dict[str, str]:
    """Get a complete set of browser headers to mimic a real browser."""
    headers = BROWSER_HEADERS.copy()
    headers["User-Agent"] = user_agent
    
    languages = ["en-US,en;q=0.9", "en-GB,en;q=0.8", "en;q=0.7"]
    random.shuffle(languages)
    headers["Accept-Language"] = ",".join(languages)
    
    return headers

async def fetch_with_rate_limit(url: str, headers: Dict[str, str], session: aiohttp.ClientSession) -> str:
    """Fetch URL content with rate limiting."""
    async with rate_limiter:
        async with session.get(
            url,
            headers=headers,
            timeout=aiohttp.ClientTimeout(total=10)
        ) as response:
            response.raise_for_status()
            return await response.text()



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
    
    # Convert to markdown
    converter = get_html2text_converter()
    # write the html_with_absolute_urls to a file
    with open("html_with_absolute_urls.html", "w") as file:
        file.write(html_with_absolute_urls)
    markdown_text = converter.handle(html_with_absolute_urls)
    
    # Clean up the markdown
    return clean_markdown(markdown_text) 

def async_convert_html_to_markdown(html_content: str, base_url: str) -> str:
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


async def async_convert_url_to_markdown(url: str, user_agent: str = DEFAULT_USER_AGENT) -> str | None:
    """Async version of URL to markdown conversion with browser-like behavior."""
    headers = get_browser_headers(user_agent)
    
    async with aiohttp.ClientSession() as session:
        try:
            # Get cookies first
            await fetch_with_rate_limit(url, headers, session)
            # Main request
            html_content = await fetch_with_rate_limit(url, headers, session)
            return async_convert_html_to_markdown(html_content, url)
        except Exception as e:
            print(f"Error converting {url}: {str(e)}")
            return None

async def time_async_function(func: Callable[..., Awaitable[T | None]], *args: Any, **kwargs: Any) -> Tuple[T | None, float]:
    """
    Measure the execution time of an async function.

    Parameters:
        func (coroutine): The asynchronous function to be timed.
        *args: Positional arguments to pass to the function.
        **kwargs: Keyword arguments to pass to the function.

    Returns:
        tuple: (result, elapsed_time) where
            - result: The return value of the async function.
            - elapsed_time: Execution time in seconds.
    """
    start_time = time.monotonic()
    try:
        result = await func(*args, **kwargs)
    except Exception as e:
        print("Error in async function", e)
        result = None
    end_time = time.monotonic()
    elapsed_time = end_time - start_time
    return result, elapsed_time

async def async_convert_urls_to_markdown(
    urls: List[str],
    user_agent: str = DEFAULT_USER_AGENT,
    max_concurrent: int = MAX_CONCURRENT_REQUESTS
) -> List[Tuple[str | None, float]]:
    """Convert multiple URLs to markdown concurrently with rate limiting."""
    # Update rate limiter based on parameter
    global rate_limiter
    rate_limiter = Semaphore(max_concurrent)

    session = requests.Session()
    # Create tasks for all URLs
    tasks = [
        time_async_function(async_convert_url_to_markdown, url, user_agent)
        for url in urls
    ]

    
    # Run all tasks concurrently
    return await asyncio.gather(*tasks)

