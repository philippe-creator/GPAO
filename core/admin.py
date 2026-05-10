from django.contrib import admin
from .models import *

for model in [Article, Supplier, Customer, Machine, BOM, RoutingOperation, MPSItem, ScheduledReceipt,
              CustomerOrder, CustomerOrderLine, ManufacturingOrder, WorkOrder, InventoryMovement,
              QualityCheck, MaintenanceTicket]:
    admin.site.register(model)
