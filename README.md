# Drawtab

Web application for automating the creation and delivery of personalized event flyers. Allows users to upload PNG templates, define dynamic hotspots, schedule events, and send flyers via email for birthdays, anniversaries, and other occasions.

## Features

- Upload PNG templates and define hotspots for dynamic content
- Manage contacts and events
- Generate flyers using serverless Python functions
- Automated email delivery for scheduled events
- Dashboard for analytics and management

## Technology

- Next.js 14 (App Router)
- Tailwind CSS
- Appwrite (database, storage, authentication, serverless functions)
- Python (Pillow for image processing)

## Getting Started

1. Clone the repository
2. Install dependencies: `npm install`
3. Configure environment variables in `.env.local` (see `.env.local.example`)
4. Set up Appwrite project, database collections, and storage buckets
5. Deploy Appwrite functions from the `functions/` directory
6. Run the development server: `npm run dev`

## Project Structure

```
src/
  app/           # Next.js pages and routes
  components/    # Reusable React components
  contexts/      # React context providers
  lib/           # Utility libraries
  types/         # TypeScript types
functions/       # Appwrite serverless functions
```

## URL Structure

- `/` - Homepage
- `/auth/login` - Login
- `/auth/register` - Registration
- `/dashboard` - Main dashboard (protected)
- `/dashboard/templates` - Template management
- `/dashboard/contacts` - Contact management
- `/dashboard/events` - Event scheduling
- `/dashboard/calendar` - Calendar view
- `/account/profile` - User profile

## Contributing

Contributions are welcome. Please open issues or submit pull requests for improvements and bug fixes.

## License

This project is licensed under the MIT License.
