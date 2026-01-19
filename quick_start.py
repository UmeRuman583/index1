#!/usr/bin/env python3
"""
Quick Start Script - Google Instant Indexer
Run this script to quickly index your URLs
"""

from google_indexer import GoogleInstantIndexer
import json
import time
from datetime import datetime

def print_header():
    print("=" * 70)
    print("         GOOGLE INSTANT INDEXER - QUICK START")
    print("=" * 70)
    print("Supports: PDF | HTML | Forum | Web 2.0 | Tier 1/2/3 Backlinks")
    print("=" * 70)
    print()

def main():
    print_header()
    
    # Configuration
    USE_GOOGLE_API = False  # Set to True if you have service account JSON
    SERVICE_ACCOUNT_FILE = "service-account.json"  # Update path if needed
    
    # Your URLs to index (edit this list)
    urls_to_index = [
        # HTML Pages
        "https://example.com/page1.html",
        "https://example.com/blog/article-1",
        
        # PDF Documents
        "https://example.com/whitepaper.pdf",
        "https://example.com/guide.pdf",
        
        # Forum Links
        "https://forum.example.com/threads/topic-123",
        
        # Web 2.0 Properties
        "https://medium.com/@youruser/post-456",
        "https://wordpress.com/yoursite/article",
        
        # Backlinks (Tier 1, 2, 3)
        "https://tier1-backlink.com/your-link",
        "https://tier2-backlink.com/your-link",
        "https://tier3-backlink.com/your-link",
    ]
    
    # Initialize indexer
    if USE_GOOGLE_API:
        print(f"🔧 Initializing with Google API ({SERVICE_ACCOUNT_FILE})...")
        indexer = GoogleInstantIndexer(service_account_file=SERVICE_ACCOUNT_FILE)
    else:
        print("🔧 Initializing with ping methods (no API key needed)...")
        indexer = GoogleInstantIndexer()
    
    print(f"📋 URLs to index: {len(urls_to_index)}")
    print()
    
    # Start indexing
    print("🚀 Starting rapid indexing...")
    print("-" * 70)
    
    start_time = time.time()
    
    # Method 1: If using Google API, index one by one for detailed feedback
    if USE_GOOGLE_API and indexer.indexing_service:
        results = []
        for i, url in enumerate(urls_to_index, 1):
            print(f"[{i}/{len(urls_to_index)}] Indexing: {url}")
            result = indexer.index_via_google_api(url)
            results.append(result)
            
            if result['status'] == 'success':
                print(f"    ✓ Success!")
            else:
                print(f"    ✗ Failed: {result.get('error', 'Unknown error')}")
            
            time.sleep(0.5)  # Small delay between requests
    
    # Method 2: Bulk parallel indexing (faster for many URLs)
    else:
        print("Using parallel processing for maximum speed...")
        results = indexer.rapid_index_bulk(urls_to_index, max_workers=10)
    
    # Calculate time taken
    end_time = time.time()
    duration = end_time - start_time
    
    print("-" * 70)
    print()
    
    # Analyze results
    successful = 0
    failed = 0
    
    for result in results:
        if 'methods_used' in result:
            # Bulk result format
            success_methods = [m for m in result['methods_used'] 
                             if m.get('status') == 'success']
            if success_methods:
                successful += 1
            else:
                failed += 1
        elif result.get('status') == 'success':
            successful += 1
        else:
            failed += 1
    
    # Print summary
    print("📊 INDEXING SUMMARY")
    print("=" * 70)
    print(f"✓ Successful: {successful}/{len(urls_to_index)}")
    print(f"✗ Failed: {failed}/{len(urls_to_index)}")
    print(f"⏱️  Time taken: {duration:.2f} seconds")
    print(f"⚡ Speed: {len(urls_to_index)/duration:.2f} URLs/second")
    print()
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file = f"indexing_results_{timestamp}.json"
    indexer.save_results(results, results_file)
    print(f"💾 Detailed results saved to: {results_file}")
    print()
    
    # Next steps
    print("📌 NEXT STEPS:")
    print("-" * 70)
    print("1. Wait 2-10 minutes for indexing to complete")
    print("2. Check Google Search Console > Coverage report")
    print("3. Verify indexing: site:yourdomain.com in Google search")
    print("4. Monitor crawl stats in Search Console")
    print()
    
    if not USE_GOOGLE_API:
        print("💡 TIP: For INSTANT indexing, set up Google Indexing API!")
        print("   See README.md for setup instructions")
        print()
    
    print("=" * 70)
    print("✨ Indexing process complete!")
    print("=" * 70)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Indexing interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        print("Check README.md for troubleshooting help")
