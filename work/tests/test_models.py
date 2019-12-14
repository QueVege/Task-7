from django.test import TestCase
from django.utils import timezone
 
from work.models import (
    Company, Manager, Work,
    WorkPlace, Worker, WorkTime)

 
class CreatingModelsTest(TestCase):
    def setUp(self):
        self.date_first = timezone.now()
        self.date_second = timezone.now()

        self.company_obj = Company.objects.create(
            name="NewCompany"
        )
        self.work_obj = Work.objects.create(
            company=self.company_obj,
            name="Python Developer",
            created_date=self.date_first
        )
        self.worker_obj = Worker.objects.create(
            first_name="First",
            last_name="Worker"
        )
        self.wp_obj = WorkPlace.objects.create(
            work=self.work_obj,
            worker=self.worker_obj,
        )


    def test_company(self):
        self.assertEqual(self.company_obj.name, "NewCompany")


    def test_manager(self):
        manager_obj = Manager.objects.create(
            company=self.company_obj,
            first_name="First",
            last_name="Manager"
        )
        self.assertEqual(manager_obj.company.name, "NewCompany")
        self.assertEqual(manager_obj.first_name, "First")
        self.assertEqual(manager_obj.last_name, "Manager")


    def test_work(self):
        self.assertEqual(self.work_obj.company.name, "NewCompany")
        self.assertEqual(self.work_obj.name, "Python Developer")
        self.assertEqual(self.work_obj.created_date, self.date_first)


    def test_worker(self):
        self.assertEqual(self.worker_obj.first_name, "First")
        self.assertEqual(self.worker_obj.last_name, "Worker")


    def test_workplace(self):
        self.assertEqual(self.wp_obj.work.name, "Python Developer")
        self.assertEqual(self.wp_obj.worker.first_name, "First")
        self.assertEqual(self.wp_obj.status, 0)


    def test_worktime(self):
        wt_obj = WorkTime.objects.create(
            date_start=self.date_first,
            date_end=self.date_second,
            worker=self.worker_obj,
            workplace=self.wp_obj
        )
        self.assertEqual(wt_obj.date_start, self.date_first)
        self.assertEqual(wt_obj.date_end, self.date_second)
        self.assertEqual(wt_obj.worker.first_name, "First")
        self.assertEqual(wt_obj.workplace.work.name, "Python Developer")
        self.assertEqual(wt_obj.status, 0)
