from django.db import models
from django.urls import reverse
# Create your models here.
def incrementrepid():
    lastid = patientreport.objects.all().order_by('report_id').last()
    newid = lastid.report_id + 1
    return newid
class patient(models.Model):
    user_id = models.AutoField
    user_fname = models.CharField(max_length=50)
    user_lname = models.CharField(max_length=50)
    user_dob = models.DateField()
    type = models.CharField(max_length=10)
    gender = models.CharField(max_length=6)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    is_verified = models.BooleanField(default=True)
    timeStamp = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return self.user_fname + ' ' + self.user_lname

class doctor(models.Model):
    doc_id = models.AutoField
    doc_fname = models.CharField(max_length=50)
    doc_lname = models.CharField(max_length=50)
    doc_dob = models.DateField()
    type = models.CharField(max_length=10)
    gender = models.CharField(max_length=6)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    hospital = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    timeStamp = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return 'Dr. ' + self.doc_fname + ' ' + self.doc_lname

class userpic(models.Model):
    # user_fname = models.CharField(max_length=50)
    email = models.EmailField()
    img = models.ImageField(null=True, blank=True, upload_to="flow/images")
    timeStamp = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return self.email
    def get_absolute_url(self):
        return reverse('userhome')#, args=(str(self.id)))

class doctorpic(models.Model):
    # doctor_fname = models.CharField(max_length=50)
    email = models.EmailField()
    img = models.ImageField(null=True, blank=True, upload_to="flow/images")
    timeStamp = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return self.email

class patientreport(models.Model):
    report_id = models.IntegerField(primary_key=True, default=incrementrepid,editable=False)
    email = models.EmailField()
    pname = models.CharField(max_length=100)
    testname = models.CharField(max_length=500)
    refby = models.CharField(max_length=500)
    date_of_report = models.DateField()
    summary = models.TextField(max_length=1000)
    report = models.FileField(upload_to='flow/reports')
    feedback = models.TextField(max_length=1000,default="",blank=True)
    timeStamp = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        time1 = str(self.timeStamp).split(".")
        time2 = time1[0]
        return self.pname + '_'+ time2 + ' : ' + self.testname



class vital(models.Model):
    record_id = models.AutoField
    email = models.EmailField()
    name = models.CharField(max_length=100)
    sys = models.IntegerField()
    dia = models.IntegerField()
    pulse = models.IntegerField()
    temp = models.FloatField()
    spo2 = models.IntegerField()
    news = models.IntegerField(default=100)
    timeStamp = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        time1 = str(self.timeStamp).split(".")
        time2 = time1[0]
        return self.name + '_'+ time2

class patdoc(models.Model):
    relation_id= models.AutoField
    doc_email = models.CharField(max_length=50)
    patient_email = models.CharField(max_length=50)
    timeStamp = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return self.patient_email + '<->' + self.doc_email

class habits(models.Model):
    pat_id = models.AutoField
    email = models.EmailField()
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    sleep = models.IntegerField()
    smoke = models.IntegerField()
    exercise = models.IntegerField()
    alcohol = models.IntegerField()
    timeStamp = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        return self.name