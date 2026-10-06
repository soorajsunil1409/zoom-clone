import MeetingRow from "./MeetingRow";

type Meeting = {
	time: string;
	title: string;
	meetingId: string;
	duration?: string;
};

type MeetingSectionProps = {
	title: string;
	meetings: Meeting[];
	status: "upcoming" | "recent";
};

export default function MeetingSection({
	title,
	meetings,
	status,
}: MeetingSectionProps) {
	return (
		<div className="flex flex-col gap-3">
			<div className="flex items-center justify-between px-1">
				<h2 className="text-lg font-semibold text-[#232333]">
					{title}
				</h2>

				<button className="text-sm font-medium text-[#0B5CFF]">
					View all
				</button>
			</div>

			<div className="flex max-h-40 flex-col overflow-y-auto rounded-xl border border-[#E8E8EF] bg-white">
				{meetings.map((meeting) => (
					<MeetingRow
						key={`${meeting.meetingId}-${meeting.time}`}
						{...meeting}
						status={status}
					/>
				))}
			</div>
		</div>
	);
}