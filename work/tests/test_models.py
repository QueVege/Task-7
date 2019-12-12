# from django.contrib.auth.models import User
# from django.test import TestCase
 
# from users.models import Users
# from users.tests.mocks.mock_files import load_file
 
 
# class UserModelsTest(TestCase):
#    def test_user(self):
#        standard_user = User.objects.create_user(
#            username="test",
#            email="test@example.com",
#            password="test_password"
#        )
#        user = Users.objects.create(
#            user=standard_user,
#            photo=load_file()
#        )
#        self.assertEqual(user.user.username, "test")
#        self.assertEqual(user.user.email, "test@example.com")