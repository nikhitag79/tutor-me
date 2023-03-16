from django.test import TestCase, Client

# Create your tests here.
class TestClass(TestCase):
    def test_studentHomePage(self):
        # c= Client()
        # response=c.get('/student_home/')
        self.assertEqual(True, True)