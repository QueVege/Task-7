from django.shortcuts import render
from django.http import Http404
from django.shortcuts import get_object_or_404
from .models import (
    Company, Work, Worker)
from django.views.generic import (
    View, ListView, DetailView)
import logging


logging.basicConfig(level=logging.DEBUG)


class CompList(ListView):
    model = Company
    template_name = 'work/comp_list.html'
    context_object_name = 'companies'


class CompDetail(DetailView):
    model = Company
    template_name = 'work/comp_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        logging.info("Can you see me?")
        logging.error('Error is here')

        managers = self.get_object().managers.all()

        context['works'] = Work.objects.filter(
                           id__in=[m.id for m in managers])
        return context

class ManagList(DetailView):
    model = Company
    template_name = 'work/manag_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['managers'] = self.get_object().managers.all()
        return context


class WorkerList(ListView):
    model = Worker
    template_name = 'work/worker_list.html'
    context_object_name = 'workers'


class WorkerDetail(DetailView):
    model = Worker
    template_name = 'work/worker_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['workplaces'] = self.get_object().workplaces.all()
        return context
