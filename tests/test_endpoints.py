import pytest
from pathlib import Path
from fastapi.testclient import TestClient
from app import app
import pytest_asyncio
import aiohttp
from aiohttp import web
import asyncio

# Test data directory for sample HTML files
TEST_DATA_DIR = Path(__file__).parent / "test_data"
TEST_DATA_DIR.mkdir(exist_ok=True)

# Create mock HTML content
MOCK_HTML = {
    "simple.html": """
        <html>
            <head><title>Simple Test Page</title></head>
            <body>
                <h1>Welcome to Test Page</h1>
                <p>This is a test paragraph.</p>
                <a href="https://example.com">Test Link</a>
            </body>
        </html>
    """,
    "complex.html": """
        <html>
            <head><title>Complex Test Page</title></head>
            <body>
                <h1>Complex Page</h1>
                <h2>Subsection</h2>
                <ul>
                    <li>Item 1</li>
                    <li>Item 2</li>
                </ul>
                <a href="https://test.com">Link 1</a>
                <a href="https://example.org">Link 2</a>
            </body>
        </html>
    """,
    "invalid.html": "Invalid HTML content"
}

class MockServer:
    def __init__(self):
        self.app = web.Application()
        self.app.router.add_get('/{filename}', self.handle_request)
        self.runner = None
        self.site = None
        self.url = None

    async def handle_request(self, request):
        filename = request.match_info['filename']
        if filename in MOCK_HTML:
            return web.Response(text=MOCK_HTML[filename], content_type='text/html')
        return web.Response(status=404)

    async def start(self):
        self.runner = web.AppRunner(self.app)
        await self.runner.setup()
        self.site = web.TCPSite(self.runner, 'localhost', 0)
        await self.site.start()
        port = self.site._server.sockets[0].getsockname()[1]
        self.url = f"http://localhost:{port}"
        return self.url

    async def stop(self):
        if self.runner:
            await self.runner.cleanup()

@pytest.fixture
async def mock_server():
    server = MockServer()
    url = await server.start()
    yield url
    await server.stop()

@pytest.fixture
def client():
    return TestClient(app)

@pytest.mark.asyncio
async def test_convert_single_url(client, mock_server):
    url = f"{mock_server}/simple.html"
    response = client.get(f"/convert?url={url}")
    
    assert response.status_code == 200
    assert isinstance(response.text, str)
    assert len(response.text) > 0
    # Basic markdown validation
    assert "# Welcome to Test Page" in response.text
    assert "[Test Link]" in response.text

@pytest.mark.asyncio
async def test_batch_convert(client, mock_server):
    urls = [
        f"{mock_server}/simple.html",
        f"{mock_server}/complex.html",
    ]
    
    response = client.post(
        "/convert/batch",
        json={"urls": urls}
    )
    
    assert response.status_code == 200
    response_data = response.json()
    results = response_data["results"]
    assert len(results) == len(urls)
    
    for result in results:
        assert isinstance(result["markdown"], str)
        assert len(result["markdown"]) > 0
        assert result["error"] is None

@pytest.mark.asyncio
async def test_convert_with_invalid_url(client):
    url = "not-a-valid-url"
    response = client.get(f"/convert?url={url}")
    
    assert response.status_code == 400
    assert "detail" in response.json()

@pytest.mark.asyncio
async def test_batch_convert_with_mixed_urls(client, mock_server):
    urls = [
        f"{mock_server}/simple.html",
        "not-a-valid-url",
        f"{mock_server}/complex.html"
    ]
    
    response = client.post(
        "/convert/batch",
        json={"urls": urls}
    )
    
    assert response.status_code == 200
    response_data = response.json()
    results = response_data["results"]
    assert len(results) == len(urls)
    
    # First URL should succeed
    assert results[0]["success"] is True
    assert len(results[0]["markdown"]) > 0
    
    # Invalid URL should fail
    assert results[1]["success"] is False
    assert "error" in results[1]
    
    # Last URL should succeed
    assert results[2]["success"] is True
    assert len(results[2]["markdown"]) > 0

@pytest.mark.asyncio
async def test_convert_with_custom_user_agent(client, mock_server):
    url = f"{mock_server}/simple.html"
    headers = {"User-Agent": "Custom-Test-Agent/1.0"}
    
    response = client.get(
        f"/convert?url={url}",
        headers=headers
    )
    
    assert response.status_code == 200
    assert isinstance(response.text, str)
    assert len(response.text) > 0

@pytest.mark.asyncio
async def test_large_batch_convert(client, mock_server):
    urls = [f"{mock_server}/simple.html"] * 5 + [f"{mock_server}/complex.html"] * 5
    
    response = client.post(
        "/convert/batch",
        json={"urls": urls}
    )
    
    assert response.status_code == 200
    response_data = response.json()
    results = response_data["results"]
    assert len(results) == len(urls)
    
    for result in results:
        assert "markdown" in result
        assert len(result["markdown"]) > 0
        assert result["success"] is True
        assert result["error"] is None