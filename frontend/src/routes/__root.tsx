import { AppLayout } from '@/components/layout'
import { Link, Outlet, createRootRoute } from '@tanstack/react-router'

export const Route = createRootRoute({
  component: RootLayout,
})

function RootLayout() {
  return (
    <div className="w-full h-screen bg-background flex   justify-center">
        <div className="overflow-hidden w-full flex   justify-center">
            <Outlet />
        </div>
    </div>
  )
}
