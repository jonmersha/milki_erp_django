from pathlib import Path
from django.http import HttpResponse
from django.views import View

class FrontendAppView(View):
    def get(self, request, *args, **kwargs):
        index_file = Path(__file__).resolve().parent.parent / "frontend" / "dist" / "index.html"
        try:
            with open(Path(__file__).resolve().parent.parent / 'frontend' / 'dist' / 'index.html') as f:
                return HttpResponse(f.read())
        except FileNotFoundError:
            return HttpResponse(
                "Vite build not found. Run 'npm run build' in frontend folder.",
                status=501,
            )

from django.views import View
class ServiceWorkerView(View):
    def get(self, request, *args, **kwargs):
        path = Path(__file__).resolve().parent.parent / 'frontend' / 'dist' / 'service-worker.js'
        if path.exists():
            return HttpResponse(path.read_text(), content_type='application/javascript')
        return HttpResponse("Service worker not found", status=404)
