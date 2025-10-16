from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Warehouse, ProductPackage, Product, Stock, InventoryMovementLog,StockTransfer
from .serializers import (
    WarehouseSerializer, ProductPackageSerializer, ProductSerializer,
    StockSerializer, InventoryMovementSerializer,StockTransferSerializer
)
from rest_framework.decorators import action
from django.db import transaction

class WarehouseViewSet(viewsets.ModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    permission_classes = [IsAuthenticated]

class ProductPackageViewSet(viewsets.ModelViewSet):
    queryset = ProductPackage.objects.all()
    serializer_class = ProductPackageSerializer
    permission_classes = [IsAuthenticated]

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

class StockViewSet(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    permission_classes = [IsAuthenticated]

class InventoryMovementViewSet(viewsets.ModelViewSet):
    queryset = InventoryMovementLog.objects.all()
    serializer_class = InventoryMovementSerializer
    permission_classes = [IsAuthenticated]


# class StockTransferViewSet(viewsets.ModelViewSet):
#     queryset = StockTransfer.objects.all().order_by('-created_at')
#     serializer_class = StockTransferSerializer

#     def update(self, request, *args, **kwargs):
#         transfer = self.get_object()
#         if transfer.status != "PENDING":
#             return Response(
#                 {"detail": "Only pending transfers can be updated."},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#         return super().update(request, *args, **kwargs)

#     @action(detail=True, methods=['post'])
#     def authorize(self, request, pk=None):
#         transfer = self.get_object()
#         if transfer.status != "PENDING":
#             return Response({"detail": "Only pending transfers can be authorized."}, status=400)
#         transfer.status = "IN_PROGRESS"
#         transfer.save()
#         return Response({"detail": "Transfer authorized."}, status=200)

#     @action(detail=True, methods=['post'])
#     def complete(self, request, pk=None):
#         transfer = self.get_object()
#         if transfer.status != "IN_PROGRESS":
#             return Response({"detail": "Only in-progress transfers can be completed."}, status=400)
#         transfer.status = "COMPLETED"
#         transfer.save()
#         return Response({"detail": "Transfer completed successfully."}, status=200)

#     @action(detail=True, methods=['post'])
#     def cancel(self, request, pk=None):
#         transfer = self.get_object()
#         if transfer.status not in ["PENDING", "IN_PROGRESS"]:
#             return Response({"detail": "Only pending or in-progress transfers can be cancelled."}, status=400)
#         transfer.status = "CANCELLED"
#         transfer.save()
#         return Response({"detail": "Transfer cancelled and stock restored."}, status=200)


class StockTransferViewSet(viewsets.ModelViewSet):
    """
    Manages the full lifecycle of stock transfers between warehouses.
    - PENDING: draft stage (quantity locked in source)
    - IN_PROGRESS: authorized and editable (but cannot revert to pending)
    - COMPLETED: finalized (stock moved)
    - CANCELLED: reversed (stock restored)
    """
    queryset = StockTransfer.objects.all().order_by('-created_at')
    serializer_class = StockTransferSerializer

    def perform_create(self, serializer):
        transfer = serializer.save()

        if transfer.source_warehouse == transfer.destination_warehouse:
            raise ValueError("Source and destination warehouses cannot be the same.")

        with transaction.atomic():
            source_stock = Stock.objects.select_for_update().filter(
                warehouse=transfer.source_warehouse,
                product=transfer.product
            ).first()

            if not source_stock:
                raise ValueError("Source stock record not found.")

            if source_stock.quantity < transfer.quantity:
                raise ValueError("Insufficient stock in source warehouse.")

            # Deduct available stock and lock the amount
            source_stock.quantity -= transfer.quantity
            source_stock.locked_amount += transfer.quantity
            source_stock.save(update_fields=["quantity", "locked_amount"])

    def perform_update(self, serializer):
        """
        Updates a transfer while ensuring:
        - PENDING and IN_PROGRESS can be modified
        - COMPLETED and CANCELLED cannot
        - Re-locks stock appropriately on source change
        - Prevents reverting IN_PROGRESS to PENDING
        """
        transfer = self.get_object()
        old_status = transfer.status

        if old_status in ["COMPLETED", "CANCELLED"]:
            raise ValueError("Completed or cancelled transfers cannot be updated.")

        old_source = Stock.objects.filter(
            warehouse=transfer.source_warehouse,
            product=transfer.product
        ).first()
        old_quantity = transfer.quantity

        updated_transfer = serializer.save()

        if updated_transfer.source_warehouse == updated_transfer.destination_warehouse:
            raise ValueError("Source and destination warehouses cannot be the same.")

        # Prevent reverting back to pending
        if old_status == "IN_PROGRESS" and updated_transfer.status == "PENDING":
            raise ValueError("Cannot revert an in-progress transfer back to pending.")

        with transaction.atomic():
            # Revert previous lock from old source if product or warehouse changed
            if (
                old_source
                and (
                    old_source.warehouse != updated_transfer.source_warehouse
                    or old_source.product != updated_transfer.product
                    or old_quantity != updated_transfer.quantity
                )
            ):
                old_source.quantity += old_quantity
                old_source.locked_amount -= old_quantity
                old_source.save(update_fields=["quantity", "locked_amount"])

            # Apply new lock if still pending or in progress
            if updated_transfer.status in ["PENDING", "IN_PROGRESS"]:
                new_source = Stock.objects.select_for_update().filter(
                    warehouse=updated_transfer.source_warehouse,
                    product=updated_transfer.product
                ).first()

                if not new_source:
                    raise ValueError("Source stock record not found.")

                if new_source.quantity < updated_transfer.quantity:
                    raise ValueError("Insufficient stock in source warehouse.")

                new_source.quantity -= updated_transfer.quantity
                new_source.locked_amount += updated_transfer.quantity
                new_source.save(update_fields=["quantity", "locked_amount"])

    @action(detail=True, methods=['post'])
    def authorize(self, request, pk=None):
        transfer = self.get_object()
        if transfer.status != "PENDING":
            return Response({"detail": "Only pending transfers can be authorized."}, status=400)

        transfer.status = "IN_PROGRESS"
        transfer.save(update_fields=["status"])
        return Response({"detail": "Transfer authorized successfully."}, status=200)

    # @action(detail=True, methods=['post'])
    # def complete(self, request, pk=None):
    #     """
    #     Completes a transfer:
    #     - Moves stock from source to destination
    #     - Creates destination stock if not found
    #     - Frees locked stock
    #     """
    #     transfer = self.get_object()
    #     if transfer.status != "IN_PROGRESS":
    #         return Response({"detail": "Only in-progress transfers can be completed."}, status=400)

    #     if transfer.source_warehouse == transfer.destination_warehouse:
    #         return Response({"detail": "Source and destination warehouses cannot be the same."}, status=400)

    #     with transaction.atomic():
    #         source_stock = Stock.objects.select_for_update().filter(
    #             warehouse=transfer.source_warehouse,
    #             product=transfer.product
    #         ).first()

    #         if not source_stock or source_stock.locked_amount < transfer.quantity:
    #             return Response({"detail": "Not enough locked stock to complete transfer."}, status=400)

    #         # Release locked stock from source
    #         source_stock.locked_amount -= transfer.quantity
    #         source_stock.save(update_fields=["locked_amount"])

    #         # Add to destination warehouse stock (create if not exists)
    #         dest_stock, created = Stock.objects.get_or_create(
    #             warehouse=transfer.destination_warehouse,
    #             product=transfer.product,
    #             defaults={
    #                 "quantity": 0,
    #                 "locked_amount": 0,
    #                 "unit_price": source_stock.unit_price,
    #                 "total_value": 0
    #             }
    #         )
    #         dest_stock.quantity += transfer.quantity
    #         dest_stock.save(update_fields=["quantity"])

    #         transfer.status = "COMPLETED"
    #         transfer.save(update_fields=["status"])

    #     msg = "Transfer completed successfully."
    #     if created:
    #         msg += " New stock record created in destination warehouse."
    #     return Response({"detail": msg}, status=200)
    @action(detail=True, methods=['post'])
    def complete(self, request, pk=None):
        """
        Completes a transfer:
        - Moves stock from source to destination
        - Creates destination stock if not found
        - Frees locked stock
        """
        transfer = self.get_object()
        if transfer.status != "IN_PROGRESS":
            return Response({"detail": "Only in-progress transfers can be completed."}, status=400)

        if transfer.source_warehouse == transfer.destination_warehouse:
            return Response({"detail": "Source and destination warehouses cannot be the same."}, status=400)

        with transaction.atomic():
            # Step 1: Lock source
            source_stock = Stock.objects.select_for_update().filter(
                warehouse=transfer.source_warehouse,
                product=transfer.product
            ).first()

            if not source_stock or source_stock.locked_amount < transfer.quantity:
                return Response({"detail": "Not enough locked stock to complete transfer."}, status=400)

            # Step 2: Reduce locked stock from source
            source_stock.locked_amount -= transfer.quantity
            source_stock.save(update_fields=["locked_amount"])

            # Step 3: Create or update destination stock safely
            dest_stock = Stock.objects.select_for_update().filter(
                warehouse=transfer.destination_warehouse,
                product=transfer.product
            ).first()

            if not dest_stock:
                # Explicit creation ensures ID generator runs properly
                dest_stock = Stock(
                    product=transfer.product,
                    warehouse=transfer.destination_warehouse,
                    quantity=0,
                    locked_amount=0,
                    unit_price=source_stock.unit_price,
                    total_value=0
                )
                dest_stock.save(force_insert=True)
                created = True
            else:
                created = False

            # Step 4: Add transferred quantity
            dest_stock.quantity += transfer.quantity
            dest_stock.save(update_fields=["quantity"])

            # Step 5: Update transfer status
            transfer.status = "COMPLETED"
            transfer.save(update_fields=["status"])

        msg = "Transfer completed successfully."
        if created:
            msg += " New stock record created in destination warehouse."
        return Response({"detail": msg}, status=200)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """
        Cancels a transfer:
        - Restores locked stock back to available quantity
        """
        transfer = self.get_object()

        if transfer.status not in ["PENDING", "IN_PROGRESS"]:
            return Response({"detail": "Only pending or in-progress transfers can be cancelled."}, status=400)

        with transaction.atomic():
            source_stock = Stock.objects.select_for_update().filter(
                warehouse=transfer.source_warehouse,
                product=transfer.product
            ).first()

            if not source_stock:
                return Response({"detail": "Source stock record not found."}, status=400)

            source_stock.quantity += transfer.quantity
            if source_stock.locked_amount >= transfer.quantity:
                source_stock.locked_amount -= transfer.quantity
            source_stock.save(update_fields=["quantity", "locked_amount"])

            transfer.status = "CANCELLED"
            transfer.save(update_fields=["status"])

        return Response({"detail": "Transfer cancelled and stock restored."}, status=200)