'use client'

import { useState, useRef } from 'react'
import { Metadata } from 'next'
import Link from 'next/link'
import { 
  CloudArrowUpIcon, 
  PhotoIcon, 
  XMarkIcon,
  PlusIcon,
  CursorArrowRaysIcon
} from '@heroicons/react/24/outline'

// Note: This would normally be imported from metadata in a separate file
// export const metadata: Metadata = {
//   title: 'New Template - Drawtab',
//   description: 'Upload a new flyer template and define hotspots.',
// }

interface Hotspot {
  id: string
  x: number
  y: number
  width: number
  height: number
  type: 'text' | 'image'
  label: string
}

export default function NewTemplatePage() {
  const [templateFile, setTemplateFile] = useState<File | null>(null)
  const [templatePreview, setTemplatePreview] = useState<string | null>(null)
  const [hotspots, setHotspots] = useState<Hotspot[]>([])
  const [isDefiningHotspot, setIsDefiningHotspot] = useState(false)
  const [currentHotspotType, setCurrentHotspotType] = useState<'text' | 'image'>('text')
  const [templateName, setTemplateName] = useState('')
  const [templateCategory, setTemplateCategory] = useState('Birthday')
  const fileInputRef = useRef<HTMLInputElement>(null)

  const categories = ['Birthday', 'Anniversary', 'Promotion', 'Holiday', 'Welcome', 'General']

  const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0]
    if (file && file.type.includes('image')) {
      setTemplateFile(file)
      
      // Create preview URL
      const reader = new FileReader()
      reader.onload = (e) => {
        setTemplatePreview(e.target?.result as string)
      }
      reader.readAsDataURL(file)
    }
  }

  const handleImageClick = (event: React.MouseEvent<HTMLDivElement>) => {
    if (!isDefiningHotspot) return
    
    const rect = event.currentTarget.getBoundingClientRect()
    const x = ((event.clientX - rect.left) / rect.width) * 100
    const y = ((event.clientY - rect.top) / rect.height) * 100
    
    const newHotspot: Hotspot = {
      id: `hotspot-${Date.now()}`,
      x,
      y,
      width: 20, // Default width in percentage
      height: 10, // Default height in percentage
      type: currentHotspotType,
      label: `${currentHotspotType === 'text' ? 'Text' : 'Image'} ${hotspots.length + 1}`
    }
    
    setHotspots([...hotspots, newHotspot])
    setIsDefiningHotspot(false)
  }

  const removeHotspot = (id: string) => {
    setHotspots(hotspots.filter(h => h.id !== id))
  }

  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault()
    // Here you would submit to Appwrite
    console.log({
      name: templateName,
      category: templateCategory,
      file: templateFile,
      hotspots
    })
  }

  return (
    <div className="py-6">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 md:px-8">
        {/* Header */}
        <div className="md:flex md:items-center md:justify-between">
          <div className="min-w-0 flex-1">
            <h1 className="text-2xl font-semibold text-gray-900">New Template</h1>
            <p className="mt-1 text-sm text-gray-500">
              Upload a PNG template and define hotspots for dynamic content
            </p>
          </div>
          <div className="mt-4 flex md:mt-0 md:ml-4">
            <Link
              href="/dashboard/templates"
              className="inline-flex items-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
            >
              Cancel
            </Link>
          </div>
        </div>

        <form onSubmit={handleSubmit} className="mt-8 space-y-8">
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
            {/* Left Column - Form */}
            <div className="space-y-6">
              {/* Template Info */}
              <div className="bg-white shadow rounded-lg p-6">
                <h3 className="text-lg font-medium text-gray-900 mb-4">Template Information</h3>
                
                <div className="space-y-4">
                  <div>
                    <label htmlFor="template-name" className="block text-sm font-medium text-gray-700">
                      Template Name
                    </label>
                    <input
                      type="text"
                      id="template-name"
                      value={templateName}
                      onChange={(e) => setTemplateName(e.target.value)}
                      className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-500"
                      placeholder="e.g., Birthday Celebration Template"
                      required
                    />
                  </div>
                  
                  <div>
                    <label htmlFor="template-category" className="block text-sm font-medium text-gray-700">
                      Category
                    </label>
                    <select
                      id="template-category"
                      value={templateCategory}
                      onChange={(e) => setTemplateCategory(e.target.value)}
                      className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-primary-500 focus:border-primary-500"
                    >
                      {categories.map((category) => (
                        <option key={category} value={category}>
                          {category}
                        </option>
                      ))}
                    </select>
                  </div>
                </div>
              </div>

              {/* File Upload */}
              <div className="bg-white shadow rounded-lg p-6">
                <h3 className="text-lg font-medium text-gray-900 mb-4">Upload Template</h3>
                
                {!templateFile ? (
                  <div
                    onClick={() => fileInputRef.current?.click()}
                    className="mt-1 flex justify-center px-6 pt-5 pb-6 border-2 border-gray-300 border-dashed rounded-md cursor-pointer hover:border-gray-400"
                  >
                    <div className="space-y-1 text-center">
                      <CloudArrowUpIcon className="mx-auto h-12 w-12 text-gray-400" />
                      <div className="flex text-sm text-gray-600">
                        <span className="font-medium text-primary-600 hover:text-primary-500">
                          Upload a file
                        </span>
                        <span className="pl-1">or drag and drop</span>
                      </div>
                      <p className="text-xs text-gray-500">PNG up to 10MB</p>
                    </div>
                  </div>
                ) : (
                  <div className="flex items-center justify-between p-3 bg-gray-50 rounded-md">
                    <div className="flex items-center">
                      <PhotoIcon className="h-8 w-8 text-gray-400" />
                      <span className="ml-2 text-sm text-gray-900">{templateFile.name}</span>
                    </div>
                    <button
                      type="button"
                      onClick={() => {
                        setTemplateFile(null)
                        setTemplatePreview(null)
                        setHotspots([])
                      }}
                      className="text-gray-400 hover:text-gray-600"
                    >
                      <XMarkIcon className="h-5 w-5" />
                    </button>
                  </div>
                )}
                
                <input
                  ref={fileInputRef}
                  type="file"
                  accept="image/png"
                  onChange={handleFileUpload}
                  className="hidden"
                />
              </div>

              {/* Hotspot Controls */}
              {templatePreview && (
                <div className="bg-white shadow rounded-lg p-6">
                  <h3 className="text-lg font-medium text-gray-900 mb-4">Define Hotspots</h3>
                  
                  <div className="space-y-4">
                    <p className="text-sm text-gray-600">
                      Click on the template preview to add hotspots where dynamic content will be placed.
                    </p>
                    
                    <div className="flex space-x-3">
                      <button
                        type="button"
                        onClick={() => {
                          setIsDefiningHotspot(true)
                          setCurrentHotspotType('text')
                        }}
                        className={`inline-flex items-center px-3 py-2 border text-sm font-medium rounded-md ${
                          isDefiningHotspot && currentHotspotType === 'text'
                            ? 'bg-primary-600 text-white border-primary-600'
                            : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-50'
                        }`}
                      >
                        <PlusIcon className="mr-2 h-4 w-4" />
                        Add Text Area
                      </button>
                      <button
                        type="button"
                        onClick={() => {
                          setIsDefiningHotspot(true)
                          setCurrentHotspotType('image')
                        }}
                        className={`inline-flex items-center px-3 py-2 border text-sm font-medium rounded-md ${
                          isDefiningHotspot && currentHotspotType === 'image'
                            ? 'bg-primary-600 text-white border-primary-600'
                            : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-50'
                        }`}
                      >
                        <PlusIcon className="mr-2 h-4 w-4" />
                        Add Image Area
                      </button>
                    </div>
                    
                    {isDefiningHotspot && (
                      <div className="flex items-center p-3 bg-blue-50 rounded-md">
                        <CursorArrowRaysIcon className="h-5 w-5 text-blue-600" />
                        <span className="ml-2 text-sm text-blue-800">
                          Click on the template to place a {currentHotspotType} hotspot
                        </span>
                      </div>
                    )}
                    
                    {/* Hotspot List */}
                    {hotspots.length > 0 && (
                      <div>
                        <h4 className="text-sm font-medium text-gray-900 mb-2">Hotspots</h4>
                        <div className="space-y-2">
                          {hotspots.map((hotspot) => (
                            <div key={hotspot.id} className="flex items-center justify-between p-2 bg-gray-50 rounded">
                              <span className="text-sm text-gray-900">{hotspot.label}</span>
                              <button
                                type="button"
                                onClick={() => removeHotspot(hotspot.id)}
                                className="text-red-600 hover:text-red-800"
                              >
                                <XMarkIcon className="h-4 w-4" />
                              </button>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              )}
            </div>

            {/* Right Column - Preview */}
            <div className="space-y-6">
              <div className="bg-white shadow rounded-lg p-6">
                <h3 className="text-lg font-medium text-gray-900 mb-4">Template Preview</h3>
                
                {templatePreview ? (
                  <div
                    className="relative border-2 border-gray-200 rounded-lg overflow-hidden cursor-crosshair"
                    onClick={handleImageClick}
                  >
                    <img
                      src={templatePreview}
                      alt="Template preview"
                      className="w-full h-auto"
                    />
                    
                    {/* Hotspot overlays */}
                    {hotspots.map((hotspot) => (
                      <div
                        key={hotspot.id}
                        className={`absolute border-2 ${
                          hotspot.type === 'text' ? 'border-blue-500 bg-blue-100' : 'border-green-500 bg-green-100'
                        } border-dashed bg-opacity-30`}
                        style={{
                          left: `${hotspot.x}%`,
                          top: `${hotspot.y}%`,
                          width: `${hotspot.width}%`,
                          height: `${hotspot.height}%`,
                        }}
                      >
                        <div className={`absolute -top-6 left-0 px-2 py-1 text-xs font-medium rounded ${
                          hotspot.type === 'text' ? 'bg-blue-500 text-white' : 'bg-green-500 text-white'
                        }`}>
                          {hotspot.label}
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="flex items-center justify-center h-64 bg-gray-100 rounded-lg">
                    <div className="text-center">
                      <PhotoIcon className="mx-auto h-12 w-12 text-gray-400" />
                      <p className="mt-2 text-sm text-gray-500">Upload a template to see preview</p>
                    </div>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Submit Button */}
          <div className="flex justify-end">
            <button
              type="submit"
              disabled={!templateFile || !templateName}
              className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md shadow-sm text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Create Template
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
