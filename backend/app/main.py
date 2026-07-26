from fastapi import (
    FastAPI,
    UploadFile,
    File,
    HTTPException
)

from fastapi.middleware.cors import CORSMiddleware

from app.services.documents_service import (
    extract_text
)

from app.services.gemini_service import (
    analyze_report,
    ask_report_question
)

from app.schemas import (
    AskRequest
)


app = FastAPI(
    title="AI Medical Report Simplifier",
    description="AI-powered medical report understanding system",
    version="1.0.0"
)


# -------------------------
# CORS
# -------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://ai-medical-report-simplifier.onrender.com"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -------------------------
# Health Check
# -------------------------

@app.get("/")
def root():

    return {
        "message": "AI Medical Report Simplifier API is running"
    }


# -------------------------
# Analyze Report
# -------------------------

@app.post("/api/analyze")
async def analyze_medical_report(
    file: UploadFile = File(...)
):

    allowed_extensions = [
        ".pdf",
        ".jpg",
        ".jpeg",
        ".png"
    ]

    filename = file.filename.lower()

    if not any(
        filename.endswith(ext)
        for ext in allowed_extensions
    ):

        raise HTTPException(
            status_code=400,
            detail="Only PDF, JPG, JPEG and PNG files are supported"
        )


    try:

        file_bytes = await file.read()


        # Extract text
        report_text = extract_text(
            file_bytes,
            file.filename
        )


        if not report_text:

            raise HTTPException(
                status_code=400,
                detail="Could not extract text from the report"
            )


        # Analyze with Gemini
        result = analyze_report(
            report_text
        )


        return {
            "success": True,
            "filename": file.filename,
            "extracted_text": report_text,
            "analysis": result
        }


    except HTTPException:

        raise


    except Exception as e:

        print("ERROR:", e)

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# -------------------------
# Ask My Report
# -------------------------

@app.post("/api/ask")
async def ask_my_report(
    request: AskRequest
):

    try:

        answer = ask_report_question(
            question=request.question,
            report_context=request.report_context
        )


        return {
            "success": True,
            "answer": answer
        }


    except Exception as e:

        print("ERROR:", e)

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )