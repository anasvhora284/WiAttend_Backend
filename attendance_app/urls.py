"""attendance_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from api.views import CreateAttendance,CreateStudent,Login,SignUp,GetAttendance,UploadImage,AddSession,DeleteSession,SessionAuth,WifiAuth

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/create_student', CreateStudent),
    path('api/signup', SignUp),
    path('api/login', Login),
    path('api/create_attendance',CreateAttendance),
    path('api/get_attendance',GetAttendance),
    path('api/upload_image',UploadImage),
    path('api/addsession',AddSession),
    path('api/deletesession/<int:session_id>',DeleteSession),
    path('api/sessionauth/<int:session_id>',SessionAuth),
    path('api/wifiauth/<str:wifi_ip>',WifiAuth)

]
