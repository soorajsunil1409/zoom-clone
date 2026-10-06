from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.config import settings
from app.models import (
    Meeting,
    MeetingStatus,
    Participant,
    ParticipantRole,
    ParticipantStatus,
)
from app.schemas import JoinRequest
from app.utils import generate_token


def get_active_participants(
    db: Session,
    meeting_id: int,
) -> list[Participant]:
    return (
        db.query(Participant)
        .filter(
            Participant.meeting_id == meeting_id,
            Participant.status == ParticipantStatus.joined,
        )
        .all()
    )


def get_participant_by_token(
    db: Session,
    token: str,
) -> Participant | None:
    return (
        db.query(Participant)
        .filter(Participant.token == token)
        .first()
    )


def join_meeting(
    db: Session,
    meeting: Meeting,
    data: JoinRequest,
) -> Participant:
    if meeting.status == MeetingStatus.ended:
        raise ValueError("Meeting has ended")

    active = get_active_participants(db, meeting.id)

    if len(active) >= settings.max_participants:
        raise ValueError("Meeting is full")

    host_exists = any(
        participant.role == ParticipantRole.host
        for participant in active
    )

    role = ParticipantRole.participant

    if not host_exists or data.as_host:
        role = ParticipantRole.host

    participant = Participant(
        meeting_id=meeting.id,
        display_name=data.display_name,
        role=role,
        status=ParticipantStatus.joined,
        token=generate_token(),
        is_muted=data.is_muted,
        is_video_on=data.is_video_on,
        is_screen_sharing=False,
        joined_at=datetime.now(timezone.utc),
    )

    db.add(participant)
    db.commit()
    db.refresh(participant)

    return participant


def leave_meeting(
    db: Session,
    participant: Participant,
) -> Participant:
    if participant.status != ParticipantStatus.joined:
        return participant

    participant.status = ParticipantStatus.left
    participant.left_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(participant)

    return participant


def remove_participant(
    db: Session,
    participant: Participant,
) -> Participant:
    participant.status = ParticipantStatus.removed
    participant.left_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(participant)

    return participant


def update_media_state(
    db: Session,
    participant: Participant,
    is_muted: bool | None = None,
    is_video_on: bool | None = None,
    is_screen_sharing: bool | None = None,
) -> Participant:
    if is_muted is not None:
        participant.is_muted = is_muted

    if is_video_on is not None:
        participant.is_video_on = is_video_on

    if is_screen_sharing is not None:
        participant.is_screen_sharing = is_screen_sharing

    db.commit()
    db.refresh(participant)

    return participant


def mute_all(
    db: Session,
    meeting_id: int,
    exclude_participant_id: int | None = None,
) -> int:
    query = db.query(Participant).filter(
        Participant.meeting_id == meeting_id,
        Participant.status == ParticipantStatus.joined,
    )

    if exclude_participant_id is not None:
        query = query.filter(
            Participant.id != exclude_participant_id
        )

    participants = query.all()

    for participant in participants:
        participant.is_muted = True

    db.commit()

    return len(participants)