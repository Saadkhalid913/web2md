# HTML to Markdown Converter API

A FastAPI-based web service that converts HTML web pages to clean, readable Markdown format. The service provides both single-page and batch conversion endpoints, making it easy to transform web content into Markdown at scale.

## Features

- Convert single web pages to Markdown via API endpoint
- Batch convert multiple URLs in a single request
- Handles relative URLs by converting them to absolute URLs
- Configurable user agent for web requests
- Built on FastAPI for high performance and easy API documentation
- Uses the battle-tested html2text library for reliable HTML to Markdown conversion

## Installation & Setup

### Using Docker (Recommended)

1. Clone the repository with submodules:

   ```
   git clone --recurse-submodules https://github.com/Saadkhalid913/web2md.git
   ```

2. Navigate to the project directory:

   ```
   cd web2md
   ```

3. Build the Docker container:

   ```
   docker build -t html2md .
   ```

4. Run the container:
   ```
   docker run -p 8000:8000 html2md
   ```

The API will be available at `http://localhost:8000`

### Local Installation

1. Clone the repository with submodules:

   ```
   git clone --recurse-submodules https://github.com/Saadkhalid913/web2md.git
   ```

2. Navigate to the project directory:

   ```
   cd web2md
   ```

3. Create a virtual environment:

   ```
   python -m venv venv
   ```

4. Activate the virtual environment:

   - On Unix or MacOS:
     ```
     source venv/bin/activate
     ```
   - On Windows:
     ```
     venv\Scripts\activate
     ```

5. Install the main dependencies:

   ```
   pip install -r requirements.txt
   ```

6. Install the html_parser submodule:

   ```
   cd html_parser
   pip install -e .
   cd ..
   ```

7. Run the application:
   ```
   uvicorn app:app --host 0.0.0.0 --port 8000
   ```

## API Usage

### Single URL Conversion

Convert a single webpage to Markdown:

```
curl "http://localhost:8000/convert?url=https://saadkhalid.com"
```

Example Response:

```
# Saad Khalid

CS @ [McMasterU](<https://McMaster.ca>)


## Previously

Infrastructure Engineering @ [Shopify](<https://shopify.com>)

Backend dev @ [Aviato](<https://aviato.co>)

Core dev @ [PadawanDAO](<https://padawandao.com>)

North American finalist in Microsoft's [Imagine Cup](<https://imaginecup.microsoft.com/en-us/Team/550518d7-d2a6-4e64-96e5-a82bba7fe27c>)

Re-implemented the [U-NET paper](<https://arxiv.org/abs/1505.04597>)

Shipped an anonymized chat app at [Buildspace](<https://buildspace.so>) Nights and Weekends

Developed CNNs from first-principles. Work can be found [here](<https://saadk.notion.site/Convolutional-Neural-Network-From-Scratch-53ef425cc27a45f88c75eba1ff470aab>).


**Last Updated: 22/08/2024**


[Github](<https://github.com/saadkhalid913>)[Twitter](<https://twitter.com/saad89d>)[LinkedIn](<https://www.linkedin.com/in/saad-khalid1/>)[YouTube](<https://www.youtube.com/channel/UC4jTfAsz_ZvQUIFfkGamZXw/featured>)

[Projects](<https://saadkhalid.com/projects>)[Contact](<https://saadkhalid.com/contact>)[My Tech Stack](<https://saadkhalid.com/tech-stack>)

[More about me →](<https://saadkhalid.com/whoami>)

Saad Khalid 2023
```

### Batch URL Conversion

Convert multiple webpages to Markdown in a single request:

```
curl -X POST "http://localhost:8000/convert/batch" \
     -H "Content-Type: application/json" \
     -d '{
       "urls": [
         "https://saadkhalid.com",
         "https://example.com"
       ]
     }'
```

Example Response:

```
{
    "results": [
        {
            "url": "https://saadkhalid.com",
            "markdown": "# Saad Khalid\n\nSoftware Engineer based in Toronto...",
            "success": true,
            "error": null
        },
        {
            "url": "https://example.com",
            "markdown": "# Example Domain\n\nThis domain is for use in illustrative examples...",
            "success": true,
            "error": null
        }
    ]
}
```

Each result in the batch response includes:

- `url`: The original URL requested
- `markdown`: The converted markdown text (if successful)
- `success`: Boolean indicating if the conversion succeeded
- `error`: Error message if the conversion failed, null otherwise

## License

This project is licensed under the GNU GPL v3 License - see the LICENSE file for details.
