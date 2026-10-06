import { MicOff, User } from "lucide-react";

type VideoTileProps = {
  name: string;
  initials: string;
  isSelf: boolean;
  isMuted: boolean;
  isVideoOn: boolean;
  isHost: boolean;
};

export default function VideoTile({
  name,
  initials,
  isSelf,
  isMuted,
  isVideoOn,
  isHost,
}: VideoTileProps) {
  return (
    <div
      className={`relative flex aspect-video min-h-0 items-center justify-center overflow-hidden rounded-lg bg-[#27272A] ${
        isSelf ? "ring-2 ring-zoom-blue" : ""
      }`}
    >
      {isVideoOn ? (
        <div className="flex h-full w-full items-center justify-center bg-[#3F3F46]">
          <div className="flex h-20 w-20 items-center justify-center rounded-full bg-zoom-blue text-2xl font-semibold text-white">
            {initials}
          </div>
        </div>
      ) : (
        <div className="flex flex-col items-center gap-3">
          <div className="flex h-20 w-20 items-center justify-center rounded-full bg-[#3F3F46]">
            <User size={32} className="text-[#A1A1AA]" />
          </div>

          <span className="text-sm text-[#D4D4D8]">
            Camera off
          </span>
        </div>
      )}

      <div className="absolute bottom-3 left-3 flex items-center gap-2 rounded-md bg-black/60 px-2 py-1">
        {isMuted && (
          <MicOff
            size={14}
            className="text-[#F87171]"
          />
        )}

        <span className="text-xs font-medium text-white">
          {name}
          {isSelf ? " (You)" : ""}
        </span>

        {isHost && (
          <span className="text-[10px] text-[#A1A1AA]">
            Host
          </span>
        )}
      </div>
    </div>
  );
}