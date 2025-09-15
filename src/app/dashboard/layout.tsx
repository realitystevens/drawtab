import DashboardLayout from '@/components/DashboardLayout'
import { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'Dashboard | Drawtab',
  description: 'Manage your automated flyer campaigns and view analytics.',
}

export default function DashboardLayoutWrapper({
  children,
}: {
  children: React.ReactNode
}) {
  return <DashboardLayout>{children}</DashboardLayout>
}
