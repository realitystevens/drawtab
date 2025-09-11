from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json

# API Placeholder views - will be implemented later


@csrf_exempt
@login_required
def template_list_api(request):
    """API endpoint for templates"""
    if request.method == 'GET':
        return JsonResponse({'templates': []})
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
@login_required
def template_detail_api(request, pk):
    """API endpoint for template detail"""
    return JsonResponse({'template': {'id': pk, 'name': 'Sample Template'}})


@csrf_exempt
@login_required
def template_upload_api(request):
    """API endpoint for template upload"""
    if request.method == 'POST':
        return JsonResponse({'status': 'success', 'message': 'Template uploaded'})
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
@login_required
def event_list_api(request):
    """API endpoint for events"""
    if request.method == 'GET':
        return JsonResponse({'events': []})
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
@login_required
def event_detail_api(request, pk):
    """API endpoint for event detail"""
    return JsonResponse({'event': {'id': pk, 'title': 'Sample Event'}})


@csrf_exempt
@login_required
def event_create_api(request):
    """API endpoint for event creation"""
    if request.method == 'POST':
        return JsonResponse({'status': 'success', 'message': 'Event created'})
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
@login_required
def event_execute_api(request, pk):
    """API endpoint for event execution"""
    if request.method == 'POST':
        return JsonResponse({'status': 'success', 'message': 'Event executed'})
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
@login_required
def recipient_list_api(request):
    """API endpoint for recipients"""
    if request.method == 'GET':
        return JsonResponse({'recipients': []})
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
@login_required
def recipient_import_api(request):
    """API endpoint for recipient import"""
    if request.method == 'POST':
        return JsonResponse({'status': 'success', 'message': 'Recipients imported'})
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
@login_required
def notification_stats_api(request):
    """API endpoint for notification statistics"""
    stats = {
        'total': 100,
        'sent': 85,
        'failed': 10,
        'pending': 5
    }
    return JsonResponse(stats)


@csrf_exempt
@login_required
def dashboard_data_api(request):
    """API endpoint for dashboard data"""
    data = {
        'recent_events': [],
        'upcoming_events': [],
        'statistics': {
            'total_templates': 0,
            'total_events': 0,
            'total_recipients': 0
        }
    }
    return JsonResponse(data)


@csrf_exempt
@login_required
def generate_flyer_api(request):
    """API endpoint for flyer generation"""
    if request.method == 'POST':
        return JsonResponse({'status': 'success', 'flyer_url': '/media/flyers/sample.png'})
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
@login_required
def webhook_handler(request):
    """Webhook handler for external services"""
    if request.method == 'POST':
        return JsonResponse({'status': 'received'})
    return JsonResponse({'error': 'Method not allowed'}, status=405)
