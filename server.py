"""
Server API Entry Point - RESTful API using FastAPI
Usage:
    python server.py --port 8000
    # Access API at http://localhost:8000
    # API docs at http://localhost:8000/docs
"""
import argparse
import os
from typing import Dict, Any, Optional, List
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn
from shared.engine import ReportEngine


app = FastAPI(
    title="ESG Report Generation API",
    description="Three-channel parallel architecture for ESG report generation",
    version="1.0.0"
)


class GenerateRequest(BaseModel):
    """Request model for report generation"""
    module: str  # environment, company, governance, or "all"
    mode: Optional[str] = "mock"  # mock, llm-test, production
    input_data: Optional[Dict[str, Any]] = None


class GenerateResponse(BaseModel):
    """Response model for report generation"""
    success: bool
    mode: str
    module: str
    result: Dict[str, Any]
    message: Optional[str] = None


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "ESG Report Generation API",
        "version": "1.0.0",
        "endpoints": {
            "generate": "/api/generate",
            "modules": "/api/modules",
            "health": "/api/health",
            "docs": "/docs"
        }
    }


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "ESG Report API"}


@app.get("/api/modules")
async def get_modules():
    """Get available modules"""
    engine = ReportEngine()
    return {
        "modules": engine.get_available_modules(),
        "modes": ["mock", "llm-test", "production"]
    }


@app.post("/api/generate", response_model=GenerateResponse)
async def generate_report(request: GenerateRequest):
    """
    Generate report for specified module
    
    Request body:
    {
        "module": "environment",  // or "company", "governance", "all"
        "mode": "mock",  // or "llm-test", "production"
        "input_data": {
            "company_name": "Sample Company",
            "year": "2025"
        }
    }
    """
    try:
        # Initialize engine with specified mode
        engine = ReportEngine(mode=request.mode)
        
        # Prepare input data
        input_data = request.input_data or {
            "company_name": "Sample Company",
            "year": "2025"
        }
        
        # Determine modules to generate
        if request.module == "all":
            modules = None
        else:
            if request.module not in engine.get_available_modules():
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid module: {request.module}. Available: {engine.get_available_modules()}"
                )
            modules = [request.module]
        
        # Generate reports
        results = engine.generate_all(input_data, modules)
        
        # Format response
        if request.module == "all":
            return GenerateResponse(
                success=True,
                mode=request.mode,
                module="all",
                result=results,
                message=f"Generated reports for {len(results)} module(s)"
            )
        else:
            if request.module in results and "error" in results[request.module]:
                raise HTTPException(
                    status_code=500,
                    detail=f"Generation failed: {results[request.module]['error']}"
                )
            
            return GenerateResponse(
                success=True,
                mode=request.mode,
                module=request.module,
                result=results.get(request.module, {}),
                message="Report generated successfully"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.get("/api/generate/{module}")
async def generate_module_get(module: str, mode: str = "mock"):
    """
    Generate report via GET request (convenience endpoint)
    
    Query parameters:
    - module: environment, company, governance, or all
    - mode: mock, llm-test, or production
    """
    request = GenerateRequest(module=module, mode=mode)
    return await generate_report(request)


def main():
    parser = argparse.ArgumentParser(description='ESG Report Generation API Server')
    parser.add_argument(
        '--port',
        type=int,
        default=8000,
        help='Port number (default: 8000)'
    )
    parser.add_argument(
        '--host',
        type=str,
        default='127.0.0.1',
        help='Host address (default: 127.0.0.1)'
    )
    
    args = parser.parse_args()
    
    print(f"Starting ESG Report API Server...")
    print(f"Server will be available at: http://{args.host}:{args.port}")
    print(f"API documentation at: http://{args.host}:{args.port}/docs")
    print(f"Health check at: http://{args.host}:{args.port}/api/health")
    
    uvicorn.run(app, host=args.host, port=args.port)


if __name__ == '__main__':
    main()

