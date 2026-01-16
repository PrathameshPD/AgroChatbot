import os
import json
from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Import RAG logic
import sys
sys.path.append(os.path.dirname(__file__))
from agentic_rag import get_response

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Mount reports directory
from fastapi.staticfiles import StaticFiles
reports_dir = os.path.join(os.path.dirname(__file__), "reports")
os.makedirs(reports_dir, exist_ok=True)
app.mount("/reports", StaticFiles(directory=reports_dir), name="reports")

# --- AGROBOT /ask ENDPOINT ---
@app.post("/ask")
async def ask(
    query: str = Form(...),
    session_id: str = Form("default")
):
    try:
        # Pass session_id to get_response
        response_text = get_response(query, session_id=session_id)
        return {"response": response_text}
    except Exception as e:
        return JSONResponse(status_code=500, content={"response": f"Error: {str(e)}"})

working_dir = os.path.dirname(os.path.abspath(__file__))
