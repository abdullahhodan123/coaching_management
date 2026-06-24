from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from datetime import datetime
from django.shortcuts import render, get_object_or_404
from .models import Student, Payment, ClassRoom, Attendance
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from datetime import date, time, datetime
from django.utils import timezone
import requests
import threading
from django.conf import settings
 
from .forms import (
    StudentRegistrationForm,
    TeacherRegistrationForm,
    UserLoginForm
)



# ─────────────────────────────────────────
#  SMS Utilities
# ─────────────────────────────────────────
 
def format_bd_number(phone):
    number = phone.strip().replace(' ', '').replace('-', '')
    if number.startswith('0'):
        return '88' + number
    return number
 
 
def send_sms(to_number, message):
    number = format_bd_number(to_number)
    url = "http://bulksmsbd.net/api/smsapi"
    params = {
        'api_key':  settings.BULKSMS_API_KEY,
        'type':     'text',
        'number':   number,
        'senderid': settings.BULKSMS_SENDER_ID,
        'message':  message,
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        if data.get('response_code') == 202:
            print(f"✅ SMS sent to {number}")
            return True
        else:
            print(f"❌ SMS failed: {data}")
            return False
    except Exception as e:
        print(f"❌ SMS error: {e}")
        return False
 
 
def send_attendance_sms(student, status, date):
    status_text = "অনুপস্থিত" if status == 'absent' else "দেরিতে এসেছে"
    message = (
        f"প্রিয় অভিভাবক,\n\n"
        f"আপনার সন্তান {student.full_name} "
        f"আজ ({date.strftime('%d/%m/%Y')}) ক্লাসে {status_text}।\n\n"
        f"ধন্যবাদ,\n"
        f"কর্ণফুলী বিজ্ঞান একাডেমি"
    )
    if student.guardian_phone_1:
        send_sms(student.guardian_phone_1, message)
    if student.guardian_phone_2:
        send_sms(student.guardian_phone_2, message)
 
 
def send_attendance_sms_async(student, status, date):
    thread = threading.Thread(
        target=send_attendance_sms,
        args=(student, status, date)
    )
    thread.daemon = True
    thread.start()
 
 
# নতুন: Payment confirmation SMS
def send_payment_sms(student, month, year):
    month_names_bn = {
        1: "জানুয়ারি", 2: "ফেব্রুয়ারি", 3: "মার্চ", 4: "এপ্রিল",
        5: "মে", 6: "জুন", 7: "জুলাই", 8: "আগস্ট",
        9: "সেপ্টেম্বর", 10: "অক্টোবর", 11: "নভেম্বর", 12: "ডিসেম্বর"
    }
    month_name = month_names_bn.get(month, str(month))
 
    message = (
        f"প্রিয় অভিভাবক,\n\n"
        f"আপনার সন্তান {student.full_name}-এর {month_name} {year} "
        f"মাসের বেতন সফলভাবে গ্রহণ করা হয়েছে।\n\n"
        f"ধন্যবাদান্তে,\n"
        f"কর্ণফুলী বিজ্ঞান একাডেমি"
    )
 
    if student.guardian_phone_1:
        send_sms(student.guardian_phone_1, message)
    if student.guardian_phone_2:
        send_sms(student.guardian_phone_2, message)
 
 
def send_payment_sms_async(student, month, year):
    thread = threading.Thread(
        target=send_payment_sms,
        args=(student, month, year)
    )
    thread.daemon = True
    thread.start()
 
 
# ─────────────────────────────────────────
#  Auth Views
# ─────────────────────────────────────────
 
def student_register(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration successful. Wait for approval.")
            return redirect('login')
    else:
        form = StudentRegistrationForm()
 
    return render(request, 'Student_reg.html', {'form': form})
 
 
def teacher_register(request):
    if request.method == 'POST':
        form = TeacherRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Teacher account created successfully.")
            return redirect('login')
    else:
        form = TeacherRegistrationForm()
 
    return render(request, 'teacher_reg.html', {'form': form})
 
 
def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
 
            if user.role == 'student':
                if not user.student.is_approved:
                    messages.error(request, "Your account is not approved yet.")
                    return redirect('login')
 
            login(request, user)
            messages.success(request, "Login successful.")
            return redirect('home')
    else:
        form = UserLoginForm()
 
    return render(request, 'login.html', {'form': form})
 
 
def user_logout(request):
    logout(request)
    messages.success(request, "Logout successful.")
    return redirect('login')
 
 
# ─────────────────────────────────────────
#  Main Views
# ─────────────────────────────────────────
 
# def home(request):
#     return render(request, 'home.html')
 
 
def class_list(request):
    classes = ClassRoom.objects.all()
    return render(request, 'class_list.html', {'classes': classes})
 
 
def student_list(request, class_id):
    now = datetime.now()
    current_month = now.month
    current_year  = now.year
 
    classroom = get_object_or_404(ClassRoom, id=class_id)
    students  = Student.objects.filter(
        classroom=classroom,
        is_approved=True
    ).select_related('user', 'classroom')
 
    student_data = []
    for student in students:
        is_paid = Payment.objects.filter(
            student=student,
            month=current_month,
            year=current_year,
            is_paid=True
        ).exists()
        student_data.append({'student': student, 'is_paid': is_paid})
 
    paid_count = sum(1 for item in student_data if item['is_paid'])
 
    context = {
        'classroom':    classroom,
        'student_data': student_data,
        'month':        current_month,
        'year':         current_year,
        'paid_count':   paid_count,
        'unpaid_count': len(student_data) - paid_count,
    }
    return render(request, 'student_list.html', context)
 
 
@require_POST
def mark_payment(request, student_id):
    now     = datetime.now()
    student = get_object_or_404(Student, id=student_id)
 
    payment, created = Payment.objects.get_or_create(
        student=student,
        month=now.month,
        year=now.year,
        defaults={'is_paid': True}
    )
 
    if not created:
        payment.is_paid = not payment.is_paid
        payment.save()
 
    # নতুন paid হলেই SMS যাবে, unpaid করলে যাবে না
    if payment.is_paid:
        send_payment_sms_async(student, now.month, now.year)
 
    return JsonResponse({'is_paid': payment.is_paid})
 
 
# ─────────────────────────────────────────
#  Attendance View  (SMS যোগ করা হয়েছে)
# ─────────────────────────────────────────
 
@login_required
def take_attendance(request, classroom_id):
    classroom = get_object_or_404(ClassRoom, id=classroom_id)
    students  = Student.objects.filter(classroom=classroom, is_approved=True).order_by('full_name')
    today     = timezone.localdate()
 
    if request.method == 'POST':
        for student in students:
            status = request.POST.get(f'status_{student.id}', 'absent')
 
            attendance, created = Attendance.objects.update_or_create(
                student=student,
                date=today,
                defaults={'status': status}
            )
 
            # শুধু প্রথমবার attendance নেওয়ার সময় SMS যাবে, পরে edit করলে যাবে না
            if created and status in ('absent', 'late'):
                send_attendance_sms_async(student, status, today)
 
        messages.success(request, f"Attendance saved for {today.strftime('%d %B %Y')} ✓")
        return redirect('take_attendance', classroom_id=classroom.id)
 
    # আজকের existing attendance
    existing     = Attendance.objects.filter(student__classroom=classroom, date=today)
    existing_map = {a.student_id: a.status for a in existing}
 
    # Summary
    total_days = Attendance.objects.filter(
        student__classroom=classroom
    ).values('date').distinct().count()
 
    student_summary = []
    for student in students:
        att = Attendance.objects.filter(student=student)
        student_summary.append({
            'student': student,
            'present': att.filter(status='present').count(),
            'absent':  att.filter(status='absent').count(),
            'late':    att.filter(status='late').count(),
            'today':   existing_map.get(student.id, None),
        })
 
    context = {
        'classroom':       classroom,
        'students':        students,
        'today':           today,
        'existing_map':    existing_map,
        'already_taken':   existing.exists(),
        'student_summary': student_summary,
        'total_days':      total_days,
        'total_present':   sum(s['present'] for s in student_summary),
        'total_absent':    sum(s['absent']  for s in student_summary),
        'total_late':      sum(s['late']    for s in student_summary),
    }
    return render(request, 'take_attendance.html', context)





# ─────────────────────────────────────────
#  Teacher Panel — Student Approval
# ─────────────────────────────────────────

@login_required
def pending_students(request):
    # শুধু teacher রাই access করতে পারবে
    if request.user.role != 'teacher':
        messages.error(request, "Access denied.")
        return redirect('home')

    pending = Student.objects.filter(is_approved=False).select_related('user', 'classroom')

    context = {
        'pending_students': pending,
    }
    return render(request, 'pending_students.html', context)


@login_required
@require_POST
def approve_student(request, student_id):
    if request.user.role != 'teacher':
        return JsonResponse({'error': 'Access denied'}, status=403)

    student = get_object_or_404(Student, id=student_id)
    action  = request.POST.get('action')  # 'approve' or 'reject'

    if action == 'approve':
        student.is_approved = True
        student.save()
        return JsonResponse({'status': 'approved', 'name': student.full_name})

    elif action == 'reject':
        student.user.delete()  # Student + User দুটোই delete হবে (CASCADE)
        return JsonResponse({'status': 'rejected'})

    return JsonResponse({'error': 'Invalid action'}, status=400)