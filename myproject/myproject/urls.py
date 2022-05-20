from django.urls import path
 
from . import views
 
urlpatterns = [
    path('hello/', views.hello),
    path('writeMedicalAdvice', views.writeMedicalAdvice),
    path('queryMedicalAdvice', views.queryMedicalAdvice),
    path('traceBackward', views.traceBackward),
    path('traceForward', views.traceForward),

    path('writeAdmissionRecord', views.writeAdmissionRecord),
    path('traceAdmissionRecord', views.traceAdmissionRecord),
    path('writeAdtmpRecord', views.writeAdtmpRecord),
    path('judgeFeeErr', views.judgeFeeErr),
    path('judgePathSeqError', views.judgePathSeqError),
    path('judgeRepeatedAdmission', views.judgeRepeatedAdmission),

]
