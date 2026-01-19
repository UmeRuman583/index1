"""
Google Instant Indexer - Multi-Method Indexing System
Supports: PDF Links, HTML Links, Forum Links, Web 2.0, Tier 1/2/3 Backlinks
"""

import requests
import json
import time
from datetime import datetime
from typing import List, Dict
import concurrent.futures
from urllib.parse import urlparse, quote
import xml.etree.ElementTree as ET
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class GoogleInstantIndexer:
    def __init__(self, service_account_file: str = None):
        """
        Initialize the indexer with multiple indexing methods
        
        Args:
            service_account_file: Path to Google service account JSON file
        """
        self.service_account_file = service_account_file
        self.indexing_service = None
        self.results = []
        
        # Initialize Google Indexing API if credentials provided
        if service_account_file:
            self._init_google_api()
    
    def _init_google_api(self):
        """Initialize Google Indexing API"""
        try:
            SCOPES = ["https://www.googleapis.com/auth/indexing"]
            credentials = service_account.Credentials.from_service_account_file(
                self.service_account_file, scopes=SCOPES
            )
            self.indexing_service = build('indexing', 'v3', credentials=credentials)
            print("✓ Google Indexing API initialized successfully")
        except Exception as e:
            print(f"✗ Google Indexing API initialization failed: {e}")
    
    def index_via_google_api(self, url: str) -> Dict:
        """
        Index URL using official Google Indexing API
        Best for: High-priority pages, instant indexing
        """
        if not self.indexing_service:
            return {"method": "Google API", "url": url, "status": "failed", 
                    "message": "API not initialized"}
        
        try:
            body = {
                "url": url,
                "type": "URL_UPDATED"
            }
            response = self.indexing_service.urlNotifications().publish(body=body).execute()
            return {
                "method": "Google Indexing API",
                "url": url,
                "status": "success",
                "response": response,
                "timestamp": datetime.now().isoformat()
            }
        except HttpError as e:
            return {
                "method": "Google Indexing API",
                "url": url,
                "status": "failed",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def index_via_indexnow(self, urls: List[str], host: str, api_key: str) -> Dict:
        """
        Index URLs using IndexNow API (Bing, Yandex, etc.)
        Fast alternative indexing method
        """
        endpoint = "https://api.indexnow.org/indexnow"
        
        payload = {
            "host": host,
            "key": api_key,
            "keyLocation": f"https://{host}/{api_key}.txt",
            "urlList": urls
        }
        
        try:
            response = requests.post(
                endpoint,
                json=payload,
                headers={"Content-Type": "application/json; charset=utf-8"}
            )
            
            return {
                "method": "IndexNow API",
                "urls": urls,
                "status": "success" if response.status_code == 200 else "failed",
                "status_code": response.status_code,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "method": "IndexNow API",
                "urls": urls,
                "status": "failed",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def ping_sitemap(self, sitemap_url: str) -> Dict:
        """
        Ping Google with sitemap URL
        Good for: Batch indexing, regular updates
        """
        ping_url = f"https://www.google.com/ping?sitemap={quote(sitemap_url)}"
        
        try:
            response = requests.get(ping_url, timeout=10)
            return {
                "method": "Sitemap Ping",
                "sitemap_url": sitemap_url,
                "status": "success" if response.status_code == 200 else "failed",
                "status_code": response.status_code,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "method": "Sitemap Ping",
                "sitemap_url": sitemap_url,
                "status": "failed",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def create_dynamic_sitemap(self, urls: List[str], filename: str = "dynamic_sitemap.xml") -> str:
        """
        Create a dynamic sitemap for the URLs
        Returns: Path to sitemap file
        """
        urlset = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")
        
        for url in urls:
            url_elem = ET.SubElement(urlset, "url")
            loc = ET.SubElement(url_elem, "loc")
            loc.text = url
            lastmod = ET.SubElement(url_elem, "lastmod")
            lastmod.text = datetime.now().strftime("%Y-%m-%d")
            changefreq = ET.SubElement(url_elem, "changefreq")
            changefreq.text = "daily"
            priority = ET.SubElement(url_elem, "priority")
            priority.text = "1.0"
        
        tree = ET.ElementTree(urlset)
        tree.write(filename, encoding="utf-8", xml_declaration=True)
        return filename
    
    def ping_external_services(self, url: str) -> List[Dict]:
        """
        Ping multiple external indexing services
        Increases chances of discovery
        """
        results = []
        
        # List of ping services
        services = [
            f"https://www.google.com/ping?sitemap={quote(url)}",
            f"https://www.bing.com/ping?sitemap={quote(url)}",
            f"https://submissions.ask.com/ping?sitemap={quote(url)}",
        ]
        
        for service in services:
            try:
                response = requests.get(service, timeout=5)
                results.append({
                    "service": service,
                    "status": "success" if response.status_code == 200 else "failed",
                    "status_code": response.status_code
                })
            except Exception as e:
                results.append({
                    "service": service,
                    "status": "failed",
                    "error": str(e)
                })
        
        return results
    
    def check_indexing_status(self, url: str) -> Dict:
        """
        Check if URL is indexed on Google
        """
        search_query = f"site:{url}"
        search_url = f"https://www.google.com/search?q={quote(search_query)}"
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        
        try:
            response = requests.get(search_url, headers=headers, timeout=10)
            # Simple check - if the URL appears in results
            is_indexed = url in response.text
            return {
                "url": url,
                "indexed": is_indexed,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            return {
                "url": url,
                "indexed": "unknown",
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def rapid_index_single_url(self, url: str, use_all_methods: bool = True) -> Dict:
        """
        Rapidly index a single URL using all available methods
        """
        results = {
            "url": url,
            "timestamp": datetime.now().isoformat(),
            "methods_used": []
        }
        
        # Method 1: Google Indexing API (if available)
        if self.indexing_service:
            api_result = self.index_via_google_api(url)
            results["methods_used"].append(api_result)
        
        # Method 2: External pings
        if use_all_methods:
            ping_results = self.ping_external_services(url)
            results["methods_used"].extend(ping_results)
        
        return results
    
    def rapid_index_bulk(self, urls: List[str], max_workers: int = 10) -> List[Dict]:
        """
        Index multiple URLs in parallel for speed
        Supports: PDF, HTML, Forum, Web 2.0, Tier 1/2/3 backlinks
        """
        all_results = []
        
        print(f"Starting bulk indexing for {len(urls)} URLs...")
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_url = {
                executor.submit(self.rapid_index_single_url, url): url 
                for url in urls
            }
            
            for future in concurrent.futures.as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    result = future.result()
                    all_results.append(result)
                    print(f"✓ Processed: {url}")
                except Exception as e:
                    print(f"✗ Failed: {url} - {e}")
                    all_results.append({
                        "url": url,
                        "status": "failed",
                        "error": str(e)
                    })
        
        return all_results
    
    def save_results(self, results: List[Dict], filename: str = "indexing_results.json"):
        """Save indexing results to JSON file"""
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"Results saved to {filename}")


# Example usage and demonstration
if __name__ == "__main__":
    print("=" * 60)
    print("Google Instant Indexer - Multi-Method System")
    print("=" * 60)
    
    # Initialize indexer
    # For Google API: provide service_account_file path
    indexer = GoogleInstantIndexer()
    
    # Example URLs to index (supports all types)
    test_urls = [
        "https://example.com/page1.html",  # HTML page
        "https://example.com/document.pdf",  # PDF
        "https://forum.example.com/thread/123",  # Forum link
        "https://web2.example.com/post/456",  # Web 2.0
        "https://tier1.example.com/backlink",  # Tier 1 backlink
    ]
    
    print("\nIndexing Methods Available:")
    print("1. Google Indexing API (official, instant)")
    print("2. IndexNow API (Bing, fast)")
    print("3. Sitemap Ping (batch, reliable)")
    print("4. External Service Pings (wide coverage)")
    print("5. Parallel Processing (speed)")
    print("\n" + "=" * 60)
    
    # Method 1: Index single URL
    print("\n[Method 1] Single URL Indexing:")
    result = indexer.rapid_index_single_url(test_urls[0])
    print(json.dumps(result, indent=2))
    
    # Method 2: Bulk indexing with parallel processing
    print("\n[Method 2] Bulk Parallel Indexing:")
    bulk_results = indexer.rapid_index_bulk(test_urls, max_workers=5)
    
    # Save results
    indexer.save_results(bulk_results)
    
    print("\n" + "=" * 60)
    print("Indexing Complete!")
    print("=" * 60)
