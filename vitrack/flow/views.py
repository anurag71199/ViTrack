from django.shortcuts import render, redirect

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse
from flow.models import patient
from flow.models import doctor
from flow.models import userpic
from flow.models import doctorpic
from flow.models import patientreport
from flow.models import vital
from flow.models import patdoc
from flow.models import habits
from flow.models import querylog
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from statistics import mode
from django.views.generic import CreateView
from django.views.generic import TemplateView
from .forms import picform
from .forms import docpicform
from .forms import reportform
import pickle
from datetime import date
import random
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

def index(request):
    return render(request, 'flow/index.html')

def about(request):
    return render(request, 'flow/about.html')

def doctorlogin(request):
    return render(request, 'flow/doctorlogin.html')

def userlogin(request):
    return render(request, 'flow/userlogin.html')

def register(request):
    return render(request, 'flow/register.html')

def doctorreg(request):
    if request.method=='POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        date = request.POST['date']
        gender = request.POST['inlineRadioOptions']
        email = request.POST['email']
        phone = request.POST['phone']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        hospital = request.POST['hospital']
        desig = request.POST['desig']
        spec = request.POST['spec']
        # print(fname, lname, date, gender, email, phone)
        if len(fname)<2 or len(lname)<2:
            messages.error(request, "Name should be atleast of 2 characters")
        elif len(phone)<10:
            messages.error(request, "Invalid Phone number")
        elif pass1 != pass2:
            messages.error(request, "Password mismatch")
        else:
            docinfo = doctor(doc_fname = fname, doc_lname=lname, doc_dob=date, gender=gender, email=email, phone=phone, hospital=hospital, designation=desig, specialization=spec)
            docinfo.save()

            myuser = User.objects.create_user(email,email,pass1, first_name=fname, last_name=lname)
            myuser_firstname = fname
            myuser_lastname = lname
            myuser.save()
            messages.success(request, "Dr." + str(fname) + " - Registration Done successfully")
            # return render(request, 'flow/index.html')
            return redirect('flowhome')
    return render(request, 'flow/doctorreg.html')

def userreg(request):
    if request.method=='POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        date = request.POST['date']
        gender = request.POST['inlineRadioOptions']
        email = request.POST['email']
        phone = request.POST['phone']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        # print(fname, lname, date, gender, email, phone)
        if len(fname)<2 or len(lname)<2:
            messages.error(request, "Name should be atleast of 2 characters")
        elif len(phone)<10:
            messages.error(request, "Invalid Phone number")
        elif pass1 != pass2:
            messages.error(request, "Password mismatch")
        else:
            subject = 'Vitrack User Account Verification'
            otp = random.randint(1000,9999)
            message = f'Your otp is {otp} '
            email_from = settings.EMAIL_HOST
            send_mail(subject,message,email_from,[email])
            return render(request, 'flow/useremailverify.html',{
                'fname':fname,'lname':lname, 'date': date, 'gender':gender, 'email': email, 'phone': phone, 'pass1': pass1, 'hiddenotp': otp
            })
    return render(request, 'flow/userreg.html')

def useremailverify(request):
    if request.method == 'POST':
        otp = request.POST['otp']
        hiddenotp = request.POST['hiddenotp']
        fname = request.POST['fname']
        lname = request.POST['lname']
        date = request.POST['date']
        gender = request.POST['gender']
        email = request.POST['email']
        phone = request.POST['phone']
        pass1 = request.POST['pass1']
        if otp == hiddenotp:
            userinfo = patient(user_fname=fname, user_lname=lname, user_dob=date, gender=gender, email=email,
                               phone=phone)
            userinfo.save()

            myuser = User.objects.create_user(email, email, pass1, first_name=fname, last_name=lname)
            myuser.save()
            messages.success(request, str(fname) + " - Registration Done successfully")

            #success mail
            template = render_to_string('flow/emailtemplate.html', {'fname': fname})
            subject = 'Welcome to Vitrack'
            message = template
            email_from = settings.EMAIL_HOST
            send_mail(subject, message, email_from, [email])
            return redirect('flowhome')
        else:
            messages.error(request, "Registration Unsuccessful!")
            return redirect("flowhome")
    return HttpResponse("404 - Not found")

