from pydantic import BaseModel

class IntentResponse(BaseModel):
    intent: str

class AttributeExtractionResponse(BaseModel):
    extracted_attributes: dict