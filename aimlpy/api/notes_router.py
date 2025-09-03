from fastapi import APIRouter
from fastapi.responses import Response
from aimlpy.entity.note_reqres import NoteResponse
from aimlpy.service.note_service import NoteService
from aimlpy.entity.common import ErrorCode

router = APIRouter(prefix="/notes", tags=["Notes"])
service = NoteService()

@router.get("/export/markdown")
def export_notes_markdown(user_id: int):
    try:
        md = service.export_notes_markdown(user_id)
        return Response(content=md, media_type="text/markdown")
    except Exception as e:
        return NoteResponse(error=True, error_code=ErrorCode.INTERNAL_SERVER_ERROR, message=str(e))

@router.get("/export/pdf")
def export_notes_pdf(user_id: int):
    try:
        data = service.export_notes_pdf(user_id)
        return Response(
            content=data,
            media_type="application/pdf",
            headers={"Content-Disposition": f"attachment; filename=notes_user_{user_id}.pdf"},
        )
    except Exception as e:
        return NoteResponse(error=True, error_code=ErrorCode.INTERNAL_SERVER_ERROR, message=str(e))
