from django.test import TestCase, Client

from main.models import ClassDatabase


# Create your tests here.
class TestClass(TestCase):
    def test_studentHomePage(self):
        c= Client()
        response=c.get('/student_home/')
        self.assertEqual(response.status_code, 200)

    def test_my_class_db_values(self):
        self.cd = ClassDatabase.objects.create(class_id="CS3240", class_mnen="CS",
                                               class_name="Software Dev", professors="Horton")
        self.assertEqual(self.cd.class_id, "CS3240")
        self.assertEqual(self.cd.class_mnen, "CS")
        self.assertEqual(self.cd.class_name, "Software Dev")
        self.assertEqual(self.cd.professors, "Horton")

    def test_course_filter(self):
        ClassDatabase.objects.create(class_id="CS3240", class_mnen="CS",
                                     class_name="Software Dev", professors="Horton")
        ClassDatabase.objects.create(class_id="APMA3100", class_mnen="APMA",
                                     class_name="Probability", professors="Ryals")
        filtered_classes = ClassDatabase.objects.filter(class_id="CS3240")
        self.assertEqual(filtered_classes.count(), 1)
        self.assertEqual(filtered_classes.first().professors, "Horton")



# More tests on Friday 3/17