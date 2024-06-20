import pytest
from django.urls import reverse
from django.contrib.auth.models import User, Permission
from finance.models import Budget, Category, Transaction, Tag


@pytest.fixture
def category():
    return Category.objects.create(name='Test Category')


@pytest.fixture
def user(db):
    # Ensure the user is created only if it doesn't exist
    if not User.objects.filter(username='testuser').exists():
        User.objects.create_user(username='testuser', password='testpass', email='testuser@example.com')
    return User.objects.get(username='testuser')


@pytest.fixture
def client_logged_in(client, user):
    client.login(username='testuser', password='testpass')
    return client


def test_add_budget_view_get(client_logged_in):
    response = client_logged_in.get(reverse('add_budget'))
    assert response.status_code == 200


def test_add_budget_view_post(client_logged_in):
    response = client_logged_in.post(reverse('add_budget'), {'name': 'Test Budget', 'amount': 1000})
    assert response.status_code == 200
    assert "Budget added successfully!" in response.content.decode()
    assert Budget.objects.filter(name='Test Budget').exists()


def test_my_budgets_view_get(client_logged_in):
    response = client_logged_in.get(reverse('my_budgets'))
    assert response.status_code == 200


def test_my_budgets_view_search(client_logged_in):
    transaction = Transaction.objects.create(amount=100, description='Test Transaction', category=None)
    response = client_logged_in.get(reverse('my_budgets'), {'search': 'Test'})
    assert response.status_code == 200
    assert 'Test Transaction' in response.content.decode()


def test_delete_budget_view_get(client_logged_in):
    budget = Budget.objects.create(name='Test Budget', amount=1000)
    response = client_logged_in.get(reverse('delete_budget', args=[budget.pk]))
    assert response.status_code == 200


def test_delete_budget_view_post(client_logged_in):
    budget = Budget.objects.create(name='Test Budget', amount=1000)
    response = client_logged_in.post(reverse('delete_budget', args=[budget.pk]))
    assert response.status_code == 302  # Redirect after deletion
    assert not Budget.objects.filter(pk=budget.pk).exists()


def test_add_transaction_view_get(client_logged_in):
    response = client_logged_in.get(reverse('add_transaction'))
    assert response.status_code == 200


def test_add_transaction_view_post(client_logged_in):
    category = Category.objects.create(name='Test Category')
    response = client_logged_in.post(reverse('add_transaction'), {
        'amount': 100,
        'description': 'Test Transaction',
        'category': category.pk
    })
    assert response.status_code == 302  # Redirect after successful form submission
    assert Transaction.objects.filter(description='Test Transaction').exists()


def test_transaction_list_view_get(client_logged_in):
    response = client_logged_in.get(reverse('transaction_list'))
    assert response.status_code == 200


def test_transaction_list_view_contents(client_logged_in, category):
    transaction = Transaction.objects.create(amount=100, description='Test Transaction', category=category)
    response = client_logged_in.get(reverse('transaction_list'))
    assert 'Test Transaction' in response.content.decode()


def test_delete_transaction_view_get(client_logged_in):
    category = Category.objects.create(name='Test Category')
    transaction = Transaction.objects.create(amount=100, description='Test Transaction', category=category)
    response = client_logged_in.get(reverse('delete_transaction', args=[transaction.pk]))
    assert response.status_code == 200


def test_delete_transaction_view_post(client_logged_in):
    category = Category.objects.create(name='Test Category')
    transaction = Transaction.objects.create(amount=100, description='Test Transaction', category=category)
    response = client_logged_in.post(reverse('delete_transaction', args=[transaction.pk]))
    assert response.status_code == 302  # Redirect after deletion
    assert not Transaction.objects.filter(pk=transaction.pk).exists()


def test_transaction_update_view_get(client_logged_in):
    category = Category.objects.create(name='Test Category')
    transaction = Transaction.objects.create(amount=100, description='Test Transaction', category=category)
    response = client_logged_in.get(reverse('update_transaction', args=[transaction.pk]))
    assert response.status_code == 200


def test_my_budgets_view_search(client_logged_in, category):
    transaction = Transaction.objects.create(amount=100, description='Test Transaction', category=category)
    response = client_logged_in.get(reverse('my_budgets'), {'search': 'Test'})
    assert response.status_code == 200
    assert 'Test Transaction' in response.content.decode()


def test_add_category_view_get(client_logged_in):
    response = client_logged_in.get(reverse('add_category'))
    assert response.status_code == 200


def test_add_category_view_post(client_logged_in):
    response = client_logged_in.post(reverse('add_category'), {'name': 'New Category'})
    assert response.status_code == 302  # Redirect after successful form submission
    assert Category.objects.filter(name='New Category').exists()


def test_category_list_view_get(client_logged_in):
    response = client_logged_in.get(reverse('category_list'))
    assert response.status_code == 200


def test_category_list_view_contents(client_logged_in):
    category = Category.objects.create(name='Test Category')
    response = client_logged_in.get(reverse('category_list'))
    assert 'Test Category' in response.content.decode()


def test_update_category_view_get(client_logged_in):
    category = Category.objects.create(name='Test Category')
    response = client_logged_in.get(reverse('update_category', args=[category.pk]))
    assert response.status_code == 200


def test_update_category_view_post(client_logged_in, category):
    category = Category.objects.create(name='Test Category')
    response = client_logged_in.post(reverse('update_category', args=[category.pk]), {'name': 'Updated Category'})
    assert response.status_code == 302  # Redirect after update
    category.refresh_from_db()
    assert category.name == 'Updated Category'


def test_delete_category_view_get(client_logged_in, category, user):
    response = client_logged_in.get(reverse('delete_category', args=[category.pk]))
    assert response.status_code == 200


def test_delete_category_view_post(client_logged_in, category, user):
    response = client_logged_in.post(reverse('delete_category', args=[category.pk]))
    assert response.status_code == 302  # Redirect after deletion
    assert not Category.objects.filter(pk=category.pk).exists()


def test_profile_view_get(client_logged_in):
    response = client_logged_in.get(reverse('profile'))
    assert response.status_code == 200


