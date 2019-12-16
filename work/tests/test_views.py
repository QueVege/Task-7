from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
import json

from django.contrib.auth.models import User
 
from work.models import (
    Company, Manager, Work,
    WorkPlace, Worker, WorkTime)

from work.forms import (
        CreateWorkTime, ChangeStatusForm)
 
 
class TestCompaniePage(TestCase):
    def setUp(self):
        self.company_obj = Company.objects.create(
            name="NewCompany"
        )
  
    def test_companies_page(self):
        response = self.client.get(reverse("work:comp_list"))
        self.assertIsNotNone(response.context["companies"])

    def test_company_detail_page(self):
        self.work_obj = Work.objects.create(
            company=self.company_obj,
            name="Python Developer",
        )
        response = self.client.get(reverse("work:comp_detail", kwargs={'pk': self.company_obj.id}))
        self.assertIsNotNone(response.context["company"])
        self.assertIsNotNone(response.context["works"])


class TestManagerPage(TestCase):
    def setUp(self):
        self.company_obj = Company.objects.create(
            name="NewCompany"
        )
        manager_obj = Manager.objects.create(
            company=self.company_obj,
            first_name="First",
            last_name="Manager"
        )

    def test_managers_page(self):
        response = self.client.get(reverse("work:manag_list", kwargs={'pk': self.company_obj.id}))
        self.assertIsNotNone(response.context["managers"])


class TestWorkerPage(TestCase):
    def setUp(self):
        self.date_first = timezone.now()
        self.date_second = timezone.now()
        self.company_obj = Company.objects.create(
            name="NewCompany"
        )
        self.work_obj = Work.objects.create(
            company=self.company_obj,
            name="Python Developer",
        )
        self.worker_obj = Worker.objects.create(
            first_name="First",
            last_name="Worker"
        )
        self.wp_obj = WorkPlace.objects.create(
            work=self.work_obj,
            worker=self.worker_obj,
            status=1
        )

    def test_workers_page(self):
        response = self.client.get(reverse("work:worker_list"))
        self.assertIsNotNone(response.context["workers"])

    def test_worker_detail_page_get(self):
        response = self.client.get(reverse("work:worker_detail", kwargs={'pk': self.worker_obj.id}))
        self.assertIsNotNone(response.context["worker"])
        self.assertIsNotNone(response.context["workplaces"])
        self.assertIsNotNone(response.context["form"])

    def test_create_wt_form(self):
        wt_obj = WorkTime.objects.create(
            date_start=self.date_first,
            date_end=self.date_second,
            worker=self.worker_obj,
            workplace=self.wp_obj
        )
        data = {'date_start': wt_obj.date_start, 'date_end': wt_obj.date_end}
        form = CreateWorkTime(data=data)
        self.assertTrue(form.is_valid())

    # def test_post_wt(self):
    #     data = {
    #         'date_start': self.date_first,
    #         'date_end': self.date_second,
    #         # 'worker': self.worker_obj.id,
    #         # 'workplace': self.wp_obj.id
    #     }
    #     self.client.post(reverse("work:worker_detail", kwargs={'pk': self.worker_obj.id}), data=data)
    #     self.assertEqual(WorkTime.objects.last().workplace.work.name, "Python Developer")
    #     self.assertEqual(WorkTime.objects.last().worker.first_name, "First")


class TestHirePage(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('admin', 'lala@lala.com', '123')
        self.client.login(username='admin', password='123')

        self.company_obj = Company.objects.create(
            name="NewCompany"
        )
        self.work_obj = Work.objects.create(
            company=self.company_obj,
            name="Python Developer",
        )
        self.worker_obj = Worker.objects.create(
            first_name="First",
            last_name="Worker"
        )

    def test_hire_page(self):
        data = {'work': self.work_obj.id, 'worker': self.worker_obj.id}

        self.client.post(reverse("work:hire"), data=data)
        self.assertEqual(WorkPlace.objects.last().work.name, "Python Developer")
        self.assertEqual(WorkPlace.objects.last().worker.first_name, "First")
