from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.config import settings
from app.models import Meeting, MeetingStatus, MeetingType, User
from app.schemas import MeetingCreate, MeetingUpdate, InstantMeetingCreate
from app.utils import (
    build_invite_link,
    format_meeting_code,
    generate_meeting_code,
    generate_passcode,
)


def create_instant_meeting(
    db: Session,
    host: User,
    data: InstantMeetingCreate | None = None,
) -> Meeting:
    title = "Instant Meeting"

    if data and data.title:
        title = data.title

    meeting = Meeting(
        meeting_code=generate_meeting_code(db),
        host_id=host.id,
        title=title,
        description=data.description if data else None,
        type=MeetingType.instant,
        status=MeetingStatus.live,
        start_time=datetime.now(timezone.utc),
        duration_minutes=data.duration_minutes if data else 60,
        timezone=data.timezone if data else "UTC",
        passcode=generate_passcode(),
        waiting_room=data.waiting_room if data else False,
        mute_on_entry=data.mute_on_entry if data else False,
        started_at=datetime.now(timezone.utc),
    )

    db.add(meeting)
    db.commit()
    db.refresh(meeting)

    return meeting


def create_scheduled_meeting(
    db: Session,
    host: User,
    data: MeetingCreate,
) -> Meeting:
    meeting = Meeting(
        meeting_code=generate_meeting_code(db),
        host_id=host.id,
        title=data.title,
        description=data.description,
        type=MeetingType.scheduled,
        status=MeetingStatus.scheduled,
        start_time=data.start_time,
        duration_minutes=data.duration_minutes,
        timezone=data.timezone,
        passcode=generate_passcode(),
        waiting_room=data.waiting_room,
        mute_on_entry=data.mute_on_entry,
    )

    db.add(meeting)
    db.commit()
    db.refresh(meeting)

    return meeting


def get_meeting(
    db: Session,
    meeting_id: int,
) -> Meeting | None:
    return db.query(Meeting).filter(
        Meeting.id == meeting_id
    ).first()


def get_meeting_by_code(
    db: Session,
    meeting_code: str,
) -> Meeting | None:
    return db.query(Meeting).filter(
        Meeting.meeting_code == meeting_code
    ).first()


def update_meeting(
    db: Session,
    meeting: Meeting,
    data: MeetingUpdate,
) -> Meeting:
    values = data.model_dump(exclude_unset=True)

    for key, value in values.items():
        setattr(meeting, key, value)

    db.commit()
    db.refresh(meeting)

    return meeting


def start_meeting(
    db: Session,
    meeting: Meeting,
) -> Meeting:
    if meeting.status == MeetingStatus.ended:
        raise ValueError("Meeting has already ended")

    now = datetime.now(timezone.utc)

    meeting.status = MeetingStatus.live
    meeting.started_at = now

    db.commit()
    db.refresh(meeting)

    return meeting


def end_meeting(
    db: Session,
    meeting: Meeting,
) -> Meeting:
    if meeting.status == MeetingStatus.ended:
        return meeting

    now = datetime.now(timezone.utc)

    meeting.status = MeetingStatus.ended
    meeting.ended_at = now

    db.commit()
    db.refresh(meeting)

    return meeting


def get_invite_link(meeting: Meeting) -> str:
    return build_invite_link(
        settings.frontend_url,
        meeting.meeting_code,
        meeting.passcode,
    )


def meeting_to_dict(meeting: Meeting) -> dict:
    return {
        "id": meeting.id,
        "meeting_code": meeting.meeting_code,
        "formatted_code": format_meeting_code(
            meeting.meeting_code
        ),
        "title": meeting.title,
        "description": meeting.description,
        "type": meeting.type.value,
        "status": meeting.status.value,
        "start_time": meeting.start_time,
        "duration_minutes": meeting.duration_minutes,
        "timezone": meeting.timezone,
        "passcode": meeting.passcode,
        "invite_link": get_invite_link(meeting),
        "waiting_room": meeting.waiting_room,
        "mute_on_entry": meeting.mute_on_entry,
        "started_at": meeting.started_at,
        "ended_at": meeting.ended_at,
        "created_at": meeting.created_at,
    }