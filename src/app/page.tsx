import Link from 'next/link'
import { ChevronRightIcon, EnvelopeIcon, CalendarIcon, PhotoIcon } from '@heroicons/react/20/solid'

export default function HomePage() {
  return (
    <div className="min-h-screen bg-white">
      {/* Header */}
      <header className="relative bg-white">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between py-6 md:justify-start md:space-x-10">
            <div className="flex justify-start lg:w-0 lg:flex-1">
              <Link href="/" className="text-2xl font-bold text-primary-600">
                Drawtab
              </Link>
            </div>
            <div className="hidden items-center justify-end md:flex md:flex-1 lg:w-0">
              <Link
                href="/auth/login"
                className="whitespace-nowrap text-base font-medium text-gray-500 hover:text-gray-900"
              >
                Sign in
              </Link>
              <Link
                href="/auth/register"
                className="ml-8 inline-flex items-center justify-center whitespace-nowrap rounded-md border border-transparent bg-primary-600 px-4 py-2 text-base font-medium text-white shadow-sm hover:bg-primary-700"
              >
                Get Started
              </Link>
            </div>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <main className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div className="py-16 sm:py-24">
          <div className="text-center">
            <h1 className="text-4xl font-bold tracking-tight text-gray-900 sm:text-6xl">
              Create and schedule event flyers that
              <span className="text-primary-600"> deliver themselves</span>
            </h1>
            <p className="mx-auto mt-6 max-w-2xl text-lg leading-8 text-gray-600">
              Upload your PNG templates, schedule events, and let Drawtab automatically generate and email personalized flyers for birthdays, anniversaries, and special occasions.
            </p>
            <div className="mt-10 flex items-center justify-center gap-x-6">
              <Link
                href="/auth/register"
                className="rounded-md bg-primary-600 px-6 py-3 text-base font-semibold text-white shadow-sm hover:bg-primary-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary-600"
              >
                Get Started
              </Link>
              <Link
                href="/about"
                className="text-base font-semibold leading-6 text-gray-900"
              >
                Learn more <span aria-hidden="true">→</span>
              </Link>
            </div>
          </div>
        </div>

        {/* Features Section */}
        <div className="py-16 sm:py-24">
          <div className="mx-auto max-w-7xl px-6 lg:px-8">
            <div className="mx-auto max-w-2xl lg:text-center">
              <h2 className="text-base font-semibold leading-7 text-primary-600">Automate Everything</h2>
              <p className="mt-2 text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
                Three simple steps to automated celebrations
              </p>
            </div>
            <div className="mx-auto mt-16 max-w-2xl sm:mt-20 lg:mt-24 lg:max-w-none">
              <dl className="grid max-w-xl grid-cols-1 gap-x-8 gap-y-16 lg:max-w-none lg:grid-cols-3">
                {/* Feature 1 */}
                <div className="flex flex-col">
                  <dt className="flex items-center gap-x-3 text-base font-semibold leading-7 text-gray-900">
                    <PhotoIcon className="h-5 w-5 flex-none text-primary-600" aria-hidden="true" />
                    Upload Templates + Define Hotspots
                  </dt>
                  <dd className="mt-4 flex flex-auto flex-col text-base leading-7 text-gray-600">
                    <p className="flex-auto">
                      Upload your PNG flyer templates and mark dynamic areas for photos, names, and custom text. Create beautiful designs once, use them forever.
                    </p>
                  </dd>
                </div>

                {/* Feature 2 */}
                <div className="flex flex-col">
                  <dt className="flex items-center gap-x-3 text-base font-semibold leading-7 text-gray-900">
                    <CalendarIcon className="h-5 w-5 flex-none text-primary-600" aria-hidden="true" />
                    Schedule Events
                  </dt>
                  <dd className="mt-4 flex flex-auto flex-col text-base leading-7 text-gray-600">
                    <p className="flex-auto">
                      Add birthdays, anniversaries, and special events to your calendar. Set them once and let Drawtab remember and celebrate every year.
                    </p>
                  </dd>
                </div>

                {/* Feature 3 */}
                <div className="flex flex-col">
                  <dt className="flex items-center gap-x-3 text-base font-semibold leading-7 text-gray-900">
                    <EnvelopeIcon className="h-5 w-5 flex-none text-primary-600" aria-hidden="true" />
                    Auto Email Delivery
                  </dt>
                  <dd className="mt-4 flex flex-auto flex-col text-base leading-7 text-gray-600">
                    <p className="flex-auto">
                      On the special day, personalized flyers are automatically generated and emailed to the celebrant. No manual work required.
                    </p>
                  </dd>
                </div>
              </dl>
            </div>
          </div>
        </div>

        {/* How It Works */}
        <div className="py-16 sm:py-24 bg-gray-50 rounded-3xl">
          <div className="mx-auto max-w-7xl px-6 lg:px-8">
            <div className="mx-auto max-w-2xl lg:text-center">
              <h2 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">
                How Drawtab Works
              </h2>
              <p className="mt-6 text-lg leading-8 text-gray-600">
                From template upload to automated delivery - see how simple celebration automation can be.
              </p>
            </div>
            
            <div className="mx-auto mt-16 max-w-2xl sm:mt-20 lg:mt-24 lg:max-w-none">
              <div className="grid max-w-xl grid-cols-1 gap-y-8 lg:max-w-none lg:grid-cols-3 lg:gap-x-8">
                <div className="text-center">
                  <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-lg bg-primary-600">
                    <span className="text-xl font-bold text-white">1</span>
                  </div>
                  <h3 className="mt-6 text-lg font-semibold leading-8 tracking-tight text-gray-900">Upload & Setup</h3>
                  <p className="mt-2 text-base leading-7 text-gray-600">
                    Upload your PNG templates and mark hotspots for dynamic content. Add your contacts and their special dates.
                  </p>
                </div>

                <div className="text-center">
                  <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-lg bg-primary-600">
                    <span className="text-xl font-bold text-white">2</span>
                  </div>
                  <h3 className="mt-6 text-lg font-semibold leading-8 tracking-tight text-gray-900">Schedule Events</h3>
                  <p className="mt-2 text-base leading-7 text-gray-600">
                    Create birthday and anniversary events. Set recurring dates and choose which template to use for each celebration.
                  </p>
                </div>

                <div className="text-center">
                  <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-lg bg-primary-600">
                    <span className="text-xl font-bold text-white">3</span>
                  </div>
                  <h3 className="mt-6 text-lg font-semibold leading-8 tracking-tight text-gray-900">Automatic Delivery</h3>
                  <p className="mt-2 text-base leading-7 text-gray-600">
                    On the special day, personalized flyers are generated and automatically emailed. Sit back and let Drawtab celebrate for you.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* CTA Banner */}
        <div className="py-16 sm:py-24">
          <div className="relative isolate overflow-hidden bg-primary-600 px-6 py-24 text-center shadow-2xl rounded-3xl sm:px-16">
            <h2 className="mx-auto max-w-2xl text-3xl font-bold tracking-tight text-white sm:text-4xl">
              Start automating your celebrations today
            </h2>
            <p className="mx-auto mt-6 max-w-xl text-lg leading-8 text-primary-200">
              Join hundreds of users who never miss a birthday or anniversary again. Create your first automated flyer in minutes.
            </p>
            <div className="mt-10 flex items-center justify-center gap-x-6">
              <Link
                href="/auth/register"
                className="rounded-md bg-white px-6 py-3 text-base font-semibold text-primary-600 shadow-sm hover:bg-primary-50 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-white"
              >
                Get Started Free
              </Link>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t border-gray-200">
        <div className="mx-auto max-w-7xl px-6 py-12 md:flex md:items-center md:justify-between lg:px-8">
          <div className="flex justify-center space-x-6 md:order-2">
            <Link href="/about" className="text-gray-400 hover:text-gray-500">
              About
            </Link>
            <Link href="/contact" className="text-gray-400 hover:text-gray-500">
              Contact
            </Link>
            <Link href="/pricing" className="text-gray-400 hover:text-gray-500">
              Pricing
            </Link>
          </div>
          <div className="mt-8 md:order-1 md:mt-0">
            <p className="text-center text-xs leading-5 text-gray-500">
              &copy; 2025 Drawtab. All rights reserved.
            </p>
          </div>
        </div>
      </footer>
    </div>
  )
}
