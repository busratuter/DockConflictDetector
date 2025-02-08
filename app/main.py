from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from .pdf import extract_text_from_pdf
from .openai_client import analyze_pdf_text

app = FastAPI()

# CORS ayarları
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze")
async def analyze_document(file: UploadFile = File(...)):
    try:
        # Dosya içeriğini oku
        contents = await file.read()
        
        # PDF'den metin çıkarma
        text = extract_text_from_pdf(contents)
        
        # OpenAI ile analiz
        analysis = analyze_pdf_text(text)
        
        return {"analysis": analysis}
    except Exception as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=500, detail=str(e)) 