from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView

from finance.forms import AddTransactionForm
from finance.models import Budget, Category, Transaction


class AddBudget(View):
    def get(self, request):
        return render(request, 'finance/add_budget.html')

    def post(self, request):
        name = request.POST.get('name')
        amount = request.POST.get('amount')
        Budget.objects.create(name=name, amount=amount)
        return render(request, 'finance/add_budget.html', {"success": f"Budget added successfully!"})


class MyBudgets(View):
    def get(self, request):
        budgets = Budget.objects.all()
        return render(request, "finance/my_budgets.html", {"budgets": budgets})


class AddTransaction(View):
    def get(self, request):
        form = AddTransactionForm()
        return render(request, "finance/form.html", {"form": form})

    def post(self, request):
        form = AddTransactionForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            description = form.cleaned_data['description']
            category = form.cleaned_data['category']
            Transaction.objects.create(amount=amount, description=description, category=category)
            return redirect("add_transaction")
        return render(request, "finance/form.html", {"form": form})


class AddCategoryView(CreateView):
    model = Category
    fields = "__all__"
    template_name = "finance/add_transaction.html"
    success_url = reverse_lazy("add_category")
