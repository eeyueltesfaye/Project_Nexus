from django.http import JsonResponse


class EnforceProfileCompletionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            user = request.user
            if hasattr(user, 'profile') and not user.profile.profile_completed:
                exempt_paths = [
                    '/api/profile/update/',
                    '/api/profile/status/',
                    '/api/logout/',
                    '/api/login/',
                    '/admin/',
                ]
                restricted_prefixes = [
                    '/api/jobs/',
                    '/api/saved-jobs/',
                    '/api/users/request-role/',
                    '/api/profile/resume/',
                ]
                if request.path not in exempt_paths and any(request.path.startswith(p) for p in restricted_prefixes):
                    return JsonResponse(
                        {'error': 'Complete your profile before accessing this feature.'},
                        status=403
                    )
        return self.get_response(request)
