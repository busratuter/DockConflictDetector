from pydantic import BaseModel, Field
from typing import List

class Conflict(BaseModel):
    section1: str = Field(description="First conflicting passage from the text")
    section2: str = Field(description="Second conflicting passage from the text")
    conflict_description: str = Field(description="Description of why these passages conflict")

class ConflictAnalysis(BaseModel):
    conflicts: List[Conflict] = Field(
        description="List of conflicts found in the text",
        default_factory=list
    )