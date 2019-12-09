from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.http import Http404
from django.shortcuts import get_object_or_404
from .models import (
    Company, Work, Worker, WorkTime
    )
from .forms import (
        CreateWorkTime
    )
from django.views.generic import (
    View, ListView, DetailView)
from django.views.generic import FormView
from django.views.generic.detail import SingleObjectMixin
import logging

logger = logging.getLogger('my_log')
logger.setLevel(logging.INFO)


class CompList(ListView):
    model = Company
    template_name = 'work/comp_list.html'
    context_object_name = 'companies'


class CompDetail(DetailView):
    model = Company
    template_name = 'work/comp_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        logger.info('Can you see me?')
        logger.error('Error is here!')

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


class WorkerDisplay(DetailView):
    model = Worker

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['workplaces'] = self.get_object().workplaces.all()
        context['form'] = CreateWorkTime()
        return context


class WorkerWT(SingleObjectMixin, FormView):
    template_name = 'work/worker_detail.html'
    form_class = CreateWorkTime
    initial = {
        'date_start': timezone.now,
        'date_end': timezone.now,
    }
    model = WorkTime

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            wt = form.save(commit=False)

            current_worker = Worker.objects.get(pk=kwargs['pk'])
            wt.worker = current_worker

            wt.save()
            return redirect('work:worker_detail', kwargs['pk'])

        return render(request, self.template_name, {'form': form})


class WorkerDetail(View):

    def get(self, request, *args, **kwargs):
        view = WorkerDisplay.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = WorkerWT.as_view()
        return view(request, *args, **kwargs)
