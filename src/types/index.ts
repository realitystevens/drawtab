import { Models } from 'appwrite'

// User Profile extending Appwrite User
export interface UserProfile extends Models.Document {
  userId: string
  firstName: string
  lastName: string
  company?: string
  phone?: string
  timezone: string
  emailNotifications: boolean
  createdAt: string
  updatedAt: string
}

// Template with hotspots
export interface Template extends Models.Document {
  name: string
  category: string
  description?: string
  fileId: string // Appwrite file ID
  fileUrl: string
  hotspots: Hotspot[]
  isActive: boolean
  usageCount: number
  createdBy: string // User ID
  createdAt: string
  updatedAt: string
}

// Hotspot definition for templates
export interface Hotspot {
  id: string
  type: 'text' | 'image'
  label: string
  x: number // Percentage
  y: number // Percentage
  width: number // Percentage
  height: number // Percentage
  defaultValue?: string
  required: boolean
  fontFamily?: string
  fontSize?: number
  fontColor?: string
  textAlign?: 'left' | 'center' | 'right'
}

// Contact/Staff member
export interface Contact extends Models.Document {
  firstName: string
  lastName: string
  email: string
  phone?: string
  photoId?: string // Appwrite file ID for profile photo
  photoUrl?: string
  department?: string
  position?: string
  dateOfBirth?: string
  hireDate?: string
  anniversaryDate?: string
  notes?: string
  isActive: boolean
  createdBy: string // User ID
  createdAt: string
  updatedAt: string
}

// Scheduled Event
export interface ScheduledEvent extends Models.Document {
  title: string
  description?: string
  eventType: 'birthday' | 'anniversary' | 'promotion' | 'holiday' | 'custom'
  contactId: string
  templateId: string
  scheduledDate: string // ISO string
  isRecurring: boolean
  recurrencePattern?: 'yearly' | 'monthly' | 'weekly'
  customData: Record<string, any> // Data to fill hotspots
  status: 'scheduled' | 'sent' | 'failed' | 'cancelled'
  emailSubject?: string
  emailBody?: string
  lastSentAt?: string
  nextSendAt?: string
  createdBy: string // User ID
  createdAt: string
  updatedAt: string
}

// Generated Flyer
export interface GeneratedFlyer extends Models.Document {
  eventId: string
  templateId: string
  contactId: string
  fileId: string // Appwrite file ID
  fileUrl: string
  generatedData: Record<string, any>
  status: 'generating' | 'ready' | 'sent' | 'failed'
  generatedAt: string
  sentAt?: string
  emailDeliveryStatus?: 'pending' | 'sent' | 'delivered' | 'failed' | 'bounced'
  emailDeliveryError?: string
  createdBy: string // User ID
}

// Email Log
export interface EmailLog extends Models.Document {
  flyerId?: string
  eventId?: string
  contactId: string
  recipientEmail: string
  subject: string
  body: string
  status: 'queued' | 'sending' | 'sent' | 'delivered' | 'failed' | 'bounced'
  error?: string
  sentAt?: string
  deliveredAt?: string
  openedAt?: string
  clickedAt?: string
  createdBy: string // User ID
  createdAt: string
}

// API Response types
export interface ApiResponse<T> {
  success: boolean
  data?: T
  error?: string
  message?: string
}

// Form types for components
export interface TemplateForm {
  name: string
  category: string
  description?: string
  file: File
  hotspots: Hotspot[]
}

export interface ContactForm {
  firstName: string
  lastName: string
  email: string
  phone?: string
  department?: string
  position?: string
  dateOfBirth?: string
  hireDate?: string
  anniversaryDate?: string
  notes?: string
  photo?: File
}

export interface EventForm {
  title: string
  description?: string
  eventType: string
  contactId: string
  templateId: string
  scheduledDate: string
  isRecurring: boolean
  recurrencePattern?: string
  customData: Record<string, any>
  emailSubject?: string
  emailBody?: string
}

// Dashboard Statistics
export interface DashboardStats {
  totalTemplates: number
  totalContacts: number
  scheduledEvents: number
  emailsSent: number
  recentActivity: ActivityItem[]
  upcomingEvents: UpcomingEvent[]
}

export interface ActivityItem {
  id: string
  type: string
  description: string
  timestamp: string
  metadata?: Record<string, any>
}

export interface UpcomingEvent {
  id: string
  title: string
  contactName: string
  eventType: string
  date: string
  templateName: string
  status: string
}
