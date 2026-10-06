import {
  CalendarDays,
  Home,
  LayoutGrid,
  Settings,
  Users,
  Video,
} from "lucide-react";

const items = [
  {
    label: "Home",
    icon: Home,
    active: true,
  },
  {
    label: "Meetings",
    icon: Video,
    active: false,
  },
];

const disabledItems = [
  {
    label: "Calendar",
    icon: CalendarDays,
  },
  {
    label: "Team Chat",
    icon: Users,
  },
  {
    label: "Apps",
    icon: LayoutGrid,
  },
  {
    label: "Settings",
    icon: Settings,
  },
];

export default function Sidebar() {
  return (
    <aside className="flex w-60 shrink-0 flex-col gap-6 border-r border-[#E8E8EF] bg-white p-4">
      <nav className="flex flex-col gap-1">
        {items.map((item) => {
          const Icon = item.icon;

          return (
            <button
              key={item.label}
              className={`flex h-11 items-center gap-3 rounded-lg px-4 text-sm font-medium ${
                item.active
                  ? "bg-[#EEF4FF] text-[#0B5CFF]"
                  : "text-[#747487] hover:bg-[#F7F7FA] hover:text-[#232333]"
              }`}
            >
              <Icon size={19} />
              <span>{item.label}</span>
            </button>
          );
        })}
      </nav>

      <div className="flex flex-col gap-1">
        {disabledItems.map((item) => {
          const Icon = item.icon;

          return (
            <button
              key={item.label}
              disabled
              className="flex h-11 cursor-not-allowed items-center gap-3 rounded-lg px-4 text-sm text-[#B4B4C0]"
              title="Not part of this demo"
            >
              <Icon size={19} />
              <span>{item.label}</span>
            </button>
          );
        })}
      </div>
    </aside>
  );
}