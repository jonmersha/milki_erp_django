from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.views import View

User = get_user_model()
# User = get_user_model()  # uses your custom core.User

class CreateAdminUserView(View):
    def get(self, request, *args, **kwargs):
        token = request.GET.get("token")

        # # Simple security check
        # if token != "MY_SECRET_KEY":
        #     return HttpResponse("Unauthorized", status=401)

        username = "milkiadmin"
        email = "milkiadmin@besheger.com"
        password = "Yohannes@hira123321"

        # Check if user already exists
        if User.objects.filter(username=username).exists():
            return HttpResponse("Admin user already exists.")

        # Create superuser using your custom User model
        User.objects.create_superuser(username=username, email=email, password=password)
        return HttpResponse("Admin user created successfully.")

