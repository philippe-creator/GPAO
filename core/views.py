from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Sum
from django.shortcuts import get_object_or_404, redirect, render
from .forms import CustomerOrderForm, CustomerOrderLineForm, MaintenanceTicketForm
from .models import Article, CustomerOrder, ManufacturingOrder, WorkOrder, MaintenanceTicket, Machine, InventoryMovement, RoutingOperation
from .services import compute_mrp, capacity_report, shortage_report, generate_mo_from_confirmed_orders, compute_abc

@login_required
def dashboard(request):
    compute_abc()
    shortage = shortage_report()
    context = {
        'article_count': Article.objects.count(),
        'machine_down': Machine.objects.exclude(status='AVAILABLE').count(),
        'open_maintenance': MaintenanceTicket.objects.exclude(status='RESOLVED').count(),
        'open_mo': ManufacturingOrder.objects.exclude(status='DONE').count(),
        'shortage': shortage[:10],
    }
    return render(request, 'core/dashboard.html', context)

@login_required
def article_list(request):
    compute_abc()
    articles = Article.objects.all().order_by('code')
    return render(request, 'core/article_list.html', {'articles': articles})

@login_required
def mrp_view(request):
    compute_abc()
    mrp, buckets = compute_mrp()
    return render(request, 'core/mrp.html', {'mrp': mrp, 'buckets': buckets})

@login_required
def capacity_view(request):
    report, buckets = capacity_report()
    return render(request, 'core/capacity.html', {'report': report, 'buckets': buckets})

@login_required
def offset_graph_view(request):
    mrp, buckets = compute_mrp()
    rows = []
    for article, records in mrp.items():
        launches = [r for r in records if r.planned_release > 0]
        receipts = [r for r in records if r.planned_receipt > 0]
        rows.append({'article': article, 'launches': launches, 'receipts': receipts})
    return render(request, 'core/decalages.html', {'rows': rows, 'buckets': buckets})

@login_required
def order_list(request):
    orders = CustomerOrder.objects.select_related('customer').prefetch_related('lines__article').order_by('-due_date')
    return render(request, 'core/orders.html', {'orders': orders})

@login_required
def order_create(request):
    if request.method == 'POST':
        form = CustomerOrderForm(request.POST)
        line_form = CustomerOrderLineForm(request.POST)
        if form.is_valid() and line_form.is_valid():
            order = form.save()
            line = line_form.save(commit=False)
            line.order = order
            line.save()
            messages.success(request, 'Commande créée.')
            return redirect('order_list')
    else:
        form = CustomerOrderForm()
        line_form = CustomerOrderLineForm()
    return render(request, 'core/order_form.html', {'form': form, 'line_form': line_form})

@login_required
def order_confirm(request, pk):
    order = get_object_or_404(CustomerOrder, pk=pk)
    order.status = 'CONFIRMED'
    order.save(update_fields=['status', 'updated_at'])
    messages.success(request, 'Commande confirmée.')
    return redirect('order_list')

@login_required
def generate_of(request):
    count = generate_mo_from_confirmed_orders()
    messages.success(request, f'{count} ordre(s) de fabrication généré(s).')
    return redirect('mo_list')

@login_required
def mo_list(request):
    mos = ManufacturingOrder.objects.select_related('article').prefetch_related('work_orders__operation', 'work_orders__machine').order_by('due_date')
    return render(request, 'core/mo_list.html', {'mos': mos})

@login_required
def workorder_status(request, pk, status):
    wo = get_object_or_404(WorkOrder, pk=pk)
    if status in {'PLANNED','IN_PROGRESS','PAUSED','DONE'}:
        wo.status = status
        wo.save(update_fields=['status', 'updated_at'])
        messages.success(request, f'Ordre de travail mis à jour: {status}.')
    return redirect('mo_list')

@login_required
def maintenance_list(request):
    tickets = MaintenanceTicket.objects.select_related('machine').order_by('-opened_on')
    return render(request, 'core/maintenance.html', {'tickets': tickets})

@login_required
def maintenance_create(request):
    if request.method == 'POST':
        form = MaintenanceTicketForm(request.POST)
        if form.is_valid():
            ticket = form.save()
            if ticket.status != 'RESOLVED':
                ticket.machine.status = 'DOWN'
            else:
                ticket.machine.status = 'AVAILABLE'
            ticket.machine.save(update_fields=['status', 'updated_at'])
            messages.success(request, 'Ticket maintenance enregistré.')
            return redirect('maintenance_list')
    else:
        form = MaintenanceTicketForm()
    return render(request, 'core/maintenance_form.html', {'form': form})
