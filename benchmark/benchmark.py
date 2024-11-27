import argparse
import asyncio
import aiohttp
import time
import statistics
from pathlib import Path
from typing import List, Tuple
import sys
import json

def load_urls(file_path: str) -> List[str]:
    with open(file_path, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def is_valid_markdown(text: str) -> bool:
    # Basic markdown validation
    # Check if the response contains any markdown-specific characters
    markdown_indicators = ['#', '-', '*', '`', '[', ']', '(', ')', '_']
    return any(indicator in text for indicator in markdown_indicators)

async def make_request(session: aiohttp.ClientSession, url: str, server_url: str) -> Tuple[float, bool, str]:
    start_time = time.time()
    try:
        encoded_url = url
        async with session.get(f"{server_url}/convert", params={'url': encoded_url}) as response:
            response_text = await response.text()
            duration = time.time() - start_time
            is_valid = is_valid_markdown(response_text)
            return duration, is_valid, ''
    except Exception as e:
        duration = time.time() - start_time
        return duration, False, str(e)

async def make_batch_request(session: aiohttp.ClientSession, urls: List[str], server_url: str) -> List[Tuple[float, bool, str]]:
    start_time = time.time()
    try:
        async with session.post(
            f"{server_url}/convert/batch",
            json={"urls": urls},
            headers={"Content-Type": "application/json"}
        ) as response:
            response_data = await response.json()
            duration = time.time() - start_time
            
            # Process each result from the results array
            return [
                (
                    duration / len(urls),  # Distribute total time across URLs
                    result["success"] and is_valid_markdown(result["markdown"]),
                    result.get("error", "") or ""
                )
                for result in response_data["results"]
            ]
    except Exception as e:
        duration = time.time() - start_time
        return [(duration / len(urls), False, str(e)) for _ in urls]

async def run_batch(urls: List[str], requests_per_second: int, server_url: str) -> List[float]:
    batch_size = min(requests_per_second, len(urls))
    delay = 1.0 / requests_per_second if requests_per_second > 0 else 0
    
    async with aiohttp.ClientSession() as session:
        durations = []
        valid_count = 0
        total_requests = 0
        
        print(f"\nTesting at {requests_per_second} requests/second...")
        start_time = time.time()
        
        while time.time() - start_time < 10:  # Run for 10 seconds
            batch_start = time.time()
            
            # Select URLs for this batch
            batch_urls = [
                urls[i % len(urls)]
                for i in range(total_requests, total_requests + batch_size)
            ]
            
            # Make batch request
            results = await make_batch_request(session, batch_urls, server_url)
            
            # Process results
            for duration, is_valid, error in results:
                durations.append(duration)
                if is_valid:
                    valid_count += 1
                elif error:
                    print(f"Error: {error}")
            
            total_requests += batch_size
            
            # Calculate sleep time to maintain desired rate
            elapsed = time.time() - batch_start
            sleep_time = max(0, delay * batch_size - elapsed)
            if sleep_time > 0:
                await asyncio.sleep(sleep_time)
        
        avg_duration = statistics.mean(durations) if durations else 0
        print(f"Average response time: {avg_duration*1000:.2f}ms")
        print(f"Valid responses: {valid_count}/{total_requests} ({valid_count/total_requests*100:.1f}%)")
        
        return durations

async def main():
    parser = argparse.ArgumentParser(description='Benchmark webpage-to-markdown converter')
    parser.add_argument('--port', type=int, default=8000, help='Server port (default: 8000)')
    args = parser.parse_args()
    
    urls_file = Path(__file__).parent / 'urls.dat'
    if not urls_file.exists():
        print(f"Error: {urls_file} not found")
        sys.exit(1)
    
    urls = load_urls(str(urls_file))
    if not urls:
        print("Error: No URLs found in urls.dat")
        sys.exit(1)
    
    server_url = f"http://localhost:{args.port}"
    requests_per_second = 10
    
    while True:
        durations = await run_batch(urls, requests_per_second, server_url)
        avg_duration = statistics.mean(durations)
        
        if avg_duration > 0.5:  # Stop if average time exceeds 100ms
            print(f"\nBenchmark completed: Average response time exceeded 100ms at {requests_per_second} requests/second")
            break
            
        if requests_per_second < 100:
            requests_per_second = 100
        else:
            requests_per_second += 1000

if __name__ == "__main__":
    asyncio.run(main()) 