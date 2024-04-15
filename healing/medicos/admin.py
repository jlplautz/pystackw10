from django.contrib import admin

from .models import DadosMedico, Especialidades

# Register your models here.
admin.site.register(Especialidades)
admin.site.register(DadosMedico)
