"use client";

import {
	ChevronUp,
	MessageSquare,
	Mic,
	MoreHorizontal,
	MonitorUp,
	Users,
	Video,
	X,
} from "lucide-react";
import { useState } from "react";

type Participant = {
	id: string;
	name: string;
	initials: string;
	isSelf: boolean;
	isMuted: boolean;
	isVideoOn: boolean;
	isHost: boolean;
};

type ControlBarProps = {
	participants: Participant[];
};

export default function ControlBar({
	participants,
}: ControlBarProps) {
	const [showParticipants, setShowParticipants] = useState(false);

	return (
		<>
			{showParticipants && (
				<div className="absolute inset-x-0 bottom-0 top-0 z-30 flex justify-end">
					<div
						className="
        flex h-full w-full flex-col
        bg-[#18181B]
        shadow-2xl

        sm:w-[360px]
        sm:border-l sm:border-[#3F3F46]
      "
					>
						<div className="flex shrink-0 items-center justify-between border-b border-[#3F3F46] px-4 py-4 sm:px-5">
							<div className="flex min-w-0 flex-col gap-1">
								<span className="text-base font-semibold text-white">
									Participants
								</span>

								<span className="text-xs text-[#A1A1AA]">
									{participants.length} participants
								</span>
							</div>

							<button
								onClick={() => setShowParticipants(false)}
								className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg text-[#A1A1AA] transition-colors hover:bg-[#27272A] hover:text-white"
							>
								<X size={18} />
							</button>
						</div>

						<div className="flex min-h-0 flex-1 flex-col overflow-y-auto">
							{participants.map((participant) => (
								<div
									key={participant.id}
									className="flex shrink-0 items-center gap-3 border-b border-[#27272A] px-4 py-3 sm:px-5"
								>
									<div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full bg-zoom-blue text-xs font-semibold text-white">
										{participant.initials}
									</div>

									<div className="flex min-w-0 flex-1 flex-col gap-0.5">
										<span className="truncate text-sm font-medium text-white">
											{participant.name}
											{participant.isSelf && " (You)"}
										</span>

										{participant.isHost && (
											<span className="text-[11px] text-[#A1A1AA]">
												Host
											</span>
										)}
									</div>

									<div className="flex shrink-0 items-center gap-2">
										<Mic
											size={16}
											className={
												participant.isMuted
													? "text-[#F87171]"
													: "text-[#A1A1AA]"
											}
										/>

										<div
											className={`h-2 w-2 rounded-full ${participant.isVideoOn
													? "bg-zoom-success"
													: "bg-[#71717A]"
												}`}
										/>
									</div>
								</div>
							))}
						</div>
					</div>
				</div>
			)}

			<div className="absolute bottom-0 left-0 right-0 z-20 flex h-16 items-center justify-center px-2 sm:h-20 sm:px-4">
				<div className="flex max-w-full items-center gap-1 overflow-x-auto rounded-2xl bg-[#27272A] p-1.5 shadow-2xl sm:gap-2 sm:p-2">
					<button className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl text-[#D4D4D8] transition-colors hover:bg-[#3F3F46] hover:text-white sm:h-14 sm:w-16 sm:flex-col sm:gap-1">
						<Mic size={20} />
						<span className="hidden text-[11px] sm:block">
							Mute
						</span>
					</button>

					<button className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl text-[#D4D4D8] transition-colors hover:bg-[#3F3F46] hover:text-white sm:h-14 sm:w-16 sm:flex-col sm:gap-1">
						<Video size={20} />
						<span className="hidden text-[11px] sm:block">
							Video
						</span>
					</button>

					<button
						onClick={() =>
							setShowParticipants((current) => !current)
						}
						className={`flex h-12 w-12 shrink-0 items-center justify-center rounded-xl transition-colors sm:h-14 sm:w-16 sm:flex-col sm:gap-1 ${showParticipants
								? "bg-[#3F3F46] text-white"
								: "text-[#D4D4D8] hover:bg-[#3F3F46] hover:text-white"
							}`}
					>
						<Users size={20} />

						<span className="hidden text-[11px] sm:block">
							Participants
						</span>
					</button>

					<button className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl text-[#D4D4D8] transition-colors hover:bg-[#3F3F46] hover:text-white sm:h-14 sm:w-16 sm:flex-col sm:gap-1">
						<MessageSquare size={20} />

						<span className="hidden text-[11px] sm:block">
							Chat
						</span>
					</button>

					<button className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl text-[#D4D4D8] transition-colors hover:bg-[#3F3F46] hover:text-white sm:h-14 sm:w-16 sm:flex-col sm:gap-1">
						<MonitorUp size={20} />

						<span className="hidden text-[11px] sm:block">
							Share
						</span>
					</button>

					<button className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl text-[#D4D4D8] transition-colors hover:bg-[#3F3F46] hover:text-white sm:h-14 sm:w-16 sm:flex-col sm:gap-1">
						<MoreHorizontal size={20} />

						<span className="hidden text-[11px] sm:block">
							More
						</span>
					</button>

					<div className="mx-1 h-8 w-px shrink-0 bg-[#52525B]" />

					<button className="flex h-12 shrink-0 items-center gap-1 rounded-xl bg-zoom-danger px-3 text-sm font-medium text-white hover:bg-[#c92121] sm:px-4">
						<span className="hidden sm:block">
							End
						</span>

						<ChevronUp size={15} />
					</button>
				</div>
			</div>
		</>
	);
}