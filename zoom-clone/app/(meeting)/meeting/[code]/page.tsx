import ControlBar from "@/components/room/ControlBar";
import MeetingInfo from "@/components/room/MeetingInfo";
import ParticipantGrid from "@/components/room/ParticipantGrid";

const participants = [
  {
    id: "1",
    name: "Alex Morgan",
    initials: "AM",
    isSelf: false,
    isMuted: false,
    isVideoOn: true,
    isHost: true,
  },
  {
    id: "2",
    name: "John Smith",
    initials: "JS",
    isSelf: false,
    isMuted: true,
    isVideoOn: true,
    isHost: false,
  },
  {
    id: "3",
    name: "Sarah Lee",
    initials: "SL",
    isSelf: false,
    isMuted: false,
    isVideoOn: false,
    isHost: false,
  },
  {
    id: "4",
    name: "You",
    initials: "YO",
    isSelf: true,
    isMuted: false,
    isVideoOn: true,
    isHost: false,
  },
];

export default async function MeetingPage({
  params,
}: {
  params: Promise<{ code: string }>;
}) {
  const { code } = await params;

  return (
    <div className="flex h-screen flex-col overflow-hidden bg-[#18181B] text-white pt-12">
      <MeetingInfo
        title="Product Team Sync"
        meetingId={code}
      />

      <main className="flex min-h-0 flex-1 items-center justify-center p-4 pb-24">
        <ParticipantGrid participants={participants} />
      </main>

      <ControlBar participants={participants} />
    </div>
  );
}