from django import forms
from flow.models import userpic
from flow.models import doctorpic
from flow.models import patientreport
from datetime import datetime

class picform(forms.ModelForm):
    class Meta:
        model = userpic
        fields = ['email','img',]
        labels = {
            "email": "EMAIL ID",
            "img": "Profile Picture"
        }
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-control'})
        }
class docpicform(forms.ModelForm):
    class Meta:
        model = doctorpic
        fields = ['email','img',]
        labels = {
            "email": "EMAIL ID",
            "img": "Profile Picture"
        }
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-control'})
        }

class reportform(forms.ModelForm):
    class Meta:
        model = patientreport
        date_range = 80
        this_year = datetime.now().year
        fields = ['email','pname','testname','refby','date_of_report','summary','report']
        labels = {
            "email": "EMAIL ID",
            "pname": "Patient Name",
            "testname": "Name of the Test",
            "refby": "Referred by: (Doctor/Hospital)",
            "date_of_report": "Date of Report",
            "summary": "Brief Summary of Report",
            "report": "Upload Report (pdf)",
        }
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-control', 'label': 'First Name'}),
            'pname': forms.TextInput(attrs={'class': 'form-control'}),
            'testname': forms.TextInput(attrs={'class': 'form-control'}),
            'refby': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_report': forms.SelectDateWidget(years=range(this_year - date_range, this_year + date_range)),
            'summary': forms.Textarea(attrs={'class': 'form-control'}),
        }

