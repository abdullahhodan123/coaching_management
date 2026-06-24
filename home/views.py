from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import (
    SiteSettings, Course, Teacher, Result,
    Notice, GalleryImage, FAQ, BatchSchedule
)


def home_view(request):
    settings    = SiteSettings.objects.first()
    courses     = Course.objects.all()
    teachers    = Teacher.objects.all()
    latest_year = Result.objects.values_list("year", flat=True).first()
    results     = Result.objects.filter(year=latest_year) if latest_year else []
    notices     = Notice.objects.all()
    gallery     = GalleryImage.objects.all()[:8]
    faqs        = FAQ.objects.all()
    schedules   = BatchSchedule.objects.select_related("course", "teacher").all()

    is_teacher  = request.user.is_authenticated and request.user.role == 'teacher'

    return render(request, "home.html", {
        "settings":    settings,
        "courses":     courses,
        "teachers":    teachers,
        "results":     results,
        "latest_year": latest_year,
        "notices":     notices,
        "gallery":     gallery,
        "faqs":        faqs,
        "schedules":   schedules,
        "is_teacher":  is_teacher,
    })


@login_required
def notice_add(request):
    if request.user.role != 'teacher':
        return redirect('home')
    if request.method == 'POST':
        Notice.objects.create(
            title=request.POST['title'],
            body=request.POST['body'],
            notice_type=request.POST.get('notice_type', 'general'),
            is_pinned=request.POST.get('is_pinned') == 'on',
        )
    return redirect('home')


@login_required
def notice_edit(request, pk):
    if request.user.role != 'teacher':
        return redirect('home')
    notice = get_object_or_404(Notice, pk=pk)
    if request.method == 'POST':
        notice.title       = request.POST['title']
        notice.body        = request.POST['body']
        notice.notice_type = request.POST.get('notice_type', 'general')
        notice.is_pinned   = request.POST.get('is_pinned') == 'on'
        notice.save()
    return redirect('home')


@login_required
def notice_delete(request, pk):
    if request.user.role != 'teacher':
        return redirect('home')
    notice = get_object_or_404(Notice, pk=pk)
    notice.delete()
    return redirect('home')