from django import forms
from .models import CustomerOrder, CustomerOrderLine, MaintenanceTicket

class CustomerOrderForm(forms.ModelForm):
    class Meta:
        model = CustomerOrder
        fields = ['number', 'customer', 'due_date', 'status']
        widgets = {'due_date': forms.DateInput(attrs={'type': 'date'})}

class CustomerOrderLineForm(forms.ModelForm):
    class Meta:
        model = CustomerOrderLine
        fields = ['article', 'quantity']

class MaintenanceTicketForm(forms.ModelForm):
    class Meta:
        model = MaintenanceTicket
        fields = ['machine', 'title', 'description', 'status', 'opened_on', 'resolved_on']
        widgets = {
            'opened_on': forms.DateInput(attrs={'type': 'date'}),
            'resolved_on': forms.DateInput(attrs={'type': 'date'}),
        }
