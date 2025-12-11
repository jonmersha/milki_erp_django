from pathlib import Path
from django.http import HttpResponse
from django.views import View

class FrontendAppView(View):
    def get(self, request, *args, **kwargs):
        index_file = Path(__file__).resolve().parent.parent / "frontend" / "dist" / "index.html"
        try:
            with open(index_file, encoding="utf-8") as f:
                return HttpResponse(f.read())
        except FileNotFoundError:
            return HttpResponse(
                "Vite build not found. Run 'npm run build' in frontend folder.",
                status=501,
            )
