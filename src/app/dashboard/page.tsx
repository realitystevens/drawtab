import { Metadata } from 'next'
import { 
  ChartBarIcon, 
  DocumentIcon, 
  UsersIcon, 
  CalendarIcon 
} from '@heroicons/react/24/outline'

export const metadata: Metadata = {
  title: 'Dashboard | Drawtab',
  description: 'Manage your automated flyer campaigns and view analytics.',
}

const stats = [
  { name: 'Total Templates', value: '12', icon: DocumentIcon },
  { name: 'Active Contacts', value: '156', icon: UsersIcon },
  { name: 'Scheduled Events', value: '24', icon: CalendarIcon },
  { name: 'Emails Sent', value: '89', icon: ChartBarIcon },
]

const recentActivity = [
  {
    id: 1,
    type: 'Email Sent',
    description: 'Birthday flyer sent to John Doe',
    time: '2 hours ago',
  },
  {
    id: 2,
    type: 'Template Upload',
    description: 'New anniversary template uploaded',
    time: '4 hours ago',
  },
  {
    id: 3,
    type: 'Event Scheduled',
    description: 'Sarah\'s birthday scheduled for next month',
    time: '1 day ago',
  },
  {
    id: 4,
    type: 'Contact Added',
    description: '5 new contacts imported',
    time: '2 days ago',
  },
]

const upcomingEvents = [
  {
    id: 1,
    name: 'John Doe',
    type: 'Birthday',
    date: 'Tomorrow',
    template: 'Birthday Template #1',
  },
  {
    id: 2,
    name: 'Sarah Johnson',
    type: 'Work Anniversary',
    date: 'In 3 days',
    template: 'Anniversary Template #2',
  },
  {
    id: 3,
    name: 'Mike Wilson',
    type: 'Birthday',
    date: 'Next week',
    template: 'Birthday Template #3',
  },
]

export default function DashboardPage() {
  return (
    <div className="py-6">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 md:px-8">
        <h1 className="text-2xl font-semibold text-gray-900">Dashboard</h1>
      </div>
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 md:px-8">
        {/* Stats */}
        <div className="mt-8">
          <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
            {stats.map((item) => (
              <div key={item.name} className="bg-white overflow-hidden shadow rounded-lg">
                <div className="p-5">
                  <div className="flex items-center">
                    <div className="flex-shrink-0">
                      <item.icon className="h-6 w-6 text-gray-400" />
                    </div>
                    <div className="ml-5 w-0 flex-1">
                      <dl>
                        <dt className="text-sm font-medium text-gray-500 truncate">
                          {item.name}
                        </dt>
                        <dd className="text-lg font-medium text-gray-900">
                          {item.value}
                        </dd>
                      </dl>
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Two column layout */}
        <div className="mt-8 grid grid-cols-1 gap-6 lg:grid-cols-2">
          {/* Recent Activity */}
          <div className="bg-white shadow rounded-lg">
            <div className="px-6 py-4 border-b border-gray-200">
              <h3 className="text-lg font-medium text-gray-900">Recent Activity</h3>
            </div>
            <div className="divide-y divide-gray-200">
              {recentActivity.map((activity) => (
                <div key={activity.id} className="px-6 py-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm font-medium text-gray-900">
                        {activity.type}
                      </p>
                      <p className="text-sm text-gray-500">
                        {activity.description}
                      </p>
                    </div>
                    <div className="text-sm text-gray-500">
                      {activity.time}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Upcoming Events */}
          <div className="bg-white shadow rounded-lg">
            <div className="px-6 py-4 border-b border-gray-200">
              <h3 className="text-lg font-medium text-gray-900">Upcoming Events</h3>
            </div>
            <div className="divide-y divide-gray-200">
              {upcomingEvents.map((event) => (
                <div key={event.id} className="px-6 py-4">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm font-medium text-gray-900">
                        {event.name}
                      </p>
                      <p className="text-sm text-gray-500">
                        {event.type} • {event.template}
                      </p>
                    </div>
                    <div className="text-sm text-gray-500">
                      {event.date}
                    </div>
                  </div>
                </div>
              ))}
            </div>
            <div className="px-6 py-3 bg-gray-50 text-right">
              <a href="/dashboard/events" className="text-sm font-medium text-primary-600 hover:text-primary-500">
                View all events →
              </a>
            </div>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="mt-8 bg-white shadow rounded-lg">
          <div className="px-6 py-4 border-b border-gray-200">
            <h3 className="text-lg font-medium text-gray-900">Quick Actions</h3>
          </div>
          <div className="px-6 py-4">
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
              <a
                href="/dashboard/templates/new"
                className="relative group bg-white p-6 focus-within:ring-2 focus-within:ring-inset focus-within:ring-primary-500 rounded-lg border border-gray-200 hover:border-gray-300"
              >
                <div>
                  <span className="rounded-lg inline-flex p-3 bg-primary-50 text-primary-600 ring-4 ring-white">
                    <DocumentIcon className="h-6 w-6" />
                  </span>
                </div>
                <div className="mt-4">
                  <h3 className="text-lg font-medium">
                    <span className="absolute inset-0" />
                    Upload Template
                  </h3>
                  <p className="mt-2 text-sm text-gray-500">
                    Add a new PNG template for your flyers
                  </p>
                </div>
              </a>

              <a
                href="/dashboard/contacts"
                className="relative group bg-white p-6 focus-within:ring-2 focus-within:ring-inset focus-within:ring-primary-500 rounded-lg border border-gray-200 hover:border-gray-300"
              >
                <div>
                  <span className="rounded-lg inline-flex p-3 bg-primary-50 text-primary-600 ring-4 ring-white">
                    <UsersIcon className="h-6 w-6" />
                  </span>
                </div>
                <div className="mt-4">
                  <h3 className="text-lg font-medium">
                    <span className="absolute inset-0" />
                    Add Contacts
                  </h3>
                  <p className="mt-2 text-sm text-gray-500">
                    Import or add new contacts manually
                  </p>
                </div>
              </a>

              <a
                href="/dashboard/events"
                className="relative group bg-white p-6 focus-within:ring-2 focus-within:ring-inset focus-within:ring-primary-500 rounded-lg border border-gray-200 hover:border-gray-300"
              >
                <div>
                  <span className="rounded-lg inline-flex p-3 bg-primary-50 text-primary-600 ring-4 ring-white">
                    <CalendarIcon className="h-6 w-6" />
                  </span>
                </div>
                <div className="mt-4">
                  <h3 className="text-lg font-medium">
                    <span className="absolute inset-0" />
                    Schedule Event
                  </h3>
                  <p className="mt-2 text-sm text-gray-500">
                    Create a new birthday or anniversary event
                  </p>
                </div>
              </a>

              <a
                href="/dashboard/calendar"
                className="relative group bg-white p-6 focus-within:ring-2 focus-within:ring-inset focus-within:ring-primary-500 rounded-lg border border-gray-200 hover:border-gray-300"
              >
                <div>
                  <span className="rounded-lg inline-flex p-3 bg-primary-50 text-primary-600 ring-4 ring-white">
                    <ChartBarIcon className="h-6 w-6" />
                  </span>
                </div>
                <div className="mt-4">
                  <h3 className="text-lg font-medium">
                    <span className="absolute inset-0" />
                    View Calendar
                  </h3>
                  <p className="mt-2 text-sm text-gray-500">
                    See all upcoming events in calendar view
                  </p>
                </div>
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
