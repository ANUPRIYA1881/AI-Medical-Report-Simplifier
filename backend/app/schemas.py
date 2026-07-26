from pydantic import BaseModel
from typing import List


class MedicalResult(BaseModel):
    test_name: str
    value: str
    unit: str
    reference_range: str
    status: str
    explanation: str


class MedicalReportResponse(BaseModel):
    report_type: str
    summary: str
    results: List[MedicalResult]
    questions_for_doctor: List[str]


class AskRequest(BaseModel):
    question: str
    report_context: str


class AskResponse(BaseModel):
    answer: str