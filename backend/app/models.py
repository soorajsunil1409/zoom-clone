from datetime import datetime, timezone
from enum import Enum

from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    Enum as SAEnum,
    ForeignKey,
    Index,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class MeetingType(str, Enum):
    instant = "instant"
    scheduled = "scheduled"


class MeetingStatus(str, Enum):
    scheduled = "scheduled"
    live = "live"
    ended = "ended"


class ParticipantRole(str, Enum):
    host = "host"
    participant = "participant"


class ParticipantStatus(str, Enum):
    joined = "joined"
    left = "left"
    removed = "removed"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
    )

    avatar_color: Mapped[str | None] = mapped_column(
        String(20),
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    meetings: Mapped[list["Meeting"]] = relationship(
        back_populates="host",
        cascade="all, delete-orphan",
    )

    participants: Mapped[list["Participant"]] = relationship(
        back_populates="user",
    )


class Meeting(Base):
    __tablename__ = "meetings"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    meeting_code: Mapped[str] = mapped_column(
        String(11),
        unique=True,
        nullable=False,
        index=True,
    )

    host_id: Mapped[int] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    title: Mapped[str] = mapped_column(
        String(200),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
    )

    type: Mapped[MeetingType] = mapped_column(
        SAEnum(MeetingType),
        nullable=False,
    )

    status: Mapped[MeetingStatus] = mapped_column(
        SAEnum(MeetingStatus),
        nullable=False,
        default=MeetingStatus.scheduled,
    )

    start_time: Mapped[datetime | None] = mapped_column(
        DateTime,
    )

    duration_minutes: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=60,
    )

    timezone: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    passcode: Mapped[str] = mapped_column(
        String(6),
        nullable=False,
    )

    waiting_room: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    mute_on_entry: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    started_at: Mapped[datetime | None] = mapped_column(
        DateTime,
    )

    ended_at: Mapped[datetime | None] = mapped_column(
        DateTime,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    host: Mapped["User"] = relationship(
        back_populates="meetings",
    )

    participants: Mapped[list["Participant"]] = relationship(
        back_populates="meeting",
        cascade="all, delete-orphan",
    )

    chat_messages: Mapped[list["ChatMessage"]] = relationship(
        back_populates="meeting",
        cascade="all, delete-orphan",
    )

    @property
    def formatted_code(self) -> str:
        code = self.meeting_code

        if len(code) != 11:
            return code

        return f"{code[:3]} {code[3:7]} {code[7:]}"

    @property
    def invite_link(self) -> str:
        from .config import settings

        return (
            f"{settings.frontend_url}/j/"
            f"{self.meeting_code}?pwd={self.passcode}"
        )

    __table_args__ = (
        Index(
            "ix_meetings_host_status_start",
            "host_id",
            "status",
            "start_time",
        ),
        CheckConstraint(
            "duration_minutes > 0",
            name="ck_meetings_duration_positive",
        ),
    )


class Participant(Base):
    __tablename__ = "participants"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    meeting_id: Mapped[int] = mapped_column(
        ForeignKey(
            "meetings.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    user_id: Mapped[int | None] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="SET NULL",
        ),
    )

    display_name: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    role: Mapped[ParticipantRole] = mapped_column(
        SAEnum(ParticipantRole),
        nullable=False,
        default=ParticipantRole.participant,
    )

    status: Mapped[ParticipantStatus] = mapped_column(
        SAEnum(ParticipantStatus),
        nullable=False,
        default=ParticipantStatus.joined,
    )

    token: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True,
    )

    is_muted: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    is_video_on: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    is_screen_sharing: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=False,
    )

    joined_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    left_at: Mapped[datetime | None] = mapped_column(
        DateTime,
    )

    meeting: Mapped["Meeting"] = relationship(
        back_populates="participants",
    )

    user: Mapped["User | None"] = relationship(
        back_populates="participants",
    )

    chat_messages: Mapped[list["ChatMessage"]] = relationship(
        back_populates="participant",
    )

    __table_args__ = (
        Index(
            "ix_participants_meeting_status",
            "meeting_id",
            "status",
        ),
    )


class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    meeting_id: Mapped[int] = mapped_column(
        ForeignKey(
            "meetings.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    participant_id: Mapped[int] = mapped_column(
        ForeignKey(
            "participants.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    content: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
    )

    sent_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    meeting: Mapped["Meeting"] = relationship(
        back_populates="chat_messages",
    )

    participant: Mapped["Participant"] = relationship(
        back_populates="chat_messages",
    )

    __table_args__ = (
        Index(
            "ix_chat_messages_meeting_id",
            "meeting_id",
            "id",
        ),
    )