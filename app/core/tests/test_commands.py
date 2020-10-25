from unittest.mock import patch
from django.core.management import call_command
# https://docs.djangoproject.com/en/3.1/howto/custom-management-commands/#module-django.core.management
# https://docs.djangoproject.com/en/3.1/ref/django-admin/#django.core.management.call_command
# https://stackoverflow.com/questions/52621819/django-unit-test-wait-for-database
from django.db.utils import OperationalError
from django.test import TestCase


class CommandTests(TestCase):
    def test_wait_for_db_ready(self):
        """Test waiting for db when db is available"""
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            # + The way we test if the database is available in Django is using
            # + django.db.utils.ConnectionHandler, this will try to retreive
            # + the default database __getitem__ is the function that
            # + retrieves the database
            gi.return_value = True
            # + the patch() function returns a mock object where we have
            # + two properties:
            # -     return_value
            # -     call_count
            call_command('wait_for_db')
            # + test our command with call_command
            # + wait_for_db could be any name
            self.assertEqual(gi.call_count, 1)

    @patch('time.sleep', return_value=True)
    def test_wait_for_db(self, ts):
        # + When we use patch as a decorator
        # + we can mock the return value as the second argument
        # - we have to add a second argument even if we are not going to use it
        # - if we don't do that it will give us an error
        # * in this case we are mocking the timer, so we can speed up the test
        """Test waiting for db"""
        with patch('django.db.utils.ConnectionHandler.__getitem__') as gi:
            gi.side_effect = [OperationalError] * 5 + [True]
            # + the unittest.mock has side_effect method
            # + we can apply to the function that we are mocking
            # + this way we can force the function rase an error
            call_command('wait_for_db')
            self.assertEqual(gi.call_count, 6)
