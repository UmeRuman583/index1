# Google Instant Indexer - Complete Setup Guide

## 🚀 Features

This instant indexer supports:
- ✅ PDF Links
- ✅ HTML Pages
- ✅ Forum Links
- ✅ Web 2.0 Properties
- ✅ Tier 1, 2, 3 Backlinks
- ✅ Batch Processing
- ✅ Parallel Indexing (fast!)
- ✅ Multiple Indexing Methods

## 📋 Setup Instructions

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Google Indexing API Setup (RECOMMENDED)

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable the "Web Search Indexing API"
4. Create a Service Account:
   - Go to IAM & Admin > Service Accounts
   - Create Service Account
   - Download JSON key file
5. Add the service account email to Google Search Console:
   - Go to [Google Search Console](https://search.google.com/search-console)
   - Select your property
   - Go to Settings > Users and permissions
   - Add service account email as Owner

6. Save the JSON file and update the path in the code

### Step 3: IndexNow API Setup (OPTIONAL)

1. Generate an API key (any random string, e.g., UUID)
2. Create a text file: `your-api-key.txt` with the API key
3. Upload to your website root: `https://yoursite.com/your-api-key.txt`

## 🔧 Usage Examples

### Example 1: Basic Usage (No API Keys)

```python
from google_indexer import GoogleInstantIndexer

# Initialize without API (uses ping methods)
indexer = GoogleInstantIndexer()

# Index single URL
result = indexer.rapid_index_single_url("https://example.com/page.html")
print(result)
```

### Example 2: With Google API (FASTEST)

```python
from google_indexer import GoogleInstantIndexer

# Initialize with Google API
indexer = GoogleInstantIndexer(service_account_file="service-account.json")

# Index single URL via Google API
result = indexer.index_via_google_api("https://example.com/page.html")
print(result)
```

### Example 3: Bulk Indexing (All Link Types)

```python
from google_indexer import GoogleInstantIndexer

indexer = GoogleInstantIndexer(service_account_file="service-account.json")

# Mix of different link types
urls = [
    "https://example.com/article.html",           # HTML page
    "https://example.com/guide.pdf",              # PDF
    "https://forum.example.com/topic/123",        # Forum
    "https://medium.com/@user/post-456",          # Web 2.0
    "https://tier1-backlink.com/link1",           # Tier 1
    "https://tier2-backlink.com/link2",           # Tier 2
    "https://tier3-backlink.com/link3",           # Tier 3
]

# Index all URLs in parallel (FAST!)
results = indexer.rapid_index_bulk(urls, max_workers=10)

# Save results
indexer.save_results(results, "indexing_report.json")
```

### Example 4: Using IndexNow API

```python
indexer = GoogleInstantIndexer()

urls = [
    "https://yoursite.com/page1.html",
    "https://yoursite.com/page2.html"
]

result = indexer.index_via_indexnow(
    urls=urls,
    host="yoursite.com",
    api_key="your-indexnow-api-key"
)
print(result)
```

### Example 5: Sitemap Method

```python
indexer = GoogleInstantIndexer()

# Create dynamic sitemap from URLs
urls = ["https://example.com/page1", "https://example.com/page2"]
sitemap_file = indexer.create_dynamic_sitemap(urls)

# Upload sitemap to your server, then ping Google
result = indexer.ping_sitemap("https://yoursite.com/dynamic_sitemap.xml")
print(result)
```

### Example 6: Check Indexing Status

```python
indexer = GoogleInstantIndexer()

status = indexer.check_indexing_status("https://example.com/page.html")
print(f"Indexed: {status['indexed']}")
```

## 🎯 Advanced Usage Script

```python
from google_indexer import GoogleInstantIndexer
import json

def main():
    # Initialize with Google API for best results
    indexer = GoogleInstantIndexer(service_account_file="service-account.json")
    
    # Read URLs from file
    with open('urls_to_index.txt', 'r') as f:
        urls = [line.strip() for line in f if line.strip()]
    
    print(f"Indexing {len(urls)} URLs...")
    
    # Rapid bulk indexing
    results = indexer.rapid_index_bulk(urls, max_workers=20)
    
    # Analyze results
    successful = sum(1 for r in results if 'success' in str(r.get('status', '')))
    failed = len(results) - successful
    
    print(f"\n✓ Successful: {successful}")
    print(f"✗ Failed: {failed}")
    
    # Save detailed results
    indexer.save_results(results, "indexing_report.json")
    
    # Check indexing status after some time
    print("\nChecking indexing status (wait 2-3 minutes for best results)...")
    import time
    time.sleep(180)  # Wait 3 minutes
    
    for url in urls[:5]:  # Check first 5
        status = indexer.check_indexing_status(url)
        print(f"{url}: {'✓ Indexed' if status['indexed'] else '✗ Not yet'}")

if __name__ == "__main__":
    main()
```

## 📊 Indexing Methods Comparison

| Method | Speed | Reliability | Limit | Best For |
|--------|-------|-------------|-------|----------|
| Google API | ⚡⚡⚡ Instant | ⭐⭐⭐ High | 200/day | Priority pages |
| IndexNow | ⚡⚡ Fast | ⭐⭐ Medium | 10,000/day | Bulk updates |
| Sitemap Ping | ⚡ Moderate | ⭐⭐⭐ High | Unlimited | Regular crawls |
| External Pings | ⚡ Moderate | ⭐ Low | Unlimited | Extra coverage |

## 🔥 Pro Tips

1. **Use Google API for critical pages** - Limited quota but instant
2. **Combine methods** - Use multiple methods for better coverage
3. **Tier strategy**: 
   - Tier 1: Google API
   - Tier 2: IndexNow
   - Tier 3: Sitemap ping
4. **Wait time**: Pages typically index within 2-10 minutes with Google API
5. **Batch processing**: Process 50-100 URLs at a time for best results
6. **Monitor**: Check Google Search Console for indexing status

## 🚨 Important Notes

- Google Indexing API has a quota of 200 URLs per day
- IndexNow supports up to 10,000 URLs per day
- PDF and forum links may take longer to index
- Always verify indexing in Google Search Console
- Some methods work better for certain link types

## 📝 Example URLs File (urls_to_index.txt)

```
https://example.com/page1.html
https://example.com/document.pdf
https://forum.example.com/thread/123
https://medium.com/@user/article
https://backlink-tier1.com/link
https://backlink-tier2.com/link
https://backlink-tier3.com/link
```

## 🐛 Troubleshooting

**Error: "API not initialized"**
- Solution: Provide valid service account JSON file

**Error: "Permission denied"**
- Solution: Add service account email to Google Search Console as Owner

**URLs not indexing**
- Wait 2-10 minutes after submission
- Check Google Search Console for errors
- Ensure URLs are accessible and not blocked by robots.txt

**Rate limit exceeded**
- Google API: 200 URLs/day limit
- Solution: Use IndexNow or sitemap ping for additional URLs

## 📞 Support

For issues or questions, check:
- Google Search Console documentation
- IndexNow API documentation
- This README file

## 🎉 Success Metrics

After indexing, monitor:
- Google Search Console > Coverage report
- Indexed pages count
- Crawl stats
- Index time (should be minutes to hours)
