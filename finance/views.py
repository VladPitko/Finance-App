from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from finance.forms import AddTransactionForm, ProfileForm, TagForm
from finance.models import Budget, Category, Transaction, Profile, Tag


class AddBudget(LoginRequiredMixin, View):
    login_url = "/login/"
    redirect_field_name = "next"

    def get(self, request):
        return render(request, 'finance/add_budget.html')

    def post(self, request):
        name = request.POST.get('name')
        amount = request.POST.get('amount')
        Budget.objects.create(name=name, amount=amount)
        return render(request, 'finance/add_budget.html', {"success": f"Budget added successfully!"})


class MyBudgets(LoginRequiredMixin, ListView):
    login_url = "/login/"
    redirect_field_name = "next"
    model = Budget
    template_name = 'finance/my_budgets.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        recent_transactions = Transaction.objects.order_by('-pk')
        context['recent_transactions'] = recent_transactions

        search_query = self.request.GET.get('search', '')
        context['search_query'] = search_query
        if search_query:
            recent_transactions = recent_transactions.filter(
                Q(description__icontains=search_query) | Q(category__name__icontains=search_query)
            )

        context['recent_transactions'] = recent_transactions
        return context


class DeleteBudget(LoginRequiredMixin, DeleteView):
    login_url = "/login/"
    redirect_field_name = "next"
    model = Budget
    template_name = "finance/delete_form.html"
    success_url = reverse_lazy("my_budgets")


class AddTransaction(LoginRequiredMixin, View):
    login_url = "/login/"
    redirect_field_name = "next"

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


class TransactionList(LoginRequiredMixin, ListView):
    login_url = "/login/"
    redirect_field_name = "next"
    model = Transaction
    template_name = "finance/transaction_list.html"
    context_object_name = 'object_list'  # This ensures the context variable is named object_list

    def get_queryset(self):
        search_query = self.request.GET.get('search', '')
        queryset = Transaction.objects.all()
        if search_query:
            queryset = queryset.filter(
                Q(description__icontains=search_query) | Q(category__name__icontains=search_query)
            )
        return queryset


class DeleteTransactionView(LoginRequiredMixin, DeleteView):
    login_url = "/login/"
    redirect_field_name = "next"
    model = Transaction
    template_name = "finance/delete_form.html"
    success_url = reverse_lazy("transaction_list")


class TransactionUpdate(LoginRequiredMixin, UpdateView):
    login_url = "/login/"
    redirect_field_name = "next"
    model = Transaction
    fields = "__all__"
    template_name = "finance/form.html"

    def get_success_url(self):
        return reverse("update_transaction", args=(self.get_object().pk,))


class AddCategoryView(LoginRequiredMixin, CreateView):
    login_url = "/login/"
    redirect_field_name = "next"
    model = Category
    fields = "__all__"
    template_name = "finance/form.html"
    success_url = reverse_lazy("add_category")


class CategoryList(LoginRequiredMixin, ListView):
    login_url = "/login/"
    redirect_field_name = "next"
    model = Category
    template_name = "finance/category_list.html"


class UpdateCategoryView(LoginRequiredMixin, UpdateView):
    login_url = "/login/"
    redirect_field_name = "next"
    model = Category
    fields = "__all__"
    template_name = "finance/form.html"

    def get_success_url(self):
        return reverse("update_category", args=(self.get_object().pk,))


class DeleteCategoryView(LoginRequiredMixin, DeleteView):
    login_url = "/login/"
    redirect_field_name = "next"

    model = Category
    template_name = "finance/delete_form.html"
    success_url = reverse_lazy("category_list")


@login_required(login_url='/login/')
def profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user_form = request.POST
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)

        if profile_form.is_valid():
            user = request.user
            user.username = user_form['username']
            user.email = user_form['email']
            if user_form['password']:
                user.set_password(user_form['password'])
            user.save()

            profile.bio = request.POST.get('bio', '')
            if 'image' in request.FILES:
                profile.image = request.FILES['image']
            profile.save()

            messages.success(request, 'Profile updated successfully.')
            return redirect('profile')

        messages.error(request, 'Profile update failed. Please correct the errors.')
    else:
        profile_form = ProfileForm(instance=profile)

    context = {
        'user': request.user,
        'profile': profile,
        'profile_form': profile_form,
    }
    return render(request, 'finance/profile.html', context)


@login_required(login_url='/login/')
def tag_list(request):
    tags = Tag.objects.all()
    return render(request, 'finance/tag_list.html', {'tags': tags})


@login_required(login_url='/login/')
def add_tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tag_list')
    else:
        form = TagForm()
    return render(request, 'finance/add_tag.html', {'form': form})


class DeleteTag(LoginRequiredMixin, DeleteView):
    login_url = "/login/"
    redirect_field_name = "next"
    model = Tag
    template_name = "finance/delete_form.html"
    success_url = reverse_lazy("tag_list")
