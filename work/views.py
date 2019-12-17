from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from .models import (
    Company, Work, Worker, WorkTime, WorkPlace)
from .forms import (
        CreateWorkTime, ChangeStatusForm)
from django.views.generic import (
    View, ListView, DetailView, CreateView, FormView, UpdateView)
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.mixins import (
    PermissionRequiredMixin, LoginRequiredMixin
)
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
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
        context['no_approved_wp'] = self.get_object().works.exclude(
                                                    workplaces__status=1)
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['no_approved_wp'] = Worker.objects.exclude(
                                                workplaces__status=1)
        return context


class WorkerDisplay(DetailView):
    model = Worker

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['workplaces'] = self.get_object().workplaces.all()
        context['form'] = CreateWorkTime()
        if 1 in self.get_object().workplaces.values_list('status', flat=True):
            context['working_now'] = True
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
            wt.workplace = current_worker.workplaces.get(status=1)
            wt.save()
            return redirect('work:worker_detail', kwargs['pk'])

        logger.info('Form is invalid') # pragma: no cover
        return render(request, self.template_name, {
                'worker': Worker.objects.get(pk=kwargs['pk']),
                'workplaces': Worker.objects.get(pk=kwargs['pk']).workplaces.all(),
                'working_now': True,
                'form': form
            })
        

class WorkerDetail(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        view = WorkerDisplay.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = WorkerWT.as_view()
        return view(request, *args, **kwargs)


@method_decorator(login_required, name='dispatch')
class CreateWork(PermissionRequiredMixin, CreateView):
    permission_required = 'work.can_create_work'
    raise_exception = True

    model = Work
    fields = ['company', 'name']
    template_name = 'work/create_work.html'
    success_url = '/companies/'


@method_decorator(login_required, name='dispatch')
class Hire(PermissionRequiredMixin, CreateView):
    permission_required = 'work.can_hire'
    raise_exception = True

    model = WorkPlace
    fields = ['work', 'worker']
    template_name = 'work/hire.html'

    def get_success_url(self, **kwargs):
        return reverse('work:worker_detail', kwargs={'pk': self.object.worker.id})


def update_wp(request, pk):
    wp = get_object_or_404(WorkPlace, pk=pk)

    if request.method == "POST":
        form = ChangeStatusForm(request.POST, instance=wp)

        wp = form.save(commit=False)

        if 'approve_btn' in form.data:

            if WorkPlace.objects.filter(worker=wp.worker).filter(status=1).exists():
                prev_wp = WorkPlace.objects.filter(worker=wp.worker).get(status=1)
                prev_wp.status = 3
                prev_wp.save()
                    
            wp.status = 1

            if WorkPlace.objects.filter(worker=wp.worker).filter(status=0).exists():
                all_new_wp = WorkPlace.objects.filter(worker=wp.worker
                                             ).filter(status=0)
                for new_wp in all_new_wp:
                    new_wp.status = 2
                    new_wp.save()

        elif 'cancel_btn' in form.data:
            wp.status = 2

        wp.save()
        return redirect('work:worker_detail', pk=wp.worker.id)
