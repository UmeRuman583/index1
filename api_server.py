"""
FastAPI Backend for Google Instant Indexer
Handles API requests from Next.js frontend
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import sys
import os

# Add parent directory to path to import google_indexer
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from google_indexer import GoogleInstantIndexer

app = FastAPI(title="Google Instant Indexer API")

# CORS middleware for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Next.js default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global state
indexer = None
indexing_in_progress = False
last_results = []

# Models
class IndexRequest(BaseModel):
    urls: List[str]
    use_google_api: bool = False
    service_account_file: Optional[str] = None

class ConfigRequest(BaseModel):
    use_google_api: bool = False
    service_account_file: Optional[str] = None

@app.on_event("startup")
async def startup_event():
    """Initialize indexer on startup"""
    global indexer
    indexer = GoogleInstantIndexer()
    print("✓ Google Indexer API started successfully")

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "Google Instant Indexer API",
        "version": "1.0.0"
    }

@app.get("/api/health")
async def health_check():
    """Health check for frontend"""
    return {
        "status": "healthy",
        "indexer_ready": indexer is not None,
        "google_api_enabled": indexer.indexing_service is not None if indexer else False
    }

@app.post("/api/config")
async def configure(config: ConfigRequest):
    """Configure indexer settings"""
    global indexer
    
    try:
        if config.use_google_api and config.service_account_file:
            indexer = GoogleInstantIndexer(service_account_file=config.service_account_file)
        else:
            indexer = GoogleInstantIndexer()
        
        return {
            "status": "success",
            "message": "Configuration updated",
            "google_api_enabled": indexer.indexing_service is not None
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/index")
async def index_urls(request: IndexRequest, background_tasks: BackgroundTasks):
    """Start indexing URLs"""
    global indexing_in_progress, last_results
    
    if indexing_in_progress:
        raise HTTPException(
            status_code=400, 
            detail="Indexing already in progress"
        )
    
    if not request.urls:
        raise HTTPException(
            status_code=400,
            detail="No URLs provided"
        )
    
    # Update indexer if Google API requested
    if request.use_google_api and request.service_account_file:
        try:
            global indexer
            indexer = GoogleInstantIndexer(service_account_file=request.service_account_file)
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to initialize Google API: {str(e)}"
            )
    
    # Start indexing in background
    def index_task():
        global indexing_in_progress, last_results
        indexing_in_progress = True
        
        try:
            results = indexer.rapid_index_bulk(request.urls, max_workers=10)
            last_results = results
        except Exception as e:
            last_results = [{"error": str(e)}]
        finally:
            indexing_in_progress = False
    
    background_tasks.add_task(index_task)
    
    return {
        "status": "success",
        "message": f"Started indexing {len(request.urls)} URLs",
        "url_count": len(request.urls)
    }

@app.get("/api/status")
async def get_status():
    """Get current indexing status"""
    global indexing_in_progress, last_results
    
    if indexing_in_progress:
        return {
            "status": "indexing",
            "in_progress": True,
            "message": "Indexing in progress..."
        }
    
    if last_results:
        successful = sum(
            1 for r in last_results 
            if r.get('status') == 'success' or 
            any(m.get('status') == 'success' for m in r.get('methods_used', []))
        )
        
        return {
            "status": "complete",
            "in_progress": False,
            "total": len(last_results),
            "successful": successful,
            "failed": len(last_results) - successful,
            "results": last_results
        }
    
    return {
        "status": "idle",
        "in_progress": False,
        "message": "No indexing activity"
    }

@app.post("/api/check-url")
async def check_url_status(url: str):
    """Check if a URL is indexed"""
    try:
        result = indexer.check_indexing_status(url)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/methods")
async def get_methods():
    """Get available indexing methods"""
    return {
        "methods": [
            {
                "name": "Google Indexing API",
                "speed": "Instant",
                "limit": "200/day",
                "enabled": indexer.indexing_service is not None if indexer else False
            },
            {
                "name": "IndexNow API",
                "speed": "Fast",
                "limit": "10,000/day",
                "enabled": True
            },
            {
                "name": "Sitemap Ping",
                "speed": "Moderate",
                "limit": "Unlimited",
                "enabled": True
            },
            {
                "name": "External Pings",
                "speed": "Moderate",
                "limit": "Unlimited",
                "enabled": True
            }
        ]
    }

if __name__ == "__main__":
    import uvicorn
    print("=" * 70)
    print("Starting Google Instant Indexer API Server")
    print("=" * 70)
    print("API will be available at: http://localhost:8000")
    print("API Docs will be available at: http://localhost:8000/docs")
    print("=" * 70)
    uvicorn.run(app, host="0.0.0.0", port=8000)
