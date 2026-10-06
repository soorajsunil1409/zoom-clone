import type { LucideIcon } from "lucide-react";

type ActionTileProps = {
	title: string;
	description: string;
	icon: LucideIcon;
	variant?: "primary" | "default";
};

export default function ActionTile({
	title,
	description,
	icon: Icon,
	variant = "default",
}: ActionTileProps) {
	const primary = variant === "primary";

	return (
		<div className="flex flex-col gap-3">
			<button
				className={`flex size-25 items-center justify-center rounded-4xl text-white transition-all hover:scale-105 ${primary
						? "bg-zoom-orange hover:bg-zoom-orange-hover"
						: "bg-zoom-blue hover:bg-zoom-blue-hover"
					}`}
			>
				<Icon size={28} strokeWidth={2.2} className="size-full p-7" />
			</button>

			<div className="flex flex-col gap-1">
				<span className="text-md text-zoom-text text-center">
					{title}
				</span>
			</div>
		</div>
	);
}