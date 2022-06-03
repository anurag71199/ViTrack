from django.contrib import admin
from django.urls import path
from . import views
from .views import userpicupload
# from flow.views import chartview
from .views import doctorpicupload
# from .views import uploadreport
from django.contrib.auth import views as auth_views
from simple_chatbot.views import SimpleChatbot

urlpatterns = [
    # path('admin/', admin.site.urls),
    path("", views.index, name='flowhome'),
    path("index/", views.index, name='flowhome'),
    path("about/", views.about, name='about'),
    path("search/", views.search, name='search'),
    path("doctorlogin/", views.doctorlogin, name='doctorlogin'),
    path("userlogin/", views.userlogin, name='userlogin'),
    path("register/", views.register, name='register'),
    path("doctorreg/", views.doctorreg, name='doctorreg'),
    path("userreg/", views.userreg, name='userreg'),
    path("useremailverify/", views.useremailverify, name='useremailverify'),
    path("adddoc/", views.adddoc, name='adddoc'),
    path("patreport/", views.patreport, name='patreport'),
    path("docviewreport/", views.docviewreport, name='docviewreport'),
    path("userhome/", views.userhome, name='userhome'),
    path("doctorhome/", views.doctorhome, name='doctorhome'),
    path("handleLogin/", views.handleLogin, name='handleLogin'),
    path("handledocLogin/", views.handledocLogin, name='handledocLogin'),
    path("handleLogout/", views.handleLogout, name='handleLogout'),
    path("userprofile/", views.userprofile, name='userprofile'),
    path("doctorprofile/", views.doctorprofile, name='doctorprofile'),
    path("uploadreport/", views.uploadreport, name='uploadreport'),
    path("viewreport/", views.viewreport, name='viewreport'),
    path("doclist/", views.doclist, name='doclist'),
    path("mydoc/", views.mydoc, name='mydoc'),
    path("mypatient/", views.mypatient, name='mypatient'),
    path("track/", views.track, name='track'),
    path("entervital/", views.entervital, name='entervital'),
    path("userpicupload/", views.userpicupload, name='userpicupload'),
    path("doctorpicupload/", views.doctorpicupload, name='doctorpicupload'),
    path("chart/", views.chart, name='chart'),
    path("vitalstore/", views.vitalstore, name='vitalstore'),
    path("addfeed/", views.addfeed, name='addfeed'),
    path("addfeedback/", views.addfeedback, name='addfeedback'),
    path("feedbackprocess/", views.feedbackprocess, name='feedbackprocess'),
    path("alldocs/", views.alldocs, name='alldocs'),
    path("trackcontrol/", views.trackcontrol, name='trackcontrol'),
    path("getstarted/", views.getstarted, name='getstarted'),
    path("improve/", views.improve, name='improve'),
    path("dashboard/", views.dashboard, name='dashboard'),
    path("habitinput/", views.habitinput, name='habitinput'),
    path("habitstore/", views.habitstore, name='habitstore'),
    path("docviewdashboard/", views.docviewdashboard, name='docviewdashboard'),
    path("patdashboard/", views.patdashboard, name='patdashboard'),
    path("test/", views.test, name='test'),
    path("chatrep/", views.chatrep, name='chatrep'),
    path("simple_chatbot/", SimpleChatbot.as_view()),
    # path("changepass/", views.changepass, name='changepass'),
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='flow/changepass.html'), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='flow/passmailsent.html'), name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='flow/confirmreset.html'), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='flow/passchangecomplete.html'), name="password_reset_complete"),
    # path("uploadreport/", uploadreport.as_view(), name='uploadreport'),
]


