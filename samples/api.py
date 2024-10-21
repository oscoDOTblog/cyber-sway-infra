# uvicorn samples.api:app --reload
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import os
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    print("Server is starting...")

@app.get('/api/landmarks/{request_name}')
async def serve_landmarks(request_name: str):
    # Construct the path to the JSON file
    json_file_path = os.path.join('results', request_name, 'landmarks.json')
    
    # Check if the file exists
    if os.path.exists(json_file_path):
        print(f"Serving file: {json_file_path}")
        return FileResponse(json_file_path)
    else:
        raise HTTPException(status_code=404, detail="File not found")

@app.get('/api/hello')
async def hello():
    return {"Hello": "World"}

@app.get('/api/metadata/{request_name}')
async def serve_metadata(request_name: str):
    # Construct the path to the JSON file
    json_file_path = os.path.join('results', request_name, 'metadata.json')
    
    # Check if the file exists
    if os.path.exists(json_file_path):
        print(f"Serving file: {json_file_path}")
        return FileResponse(json_file_path)
    else:
        raise HTTPException(status_code=404, detail="File not found")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# ... existing code ...
