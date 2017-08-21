from django.contrib import admin
from .models import Batch,Member,Fee,FeeDetails
# Register your models here.
admin.site.register(Batch)
admin.site.register(Member)
admin.site.register(Fee)
admin.site.register(FeeDetails)
