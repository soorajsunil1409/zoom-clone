import { ChevronRight } from "lucide-react";

type MeetingRowProps = {
  time: string;
  title: string;
  meetingId: string;
  status: "upcoming" | "recent";
  duration?: string;
};

export default function MeetingRow({
  time,
  title,
  meetingId,
  status,
  duration,
}: MeetingRowProps) {
  return (
    <div className="flex w-full flex-col gap-4 border-b border-[#E8E8EF] px-4 py-4 last:border-b-0 sm:px-5 sm:py-5 md:flex-row md:items-center md:justify-between md:gap-6">
      <div className="flex min-w-0 flex-1 items-start gap-4 sm:gap-5">
        <div className="flex w-28 shrink-0 flex-col gap-1 sm:w-36 lg:w-45">
          <span className="truncate text-sm font-semibold text-[#232333]">
            {time}
          </span>

          <span className="text-xs text-[#747487]">
            {status === "upcoming" ? "Upcoming" : "Completed"}
          </span>
        </div>

        <div className="flex min-w-0 flex-1 flex-col gap-1">
          <span className="truncate text-sm font-semibold text-[#232333]">
            {title}
          </span>

          <span className="truncate text-xs text-[#747487]">
            Meeting ID: {meetingId}
          </span>
        </div>
      </div>

      {status === "upcoming" ? (
        <button className="flex w-full shrink-0 items-center justify-center gap-2 rounded-lg bg-[#0B5CFF] px-4 py-2 text-sm font-semibold text-white transition-colors hover:bg-[#084dcc] md:w-auto">
          Start
          <ChevronRight size={16} />
        </button>
      ) : (
        <span className="shrink-0 text-sm font-medium text-[#747487]">
          {duration}
        </span>
      )}
    </div>
  );
}