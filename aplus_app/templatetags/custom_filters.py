from django import template
from ..models import *

register = template.Library()


@register.filter(name='get_room_score')
def get_room_score(student: Student, room: Room):
    return student.get_room_score(room=room)


@register.filter(name='get_course_score')
def get_course_score(student: Student, course: Course):
    return student.get_course_score(course=course)


@register.filter(name='get_student_attendance')
def get_student_attendance(course: Course, student: Student):
    c = Course.objects.get(pk=course.id)
    return c.get_student_attendance(student=student)


@register.filter(name='course_has_student')
def course_has_student(course: Course, student: Student):
    c = Course.objects.get(pk=course.id)
    return c.has_student(student=student)


@register.filter(name='has_student')
def has_student(room: Room, student: Student):
    r = Room.objects.get(pk=room.id)
    return r.has_student(student=student)


@register.filter(name='get_attendance')
def get_attendance(student: Student, course: Course):
    return student.get_attendance(course=course)


@register.filter(name='get_recent_rooms')
def get_recent_rooms(staff: Staff, number: int):
    return staff.get_recent_rooms(number=number)


@register.filter(name='student_get_recent_rooms')
def student_get_recent_rooms(student: Student, number: int):
    return student.get_recent_rooms(number=number)
