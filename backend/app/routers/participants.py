from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.deps import get_db
from app.schemas import JoinRequest, JoinResponse, ParticipantOut
from app.services.meeting_service import get_meeting_by_code
from app.services.participant_service import (
    get_active_participants,
    get_participant_by_token,
    join_meeting,
    leave_meeting,
)

router = APIRouter(
    prefix="/api/meetings",
    tags=["participants"],
)


@router.post(
    "/{meeting_code}/join",
    response_model=JoinResponse,
    status_code=status.HTTP_201_CREATED,
)
def join(
    meeting_code: str,
    data: JoinRequest,
    db: Session = Depends(get_db),
):
    meeting = get_meeting_by_code(
        db=db,
        meeting_code=meeting_code,
    )

    if not meeting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meeting not found",
        )

    try:
        participant = join_meeting(
            db=db,
            meeting=meeting,
            data=data,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    return participant


@router.post(
    "/{meeting_code}/leave",
    response_model=ParticipantOut,
)
def leave(
    meeting_code: str,
    token: str,
    db: Session = Depends(get_db),
):
    meeting = get_meeting_by_code(
        db=db,
        meeting_code=meeting_code,
    )

    if not meeting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meeting not found",
        )

    participant = get_participant_by_token(
        db=db,
        token=token,
    )

    if not participant or participant.meeting_id != meeting.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Participant not found",
        )

    return leave_meeting(
        db=db,
        participant=participant,
    )


@router.get(
    "/{meeting_code}/participants",
    response_model=list[ParticipantOut],
)
def participants(
    meeting_code: str,
    db: Session = Depends(get_db),
):
    meeting = get_meeting_by_code(
        db=db,
        meeting_code=meeting_code,
    )

    if not meeting:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Meeting not found",
        )

    return get_active_participants(
        db=db,
        meeting_id=meeting.id,
    )