"use client";

import { useEffect, useState } from "react";
import { Clock } from "lucide-react";

export default function ClockCard() {
  const [time, setTime] = useState("");

  useEffect(() => {
    const update = () => {
      setTime(
        new Intl.DateTimeFormat("en-IN", {
          hour: "numeric",
          minute: "2-digit",
          hour12: true,
        }).format(new Date())
      );
    };

    update();

    const interval = setInterval(update, 1000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="flex min-h-36 flex-col justify-between bg-[rgb(54,69,79)] p-6 text-white">
      <div className="flex items-center gap-2 text-white/60">
        <Clock size={18} />
        <span className="text-sm">Your local time</span>
      </div>

      <div className="flex flex-col gap-1">
        <span className="text-4xl font-semibold tracking-tight">
          {time || "--:--"}
        </span>

        <span className="text-sm text-white/60">
          Chennai, India
        </span>
      </div>
    </div>
  );
}