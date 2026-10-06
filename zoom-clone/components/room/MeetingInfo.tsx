"use client";

import { Copy, Info } from "lucide-react";
import { useEffect, useState } from "react";

type MeetingInfoProps = {
  title: string;
  meetingId: string;
};

export default function MeetingInfo({
  title,
  meetingId,
}: MeetingInfoProps) {
  const [elapsed, setElapsed] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setElapsed((value) => value + 1);
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  const minutes = Math.floor(elapsed / 60)
    .toString()
    .padStart(2, "0");

  const seconds = (elapsed % 60)
    .toString()
    .padStart(2, "0");

  return (
    <div className="absolute left-5 top-5 z-20 flex items-center gap-3">
      <button className="flex h-9 w-9 items-center justify-center rounded-lg bg-black/50 text-white backdrop-blur-sm hover:bg-black/70">
        <Info size={17} />
      </button>

      <div className="flex flex-col gap-0.5">
        <span className="text-sm font-medium text-white">
          {title}
        </span>

        <div className="flex items-center gap-2 text-xs text-[#A1A1AA]">
          <span>{meetingId}</span>
          <span>•</span>
          <span>
            {minutes}:{seconds}
          </span>

          <button className="text-[#D4D4D8] hover:text-white">
            <Copy size={13} />
          </button>
        </div>
      </div>
    </div>
  );
}