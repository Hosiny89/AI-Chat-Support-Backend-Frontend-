from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import get_db
from schemas.note import NoteBase, NoteDisplay, NoteCreate, NoteUpdate
import crud, schemas
from crud import note as crud_note
from typing import List
from db.models import Note

# -------------------------- تعريف الراوتر ------------------------------
router = APIRouter(
    prefix="/notes",
    tags=["Notes"]
)

# ---------------------------انشاء نوتة جديدة------------------------------
@router.post("/", response_model=NoteDisplay)
def create_note(note: NoteBase, db: Session = Depends(get_db)):
    return crud_note.create_note(db=db, note=note)


#------------------------ استرجاع نوتة واحدة بالـ id ----------------------
@router.get("/{note_id}")
def get_note_by_id(note_id: int, db: Session = Depends(get_db)):
    db_note = crud_note.get_note(db, note_id=note_id)
    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return db_note

# -------------------------- دالة لجلب كل النوتات --------------------------
@router.get("/", response_model=List[NoteDisplay])
def get_notes(db: Session = Depends(get_db)):
    return crud_note.get_notes(db=db)

#-----------------دالة لجلب ملاحظة واحدة فقط عن طريق ال id -----------------
@router.get("/{note_id}", response_model=NoteDisplay)
def get_note(note_id: int, db: Session = Depends(get_db)):
    try:
        db_note = crud_note.get_note(db, note_id=note_id)
        if db_note is None:
            raise HTTPException(status_code=404, detail="Note not found")
        return db_note
    except Exception as e:
        print("DEBUG ERROR:", e)
        raise HTTPException(status_code=500, detail=str(e))
        
#-------------------------------- Update note ---------------------------------
@router.put("/{note_id}", response_model=NoteBase)
def update_note(note_id: int, note: NoteCreate, db: Session = Depends(get_db)):
    db_note = crud_note.get_note(db, note_id=note_id)
    if db_note is None:
        raise HTTPException(status_code=404, detail="Note not found")
    return crud_note.update_note(db=db, note_id=note_id, note=note)

#-------------------------------- Search notes by title -------------------------
@router.get("/search/", response_model=List[NoteDisplay])
def search_notes(query: str, db: Session = Depends(get_db)):
    notes = db.query(Note).filter(Note.title.contains(query)).all()
    return notes

#--------------------------------- Delete note ---------------------------------
@router.delete("/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db)):
    success = crud_note.delete_note(db, note_id)
    if not success:
        raise HTTPException(status_code=404, detail="Note not found")
    return {"message": "Note deleted successfully"}
