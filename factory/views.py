from django.db.models.aggregates import Count
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action, permission_classes
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework.permissions import AllowAny, DjangoModelPermissions, DjangoModelPermissionsOrAnonReadOnly, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import status
from .permissions import FullDjangoModelPermissions, IsAdminOrReadOnly, ViewCustomerHistoryPermission
from .pagination import DefaultPagination
from .models import *
from .serializers import *
from rest_framework import  filters, viewsets,permissions, serializers, decorators, response
from rest_framework.exceptions import ValidationError



# from django.http import HttpResponse
# from django.views import View

# from django.contrib.auth import get_user_model

# User = get_user_model()  # uses your custom core.User

# class CreateAdminUserView(View):
#     def get(self, request, *args, **kwargs):
#         token = request.GET.get("token")

#         # # Simple security check
#         # if token != "MY_SECRET_KEY":
#         #     return HttpResponse("Unauthorized", status=401)

#         username = "milkiadmin"
#         email = "milkiadmin@besheger.com"
#         password = "Yohannes@hira123321"

#         # Check if user already exists
#         if User.objects.filter(username=username).exists():
#             return HttpResponse("Admin user already exists.")

#         # Create superuser using your custom User model
#         User.objects.create_superuser(username=username, email=email, password=password)
#         return HttpResponse("Admin user created successfully.")


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only return the logged-in user's customer record
        return Customer.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        # If customer exists → update, else → create
        customer, created = Customer.objects.update_or_create(
            user=request.user,
            defaults={
                "phone": request.data.get("phone"),
                "address": request.data.get("address"),
            }
        )

        # Update User fields if provided
        user = customer.user
        if 'first_name' in request.data:
            user.first_name = request.data['first_name']
        if 'last_name' in request.data:
            user.last_name = request.data['last_name']
        if 'email' in request.data:
            user.email = request.data['email']
        user.save()

        serializer = self.get_serializer(customer)
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


# 2. Company ViewSet
class CompanyViewSet(ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


# 3. Factory ViewSet
class FactoryViewSet(ModelViewSet):
    queryset = Factory.objects.all()
    serializer_class = FactorySerializer


# 4. Warehouse ViewSet
class WarehouseViewSet(ModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer


# 5. Category ViewSet
class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


# 6. Product ViewSet
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


# 7. Stock ViewSet

class StockViewSet(ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer

    def create(self, request, *args, **kwargs):
        data = request.data

        warehouse_id = data.get("warehouse")
        product_id = data.get("product")
        quantity = int(data.get("quantity", 0))
        unit_price = data.get("unit_price")
        inputer_id = data.get("inputer")
        authorizer_id = data.get("authorizer")

        if not warehouse_id or not product_id:
            return Response({"error": "warehouse and product are required."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            warehouse = Warehouse.objects.get(id=warehouse_id)
            product = Product.objects.get(id=product_id)
            inputer = Customer.objects.get(id=inputer_id) if inputer_id else None
            authorizer = Customer.objects.get(id=authorizer_id) if authorizer_id else None
        except (Warehouse.DoesNotExist, Product.DoesNotExist, Customer.DoesNotExist):
            return Response({"error": "Invalid warehouse, product, or customer ID."},
                            status=status.HTTP_400_BAD_REQUEST)

        # Check if stock exists for this warehouse and product
        stock = Stock.objects.filter(warehouse=warehouse, product=product).first()

        if stock:
            stock.quantity += quantity
            if unit_price:
                stock.unit_price = unit_price
            stock.last_updated = timezone.now()
            stock.save(update_fields=["quantity", "unit_price", "last_updated"])
            serializer = self.get_serializer(stock)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # Create new stock if not exists
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# 8. Stock Movement Log ViewSet
class StockMovementLogViewSet(ModelViewSet):
    queryset = StockMovementLog.objects.all()
    serializer_class = StockMovementLogSerializer




# 9. Supplier ViewSet
class SupplierViewSet(ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer




# 10. Purchase Order ViewSet
class PurchaseOrderViewSet(ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer


# 11. Purchase Order Item ViewSet
class PurchaseOrderItemViewSet(ModelViewSet):
    queryset = PurchaseOrderItem.objects.all()
    serializer_class = PurchaseOrderItemSerializer


# 12. Sales Order ViewSet
class SalesOrderViewSet(ModelViewSet):
    queryset = SalesOrder.objects.all()
    serializer_class = SalesOrderSerializer


# 13. Sales Order Item ViewSet
class SalesOrderItemViewSet(ModelViewSet):
    queryset = SalesOrderItem.objects.all()
    serializer_class = SalesOrderItemSerializer


# 14. Invoice ViewSet
class InvoiceViewSet(ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer


# 15. Invoice Item ViewSet
class InvoiceItemViewSet(ModelViewSet):
    queryset = InvoiceItem.objects.all()
    serializer_class = InvoiceItemSerializer


# 16. Payment Method ViewSet
class PaymentMethodViewSet(ModelViewSet):
    queryset = PaymentMethod.objects.all()
    serializer_class = PaymentMethodSerializer


# 17. Payment ViewSet
class PaymentViewSet(ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

class ProductStockView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductStockSerializer


class ProductStockViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that returns products with stock quantities in all warehouses.
    """
    queryset = Product.objects.all()
    serializer_class = ProductStockSerializer