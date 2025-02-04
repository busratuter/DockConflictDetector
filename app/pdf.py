from io import BytesIO
import PyPDF2

def extract_text_from_pdf(pdf_contents: bytes) -> str:
    """
    PDF içeriğini metin olarak çıkarır
    
    Args:
        pdf_contents (bytes): PDF dosyasının binary içeriği
        
    Returns:
        str: PDF'den çıkarılan metin
    """
    pdf_file = BytesIO(pdf_contents)
    
    try:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
            
        return text
    except Exception as e:
        raise Exception(f"PDF okuma hatası: {str(e)}")
    finally:
        pdf_file.close()