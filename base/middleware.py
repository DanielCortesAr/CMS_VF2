class CustomXFrameOptionsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # Permite iframes solo para ciertas URLs
        if request.path.startswith('/admin/'):
            response['X-Frame-Options'] = 'SAMEORIGIN'
        return response