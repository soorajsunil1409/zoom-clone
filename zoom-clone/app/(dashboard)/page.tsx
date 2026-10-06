import {
	Calendar1Icon,
	MonitorUp,
	Plus,
	Video,
} from "lucide-react";

import ActionTile from "@/components/home/ActionTile";
import ClockCard from "@/components/home/ClockCard";
import MeetingSection from "@/components/home/MeetingSection";

const upcomingMeetings = [
	{
		time: "10:00 AM – 11:00 AM",
		title: "Product Team Sync",
		meetingId: "123 4567 8901",
	},
	{
		time: "2:30 PM – 3:00 PM",
		title: "Project Review",
		meetingId: "987 6543 2109",
	},
	{
		time: "5:00 PM – 6:00 PM",
		title: "Client Discussion",
		meetingId: "456 7890 1234",
	},
];

const recentMeetings = [
	{
		time: "Yesterday · 4:00 PM",
		title: "Engineering Standup",
		meetingId: "321 6547 8901",
		duration: "42 min",
	},
	{
		time: "Oct 4 · 11:00 AM",
		title: "Design Review",
		meetingId: "555 1234 6789",
		duration: "58 min",
	},
];

export default function HomePage() {
	return (
		<div className="flex min-h-full flex-col gap-8 p-8 size-full">
			{/* <div className="flex flex-col gap-2">
				<span className="text-sm font-medium text-[#747487]">
					Tuesday, October 6
				</span>

				<h1 className="text-3xl font-semibold tracking-tight text-[#232333]">
					Good evening, Alex
				</h1>

				<p className="text-sm text-[#747487]">
					Start a meeting, join a call, or schedule your next one.
				</p>
			</div> */}

			<div className="flex gap-30 justify-center items-center h-full">
				<div className="grid grid-cols-2 gap-15 h-fit">
					<ActionTile
						title="New meeting"
						description="Start an instant meeting"
						icon={Video}
						variant="primary"
					/>

					<ActionTile
						title="Join"
						description="Join with a meeting ID"
						icon={Plus}
					/>

					<ActionTile
						title="Schedule"
						description="Plan a meeting"
						icon={Calendar1Icon}
					/>

					<ActionTile
						title="Share screen"
						description="Share your screen"
						icon={MonitorUp}
					/>
				</div>

				<div className="flex flex-col border rounded-3xl overflow-hidden">
					<ClockCard />

					<div className="flex flex-col gap-8 p-5">
						<MeetingSection
							title="Upcoming"
							meetings={upcomingMeetings}
							status="upcoming"
						/>

						<MeetingSection
							title="Recent"
							meetings={recentMeetings}
							status="recent"
						/>
					</div>
				</div>
			</div>
		</div>
	);
}