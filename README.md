# DockConflictDetector

This project is a FastAPI application that detects conflicting statements in PDF documents. It uses Azure OpenAI service to analyze potential conflicts within PDF content.

## Requirements

- Python 3.8+
- FastAPI
- PyPDF2
- Azure OpenAI API access

## Installation

1. Clone the project:
```bash
git clone <repository-url>
cd DockConflictDetector
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Unix/macOS
# or
.\venv\Scripts\activate  # Windows
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Create `.env` file and add required variables:
```env
OPENAI_API_KEY=your_api_key
OPENAI_API_VERSION=your_api_version
OPENAI_API_BASE=your_api_base
OPENAI_DEPLOYMENT_NAME=your_deployment_name
```

## Running the Application

To start the application:

```bash
uvicorn app.main:app --reload --port 8000
```

To access the API documentation, open the following URL in your browser:
```
http://localhost:8000/docs
```

## API Usage

- Use the `/upload` endpoint to upload PDF files
- Only PDF format files are accepted
- The content of the uploaded PDF is analyzed to detect conflicting statements
- Results are returned in JSON format
