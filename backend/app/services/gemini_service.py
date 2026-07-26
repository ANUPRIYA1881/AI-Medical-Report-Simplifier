import json

from google import genai
from google.genai import types

from app.config import GEMINI_API_KEY


client = genai.Client(
    api_key=GEMINI_API_KEY
)


REPORT_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "report_type": {
            "type": "STRING"
        },
        "summary": {
            "type": "STRING"
        },
        "results": {
            "type": "ARRAY",
            "items": {
                "type": "OBJECT",
                "properties": {
                    "test_name": {
                        "type": "STRING"
                    },
                    "value": {
                        "type": "STRING"
                    },
                    "unit": {
                        "type": "STRING"
                    },
                    "reference_range": {
                        "type": "STRING"
                    },
                    "status": {
                        "type": "STRING"
                    },
                    "explanation": {
                        "type": "STRING"
                    }
                },
                "required": [
                    "test_name",
                    "value",
                    "unit",
                    "reference_range",
                    "status",
                    "explanation"
                ]
            }
        },
        "questions_for_doctor": {
            "type": "ARRAY",
            "items": {
                "type": "STRING"
            }
        }
    },
    "required": [
        "report_type",
        "summary",
        "results",
        "questions_for_doctor"
    ]
}


def analyze_report(report_text: str):

    prompt = f"""
You are an AI medical report education assistant.

Your task is to analyze the medical report text provided below.

IMPORTANT SAFETY RULES:

1. Do not diagnose diseases.
2. Do not prescribe medication.
3. Do not recommend specific treatment.
4. Do not claim certainty about a medical condition.
5. Only explain the information present in the report.
6. Use the reference range provided by the report whenever available.
7. If no reference range is available, say "Not provided".
8. Clearly distinguish between educational explanations and medical advice.
9. The explanation should be understandable to a normal person.
10. Do not invent test results.

For each medical test:

- Identify test name.
- Extract the value.
- Extract unit.
- Extract reference range.
- Determine whether the value is Normal, Low, High, or Unknown.
- Give a simple educational explanation.

Generate 3-5 useful questions that the patient could discuss with their doctor.

MEDICAL REPORT:

{report_text}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=REPORT_SCHEMA,
            temperature=0.2
        )
    )

    return json.loads(response.text)


def ask_report_question(
    question: str,
    report_context: str
):

    prompt = f"""
You are an AI assistant that helps users understand
their own medical report.

Answer the user's question using ONLY the provided
report context.

Do not diagnose.

Do not prescribe medication.

Do not invent information.

If the answer cannot be determined from the report,
say that clearly.

Give an easy-to-understand educational explanation.

Always remind the user that the information is not
a substitute for professional medical advice when
appropriate.

REPORT:

{report_context}

USER QUESTION:

{question}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text