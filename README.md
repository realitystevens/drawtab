# Drawtab - Automated Flyer Creation Platform

## 🎯 Project Overview

Drawtab is a modern web application that automates the creation and delivery of personalized event flyers. Users can upload PNG templates, define dynamic hotspots, schedule events, and automatically send personalized flyers via email for birthdays, anniversaries, and other celebrations.

## 🏗️ Architecture

### Frontend: Next.js 14 with TypeScript

- **Framework**: Next.js 14 with App Router
- **Styling**: Tailwind CSS
- **UI Components**: Heroicons
- **Authentication**: Appwrite Auth
- **State Management**: React Context

### Backend: Appwrite Cloud

- **Database**: Appwrite Database
- **Storage**: Appwrite Storage (for templates and generated flyers)
- **Functions**: Python serverless functions
- **Authentication**: Appwrite Auth

### Key Features

- ✅ **Template Management**: Upload PNG templates with hotspot definition
- ✅ **Contact Management**: Staff/contact database with photos
- ✅ **Event Scheduling**: Automated birthday/anniversary scheduling
- ✅ **Flyer Generation**: Python-based image processing with Pillow
- ✅ **Email Delivery**: Automated email sending with flyer attachments
- ✅ **Dashboard**: Analytics and management interface

## 🚀 Quick Start

### 1. Setup Appwrite Project

