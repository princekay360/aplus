from django.http import HttpResponse
from django.shortcuts import render, redirect
from ..models import *
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages


def home(request):
    try:
        if request.session["active_student_id"] == "":
            return redirect("student_login")
    except KeyError:
        request.session["active_student_id"] = ""
        return redirect("student_home")

    try:
        active_student = Student.objects.get(pk=request.session["active_student_id"])
        context = {
            "me": active_student,
            "me_name_0": active_student.name[0],
            "attend_attempt_log": request.session["attend_attempt_log"]
        }
        request.session["attend_attempt_log"] = {}
        return render(request, 'aplus_app/student/home.html', context)
    except ObjectDoesNotExist:
        request.session["active_student_id"] = ""
        return redirect("student_home")


def login(request):
    if request.method == "POST":
        student_id = request.POST['id']
        password = request.POST['password']

        try:
            student = Student.objects.get(pk=student_id)
            if password == student.password:
                request.session['active_student_id'] = student_id
                return redirect("student_home")
            else:
                request.session['active_student_id'] = ""
                return HttpResponse("Invalid Logins")
        except ObjectDoesNotExist:
            request.session['active_student_id'] = ""
            return HttpResponse("UNKOWN")

    return render(request, "aplus_app/student/login.html")


def logout(request):
    request.session["active_student_id"] = ""
    return redirect("student_home")


def signup(request):
    context = {
        "groups": Group.objects.all()
    }
    if request.method == "POST":
        student_id = request.POST['id']
        full_name = request.POST['full_name']
        level = request.POST['level']
        group_id = request.POST['group_id']
        password = request.POST['password']

        try:
            student = Student.objects.get(pk=student_id)
            return HttpResponse("Student Already Exist")
        except ObjectDoesNotExist:
            new_student = Student(
                id=student_id,
                level=level,
                group=Group.objects.get(pk=group_id),
                password=password,
                name=full_name
            )

            new_student.save()
            request.session['active_student_id'] = student_id
            return redirect("student_home")

    return render(request, "aplus_app/student/signup.html", context)


def register_course(request):
    try:
        if request.session["active_student_id"] == "":
            return redirect("student_login")
    except KeyError:
        request.session["active_student_id"] = ""
        return redirect("student_home")

    try:
        active_student = Student.objects.get(pk=request.session["active_student_id"])
        if request.method == "POST":
            course_id = request.POST['course_id']
            course = Course.objects.get(pk=course_id)
            course.add_student(student=active_student.id)
            return redirect("student_home")
    except ObjectDoesNotExist:
        request.session["active_student_id"] = ""
        return redirect("student_home")


def attend_room(request):
    try:
        if request.session["active_student_id"] == "":
            return redirect("student_login")
    except KeyError:
        request.session["active_student_id"] = ""
        return redirect("student_home")

    try:
        active_student = Student.objects.get(pk=request.session["active_student_id"])
        if request.method == "POST":
            room_id = request.POST["room_id"]
            key = request.POST["key"]

            room = Room.objects.get(pk=room_id)

            if room.key == key:
                a = room.add_attendant(active_student)
                request.session["attend_attempt_log"] = {
                    "msg": a["msg"],
                    "code": a["code"]
                }
                return redirect("student_home")
            else:
                return HttpResponse("<b>Wrong Key</b>")

    except ObjectDoesNotExist:
        request.session["active_student_id"] = ""
        return redirect("student_home")


def attend_room_with_qrcode(request, room_id):
    try:
        if request.session["active_student_id"] == "":
            return redirect("student_login_cause_by_qr", room_id=room_id)
    except KeyError:
        request.session["active_student_id"] = ""
        return redirect("student_login_cause_by_qr", room_id=room_id)

    try:
        active_student = Student.objects.get(pk=request.session["active_student_id"])
        room = Room.objects.get(pk=room_id)
        a = room.add_attendant(active_student)
        request.session["attend_attempt_log"] = {
            "msg": a["msg"],
            "code": a["code"]
        }
        return redirect("student_home")

    except ObjectDoesNotExist:
        request.session["active_student_id"] = ""
        return redirect("student_login_cause_by_qr", room_id=room_id)


def login_cause_by_qr(request, room_id):
    context = {
        "room_id": room_id,
        "room": Room.objects.get(pk=room_id)
    }
    if request.method == "POST":
        student_id = request.POST['id']
        password = request.POST['password']

        try:
            student = Student.objects.get(pk=student_id)
            if password == student.password:
                request.session['active_student_id'] = student_id
                return redirect('attend_room_with_qrcode', room_id=room_id)
            else:
                request.session['active_student_id'] = ""
                return HttpResponse("Invalid Logins")
        except ObjectDoesNotExist:
            request.session['active_student_id'] = ""
            return HttpResponse("UNKOWN")

    return render(request, "aplus_app/student/login_cause_by_qr.html", context)


def course(request, course_id):
    try:
        if request.session["active_student_id"] == "":
            return redirect("student_login")
    except KeyError:
        request.session["active_student_id"] = ""
        return redirect("student_home")

    try:
        active_student = Student.objects.get(pk=request.session["active_student_id"])
        _course = Course.objects.get(pk=course_id)
        context = {
            "me": active_student,
            "me_name_0": active_student.name[0],
            "course": _course
        }
        request.session["attend_attempt_log"] = {}
        return render(request, 'aplus_app/student/course.html', context)
    except ObjectDoesNotExist:
        request.session["active_student_id"] = ""
        return redirect("student_home")
