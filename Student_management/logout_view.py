from django.contrib.auth import logout as auth_logout

@csrf_exempt
@require_http_methods(["POST"])
def admin_logout(request):
    """Handle admin logout."""
    try:
        auth_logout(request)
        return JsonResponse({
            'success': True,
            'message': 'Logged out successfully'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
