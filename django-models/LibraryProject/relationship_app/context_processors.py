def user_role(request):
    return {
        'user_role': getattr(request, 'user_role', None)
    }