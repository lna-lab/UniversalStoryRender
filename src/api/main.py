from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pathlib import Path
import sys
import shutil
from typing import Optional

# Attempt to import pypdf for PDF processing
try:
    from pypdf import PdfReader
    HAS_PYPDF = True
except ImportError:
    HAS_PYPDF = False

# Setup paths
current_dir = Path(__file__).resolve().parent
project_root = current_dir.parent.parent
sys.path.append(str(project_root / "src"))

from core.engine import StoryEngine

app = FastAPI(title="Universal Story Renderer API")

# Allow CORS for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Engine
ontology_path = project_root / "ontology"
# Note: Engine might need to be initialized lazily or mocked if ontology doesn't exist yet
# engine = StoryEngine(ontology_path)

# Preset path
preset_path = project_root / "assets" / "preset.md"

class StoryRequest(BaseModel):
    text: str
    domain: str

class StoryResponse(BaseModel):
    story: str
    logs: list[str]
    graph: dict
    soul_structure: dict # Explicitly adding soul structure


class PresetResponse(BaseModel):
    text: str

@app.get("/api/health")
async def health_check():
    return {"status": "ok"}

@app.get("/api/preset", response_model=PresetResponse)
async def get_preset():
    if preset_path.exists():
        try:
            content = preset_path.read_text(encoding="utf-8")
            return {"text": content}
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to read preset: {str(e)}")
    return {"text": ""}

@app.post("/api/upload", response_model=PresetResponse)
async def upload_file(file: UploadFile = File(...)):
    filename = file.filename.lower()
    content = ""

    try:
        if filename.endswith(".pdf"):
            if not HAS_PYPDF:
                raise HTTPException(status_code=400, detail="PDF processing not available (pypdf not installed)")
            
            # Save temporary file to read
            temp_path = project_root / "temp_upload.pdf"
            with temp_path.open("wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            try:
                reader = PdfReader(str(temp_path))
                text_parts = []
                for page in reader.pages:
                    text_parts.append(page.extract_text())
                content = "\n".join(text_parts)
            finally:
                if temp_path.exists():
                    temp_path.unlink()

        elif filename.endswith(".txt") or filename.endswith(".md"):
            content_bytes = await file.read()
            # Try decoding with utf-8, fallback to shift_jis if needed (common in Japan)
            try:
                content = content_bytes.decode("utf-8")
            except UnicodeDecodeError:
                try:
                    content = content_bytes.decode("shift_jis")
                except UnicodeDecodeError:
                    raise HTTPException(status_code=400, detail="Could not decode file content. Please use UTF-8.")
        else:
            raise HTTPException(status_code=400, detail="Unsupported file type. Please upload .txt, .md, or .pdf")

        return {"text": content}

    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/render", response_model=StoryResponse)
async def render_story(request: StoryRequest):
    # Initialize engine (lazy init to avoid overhead on import if needed)
    engine = StoryEngine(ontology_path)
    
    result = engine.process(request.text, request.domain)
    
    return {
        "story": result["story"],
        "logs": result["logs"],
        "graph": result["graph"],
        "soul_structure": result["graph"] # Using graph/soul as the structure
    }

# Mount static files (Frontend)
static_dir = project_root / "src" / "web" / "static"
if static_dir.exists():
    # Mount /static explicit endpoint first
    app.mount("/static", StaticFiles(directory=str(static_dir), html=True), name="static_files")
    # Then mount root
    app.mount("/", StaticFiles(directory=str(static_dir), html=True), name="root")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
