import {
  Bell,
  ChevronDown,
  Search,
  Settings,
} from "lucide-react";

export default function Header() {
  return (
    <header className="flex h-16 shrink-0 items-center justify-between border-b border-[#E8E8EF] bg-white px-6">
      <div className="flex items-center gap-8">
        <div className="flex items-center">
          <span className="text-2xl font-bold tracking-tight text-[#0B5CFF]">
            zoom
          </span>
        </div>

        <div className="flex h-10 w-72 items-center gap-3 rounded-full bg-[#F7F7FA] px-4 text-[#747487]">
          <Search size={18} />
          <span className="text-sm">Search</span>
        </div>
      </div>

      <div className="flex items-center gap-5">
        <button className="text-[#747487] transition-colors hover:text-[#232333]">
          <Settings size={20} />
        </button>

        <button className="relative text-[#747487] transition-colors hover:text-[#232333]">
          <Bell size={20} />

          <span className="absolute -right-1 -top-1 flex h-2 w-2 rounded-full bg-[#0B5CFF]" />
        </button>

        <div className="flex cursor-pointer items-center gap-2">
          <div className="flex h-9 w-9 items-center justify-center rounded-full bg-[#0B5CFF] text-sm font-semibold text-white">
            AM
          </div>

          <div className="hidden flex-col lg:flex">
            <span className="text-sm font-semibold text-[#232333]">
              Alex Morgan
            </span>
            <span className="text-xs text-[#747487]">
              Personal
            </span>
          </div>

          <ChevronDown size={16} className="text-[#747487]" />
        </div>
      </div>
    </header>
  );
}