from django.urls import path
from .views import *

urlpatterns = [
    path('home', home, name="staff_home"),
    path('students', students, name="staff_students"),
    path('room/<str:room_id>', room, name="staff_room"),
    path('reward_plus_1/<str:student_id>&<str:room_id>', reward_plus_1, name="staff_reward_plus_1"),
    path('student/<str:student_id>', student, name="staff_student"),
    path('open_room/<str:room_id>', open_room, name="staff_open_room"),
    path('close_room/<str:room_id>', close_room, name="staff_close_room"),
    path('rooms', rooms, name="staff_rooms"),
    path('login', login, name="staff_login"),
    path('logout', logout, name="staff_logout"),
    path('add_course', add_course, name="staff_add_course"),
    path('add_room', add_room, name="staff_add_room"),
]