1. Create an Appwrite account at [cloud.appwrite.io](https://cloud.appwrite.io)
2. Create a new project
3. Note your Project ID and Endpoint

### 2. Configure Database Collections

Create the following collections in your Appwrite database:

#### Templates Collection

```json
{
  "name": "string",
  "category": "string",
  "description": "string",
  "fileId": "string",
  "fileUrl": "string",
  "hotspots": "array",
  "isActive": "boolean",
  "usageCount": "integer",
  "createdBy": "string",
  "createdAt": "datetime",
  "updatedAt": "datetime"
}
```

#### Contacts Collection

```json
{
  "firstName": "string",
  "lastName": "string",
  "email": "string",
  "phone": "string",
  "photoId": "string",
  "photoUrl": "string",
  "department": "string",
  "position": "string",
  "dateOfBirth": "datetime",
  "hireDate": "datetime",
  "anniversaryDate": "datetime",
  "notes": "string",
  "isActive": "boolean",
  "createdBy": "string",
  "createdAt": "datetime",
  "updatedAt": "datetime"
}
```

#### Events Collection

```json
{
  "title": "string",
  "description": "string",
  "eventType": "string",
  "contactId": "string",
  "templateId": "string",
  "scheduledDate": "datetime",
  "isRecurring": "boolean",
  "recurrencePattern": "string",
  "customData": "object",
  "status": "string",
  "emailSubject": "string",
  "emailBody": "string",
  "lastSentAt": "datetime",
  "nextSendAt": "datetime",
  "createdBy": "string",
  "createdAt": "datetime",
  "updatedAt": "datetime"
}
```

#### Generated Flyers Collection

```json
{
  "eventId": "string",
  "templateId": "string",
  "contactId": "string",
  "fileId": "string",
  "fileUrl": "string",
  "generatedData": "object",
  "status": "string",
  "generatedAt": "datetime",
  "sentAt": "datetime",
  "emailDeliveryStatus": "string",
  "emailDeliveryError": "string",
  "createdBy": "string"
}
```

### 3. Setup Storage Buckets

Create these storage buckets:

- `templates` - For PNG template files
- `generated_flyers` - For generated flyer images
- `user_photos` - For contact profile photos

### 4. Deploy Appwrite Functions

Deploy the Python functions in the `functions/` directory:

#### Flyer Generation Function

```bash
cd functions/generate-flyer
appwrite functions create \\
  --functionId generate-flyer \\
  --name "Generate Flyer" \\
  --runtime python-3.11 \\
  --entrypoint main.py
```

#### Email Sending Function

```bash
cd functions/send-email
appwrite functions create \\
  --functionId send-email \\
  --name "Send Email" \\
  --runtime python-3.11 \\
  --entrypoint main.py
```

### 5. Configure Environment Variables

Copy `.env.local.example` to `.env.local` and configure:

```env
NEXT_PUBLIC_APPWRITE_ENDPOINT=https://cloud.appwrite.io/v1
NEXT_PUBLIC_APPWRITE_PROJECT_ID=your-project-id
NEXT_PUBLIC_APPWRITE_DATABASE_ID=your-database-id

# Collections
NEXT_PUBLIC_COLLECTION_TEMPLATES=templates
NEXT_PUBLIC_COLLECTION_CONTACTS=contacts
NEXT_PUBLIC_COLLECTION_EVENTS=events
NEXT_PUBLIC_COLLECTION_GENERATED_FLYERS=generated_flyers

# Storage Buckets
NEXT_PUBLIC_BUCKET_TEMPLATES=templates
NEXT_PUBLIC_BUCKET_GENERATED_FLYERS=generated_flyers
NEXT_PUBLIC_BUCKET_USER_PHOTOS=user_photos

# Functions
NEXT_PUBLIC_FUNCTION_GENERATE_FLYER=generate-flyer
NEXT_PUBLIC_FUNCTION_SEND_EMAIL=send-email
```

For the email function, add these environment variables in Appwrite:

```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
FROM_EMAIL=your-email@gmail.com
FROM_NAME=Drawtab
```

### 6. Install and Run

```bash
# Install dependencies
npm install

# Run development server
npm run dev
```

Visit `http://localhost:3000` to see the application.

## 📁 Project Structure

```
src/
├── app/                    # Next.js App Router
│   ├── (auth)/            # Authentication pages
│   ├── dashboard/         # Dashboard pages
│   └── page.tsx           # Homepage
├── components/            # Reusable components
├── contexts/              # React contexts
├── lib/                   # Utility libraries
├── types/                 # TypeScript types
└── functions/             # Appwrite serverless functions
    ├── generate-flyer/    # Flyer generation
    └── send-email/        # Email delivery
```

## 🎨 URL Structure

### Public Pages

- `/` - Homepage with marketing content
- `/about` - About page
- `/contact` - Contact page
- `/pricing` - Pricing page

### Authentication

- `/auth/login` - User login
- `/auth/register` - User registration
- `/auth/reset-password` - Password reset

### Dashboard (Protected)

- `/dashboard` - Main dashboard overview
- `/dashboard/templates` - Template management
- `/dashboard/templates/new` - Upload new template
- `/dashboard/contacts` - Contact management
- `/dashboard/events` - Event scheduling
- `/dashboard/calendar` - Calendar view
- `/dashboard/settings` - User settings

### Account Management

- `/account/profile` - User profile
- `/account/billing` - Billing settings
- `/account/security` - Security settings

## 🔧 Key Components

### Template Upload with Hotspots

The template upload page (`/dashboard/templates/new`) allows users to:

1. Upload PNG template files
2. Click on the template to define hotspots
3. Configure hotspot types (text/image)
4. Set hotspot properties (font, size, color)

### Flyer Generation

The `generate-flyer` function processes templates by:

1. Downloading the template image
2. Processing each hotspot with dynamic data
3. Adding text with proper wrapping and styling
4. Overlaying images with resizing
5. Returning base64-encoded result

### Email Automation

The `send-email` function handles:

1. SMTP email delivery
2. HTML and text email templates
3. Flyer attachment handling
4. Template generation for birthdays/anniversaries

## 🔄 Migration from Django

The Django backend has been successfully converted to:

- **Models → Appwrite Collections**: All Django models converted to Appwrite database collections
- **Views → Next.js Pages**: Django views converted to Next.js pages and API routes
- **Templates → React Components**: Django templates converted to React components
- **Celery Tasks → Appwrite Functions**: Background tasks converted to serverless functions
- **Image Processing → Python Functions**: FlyerGenerator converted to Appwrite function

## 🚀 Deployment

### Frontend (Next.js)

Deploy to Vercel, Netlify, or any hosting platform:

```bash
npm run build
npm start
```

### Backend (Appwrite)

Functions are deployed to Appwrite Cloud automatically.

## 🔐 Security

- Authentication handled by Appwrite Auth
- Database permissions configured per collection
- File uploads secured through Appwrite Storage
- Functions isolated in serverless environment

## 📈 Scalability

- Serverless functions auto-scale
- Appwrite Database handles high concurrency
- CDN delivery for static assets
- Efficient image processing with Pillow

## 🛠️ Development

### Adding New Features

1. Create database collections in Appwrite
2. Define TypeScript types in `src/types/`
3. Create React components and pages
4. Add Appwrite functions if needed

### Testing

- Test authentication flows
- Test template upload and hotspot definition
- Test flyer generation with sample data
- Test email delivery with test accounts

## 📞 Support

For questions or issues:

1. Check the Appwrite documentation
2. Review the Next.js documentation
3. Check the GitHub issues
4. Contact support

---

**Drawtab** - Automate your celebrations! 🎉
