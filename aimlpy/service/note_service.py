from typing import List
from aimlpy.entity.note import Note
from aimlpy.repo.note_repo import NoteRepo


class NoteService:
    def __init__(self):
        self.note_repo = NoteRepo()

    def list_notes_by_user(self, user_id: int) -> List[Note]:
        try:
            records = self.note_repo.list_by_user(user_id)
            return [Note.model_validate(r) for r in records]
        except Exception as e:
            raise Exception(f"Failed to list notes: {str(e)}")

    def export_notes_markdown(self, user_id: int) -> str:
        notes = self.list_notes_by_user(user_id)
        lines = [f"# Notes for User {user_id}\n"]
        for i, n in enumerate(notes, 1):
            lines.append(f"## Note {i}\n")
            lines.append(n.text or "")
            lines.append("")
        return "\n".join(lines)

    def export_notes_pdf(self, user_id: int) -> bytes:
        try:
            from fpdf import FPDF
        except Exception as e:
            raise Exception("fpdf is required for PDF export. Please install fpdf") from e

        notes = self.list_notes_by_user(user_id)
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()
        pdf.set_font("Arial", size=16)
        pdf.cell(200, 10, txt=f"Notes for User {user_id}", ln=True, align="L")
        pdf.set_font("Arial", size=12)

        for i, n in enumerate(notes, 1):
            pdf.ln(5)
            pdf.set_font("Arial", size=14)
            pdf.cell(0, 10, txt=f"Note {i}", ln=True)
            pdf.set_font("Arial", size=12)
            text = (n.text or "")
            for line in text.splitlines() or [""]:
                pdf.multi_cell(0, 8, line)

        return pdf.output(dest="S").encode("latin-1")
