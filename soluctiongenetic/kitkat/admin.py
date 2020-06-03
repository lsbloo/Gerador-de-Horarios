from django.contrib import admin

# Register your models here.
from .models import Criterion


# Register your models here.

class CriterionAdmin(admin.ModelAdmin):
    list_display = (
        'name','created_at','rate','description'
    )


admin.site.register(Criterion,CriterionAdmin)
