from django.shortcuts import render
from django.http import Http404
from .models import Company
from django.views import generic

def index(request):
    companies = Company.objects.all()
    context = {
        'companies': companies,
    }
    return render(request, 'work/index.html', context)


def detail(request, company_id):
    try:
        company = Company.objects.get(pk=company_id)
    except Company.DoesNotExist:
    	  raise Http404("Company does not exist")
    return render(request, 'work/detail.html', {'company': company})




# class IndexView(generic.ListView):
#     template_name = 'work/index.html'
#     context_object_name = 'companies'

#     def get_queryset(self):
#         return Company.objects.all()


# class DetailView(generic.DetailView):
#     model = Company
#     template_name = 'work/detail.html'

