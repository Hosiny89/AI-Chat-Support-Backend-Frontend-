from pydantic import BaseModel, Field
from typing import Optional

# Schema لإنشاء Note جديدة
class NoteBase(BaseModel):
    title: str = Field(..., min_length=3, max_length=100)
    content: str

class NoteCreate(NoteBase):
    pass

class NoteUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

# Schema لعرض Note
class NoteDisplay(NoteBase):
    id: int

    class Config:
        from_attributes = True
