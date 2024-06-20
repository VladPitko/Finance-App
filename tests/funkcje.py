from django.urls import reverse


def test_add_budget_view(self):
    response = self.client.get(reverse('add_budget'))
    self.assertEqual(response.status_code, 200)
    response = self.client.post(reverse('add_budget'), {'name': 'Test Budget', 'amount': 1000})
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, 'Budget added successfully!')
