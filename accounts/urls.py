from django.urls import path
from . import views



urlpatterns = [
    path(
        'student/register/',
        views.student_register,
        name='student_register'
    ),

    path(
        'teacher/register/',
        views.teacher_register,
        name='teacher_register'
    ),

    path(
        'login/',
        views.user_login,
        name='login'
    ),

    path(
        'logout/',
        views.user_logout,
        name='logout'
    ),
    # path('', views.home, name='home'),

    path('stu_list/<int:class_id>/', views.student_list, name='student_list'),
    path('class_list/',views.class_list,name = 'class_list'),
    path('class/student/<int:student_id>/payment/', views.mark_payment, name='mark_payment'),
    path('classroom/<int:classroom_id>/attendance/',        views.take_attendance,    name='take_attendance'),
    path('pending-students/',             views.pending_students,  name='pending_students'),
    path('approve-student/<int:student_id>/', views.approve_student, name='approve_student'),
    
]
    