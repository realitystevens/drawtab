import { Client, Account, Databases, Storage, Functions } from 'appwrite'

export const client = new Client()

client
  .setEndpoint(process.env.NEXT_PUBLIC_APPWRITE_ENDPOINT || 'https://cloud.appwrite.io/v1')
  .setProject(process.env.NEXT_PUBLIC_APPWRITE_PROJECT_ID || '')

export const account = new Account(client)
export const databases = new Databases(client)
export const storage = new Storage(client)
export const functions = new Functions(client)

// Database and Collection IDs
export const DATABASE_ID = process.env.NEXT_PUBLIC_APPWRITE_DATABASE_ID || ''
export const COLLECTIONS = {
  TEMPLATES: process.env.NEXT_PUBLIC_COLLECTION_TEMPLATES || '',
  CONTACTS: process.env.NEXT_PUBLIC_COLLECTION_CONTACTS || '',
  EVENTS: process.env.NEXT_PUBLIC_COLLECTION_EVENTS || '',
  GENERATED_FLYERS: process.env.NEXT_PUBLIC_COLLECTION_GENERATED_FLYERS || '',
  USERS: process.env.NEXT_PUBLIC_COLLECTION_USERS || '',
}

// Storage Bucket IDs
export const BUCKETS = {
  TEMPLATES: process.env.NEXT_PUBLIC_BUCKET_TEMPLATES || '',
  GENERATED_FLYERS: process.env.NEXT_PUBLIC_BUCKET_GENERATED_FLYERS || '',
  USER_PHOTOS: process.env.NEXT_PUBLIC_BUCKET_USER_PHOTOS || '',
}

// Function IDs
export const FUNCTIONS_IDS = {
  GENERATE_FLYER: process.env.NEXT_PUBLIC_FUNCTION_GENERATE_FLYER || '',
  SEND_EMAIL: process.env.NEXT_PUBLIC_FUNCTION_SEND_EMAIL || '',
  SCHEDULE_EVENTS: process.env.NEXT_PUBLIC_FUNCTION_SCHEDULE_EVENTS || '',
}
