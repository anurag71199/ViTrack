from django.contrib import admin

# Register your models here.
from .models import patient
from .models import doctor
from .models import userpic
from .models import doctorpic
from .models import patientreport
from .models import vital
from .models import patdoc
from .models import habits

admin.site.register(patient)
admin.site.register(doctor)
admin.site.register(userpic)
admin.site.register(doctorpic)
admin.site.register(patientreport)
admin.site.register(vital)
admin.site.register(patdoc)
admin.site.register(habits)
