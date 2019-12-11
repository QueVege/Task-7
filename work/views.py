from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from django.http import Http404
from django.shortcuts import get_object_or_404
from .models import (
    Company, Work, Worker, WorkTime, WorkPlace)
from .forms import (
        CreateWorkTime, )
from django.views.generic import (
    View, ListView, DetailView,CreateView, FormView)
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

        context['works'] = self.get_object().works.all()
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
    model = WorkTime

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            wt = form.save(commit=False)
            current_worker = Worker.objects.get(pk=kwargs['pk'])
            wt.worker = current_worker
            wt.save()
            return redirect('work:worker_detail', kwargs['pk'])
        
        logger.info('Form is invalid')
    
        # return ???
        

class WorkerDetail(View):

    def get(self, request, *args, **kwargs):
        view = WorkerDisplay.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = WorkerWT.as_view()
        return view(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class CreateWork(CreateView):
    model = Work
    fields = ['company', 'name']
    template_name = 'work/create_work.html'
    success_url = '/companies/'


@method_decorator(login_required, name='dispatch')
class Hire(CreateView):
    model = WorkPlace
    fields = ['work', 'worker']
    template_name = 'work/hire.html'
    success_url = '/workers/'

    def form_valid(self, form):
        current_worker = form.cleaned_data['worker']

        logger.info(
            f'Current worker: {current_worker.first_name} {current_worker.last_name}')

        if WorkPlace.objects.filter(worker=current_worker).exists():
            prev_wp = WorkPlace.objects.filter(worker=current_worker).latest('id')

            logger.info(
                f'Change status to Finished for: {prev_wp}')

            prev_wp.status = 3
            prev_wp.save()

        form.save()
        return super().form_valid(form)
