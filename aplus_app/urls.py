from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .student import views as student_views
from .views import index

urlpatterns = [
    path('', index, name="app_index"),
    path('staff/', include('aplus_app.staff.urls')),
    path('student/', include('aplus_app.student.urls')),
    path('qrcode/attend/<str:room_id>', student_views.attend_room_with_qrcode, name='attend_room_with_qrcode')
]


