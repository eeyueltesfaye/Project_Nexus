from django.http import JsonResponse

EXEMPT_PATHS = [
    'admin:index',
    'users:profile-update',
    'users:resume-download',
]

class EnforceProfileCompletionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            user = request.user
            if hasattr(user, 'profile'):
                if not user.profile.profile_completed:
                    restricted_paths = [
                        '/api/jobs/apply/',
                        '/api/jobs/post/',
                        # Add more restricted URLs
                    ]
                    if request.path in restricted_paths:
                        return JsonResponse(
                            {'error': 'Complete your profile before proceeding.'},
                            status=403
                        )
        return self.get_response(request)
