from django.shortcuts import render
from django.views import View

from finance.models import Budget


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
        return render(request, "finance/add_transaction.html")