def userhome(request):
    # email1 = User.objects.filter(user__username=request.user)
    current_user = request.user
    # flag = 0
    pic = None
    gender = None
    try:
        for p in userpic.objects.raw('SELECT 1 id,email,img FROM flow_userpic'):
            # print(p.email)
            if current_user.email == p.email:
                pic = p.img
                # print("here")
                break
    except userpic.DoesNotExist:
         pic = None
    # print(pic)
    # print(current_user.email)
    for p in patient.objects.raw('SELECT 1 id,email,gender FROM flow_patient'):
        if current_user.email == p.email:
            gender = p.gender
    return render(request, 'flow/userhome.html',{"gender" : gender,"pic" : pic})

def doctorhome(request):
    current_user = request.user
    pic = None
    gender = None
    try:
        for p in doctorpic.objects.raw('SELECT 1 id,email,img FROM flow_doctorpic'):
            if current_user.email == p.email:
                pic = p.img
                break
    except doctorpic.DoesNotExist:
        pic = None
    # print(current_user.email)
    for p in doctor.objects.raw('SELECT 1 id,email,gender FROM flow_doctor'):
        if current_user.email == p.email:
            gender = p.gender
    docs = []
    for p in patdoc.objects.raw('SELECT 1 id,doc_email,patient_email FROM flow_patdoc'):
        if p.doc_email == current_user.email:
            docs.append(p.patient_email)
    all = []
    temp = []
    dp = []
    # print(docs)
    for i in docs:
        temp.extend(list(patientreport.objects.filter(email=i)))
    flag = 0
    for i in temp:
        if i.feedback == "":
            flag=1
            all.append(i)
    if flag == 0:
        return render(request, 'flow/doctorhome.html', {"gender": gender, "pic": pic, 'flag': 0})
    else:
        return render(request, 'flow/doctorhome.html', {"gender": gender, "pic": pic, 'all': all})

def handleLogin(request):
    if request.method == 'POST':
        loginemail = request.POST['loginemail']
        loginpass = request.POST['loginpass']
        # type = request.POST['type']
        for p in patient.objects.raw('SELECT 1 id,email FROM flow_patient'):
            # print(p.email)
            if p.email == loginemail:
                print("yes")
                user = authenticate(username=loginemail,password=loginpass)

                if user is not None:
                    print("None")
                    login(request,user)
                    return redirect('userhome')
                else:
                    print("erzo")
                    messages.error(request, "Invalid Credentials")
                    return redirect("flowhome")
                break
            # else:
        # print("didnt print")
        messages.error(request, "Authetication Fail! Try signing up")
        return redirect("flowhome")
    return HttpResponse("404 - Not found")

def handledocLogin(request):
    if request.method == 'POST':
        loginemail = request.POST['loginemail']
        loginpass = request.POST['loginpass']
        # type = request.POST['type']
        for p in doctor.objects.raw('SELECT 1 id,email FROM flow_doctor'):
            print(p.email)
            if p.email == loginemail:
                print("yes")
                user = authenticate(username=loginemail,password=loginpass)

                if user is not None:
                    print("None")
                    login(request,user)
                    return redirect('doctorhome')
                else:
                    print("erzo")
                    messages.error(request, "Invalid Credentials")
                    return redirect("flowhome")
                break
            # else:
        # print("didnt print")
        messages.error(request, "Authetication Fail! Try signing up")
        return redirect("flowhome")
    return HttpResponse("404 - Not found")

def handleLogout(request):
    logout(request)
    messages.success(request, " Logged out successfully")
    return redirect('flowhome')
    return render(request, 'flow/handleLogout.html')

def userprofile(request):
    current_user = request.user
    pic = None
    try:
        for p in userpic.objects.raw('SELECT 1 id,email,img FROM flow_userpic'):
            if current_user.email == p.email:
                pic = p.img
                break
    except userpic.DoesNotExist:
        pic = None
    for p in patient.objects.raw('SELECT 1 id,email,gender,phone,user_dob FROM flow_patient'):
        if current_user.email == p.email:
            phone = p.phone
            dob = p.user_dob
            gender = p.gender
    return render(request, 'flow/userprofile.html',{"gender" : gender,"pic" : pic,"phone": phone, "dob": dob})

