from django.shortcuts import render


from django.views.generic import View as gnview
from django.http import HttpResponse
from pathlib import Path

def home_view(request):
    return render(request, 'index.html')
class FrontendAppView(gnview):
    """
    Serves the compiled React app.
    """
    def get(self, request, *args, **kwargs):
        try:
            with open(Path(__file__).resolve().parent.parent / 'frontend' / 'build' / 'index.html') as f:
                return HttpResponse(f.read())
        except FileNotFoundError:
            return HttpResponse(
                "React build not found. Run 'npm run build' in the frontend folder.",
                status=501,
            )

from django.views import View
class ServiceWorkerView(View):
    def get(self, request, *args, **kwargs):
        path = Path(__file__).resolve().parent.parent / 'frontend' / 'build' / 'service-worker.js'
        if path.exists():
            return HttpResponse(path.read_text(), content_type='application/javascript')
        return HttpResponse("Service worker not found", status=404)