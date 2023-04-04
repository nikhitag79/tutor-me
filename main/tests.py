from django.test import TestCase, Client
from django.urls import reverse

from main.models import ClassDatabase
from oauth_app.models import User
import djmoney
from djmoney.money import Money



# Create your tests here.
class TestClass(TestCase):
    def test_studentHomePage(self):
        c= Client()
        response=c.get('/student_home/')
        self.assertEqual(response.status_code, 200)

    def test_defaultUserType(self):
        self.tutor = User.objects.create()
        self.assertEqual(self.tutor.user_type, 2)

    def test_declaringTutorType(self):
        self.tutor = User.objects.create(user_type=1)
        self.assertEqual(self.tutor.user_type, 1)

    def test_defaultTutorRate(self):
        self.tutor = User.objects.create(user_type=1)
        self.assertEqual(self.tutor.tutor_rate, djmoney.money.Money('0.0', 'USD'))

    def test_changingTutorRate(self):
        self.tutor = User.objects.create(user_type=1)
        self.tutor.tutor_rate = djmoney.money.Money('10.00', 'USD')
        self.assertEqual(self.tutor.tutor_rate, djmoney.money.Money('10.00', 'USD'))


    # Tutor = 1
    # Student = 2
    # Administration = 3
    # has_selected_role = models.BooleanField(default=False)
    # available_classes = {(Tutor, 'Tutor'), (Student, 'Student'), (Administration, 'Administration')}
    # user_type = models.PositiveIntegerField(choices=available_classes, default=2)
    # tutor_rate = MoneyField(max_digits=4, decimal_places=2, default_currency='USD', default=0.00)

    # def test_my_class_db_values(self):
    #     self.cd = ClassDatabase.objects.create(class_id="CS3240", class_mnen="CS",
    #                                            class_name="Software Dev", professors="Horton")
    #     self.assertEqual(self.cd.class_id, "CS3240")
    #     self.assertEqual(self.cd.class_mnen, "CS")
    #     self.assertEqual(self.cd.class_name, "Software Dev")
    #     self.assertEqual(self.cd.professors, "Horton")

    #
    # def test_course_filter(self):
    #     ClassDatabase.objects.create(class_id="CS3240", class_mnen="CS",
    #                                  class_name="Software Dev", professors="Horton")
    #     ClassDatabase.objects.create(class_id="APMA3100", class_mnen="APMA",
    #                                  class_name="Probability", professors="Ryals")
    #     filtered_classes = ClassDatabase.objects.filter(class_id="CS3240")
    #     self.assertEqual(filtered_classes.count(), 1)
    #     self.assertEqual(filtered_classes.first().professors, "Horton")
    #
    # def test_course_filter_same_mnen(self):
    #     ClassDatabase.objects.create(class_id="CS3240", class_mnen="CS",
    #                                  class_name="Software Dev", professors="Horton")
    #     ClassDatabase.objects.create(class_id="CS1110", class_mnen="CS",
    #                                  class_name="Intro", professors="Ryals")
    #     filtered_classes = ClassDatabase.objects.filter(class_mnen="CS")
    #     self.assertEqual(filtered_classes.count(), 2)
    #
    # def test_student_home_template(self):
    #     self.client = Client()
    #     response = self.client.get(reverse('student_home'))
    #     self.assertTemplateUsed(response, 'main/mnemonic_page.html')
    #
    # def test_student_home_search_template(self):
    #     self.client = Client()
    #     response = self.client.get(reverse('searchbar'))
    #     self.assertTemplateUsed(response, 'main/student_home.html')
    #     self.assertContains(response, '<th> Class id </th>')
    #
    #
# More tests on Friday 3/17