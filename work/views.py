from django.shortcuts import render
from django.http import Http404
from .models import Company
from django.views import generic


class IndexView(generic.ListView):
    template_name = 'work/index.html'
    context_object_name = 'companies'

    def get_queryset(self):
        return Company.objects.all()


class DetailView(generic.DetailView):
    model = Company
    template_name = 'work/detail.html'

