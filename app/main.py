from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from .pdf import extract_text_from_pdf
from .openai_client import analyze_pdf_text

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """
    PDF dosyası yükleyip içeriğini analiz eder.
    
    - Sadece PDF dosyaları kabul edilir
    - Dosya içeriği okunup OpenAI modeline gönderilir
    - Analiz sonuçları döndürülür
    """
    try:
        contents = await file.read()
        
        if file.content_type != "application/pdf":
            return {"error": "Sadece PDF dosyaları kabul edilmektedir."}
        
        pdf_text = extract_text_from_pdf(contents)
        ai_response = analyze_pdf_text(pdf_text)
        
        return {
            "filename": file.filename,
            "content_type": file.content_type,
            "file_size": len(contents),
            "pdf_text": pdf_text,
            "ai_analysis": ai_response
        }
    except Exception as e:
        return {"error": str(e)} 