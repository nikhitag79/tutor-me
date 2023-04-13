from django.test import TestCase, Client, RequestFactory
from django.urls import reverse
from django.utils import timezone
from django.contrib.sessions.middleware import SessionMiddleware
from main.models import ClassDatabase, Event 
from main.views import update ,remove , account 
from oauth_app.models import User
import djmoney
from djmoney.money import Money
from datetime import datetime, timedelta
from django.contrib.auth.models import Group, UserManager



# Create your tests here.
class TestClass(TestCase):

    # def setUp(self):
    #     self.tutor = User.objects.create(user_type=1)
    #     self.student = User.objects.create(user_type=2)
    # teardown
    def test_studentHomePage(self):
        c = Client()
        response = c.get('/student_home/')
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

    def test_add_event(self):
        self.group = Group.objects.create(name='Test Group', id=9)
        # self.tutor = User.objects.create(user_type=1, username="tutor_name", id=10, password='testpass')
        self.tutor = User.objects.create_user(user_type=1, username="tutor_name", id=10, password='testpass')
        # self.student = User.objects.create_user(user_type=2, username="student", id=11)
        # self.student = User.objects.create(user_type=2, id=11)
        self.group.user_set.add(self.tutor)
        self.group.save()

        start_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        end_time = (datetime.now() + timedelta(minutes=60)).strftime('%Y-%m-%d %H:%M:%S')
        params = {'title': 'Test Group', 'start': start_time, 'end': end_time, 'group': 'Test Group',
                  'user': self.tutor.id}

        # Log in as the test user
        self.assertTrue(self.client.login(username='tutor_name', password='testpass'))

        # Send the request to the view
        url = reverse('add_event')
        response = self.client.get(url, params)
        # response.user = self.tutor

        # Check that the response contains the expected data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['group'], 'Test Group')

    def test_student_to_mnemonic_on_login(self):
        self.group = Group.objects.create(name='Test Group', id=9)
        self.student = User.objects.create_user(user_type=2, username="student_name", id=10, password='testpass')
        self.group.user_set.add(self.student)
        self.group.save()

        self.assertTrue(self.client.login(username='student_name', password='testpass'))

        response = self.client.get(reverse('student_home'))
        self.assertEqual(str(response.context['user']), 'student_name')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/mnemonic_page.html')

    def test_tutor_to_mnemonic_on_login(self):
        self.group = Group.objects.create(name='Test Group', id=9)
        self.tutor = User.objects.create_user(user_type=1, username="tutor_name", id=9, password='testpass')
        self.group.user_set.add(self.tutor)
        self.group.save()

        self.assertTrue(self.client.login(username='tutor_name', password='testpass'))

        response = self.client.get(reverse('tutor_home'))
        self.assertEqual(str(response.context['user']), 'tutor_name')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/mnemonic_page.html')

    def test_schedule_view(self):
        self.group = Group.objects.create(name='Test Group', id=9)
        self.tutor = User.objects.create_user(user_type=1, username="tutor_name", id=9, password='testpass')
        self.group.user_set.add(self.tutor)
        self.group.save()

        self.assertTrue(self.client.login(username='tutor_name', password='testpass'))

        response = self.client.get(reverse('schedule'))
        self.assertEqual(str(response.context['user']), 'tutor_name')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'main/schedule.html')

    def test_all_events_future(self):
        self.group = Group.objects.create(name='Test Group', id=9)
        self.tutor = User.objects.create_user(user_type=1, username="tutor_name", id=9, password='testpass')
        self.group.user_set.add(self.tutor)
        self.group.save()

        self.assertTrue(self.client.login(username='tutor_name', password='testpass'))
    
        s_time = timezone.now()
        e_time= s_time + timezone.timedelta(hours=2)

        start_time = s_time.strftime('%Y-%m-%d %H:%M:%S')
        end_time = e_time.strftime('%Y-%m-%d %H:%M:%S')

        self.event = Event.objects.create(id=9, name="CS3240 Tutoring 1",tutor = self.tutor, month="June",weekday="Tuesday", start_hour = '12:00', end_hour = '5:00', start='2023-06-13T10:00:00Z',end='2023-06-13T12:00:00Z',)
        url = reverse('all_events')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        print(response.json())
        self.assertEqual(response.json()[0]['title'], 'CS3240 Tutoring 1')


    def test_all_events_past(self):
        self.group = Group.objects.create(name='Test Group', id=9)
        self.tutor = User.objects.create_user(user_type=1, username="tutor_name", id=9, password='testpass')
        self.group.user_set.add(self.tutor)
        self.group.save()

        self.assertTrue(self.client.login(username='tutor_name', password='testpass'))
    
        s_time = timezone.now()
        e_time= s_time + timezone.timedelta(hours=2)

        start_time = s_time.strftime('%Y-%m-%d %H:%M:%S')
        end_time = e_time.strftime('%Y-%m-%d %H:%M:%S')

        self.event = Event.objects.create(id=9, name="CS3240 Tutoring 1",tutor = self.tutor, month="January",weekday="Friday", start_hour = '12:00', end_hour = '5:00', start='2023-01-13T10:00:00Z',end='2023-01-13T12:00:00Z',)
        url = reverse('all_events')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data= response.json()
       # print(response.json())
        self.assertEqual(len(data), 0)
    

    def test_update(self):
         self.factory = RequestFactory()
         self.group = Group.objects.create(name='Test Group', id=9)
         self.tutor = User.objects.create_user(user_type=1, username="tutor_name", id=9, password='testpass')
         self.group.user_set.add(self.tutor)
         self.group.save()

         self.assertTrue(self.client.login(username='tutor_name', password='testpass'))

         self.event = Event.objects.create(id=9,name="CS3240 Tutoring 1",tutor=self.tutor,start=timezone.now(),end=timezone.now() + timezone.timedelta(hours=2))

         request = self.factory.get(
            '/update/',
            {
                'id': 9,
                'title': 'CS3240 New Title',
            }
        )
         update(request)
         updated_event = Event.objects.get(id=9)
         self.assertEqual(updated_event.name, 'CS3240 New Title')

    def test_remove_tutor(self):
        self.factory = RequestFactory()
        self.group = Group.objects.create(name='Test Group', id=9)
        self.tutor = User.objects.create_user(user_type=1, username="tutor_name", id=9, password='testpass')
        self.group.user_set.add(self.tutor)
        self.group.save()

        self.assertTrue(self.client.login(username='tutor_name', password='testpass'))
        self.event = Event.objects.create(id=9,name="CS3240 Tutoring 1",tutor=self.tutor,isAval=False)

        request = self.factory.get('/remove/', {'id': 9})
        request.user = self.tutor

        remove(request)

        #self.assertIsInstance(response, JsonResponse)
        self.assertFalse(Event.objects.filter(id=9).exists())


    def test_remove_student(self):
        self.factory = RequestFactory()
        self.group = Group.objects.create(name='Test Group', id=9)
        self.tutor = User.objects.create_user(user_type=1, username="tutor_name", id=1, password='testpass')
        self.group.user_set.add(self.tutor)
        self.assertTrue(self.client.login(username='tutor_name', password='testpass'))

        self.student = User.objects.create_user(user_type=2, username="student_name", id=9, password='testpass')
        self.group.user_set.add(self.student)
        self.group.save()

        self.assertTrue(self.client.login(username='student_name', password='testpass'))
        self.event = Event.objects.create(id=9,name="CS3240 Tutoring 1",student=self.student,isAval=False)

        request = self.factory.get('/remove/', {'id': 9})
        request.user = self.student

        remove(request)

        #self.assertIsInstance(response, JsonResponse)
        self.assertTrue(Event.objects.filter(id=9).first().isAval)
        self.assertEquals(Event.objects.filter(id=9).first().student, None)

    def test_account_logout(self):
        self.factory = RequestFactory()
        self.group = Group.objects.create(name='Test Group', id=9)
        self.tutor = User.objects.create_user(user_type=1, username="tutor_name", id=1, password='testpass')
        self.group.user_set.add(self.tutor)
        self.assertTrue(self.client.login(username='tutor_name', password='testpass'))
        #request.user = self.tutor

        request = self.factory.post('/account/', {'logout': 'Logout'})
        request.user = self.tutor
        middleware = SessionMiddleware()
        middleware.process_request(request)
        request.session.save()
        account(request)
        self.assertFalse(request.user.is_authenticated)


    def test_account_changeuser(self):
        self.factory = RequestFactory()
        self.group = Group.objects.create(name='Test Group', id=9)
        self.tutor = User.objects.create_user(user_type=1, username="tutor_name", id=1, password='testpass')
        self.group.user_set.add(self.tutor)
        self.assertTrue(self.client.login(username='tutor_name', password='testpass'))
        #request.user = self.tutor

        request = self.factory.post('/account/', {'set_username': 'Set Username', 'username': 'new_username'})
        request.user = self.tutor
        account(request)
        self.tutor.refresh_from_db()
        self.assertEqual(self.tutor.username, 'new_username')
    
    def test_change_rate(self):
        self.factory = RequestFactory()
        self.group = Group.objects.create(name='Test Group', id=9)
        self.tutor = User.objects.create_user(user_type=1, username="tutor_name", id=1, password='testpass')
        self.group.user_set.add(self.tutor)
        self.assertTrue(self.client.login(username='tutor_name', password='testpass'))
        
        request = self.factory.post('/account/', {'set_hourly': 'Set Hourly Rate', 'hourly_rate': '20.00'})
        request.user = self.tutor

        account(request)
        self.tutor.refresh_from_db()
        self.assertEqual(self.tutor.tutor_rate, Money('20.00', 'USD'))


        
        # just starting this, thinking we can test inputting a previous
        # date and making sure it gets deleted & vice versa
        #      not positive what the "day" field is in the model


    # def test_user(self):
    #     self.tutor = User.objects.create(user_type=1)
    #     self.student = User.objects.create(user_type=2)
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
