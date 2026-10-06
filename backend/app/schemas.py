from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, Field, field_validator


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


class UserOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: str
    avatar_color: str | None = None


class ParticipantOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    display_name: str
    role: ParticipantRole
    status: ParticipantStatus
    is_muted: bool
    is_video_on: bool
    is_screen_sharing: bool
    joined_at: datetime
    left_at: datetime | None = None


class MeetingCreate(BaseModel):
    title: str
    description: str | None = None
    start_time: datetime
    duration_minutes: int = Field(60, ge=1, le=1440)
    timezone: str
    waiting_room: bool = False
    mute_on_entry: bool = False

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Title cannot be empty")
        return value


class InstantMeetingCreate(BaseModel):
    title: str | None = None
    description: str | None = None
    duration_minutes: int = Field(60, ge=1, le=1440)
    timezone: str = "UTC"
    waiting_room: bool = False
    mute_on_entry: bool = False

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str | None) -> str | None:
        if value is None:
            return value

        value = value.strip()

        if not value:
            raise ValueError("Title cannot be empty")

        return value


class MeetingUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    start_time: datetime | None = None
    duration_minutes: int | None = Field(None, ge=1, le=1440)
    timezone: str | None = None
    waiting_room: bool | None = None
    mute_on_entry: bool | None = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, value: str | None) -> str | None:
        if value is None:
            return value

        value = value.strip()

        if not value:
            raise ValueError("Title cannot be empty")

        return value


class MeetingOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    meeting_code: str
    formatted_code: str
    title: str
    description: str | None
    type: MeetingType
    status: MeetingStatus
    start_time: datetime | None
    duration_minutes: int
    timezone: str
    passcode: str
    invite_link: str
    waiting_room: bool
    mute_on_entry: bool
    host: UserOut
    started_at: datetime | None
    ended_at: datetime | None
    created_at: datetime


class JoinRequest(BaseModel):
    display_name: str = Field(min_length=1, max_length=50)
    as_host: bool = False
    is_muted: bool = False
    is_video_on: bool = True

    @field_validator("display_name")
    @classmethod
    def validate_display_name(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Display name cannot be empty")

        return value


class JoinResponse(ParticipantOut):
    token: str


class ChatMessageOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    participant_id: int
    display_name: str
    content: str
    sent_at: datetime


class MuteAllOut(BaseModel):
    muted: int