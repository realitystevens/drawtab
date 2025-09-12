import { Metadata } from 'next'
import Link from 'next/link'
import { PlusIcon, PhotoIcon, EyeIcon, PencilIcon, TrashIcon } from '@heroicons/react/24/outline'

export const metadata: Metadata = {
  title: 'Templates - Drawtab',
  description: 'Manage your flyer templates and create new ones.',
}

const templates = [
  {
    id: 1,
    name: 'Birthday Celebration',
    category: 'Birthday',
    preview: '/templates/birthday-1.png',
    hotspots: 3,
    usageCount: 12,
    createdAt: '2025-01-15',
  },
  {
    id: 2,
    name: 'Work Anniversary',
    category: 'Anniversary',
    preview: '/templates/anniversary-1.png',
    hotspots: 4,
    usageCount: 8,
    createdAt: '2025-01-10',
  },
  {
    id: 3,
    name: 'Elegant Birthday',
    category: 'Birthday',
    preview: '/templates/birthday-2.png',
    hotspots: 2,
    usageCount: 15,
    createdAt: '2025-01-05',
  },
  {
    id: 4,
    name: 'Wedding Anniversary',
    category: 'Anniversary',
    preview: '/templates/anniversary-2.png',
    hotspots: 5,
    usageCount: 6,
    createdAt: '2024-12-20',
  },
]

const categories = ['All', 'Birthday', 'Anniversary', 'Promotion', 'Holiday']

export default function TemplatesPage() {
  return (
    <div className="py-6">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 md:px-8">
        {/* Header */}
        <div className="md:flex md:items-center md:justify-between">
          <div className="min-w-0 flex-1">
            <h1 className="text-2xl font-semibold text-gray-900">Templates</h1>
            <p className="mt-1 text-sm text-gray-500">
              Manage your flyer templates and create new ones
            </p>
          </div>
          <div className="mt-4 flex md:mt-0 md:ml-4">
            <Link
              href="/dashboard/templates/new"
              className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
            >
              <PlusIcon className="mr-2 h-4 w-4" />
              New Template
            </Link>
          </div>
        </div>

        {/* Filters */}
        <div className="mt-8">
          <div className="sm:hidden">
            <label htmlFor="tabs" className="sr-only">
              Select a category
            </label>
            <select
              id="tabs"
              name="tabs"
              className="block w-full focus:ring-primary-500 focus:border-primary-500 border-gray-300 rounded-md"
              defaultValue="All"
            >
              {categories.map((category) => (
                <option key={category}>{category}</option>
              ))}
            </select>
          </div>
          <div className="hidden sm:block">
            <nav className="flex space-x-8" aria-label="Tabs">
              {categories.map((category, index) => (
                <button
                  key={category}
                  className={`${
                    index === 0
                      ? 'border-primary-500 text-primary-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  } whitespace-nowrap py-2 px-1 border-b-2 font-medium text-sm`}
                >
                  {category}
                </button>
              ))}
            </nav>
          </div>
        </div>

        {/* Templates Grid */}
        <div className="mt-8 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
          {templates.map((template) => (
            <div
              key={template.id}
              className="group relative bg-white rounded-lg shadow hover:shadow-md transition-shadow duration-200"
            >
              {/* Template Preview */}
              <div className="aspect-w-3 aspect-h-4 bg-gray-200 rounded-t-lg overflow-hidden">
                <div className="w-full h-48 bg-gradient-to-br from-primary-100 to-primary-200 flex items-center justify-center">
                  <PhotoIcon className="h-12 w-12 text-primary-400" />
                  <span className="ml-2 text-primary-600 font-medium">
                    {template.name}
                  </span>
                </div>
                
                {/* Overlay actions */}
                <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-40 transition-all duration-200 flex items-center justify-center opacity-0 group-hover:opacity-100">
                  <div className="flex space-x-2">
                    <button className="p-2 bg-white rounded-full text-gray-600 hover:text-primary-600">
                      <EyeIcon className="h-5 w-5" />
                    </button>
                    <button className="p-2 bg-white rounded-full text-gray-600 hover:text-primary-600">
                      <PencilIcon className="h-5 w-5" />
                    </button>
                    <button className="p-2 bg-white rounded-full text-gray-600 hover:text-red-600">
                      <TrashIcon className="h-5 w-5" />
                    </button>
                  </div>
                </div>
              </div>

              {/* Template Info */}
              <div className="p-4">
                <h3 className="text-lg font-medium text-gray-900 truncate">
                  {template.name}
                </h3>
                <p className="text-sm text-gray-500">{template.category}</p>
                
                <div className="mt-2 flex items-center justify-between text-sm text-gray-500">
                  <span>{template.hotspots} hotspots</span>
                  <span>Used {template.usageCount} times</span>
                </div>
                
                <div className="mt-3">
                  <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-gray-100 text-gray-800">
                    {template.category}
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Empty State (when no templates) */}
        {templates.length === 0 && (
          <div className="text-center py-12">
            <PhotoIcon className="mx-auto h-12 w-12 text-gray-400" />
            <h3 className="mt-2 text-sm font-medium text-gray-900">No templates</h3>
            <p className="mt-1 text-sm text-gray-500">
              Get started by creating your first flyer template.
            </p>
            <div className="mt-6">
              <Link
                href="/dashboard/templates/new"
                className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary-600 hover:bg-primary-700"
              >
                <PlusIcon className="mr-2 h-4 w-4" />
                New Template
              </Link>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
