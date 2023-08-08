from django.http import HttpResponse
from django.shortcuts import render, redirect
from ..models import *
from django.core.exceptions import ObjectDoesNotExist


def home(request):
    try:
        if request.session["active_staff_id"] == "":
            return redirect("staff_login")
    except KeyError:
        request.session["active_staff_id"] = ""
        return redirect("staff_home")

    try:
        active_staff = Staff.objects.get(pk=request.session["active_staff_id"])
        context = {
            "staff": active_staff,
            "staff_name_0": active_staff.name[0],
        }
        return render(request, 'aplus_app/staff/home.html', context)
    except ObjectDoesNotExist:
        request.session["active_staff_id"] = ""
        return redirect("staff_home")


def login(request):
    if request.method == "POST":
        staff_id = request.POST['id']
        password = request.POST['password']

        try:
            staff = Staff.objects.get(pk=staff_id)
            if password == staff.password:
                request.session['active_staff_id'] = staff_id
                return redirect("staff_home")
            else:
                request.session['active_staff_id'] = ""
                return HttpResponse("Invalid Logins")
        except ObjectDoesNotExist:
            request.session['active_staff_id'] = ""
            return HttpResponse("UNKOWN")

    return render(request, "aplus_app/staff/login.html")


def logout(request):
    request.session["active_staff_id"] = ""
    return redirect("staff_home")


def rooms(request):
    try:
        if request.session["active_staff_id"] == "":
            return redirect("staff_login")
    except KeyError:
        request.session["active_staff_id"] = ""
        return redirect("staff_home")

    try:
        active_staff = Staff.objects.get(pk=request.session["active_staff_id"])
        context = {
            "staff": active_staff,
            "staff_name_0": active_staff.name[0],
            "groups": Group.objects.all(),
            "rooms": Room.objects.filter(course__lecturer=active_staff)
        }
        return render(request, 'aplus_app/staff/rooms.html', context)
    except ObjectDoesNotExist:
        request.session["active_staff_id"] = ""
        return redirect("staff_home")


def add_course(request):
    try:
        if request.session["active_staff_id"] == "":
            return redirect("staff_login")
    except KeyError:
        request.session["active_staff_id"] = ""
        return redirect("staff_home")

    try:
        active_staff = Staff.objects.get(pk=request.session["active_staff_id"])
        if request.method == 'POST':
            name = request.POST['name']
            rec_level = request.POST['rec_level']
            description = request.POST['description']

            active_staff.add_course(name=name, recommended_level=rec_level, description=description)

            return redirect("staff_home")
    except ObjectDoesNotExist:
        request.session["active_staff_id"] = ""
        return redirect("staff_home")


def add_room(request):
    try:
        if request.session["active_staff_id"] == "":
            return redirect("staff_login")
    except KeyError:
        request.session["active_staff_id"] = ""
        return redirect("staff_home")

    try:
        active_staff = Staff.objects.get(pk=request.session["active_staff_id"])
        if request.method == 'POST':
            name = request.POST['name']
            group_id = request.POST['group_id']
            course_id = request.POST['course_id']

            host = str(request.get_host())
            print(host)
            active_staff.add_room(name=name, group_id=group_id, course_id=course_id, host=host)

            return redirect("staff_rooms")
    except ObjectDoesNotExist:
        request.session["active_staff_id"] = ""
        return redirect("staff_home")


def students(request):
    try:
        if request.session["active_staff_id"] == "":
            return redirect("staff_login")
    except KeyError:
        request.session["active_staff_id"] = ""
        return redirect("staff_home")

    try:
        active_staff = Staff.objects.get(pk=request.session["active_staff_id"])
        context = {
            "staff": active_staff,
            "staff_name_0": active_staff.name[0],
            "groups": Group.objects.all(),
            "rooms": Room.objects.filter(course__lecturer=active_staff),
            "students": Student.objects.all()
        }
        return render(request, 'aplus_app/staff/students.html', context)
    except ObjectDoesNotExist:
        request.session["active_staff_id"] = ""
        return redirect("staff_home")


def student(request, student_id):
    try:
        if request.session["active_staff_id"] == "":
            return redirect("staff_login")
    except KeyError:
        request.session["active_staff_id"] = ""
        return redirect("staff_home")

    try:
        active_staff = Staff.objects.get(pk=request.session["active_staff_id"])
        context = {
            "staff": active_staff,
            "staff_name_0": active_staff.name[0],
            "groups": Group.objects.all(),
            "student": Student.objects.get(pk=student_id),
        }
        return render(request, 'aplus_app/staff/student.html', context)
    except ObjectDoesNotExist:
        request.session["active_staff_id"] = ""
        return redirect("staff_home")


def room(request, room_id):
    try:
        if request.session["active_staff_id"] == "":
            return redirect("staff_login")
    except KeyError:
        request.session["active_staff_id"] = ""
        return redirect("staff_home")

    try:
        active_staff = Staff.objects.get(pk=request.session["active_staff_id"])
        context = {
            "staff": active_staff,
            "staff_name_0": active_staff.name[0],
            "groups": Group.objects.all(),
            "room": Room.objects.get(pk=room_id),
            "students": Student.objects.all()
        }
        return render(request, 'aplus_app/staff/room.html', context)
    except ObjectDoesNotExist:
        request.session["active_staff_id"] = ""
        return redirect("staff_home")


def open_room(request, room_id):
    try:
        if request.session["active_staff_id"] == "":
            return redirect("staff_login")
    except KeyError:
        request.session["active_staff_id"] = ""
        return redirect("staff_home")

    try:
        active_staff = Staff.objects.get(pk=request.session["active_staff_id"])
        room = Room.objects.get(pk=room_id)
        room.open_room()
        return redirect("staff_room", room_id=room_id)
    except ObjectDoesNotExist:
        request.session["active_staff_id"] = ""
        return redirect("staff_home")


def close_room(request, room_id):
    try:
        if request.session["active_staff_id"] == "":
            return redirect("staff_login")
    except KeyError:
        request.session["active_staff_id"] = ""
        return redirect("staff_home")

    try:
        active_staff = Staff.objects.get(pk=request.session["active_staff_id"])
        room = Room.objects.get(pk=room_id)
        room.close_room()
        return redirect("staff_room", room_id=room_id)
    except ObjectDoesNotExist:
        request.session["active_staff_id"] = ""
        return redirect("staff_home")


def reward_plus_1(request, student_id, room_id):
    try:
        if request.session["active_staff_id"] == "":
            return redirect("staff_login")
    except KeyError:
        request.session["active_staff_id"] = ""
        return redirect("staff_home")

    try:
        active_staff = Staff.objects.get(pk=request.session["active_staff_id"])
        active_staff.reward_student(student=Student.objects.get(pk=student_id), room=Room.objects.get(pk=room_id))
        return redirect("staff_room", room_id=room_id)
    except ObjectDoesNotExist:
        request.session["active_staff_id"] = ""
        return redirect("staff_home")


