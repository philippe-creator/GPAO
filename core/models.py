from django.db import models
from django.utils import timezone

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

class Article(TimeStampedModel):
    TYPE_CHOICES = [
        ('RAW', 'Matière première'),
        ('COMP', 'Composant'),
        ('SFG', 'Semi-fini'),
        ('FG', 'Produit fini'),
    ]
    code = models.CharField(max_length=30, unique=True)
    designation = models.CharField(max_length=255)
    article_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='RAW')
    unit = models.CharField(max_length=20, default='u')
    current_stock = models.FloatField(default=0)
    safety_stock = models.FloatField(default=0)
    reorder_point = models.FloatField(default=0)
    annual_demand = models.FloatField(default=0)
    ordering_cost = models.FloatField(default=0)
    carrying_rate = models.FloatField(default=0.2)
    unit_cost = models.FloatField(default=0)
    lead_time_days = models.PositiveIntegerField(default=0)
    abc_class = models.CharField(max_length=1, blank=True, default='')
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['code']

    def __str__(self):
        return f"{self.code} - {self.designation}"

    @property
    def eoq(self):
        if self.annual_demand <= 0 or self.ordering_cost <= 0 or self.unit_cost <= 0 or self.carrying_rate <= 0:
            return 0
        holding_cost = self.unit_cost * self.carrying_rate
        return ((2 * self.annual_demand * self.ordering_cost) / holding_cost) ** 0.5

    @property
    def suggested_reorder_point(self):
        daily = self.annual_demand / 365 if self.annual_demand else 0
        return round(daily * self.lead_time_days + self.safety_stock, 2)

class Supplier(TimeStampedModel):
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True)
    lead_time_days = models.PositiveIntegerField(default=7)
    def __str__(self):
        return self.name

class Customer(TimeStampedModel):
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True)
    def __str__(self):
        return self.name

class Machine(TimeStampedModel):
    STATUS_CHOICES = [('AVAILABLE', 'Disponible'), ('DOWN', 'En panne'), ('MAINT', 'Maintenance')]
    code = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=255)
    weekly_capacity_hours = models.FloatField(default=40)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='AVAILABLE')
    def __str__(self):
        return f"{self.code} - {self.name}"

class BOM(TimeStampedModel):
    parent = models.ForeignKey(Article, related_name='bom_parents', on_delete=models.CASCADE)
    component = models.ForeignKey(Article, related_name='bom_components', on_delete=models.CASCADE)
    quantity = models.FloatField()
    scrap_rate = models.FloatField(default=0)
    class Meta:
        unique_together = ('parent', 'component')
        ordering = ['parent__code', 'component__code']

class RoutingOperation(TimeStampedModel):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='operations')
    sequence = models.PositiveIntegerField()
    label = models.CharField(max_length=255)
    machine = models.ForeignKey(Machine, null=True, blank=True, on_delete=models.SET_NULL)
    setup_time_hours = models.FloatField(default=0)
    unit_time_hours = models.FloatField(default=0)
    class Meta:
        ordering = ['article', 'sequence']
        unique_together = ('article', 'sequence')
    def __str__(self):
        return f"{self.article.code} - Op {self.sequence}"

class MPSItem(TimeStampedModel):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    week_start = models.DateField()
    quantity = models.FloatField()
    source = models.CharField(max_length=20, default='PDP')
    class Meta:
        ordering = ['week_start', 'article__code']
        unique_together = ('article', 'week_start', 'source')

class ScheduledReceipt(TimeStampedModel):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    due_date = models.DateField()
    quantity = models.FloatField()
    source = models.CharField(max_length=20, default='achat')
    class Meta:
        ordering = ['due_date']

class CustomerOrder(TimeStampedModel):
    STATUS_CHOICES = [('DRAFT', 'Brouillon'), ('CONFIRMED', 'Confirmée')]
    number = models.CharField(max_length=30, unique=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    due_date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='DRAFT')
    def __str__(self):
        return self.number

class CustomerOrderLine(TimeStampedModel):
    order = models.ForeignKey(CustomerOrder, related_name='lines', on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    quantity = models.FloatField()

class ManufacturingOrder(TimeStampedModel):
    STATUS_CHOICES = [('PLANNED', 'Planifié'), ('RELEASED', 'Lancé'), ('IN_PROGRESS', 'En cours'), ('DONE', 'Terminé')]
    number = models.CharField(max_length=30, unique=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    quantity = models.FloatField()
    due_date = models.DateField()
    planned_start = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PLANNED')

class WorkOrder(TimeStampedModel):
    STATUS_CHOICES = [('PLANNED', 'Planifié'), ('IN_PROGRESS', 'En cours'), ('PAUSED', 'En pause'), ('DONE', 'Terminé')]
    manufacturing_order = models.ForeignKey(ManufacturingOrder, related_name='work_orders', on_delete=models.CASCADE)
    operation = models.ForeignKey(RoutingOperation, on_delete=models.CASCADE)
    machine = models.ForeignKey(Machine, null=True, blank=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PLANNED')
    actual_hours = models.FloatField(default=0)
    good_qty = models.FloatField(default=0)
    scrap_qty = models.FloatField(default=0)
    class Meta:
        ordering = ['manufacturing_order', 'operation__sequence']

class InventoryMovement(TimeStampedModel):
    MOVEMENT_TYPES = [('IN', 'Entrée'), ('OUT', 'Sortie'), ('ADJ', 'Ajustement')]
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    movement_type = models.CharField(max_length=10, choices=MOVEMENT_TYPES)
    quantity = models.FloatField()
    reference = models.CharField(max_length=50, blank=True)
    movement_date = models.DateField(default=timezone.now)

class QualityCheck(TimeStampedModel):
    STATUS_CHOICES = [('OK', 'Conforme'), ('NOK', 'Non conforme')]
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    manufacturing_order = models.ForeignKey(ManufacturingOrder, null=True, blank=True, on_delete=models.SET_NULL)
    check_type = models.CharField(max_length=50, default='final')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='OK')
    notes = models.TextField(blank=True)

class MaintenanceTicket(TimeStampedModel):
    STATUS_CHOICES = [('OPEN', 'Ouvert'), ('IN_PROGRESS', 'En cours'), ('RESOLVED', 'Résolu')]
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='OPEN')
    opened_on = models.DateField(default=timezone.now)
    resolved_on = models.DateField(null=True, blank=True)
