from django.test import TestCase, Client
# Client allows us to make test requests to our application
# https://docs.djangoproject.com/en/2.2/topics/testing/tools/#overview-and-a-quick-example
from django.contrib.auth import get_user_model
from django.urls import reverse
# reverse allows us to generate urls for our admin page
# https://docs.djangoproject.com/en/3.1/ref/contrib/admin/


class AdminSiteTests(TestCase):
    def setUp(self):
        """setUp function that runs before each test"""
        # ! Add a client variable setted to the Client(). So though self
        # ! we can have access to this variable
        self.client = Client()
        # ! create a new superuser and set to admin_user
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@test.com',
            password='password123'
        )
        # + uses the client helper function (force_login) to login the user
        # + with django authentication
        self.client.force_login(self.admin_user)
        # ! create a normal user
        self.user = get_user_model().objects.create_user(
            email='noral_user@test.com',
            password='password123',
            name='Normal user full name'
        )

    def test_users_listed(self):
        """TEst that users are listed on user page"""
        # {{ app_label }}_{{ model_name }}_changelist, django docs
        # this method will dynamically generate the url for our admin page
        # so we don't need to hard code
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        """Test that the user edit page works"""
        # ! url = /admin/core/user/1
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test that create user page works"""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
