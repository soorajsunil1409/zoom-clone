from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.database import SessionLocal
from app.services.meeting_service import get_meeting_by_code
from app.services.participant_service import (
    get_participant_by_token,
)
from app.websocket.manager import manager


router = APIRouter()


@router.websocket(
    "/ws/meetings/{meeting_code}"
)
async def meeting_websocket(
    websocket: WebSocket,
    meeting_code: str,
    token: str,
):
    db = SessionLocal()

    try:
        meeting = get_meeting_by_code(
            db=db,
            meeting_code=meeting_code,
        )

        if not meeting:
            await websocket.close(code=4004)
            return

        participant = get_participant_by_token(
            db=db,
            token=token,
        )

        if not participant:
            await websocket.close(code=4003)
            return

        if participant.meeting_id != meeting.id:
            await websocket.close(code=4003)
            return

        await manager.connect(
            meeting_code,
            participant.id,
            websocket,
        )

        await manager.broadcast(
            meeting_code,
            {
                "type": "participant_joined",
                "participant_id": participant.id,
                "display_name": participant.display_name,
            },
            exclude=participant.id,
        )

        await websocket.send_json(
            {
                "type": "connected",
                "participant_id": participant.id,
                "participants": manager.get_participants(
                    meeting_code
                ),
            }
        )

        while True:
            message = await websocket.receive_json()

            message["from"] = participant.id

            target = message.get("to")

            if target is not None:
                await manager.send_to(
                    meeting_code,
                    target,
                    message,
                )
            else:
                await manager.broadcast(
                    meeting_code,
                    message,
                    exclude=participant.id,
                )

    except WebSocketDisconnect:
        manager.disconnect(
            meeting_code,
            participant.id if participant else -1,
        )

        await manager.broadcast(
            meeting_code,
            {
                "type": "participant_left",
                "participant_id": (
                    participant.id
                    if participant
                    else None
                ),
            },
        )

    finally:
        db.close()