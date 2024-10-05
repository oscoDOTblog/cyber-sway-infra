from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
import os

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

# ... existing code ...
