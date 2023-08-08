from django.urls import path
from .views import *

urlpatterns = [
    path('home', home, name="student_home"),
    path('course/<str:course_id>', course, name="student_course"),
    path('login', login, name="student_login"),
    path('logout', logout, name="student_logout"),
    path('signup', signup, name="student_signup"),
    path('login_cause_by_qr/<str:room_id>', login_cause_by_qr, name="student_login_cause_by_qr"),
    path('register_course', register_course, name="student_register_course"),
    path('attend_room', attend_room, name="student_attend_room"),
]


