import VideoTile from "./VideoTile";

type Participant = {
  id: string;
  name: string;
  initials: string;
  isSelf: boolean;
  isMuted: boolean;
  isVideoOn: boolean;
  isHost: boolean;
};

type ParticipantGridProps = {
  participants: Participant[];
};

export default function ParticipantGrid({
  participants,
}: ParticipantGridProps) {
  const count = participants.length;

  const gridColumns =
    count === 1
      ? "grid-cols-1"
      : count === 2
        ? "grid-cols-1 sm:grid-cols-2"
        : count <= 4
          ? "grid-cols-1 sm:grid-cols-2"
          : "grid-cols-2 md:grid-cols-3";

  return (
    <div className="h-full min-h-0 w-full overflow-y-auto">
      <div
        className={`mx-auto grid w-full max-w-7xl content-start gap-2 p-2 sm:gap-3 sm:p-4 ${gridColumns}`}
      >
        {participants.map((participant) => (
          <VideoTile
            key={participant.id}
            {...participant}
          />
        ))}
      </div>
    </div>
  );
}