def doctorprofile(request):
    current_user = request.user
    pic = None
    try:
        for p in doctorpic.objects.raw('SELECT 1 id,email,img FROM flow_doctorpic'):
            if current_user.email == p.email:
                pic = p.img
                break
    except userpic.DoesNotExist:
        pic = None
    for p in doctor.objects.raw('SELECT 1 id,email,gender,phone,doc_dob,hospital,designation,specialization FROM flow_doctor'):
        if current_user.email == p.email:
            phone = p.phone
            dob = p.doc_dob
            gender = p.gender
            hospital = p.hospital
            designation = p.designation
            specialization = p.specialization
    return render(request, 'flow/doctorprofile.html',{"gender" : gender,"pic" : pic,"phone": phone, "dob": dob,"hospital": hospital,"designation": designation,"specialization": specialization })

# class userpicupload(CreateView):
    # model = userpic
    # form_class = picform
    # template_name = 'flow/userpicupload.html'
def userpicupload(request):
    current_user = request.user
    pic = None
    try:
        for p in userpic.objects.raw('SELECT 1 id,email,img FROM flow_userpic'):
            if current_user.email == p.email:
                pic = p.img
                break
    except userpic.DoesNotExist:
        pic = None
    for p in patient.objects.raw('SELECT 1 id,email,gender FROM flow_patient'):
        if current_user.email == p.email:
            gender = p.gender
    if request.method == 'POST':
        form = picform(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('userhome')
    else:
        form = picform()
    return render(request, 'flow/userpicupload.html', {
        'form': form,
        "gender": gender, "pic": pic
    })

def doctorpicupload(request):
    current_user = request.user
    pic = None
    try:
        for p in userpic.objects.raw('SELECT 1 id,email,img FROM flow_doctorpic'):
            if current_user.email == p.email:
                pic = p.img
                break
    except doctorpic.DoesNotExist:
        pic = None
    for p in doctor.objects.raw('SELECT 1 id,email,gender FROM flow_doctor'):
        if current_user.email == p.email:
            gender = p.gender
    if request.method == 'POST':
        form = docpicform(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('doctorhome')
    else:
        form = docpicform()
    return render(request, 'flow/doctorpicupload.html', {
        'form': form,
        "gender": gender, "pic": pic
    })

def uploadreport(request):
    current_user = request.user
    pic = None
    try:
        for p in userpic.objects.raw('SELECT 1 id,email,img FROM flow_userpic'):
            if current_user.email == p.email:
                pic = p.img
                break
    except userpic.DoesNotExist:
        pic = None
    for p in patient.objects.raw('SELECT 1 id,email,gender,phone,user_dob FROM flow_patient'):
        if current_user.email == p.email:
            phone = p.phone
            dob = p.user_dob
            gender = p.gender
    if request.method == 'POST':
        form = reportform(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('userhome')
    else:
        form = reportform()
    return render(request, 'flow/uploadreport.html',{
        'form': form,
        "gender": gender, "pic": pic, "phone": phone, "dob": dob
    })

def viewreport(request):
    current_user = request.user
    flag=0
    pic = None
    try:
        for p in userpic.objects.raw('SELECT 1 id,email,img FROM flow_userpic'):
            if current_user.email == p.email:
                pic = p.img
                break
    except userpic.DoesNotExist:
        pic = None
    for p in patient.objects.raw('SELECT 1 id,email,gender,phone,user_dob FROM flow_patient'):
        if current_user.email == p.email:
            phone = p.phone
            dob = p.user_dob
            gender = p.gender
    # return render(request, 'flow/userprofile.html', {"gender": gender, "pic": pic, "phone": phone, "dob": dob})
    report = patientreport.objects.filter(email = current_user.email)
    if report.exists():
        return render(request,'flow/viewreport.html',{
            'report': report,
            'flag': 0,
            "gender": gender, "pic": pic, "phone": phone, "dob": dob
        })
    else:
        return render(request, 'flow/viewreport.html', {
            'flag': 1,"gender": gender, "pic": pic, "phone": phone, "dob": dob
        })
def searchMatch(query,p):
    query = query.lower()
    if query in p.hospital.lower() or query in p.designation.lower() or query in p.specialization.lower() or query in p.doc_fname.lower() or query in p.doc_lname.lower():
        return p.email
    else:
        return False

def search(request):
    current_user = request.user
    query = request.GET.get('search')
    docs = []
    flag=0
    for p in doctor.objects.raw('SELECT 1 id,email,doc_fname,doc_lname,doc_dob,phone,hospital,designation,specialization FROM flow_doctor'):
        match = searchMatch(query,p)
        if match != False:
            docs.append(match)
    all = []
    dp = []
    for i in docs:
        all.extend(list(doctor.objects.filter(email=i)))
        dp.extend(list(doctorpic.objects.filter(email=i)))
    pic = None
    try:
        for p in userpic.objects.raw('SELECT 1 id,email,img FROM flow_userpic'):
            if current_user.email == p.email:
                pic = p.img
                break
    except userpic.DoesNotExist:
        pic = None
    for p in patient.objects.raw('SELECT 1 id,email,gender FROM flow_patient'):
        if current_user.email == p.email:
            gender = p.gender
    havedp = []
    nodp = []
    flag = 0
    for i in all:
        for j in dp:
            if i.email == j.email:
                havedp.extend(list(doctor.objects.filter(email=i.email)))
                flag = 1
                break
        if flag == 0:
            nodp.extend(list(doctor.objects.filter(email=i.email)))
        flag = 0
    # print(all)
    # print(dp)
    if(all):
        if(dp):
            return render(request, 'flow/doclist.html',{
                'all': all,
                'dp': dp,
                'havedp': havedp,
                'nodp': nodp,
                'flag': 0,"pic": pic,'gender': gender
            })
        else:
            return render(request, 'flow/doclist.html', {
                'all': all,
                'flag': 2,"pic": pic,'gender': gender,
            })

    else:
        return render(request, 'flow/doclist.html',{
            'flag': 1,
            'query': query,"pic": pic,'gender': gender
        })

def doclist(request):
    return render(request, 'flow/doclist.html')

def track(request):
    filename = 'flow/ews_model.sav'
    loaded_model = pickle.load(open(filename, 'rb'))
    pred = loaded_model.predict([[0, 0, 0, 0, 0]])
    # pred = dict(enumerate(arr.flatten(),1))
    return render(request, 'flow/track.html',{
        'pred': pred
    })

def chart(request):
    current_user = request.user
    template_name = 'flow/chart.html'
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    # context["qs"] = vital.objects.filter(email = current_user.email)
    context = vital.objects.filter(email=current_user.email)
    # print(context)
    return render(request, template_name, {
        'context': context
    })

def adddoc(request):
    current_user = request.user
    docmail = request.GET.get('dmail')
    print(docmail)
    count = 0
    for p in patdoc.objects.raw('SELECT 1 id,doc_email,patient_email FROM flow_patdoc'):
        if current_user.email == p.patient_email:
            print(p.patient_email)
            if p.doc_email == docmail:
                print(p.doc_email)
                count = 1
                break
    if count == 0:
        userinfo = patdoc(doc_email=docmail, patient_email=current_user.email)
        userinfo.save()
    return redirect('userhome')

def mydoc(request):
    current_user = request.user
    flag=0
    pic = None
    try:
        for p in userpic.objects.raw('SELECT 1 id,email,img FROM flow_userpic'):
            if current_user.email == p.email:
                pic = p.img
                break
    except userpic.DoesNotExist:
        pic = None
    for p in patient.objects.raw('SELECT 1 id,email,gender FROM flow_patient'):
        if current_user.email == p.email:
            gender = p.gender
    # return render(request, 'flow/userprofile.html', {"gender": gender, "pic": pic, "phone": phone, "dob": dob})
    docs=[]
    for p in patdoc.objects.raw('SELECT 1 id,doc_email,patient_email FROM flow_patdoc'):
        if p.patient_email == current_user.email:
            docs.append(p.doc_email)
    all = []
    dp = []
    for i in docs:
        all.extend(list(doctor.objects.filter(email=i)))
        dp.extend(list(doctorpic.objects.filter(email=i)))

    havedp = []
    nodp = []
    flag = 0
    for i in all:
        for j in dp:
            if i.email == j.email:
                havedp.extend(list(doctor.objects.filter(email=i.email)))
                flag = 1
                break
        if flag == 0:
            nodp.extend(list(doctor.objects.filter(email=i.email)))
        flag = 0
    if (all):
        if (dp):
            return render(request, 'flow/mydoc.html', {
                'all': all,
                'dp': dp,
                'havedp': havedp,
                'nodp': nodp,
                'flag': 0,"pic": pic,'gender': gender,
            })
        else:
            return render(request, 'flow/mydoc.html', {
                'all': all,
                'flag': 2, "pic": pic,'gender': gender,
            })

    else:
        return render(request, 'flow/mydoc.html', {
            'flag': 1,
            "pic": pic,'gender': gender,
        })

def mypatient(request):
    current_user = request.user
    flag=0
    pic = None
    try:
        for p in doctorpic.objects.raw('SELECT 1 id,email,img FROM flow_doctorpic'):
            if current_user.email == p.email:
                pic = p.img
                break
    except doctorpic.DoesNotExist:
        pic = None
    for p in doctor.objects.raw('SELECT 1 id,email,gender FROM flow_doctor'):
        if current_user.email == p.email:
            gender = p.gender
    # return render(request, 'flow/userprofile.html', {"gender": gender, "pic": pic, "phone": phone, "dob": dob})
    docs=[]
    for p in patdoc.objects.raw('SELECT 1 id,doc_email,patient_email FROM flow_patdoc'):
        if p.doc_email == current_user.email:
            docs.append(p.patient_email)
    all = []
    dp = []
    # print(docs)
    for i in docs:
        all.extend(list(patient.objects.filter(email=i)))
        dp.extend(list(userpic.objects.filter(email=i)))
    # all2 = []
    # print(all)
    havedp = []
    nodp = []
    flag = 0
    for i in all:
        for j in dp:
            if i.email == j.email:
                havedp.extend(list(patient.objects.filter(email=i.email)))
                flag = 1
                break
        if flag == 0:
            nodp.extend(list(patient.objects.filter(email=i.email)))
        flag=0
    if (all):
        if (dp):
            return render(request, 'flow/mypatient.html', {
                'all': all,
                'dp': dp,
                'havedp': havedp,
                'nodp': nodp,
                'flag': 0,"pic": pic,'gender': gender
            })
        else:
            return render(request, 'flow/mypatient.html', {
                'all': all,
                'flag': 2, "pic": pic,'gender': gender,
            })

    else:
        return render(request, 'flow/mypatient.html', {
            'flag': 1,
            "pic": pic,'gender': gender
        })

def patreport(request):
    current_user = request.user
    pmail = request.GET.get('pmail')
    print(pmail)
    print(current_user)
    flag = 0
    pic = None
    try:
        for p in doctorpic.objects.raw('SELECT 1 id,email,img FROM flow_doctorpic'):
            if current_user.email == p.email:
                pic = p.img
                break
    except doctorpic.DoesNotExist:
        pic = None
    for p in doctor.objects.raw('SELECT 1 id,email,gender FROM flow_doctor'):
        if current_user.email == p.email:
            gender = p.gender
    report = patientreport.objects.filter(email=pmail)
    if report.exists():
        return render(request, 'flow/docviewreport.html', {
            'report': report,
            'flag': 0,
            "gender": gender, "pic": pic, 'pmail': pmail
        })
    else:
        return render(request, 'flow/docviewreport.html', {
            'flag': 1, "gender": gender, "pic": pic, 'pmail': pmail
        })

def docviewreport(request):
    return render(request, 'flow/docviewreport.html')

def entervital(request):
    current_user = request.user
    pic = None
    try:
        for p in userpic.objects.raw('SELECT 1 id,email,img FROM flow_userpic'):
            if current_user.email == p.email:
                pic = p.img
                break
    except userpic.DoesNotExist:
        pic = None
    for p in patient.objects.raw('SELECT 1 id,email,gender FROM flow_patient'):
        if current_user.email == p.email:
            gender = p.gender
    return render(request, 'flow/entervital.html', {
        "gender": gender, "pic": pic
    })

def vitalstore(request):
    current_user = request.user
    email = current_user.email
    name = current_user.first_name
    if request.method == 'POST':
        sys = request.POST['sys']
        dia = request.POST['dia']
        pulse = request.POST['pulse']
        temp = request.POST['temp']
        spo2 = request.POST['spo2']
        ews = news(int(sys), int(pulse), float(temp), int(spo2))
        vital_instance = vital.objects.create(email=email,name=name,sys=sys,dia=dia,pulse=pulse,temp=temp,spo2=spo2,news=ews)
        return redirect('userhome')

def addfeed(request):
    current_user = request.user
    id = request.GET.get('id')
    report = patientreport.objects.filter(report_id=id)
    return render(request,'flow/addfeedback.html',{
        'report': report}
    )

def addfeedback(request):
    return render(request,'flow/addfeedback.html')

def feedbackprocess(request):
    if request.method == 'POST':
        id = request.POST['rep_id']
        feedback = request.POST['feedback']
        patientreport.objects.filter(report_id=id).update(feedback=feedback)
        return redirect('doctorhome')

def alldocs(request):
    current_user = request.user
    pic = None
    try:
        for p in userpic.objects.raw('SELECT 1 id,email,img FROM flow_userpic'):
            if current_user.email == p.email:
                pic = p.img
                break
    except userpic.DoesNotExist:
        pic = None
    for p in patient.objects.raw('SELECT 1 id,email,gender FROM flow_patient'):
        if current_user.email == p.email:
            gender = p.gender
    docs = doctor.objects.all()
    docpics = doctorpic.objects.all()
    havedp=[]
    nodp=[]
    flag=0
    for i in docs:
        for j in docpics:
            if i.email == j.email:
                havedp.extend(list(doctor.objects.filter(email=i.email)))
                flag = 1
                break
        if flag == 0:
            nodp.extend(list(doctor.objects.filter(email=i.email)))
        flag = 0
    return render(request,'flow/alldocs.html',{
        'docs': docs, 'pic': pic, 'gender':gender, 'havedp': havedp, 'nodp': nodp, 'dp': docpics
    })

def trackcontrol(request):
    current_user = request.user
    pic = None
    try:
        for p in userpic.objects.raw('SELECT 1 id,email,img FROM flow_userpic'):
            if current_user.email == p.email:
                pic = p.img
                break
    except userpic.DoesNotExist:
        pic = None
    for p in patient.objects.raw('SELECT 1 id,email,gender FROM flow_patient'):
        if current_user.email == p.email:
            gender = p.gender
    return render(request, 'flow/trackcontrol.html',{
        'pic': pic, 'gender': gender,
    })

def getstarted(request):
    current_user = request.user
    pic = None
    try:
        for p in userpic.objects.raw('SELECT 1 id,email,img FROM flow_userpic'):
            if current_user.email == p.email:
                pic = p.img
                break
    except userpic.DoesNotExist:
        pic = None
    for p in patient.objects.raw('SELECT 1 id,email,gender FROM flow_patient'):
        if current_user.email == p.email:
            gender = p.gender
    return render(request, 'flow/getstarted.html',{
        'pic': pic, 'gender': gender,
    })
def news(sys,pulse,temp,spo2):
    if (spo2 >= 96):
        spo2 = 0
    elif (spo2 == 94 or spo2 == 95):
        spo2 = 1
    elif (spo2 == 92 or spo2 == 93):
        spo2 = 2
    else:
        spo2 = 3

    if (sys > 110 and sys < 220):
        sys = 0
    elif (sys <= 110 and sys >= 101):
        sys = 1
    elif (sys <= 100 and sys >= 91):
        sys = 2
    elif (sys <= 90 or sys >= 220):
        sys = 3

    if (pulse <= 90 and pulse >= 51):
        pulse = 0
    elif ((pulse >= 91 and pulse <= 110) or (pulse <= 50 and pulse >= 41)):
        pulse = 1
    elif (pulse >= 111 and pulse <= 130):
        pulse = 2
    elif ((pulse >= 131) or (pulse <= 40)):
        pulse = 3

    if (temp <= 100.4 and temp >= 96.9):
        temp = 0
    elif ((temp >= 100.5 and temp <= 102.2) or (temp <= 96.8 and temp >= 95.1)):
        temp = 1
    elif (temp >= 102.3):
        temp = 2
    elif (temp <= 95):
        temp = 3

    sum = sys+pulse+temp+spo2
    return sum
def health_analyze(health):
    if(health<1):
        return 0
    else:
        return 1
def health_metric(news,sys,pulse,temp,spo2):
    if(news==0):
        return 0
    elif(news>=1 and news<=4):
        if(spo2==3 or pulse==3 or temp==3 or sys==3):
            return 2
        else:
            return 1
    elif(news>=5 and news<7):
        return 3
    else:
        return 4

def dashboard(request):
    current_user = request.user
    pic = None
    try:
        for p in userpic.objects.raw('SELECT 1 id,email,img FROM flow_userpic'):
            if current_user.email == p.email:
                pic = p.img
                break
    except userpic.DoesNotExist:
        pic = None
    for p in patient.objects.raw('SELECT 1 id,email,gender FROM flow_patient'):
        if current_user.email == p.email:
            gender = p.gender
    latest = vital.objects.filter(email=current_user.email).last()
    record = vital.objects.filter(email=current_user.email)
    count = record.count()
    health = []
    modeh = 0
    health_score = 0
    ewsflag=0
    if count >= 30:
        ewsflag=1
        for i in record:
            health.append(health_metric(i.news, i.sys, i.pulse, i.temp, i.spo2))
        modeh = mode(health) #ews
        # health_score = health_analyze(modeh) #0 = healthy 1=unhealthy
    ml_active = habits.objects.filter(email=current_user.email)
    filename = 'flow/ews_model.sav'
    loaded_model = pickle.load(open(filename, 'rb'))
    ml_status = 0
    # print(record)
    if ml_active.count() == 0:
        ml_status = 0
        pred = 0
    else:
        ml_status = 1
        for i in habits.objects.raw('SELECT 1 id,email,sleep,smoke,exercise,alcohol,age FROM flow_habits'):
            if current_user.email == i.email:
                sleep = i.sleep
                smoke = i.smoke
                age = i.age
                exercise = i.exercise
                alcohol = i.alcohol
        pred = loaded_model.predict([[sleep, smoke, exercise, alcohol, age]])[0]
    # patientreport.objects.filter(report_id=id).update(feedback=feedback)
    return render(request, 'flow/dashboard.html', {
        'pic': pic, 'gender': gender, 'latest': latest,'ewsflag':ewsflag, 'record': record, 'count': count, 'ml_status': ml_status,'pred':pred,'modeh':modeh
    })
def calculate_age(born):
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))
def age_range(age):
    if(age<30):
        return 0
    elif(age>=30 and age<60):
        return 1
    else:
        return 2
def habitinput(request):
    current_user = request.user
    pic = None
    try:
        for p in userpic.objects.raw('SELECT 1 id,email,img FROM flow_userpic'):
            if current_user.email == p.email:
                pic = p.img
                break
    except userpic.DoesNotExist:
        pic = None
    for p in patient.objects.raw('SELECT 1 id,email,gender FROM flow_patient'):
        if current_user.email == p.email:
            gender = p.gender
    return render(request,'flow/habitinput.html', {
        'pic': pic, 'gender': gender,
    })

def habitstore(request):
    current_user = request.user
    email = current_user.email
    name = current_user.first_name
    #get user age
    for p in patient.objects.raw('SELECT 1 id,email,user_dob FROM flow_patient'):
        if current_user.email == p.email:
            cal_age = p.user_dob
    age = age_range(calculate_age(cal_age))
    if request.method == 'POST':
        sleep = request.POST['sleepradio']
        smoke = request.POST['smokeradio']
        exercise = request.POST['exerciseradio']
        alcohol = request.POST['alcoholradio']
        habit_instance = habits.objects.create(email=email,name=name,age=age,sleep=sleep,smoke=smoke,exercise=exercise,alcohol=alcohol)
        return redirect('dashboard')

def patdashboard(request):
    current_user = request.user
    pmail = request.GET.get('pmail')
    print(pmail)
    print(current_user)
    flag = 0
    pic = None
    try:
        for p in userpic.objects.raw('SELECT 1 id,email,img FROM flow_userpic'):
            if pmail == p.email:
                upic = p.img
                break
    except userpic.DoesNotExist:
        pic = None
    for p in patient.objects.raw('SELECT 1 id,email,gender,user_fname,user_lname FROM flow_patient'):
        if pmail == p.email:
            ugender = p.gender
            ufname = p.user_fname
            ulname = p.user_lname
    try:
        for p in doctorpic.objects.raw('SELECT 1 id,email,img FROM flow_doctorpic'):
            if current_user.email == p.email:
                pic = p.img
                break
    except doctorpic.DoesNotExist:
        pic = None
    for p in doctor.objects.raw('SELECT 1 id,email,gender FROM flow_doctor'):
        if current_user.email == p.email:
            gender = p.gender

    latest = vital.objects.filter(email=pmail).last()
    record = vital.objects.filter(email=pmail)
    count = record.count()
    health = []
    modeh = 0
    health_score = 0
    ewsflag = 0
    if count >= 30:
        ewsflag = 1
        for i in record:
            health.append(health_metric(i.news, i.sys, i.pulse, i.temp, i.spo2))
        modeh = mode(health)  # ews
        # health_score = health_analyze(modeh) #0 = healthy 1=unhealthy
    ml_active = habits.objects.filter(email=pmail)
    filename = 'flow/ews_model.sav'
    loaded_model = pickle.load(open(filename, 'rb'))
    ml_status = 0
    # print(record)
    if ml_active.count() == 0:
        ml_status = 0
        pred = 0
    else:
        ml_status = 1
        for i in habits.objects.raw('SELECT 1 id,email,sleep,smoke,exercise,alcohol,age FROM flow_habits'):
            if pmail == i.email:
                sleep = i.sleep
                smoke = i.smoke
                age = i.age
                exercise = i.exercise
                alcohol = i.alcohol
        pred = loaded_model.predict([[sleep, smoke, exercise, alcohol, age]])[0]
    # patientreport.objects.filter(report_id=id).update(feedback=feedback)
    return render(request, 'flow/docviewdashboard.html', {
        'ufname':ufname,'ulname': ulname,'upic': upic, 'ugender': ugender,'pic': pic, 'gender': gender, 'latest': latest, 'ewsflag': ewsflag, 'record': record, 'count': count,
        'ml_status': ml_status, 'pred': pred, 'modeh': modeh
    })

def docviewdashboard(request):
    return render(request, 'flow/docviewdashboard.html')

def test(request):
    return render(request, 'flow/test.html')

def changepass(request):
    current_user = request.user
    pic = None
    try:
        for p in userpic.objects.raw('SELECT 1 id,email,img FROM flow_userpic'):
            if current_user.email == p.email:
                pic = p.img
                break
    except userpic.DoesNotExist:
        pic = None
    for p in patient.objects.raw('SELECT 1 id,email,gender FROM flow_patient'):
        if current_user.email == p.email:
            gender = p.gender
    return render(request, 'flow/userpicupload.html', {
        "gender": gender, "pic": pic
    })

def chatrep(request):
    current_user = request.user
    user_email = current_user.email
    if request.GET.get('category') == 'problem':
        probcategory = request.GET.get('probcategory')
        if probcategory == 'docprob':
            issue = request.GET.get('docproblog')
            domain = request.GET.get('docprobname')
        elif probcategory == 'webprob':
            issue = request.GET.get('webproblog')
            domain = 'Website Problem'
        elif probcategory == 'otherprob':
            issue = request.GET.get('otherproblog')
            domain = request.GET.get('otherprobdomain')
        query_instance = querylog.objects.create(query_type=probcategory,issue=issue,user_email=user_email,problem_domain=domain,status=False)
    pic = None
    gender = None
    try:
        for p in userpic.objects.raw('SELECT 1 id,email,img FROM flow_userpic'):
            # print(p.email)
            if current_user.email == p.email:
                pic = p.img
                # print("here")
                break
    except userpic.DoesNotExist:
        pic = None
    # print(pic)
    # print(current_user.email)
    for p in patient.objects.raw('SELECT 1 id,email,gender FROM flow_patient'):
        if current_user.email == p.email:
            gender = p.gender
    return render(request, 'flow/userhome.html', {"gender": gender, "pic": pic})

def improve(request):
    current_user = request.user
    pic = None
    try:
        for p in userpic.objects.raw('SELECT 1 id,email,img FROM flow_userpic'):
            if current_user.email == p.email:
                pic = p.img
                break
    except userpic.DoesNotExist:
        pic = None
    for p in patient.objects.raw('SELECT 1 id,email,gender FROM flow_patient'):
        if current_user.email == p.email:
            gender = p.gender
    return render(request, 'flow/improve.html', {
        'pic': pic, 'gender': gender,
    })
