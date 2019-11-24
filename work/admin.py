from django.contrib import admin
from .models import Company
from .models import Manager
from .models import Work, Position
from .models import Worker


admin.site.register(Company)
admin.site.register(Manager)
admin.site.register(Work)
admin.site.register(Position)
admin.site.register(Worker)
