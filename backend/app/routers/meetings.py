from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.deps import get_db
from app.models import User
from app.schemas import (
	InstantMeetingCreate,
	MeetingCreate,
	MeetingOut,
	MeetingUpdate,
)
from app.services.meeting_service import (
	create_instant_meeting,
	create_scheduled_meeting,
	end_meeting,
	get_meeting_by_code,
	start_meeting,
	update_meeting,
)

router = APIRouter(
	prefix="/api/meetings",
	tags=["meetings"],
)


def get_demo_user(db: Session) -> User:
	user = db.query(User).first()

	if user:
		return user

	user = User(
		name="Demo User",
		email="demo@example.com",
		avatar_color="#6366f1",
	)

	db.add(user)
	db.commit()
	db.refresh(user)

	return user


@router.post(
	"/instant",
	response_model=MeetingOut,
	status_code=status.HTTP_201_CREATED,
)
def create_instant(
	data: InstantMeetingCreate,
	db: Session = Depends(get_db),
):
	host = get_demo_user(db)

	meeting = create_instant_meeting(
		db=db,
		host=host,
		data=data,
	)

	return meeting


@router.post(
	"",
	response_model=MeetingOut,
	status_code=status.HTTP_201_CREATED,
)
def create_scheduled(
	data: MeetingCreate,
	db: Session = Depends(get_db),
):
	host = get_demo_user(db)

	meeting = create_scheduled_meeting(
		db=db,
		host=host,
		data=data,
	)

	return meeting


@router.get(
	"/{meeting_code}",
	response_model=MeetingOut,
)
def get_meeting_details(
	meeting_code: int,
	db: Session = Depends(get_db),
):
	meeting = get_meeting_by_code(
		db=db,
		meeting_code=meeting_code,
	)
	
	print(meeting)

	if not meeting:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="Meeting not found",
		)

	return meeting


@router.patch(
	"/{meeting_code}",
	response_model=MeetingOut,
)
def update_meeting_details(
	meeting_code: int,
	data: MeetingUpdate,
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

	return update_meeting(
		db=db,
		meeting=meeting,
		data=data,
	)


@router.post(
	"/{meeting_code}/start",
	response_model=MeetingOut,
)
def start(
	meeting_code: int,
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
		return start_meeting(
			db=db,
			meeting=meeting,
		)
	except ValueError as e:
		raise HTTPException(
			status_code=status.HTTP_400_BAD_REQUEST,
			detail=str(e),
		)


@router.post(
	"/{meeting_code}/end",
	response_model=MeetingOut,
)
def end(
	meeting_code: int,
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

	return end_meeting(
		db=db,
		meeting=meeting,
	)