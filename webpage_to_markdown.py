from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse
import requests
from urllib.parse import unquote
from markdown_converter import convert_html_to_markdown

app = FastAPI()

@app.get("/convert", response_class=PlainTextResponse)
async def convert_webpage(url: str):
    try:
        # Decode URL if it's URL-encoded
        decoded_url = unquote(url)
        
        # Fetch the webpage
        response = requests.get(decoded_url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        response.raise_for_status()
        
        # Convert HTML to markdown using the separate module
        cleaned_markdown = convert_html_to_markdown(response.text, decoded_url)
        
        return cleaned_markdown
        
    except requests.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Error fetching URL: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Server error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 