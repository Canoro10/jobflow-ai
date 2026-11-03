from google import genai

from app.core.config import settings
from app.schemas.job_analysis import JobAnalysisResponse


client = genai.Client(
    api_key=settings.gemini_api_key,
)


def analyze_job_description(
    description: str,
) -> JobAnalysisResponse:

    prompt = f"""
Analyze the following job posting.

Extract only information explicitly present or reasonably inferable
from the posting.

Rules:
- Normalize technology names.
- Do not invent requirements.
- If seniority is unclear, use "Unknown".
- If remote status is unclear, return null.
- Return skills as concise technology or competency names.

JOB POSTING:

{description}
"""

    interaction = client.interactions.create(
        model=settings.gemini_model,
        input=prompt,
        response_format={
            "type": "text",
            "mime_type": "application/json",
            "schema": JobAnalysisResponse.model_json_schema(),
        },
    )

    return JobAnalysisResponse.model_validate_json(
        interaction.output_text
    )