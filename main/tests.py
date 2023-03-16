from django.test import TestCase, Client

# Create your tests here.
class TestClass(TestCase):
    def test_studentHomePage(self):
        c= Client()
        response=c.get('/student_home/')
        self.assertEqual(response.status_code, 200)

# More tests on Friday 3/17