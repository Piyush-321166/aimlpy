from typing import List, Optional
from aimlpy.entity.note import Note


class NoteRepo:
    def __init__(self):
        # In-memory storage for notes (you can replace this with DB later)
        self._notes: List[Note] = []
        self._counter: int = 1

    def add(self, note: Note) -> Note:
        note.id = self._counter
        self._counter += 1
        self._notes.append(note)
        return note

    def get_by_id(self, note_id: int) -> Optional[Note]:
        for note in self._notes:
            if note.id == note_id:
                return note
        return None

    def get_by_user(self, user_id: int) -> List[Note]:
        return [note for note in self._notes if note.user_id == user_id]

    def list_all(self) -> List[Note]:
        return self._notes

    def delete(self, note_id: int) -> bool:
        for i, note in enumerate(self._notes):
            if note.id == note_id:
                del self._notes[i]
                return True
        return False


