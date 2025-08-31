from sqlalchemy.orm import Session
from db.models import Note
from schemas.note import NoteBase, NoteUpdate
from crud import note as crud_note


def create_note(db: Session, note: NoteBase):
    db_note = Note(title=note.title, content=note.content)
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note


def get_notes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Note).offset(skip).limit(limit).all()


def get_note_by_id(db: Session, note_id: int):
    return db.query(Note).filter(Note.id == note_id).first()


def get_note(db: Session, note_id: int):
    return db.query(Note).filter(Note.id == note_id).first()


def update_note(db: Session, note_id: int, note: NoteUpdate):
    db_note = crud_note.get_note_by_id(db, note_id)
    if not db_note:
        return None
    if note.title is not None:
        db_note.title = note.title
    if note.content is not None:
        db_note.content = note.content
    db.commit()
    db.refresh(db_note)
    return db_note


def delete_note(db: Session, note_id: int):
    db_note = crud_note.get_note_by_id(db, note_id)
    if not db_note:
        return False
    db.delete(db_note)
    db.commit()
    return True
