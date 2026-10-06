import Header from "@/components/layout/Header"
import Sidebar from "@/components/layout/Sidebar"

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <div className="flex flex-col bg-white size-full">
      <Header />

      <div className="flex size-full">
        <Sidebar />

        <main className="size-full">
          {children}
        </main>
      </div>
    </div>
  )
}