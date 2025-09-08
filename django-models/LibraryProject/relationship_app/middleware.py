class UserRoleMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            # Check if user has a profile and get the role
            if hasattr(request.user, 'userprofile'):
                request.user_role = request.user.userprofile.role
            else:
                request.user_role = None
        else:
            request.user_role = None
        return self.get_response(request)