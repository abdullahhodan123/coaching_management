


from django.contrib import admin
from .models import User, ClassRoom, Student
from .models import Attendance


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'role', 'is_staff']
    list_filter = ['role', 'is_staff']
    search_fields = ['username', 'email']


@admin.register(ClassRoom)
class ClassRoomAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'full_name',
        'school_name',
        'classroom',
        'guardian_phone_1',
        'is_approved'
    ]

    list_filter = ['classroom','is_approved']
    search_fields = [
        'full_name',
        'school_name',
        'guardian_phone_1',
    ]



from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = [
        'student',
        'month',
        'year',
        'is_paid',
    ]

    list_filter = [
        'month',
        'year',
        'is_paid',
    ]

    search_fields = [
        'student__user__username',
        'student__user__first_name',
        'student__user__last_name',
    ]

    list_editable = [
        'is_paid',
    ]

    ordering = [
        '-year',
        '-month',
    ]



@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = (
        'student',
        'date',
        'time',
        'status',
    )

    list_filter = (
        'status',
        'date',
    )

    search_fields = (
        'student__full_name',
        'student__user__username',
    )

    date_hierarchy = 'date'

    ordering = ('-date', '-time')

    list_per_page = 25