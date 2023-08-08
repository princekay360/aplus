import random
import string
from io import BytesIO
import os
from django.db import models
import qrcode as qrc
from django.http import HttpResponse
from django.core.files import File
from django.conf import settings


def rgen(l):
    letter = string.ascii_uppercase
    u = "".join(random.choice(letter) for i in range(l))
    return u


def rint(l):
    num = ""
    for i in range(l):
        number = random.randint(0, 9)
        num = num + str(number)
    return num


class Staff(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    gender = models.CharField(max_length=10, default="male")
    password = models.TextField()
    img = models.ImageField(upload_to="staff/imgs")

    def add_room(self, name, group_id, course_id, host):
        room_id = ""
        if Course.objects.get(pk=course_id).room_set.all().count() == 0:
            room_id = str(f"{rgen(4)}{course_id[2:]}1")
        else:
            room_id = str(
                f"{rgen(4)}{course_id[2:]}{Course.objects.get(pk=course_id).room_set.all().count() + 1}{rgen(1)}")

        qr = qrc.QRCode(
            version=1,
            error_correction=qrc.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        data_link = f"http://{host}/qrcode/attend/{room_id}"
        qr.add_data(data_link)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        media_dir = os.path.join(settings.MEDIA_ROOT, 'qrcodes')
        if not os.path.exists(media_dir):
            os.makedirs(media_dir)

        file_path = os.path.join(media_dir, f"qr{room_id}.png")
        img.save(file_path)

        new_room = Room(
            id=room_id,
            name=name,
            group=Group.objects.get(pk=group_id),
            course=Course.objects.get(pk=course_id),
            status="Closed",
            qrcode=file_path,
            key=rint(7)
        )

        new_room.save()

    def add_course(self, name, recommended_level, description):
        course_id = ""
        if Course.objects.all().count() == 0:
            course_id = "1"
        else:
            course_id = int(list(Course.objects.all())[-1].id[2:]) + 1
        new_course = Course(
            name=name,
            recommended_level=recommended_level,
            description=description,
            id=str(f"CS{course_id}"),
            lecturer=self
        )

        new_course.save()

    def get_recent_rooms(self, number):
        rooms = Room.objects.filter(course__lecturer=self).order_by('-date')
        return rooms[:number]

    def reward_student(self, student: 'Student', room: 'Room'):
        score = Score.objects.filter(room=room).get(student=student)
        score.score += 1
        score.save()


class Course(models.Model):
    id = models.CharField(max_length=10, primary_key=True)
    name = models.CharField(max_length=100)
    recommended_level = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    lecturer = models.ForeignKey(Staff, on_delete=models.CASCADE)
    registered_students = models.JSONField(default={"data": []})

    def add_student(self, student):
        self.registered_students["data"].append(student)
        self.save()

    def get_total_students(self):
        return len(self.registered_students['data'])

    def has_student(self, student: 'Student'):
        if student.id in self.registered_students['data']:
            return True
        else:
            return False

    def get_student_attendance(self, student: 'Student'):
        total_attendance = 0
        total_room = student.group.room_set.filter(course=self)
        for room in total_room:
            if student.id in room.attendants["data"]:
                total_attendance += 1
        return str(f"{total_attendance}/{total_room.count()}")


class Group(models.Model):
    name = models.CharField(max_length=100)


class Room(models.Model):
    name = models.CharField(max_length=100)
    id = models.CharField(max_length=100, primary_key=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    status = models.CharField(max_length=20)
    attendants = models.JSONField(default={"data": []})
    date = models.DateField(auto_now=True)
    key = models.TextField(default="123456")
    qrcode = models.ImageField(upload_to="qrcodes", default="qrcodes/default", blank=True, null=True)

    def add_attendant(self, student: 'Student'):
        print(self.course.has_student(student))
        log = {}
        if self.status == "Open":
            if student.id in self.attendants['data']:
                log = {
                    "code": 2,
                    "msg": "Already Attend",
                }
                pass
            else:
                if self.course.has_student(student):
                    if student.group == self.group:
                        self.attendants['data'].append(student.id)
                        self.save()
                        new_score = Score(
                            score=1.0,
                            room=self,
                            student=student,
                        )
                        new_score.save()
                        log = {
                            "code": 1,
                            "msg": "Attend Successful",
                        }
                    else:
                        log = {
                            "code": 0,
                            "msg": "Failed! You are not in the required group",
                        }
                else:
                    log = {
                        "code": 0,
                        "msg": "Failed! You are not registered to the course",
                    }
        else:
            log = {
                "code": 0,
                "msg": "Failed! Room is Closed",
            }

        return log

    def get_attendants(self):
        attendants = []
        for _id in self.attendants['data']:
            attendant = Student.objects.get(pk=_id)
            attendants.append(attendant)

        return attendants

    def get_attendance_count(self):
        return len(self.get_attendants())

    def open_room(self):
        self.status = "Open"
        self.save()

    def close_room(self):
        self.status = "Closed"
        self.save()

    def has_student(self, student: 'Student'):
        if student.id in self.attendants['data']:
            return True
        else:
            return False


class Student(models.Model):
    name = models.CharField(max_length=100)
    id = models.CharField(max_length=20, primary_key=True)
    level = models.CharField(max_length=20)
    group = models.ForeignKey(Group, on_delete=models.SET_DEFAULT, default=5)
    password = models.TextField()

    def get_unregistered_courses(self):
        unregistered_courses = []
        for i in Course.objects.all():
            if self.id in i.registered_students["data"]:
                pass
            else:
                unregistered_courses.append(i)

        return unregistered_courses

    def get_registered_courses(self):
        registered_courses = []
        for i in Course.objects.all():
            if self.id in i.registered_students["data"]:
                registered_courses.append(i)
            else:
                pass

        return registered_courses

    def get_attendance(self, course: 'Course'):
        rooms = Room.objects.filter(course=course).filter(group=self.group)
        attend_count = 0
        for room in rooms:
            if self.id in room.attendants["data"]:
                attend_count += 1
        course_rooms_count = Room.objects.filter(course=course).filter(group=self.group).count()
        return str(f'{attend_count}/{course_rooms_count}')

    def get_recent_rooms(self, number):
        rooms = Room.objects.filter(group=self.group).order_by('-date')
        return rooms[:number]

    def get_room_score(self, room: 'Room'):
        score = Score.objects.filter(room=room).get(student=self).score
        return score

    def get_course_score(self, course: 'Course'):
        scores = Score.objects.filter(room__course=course).filter(student=self)
        score = 0
        for _score in scores:
            score = score + _score.score
        return score


class Score(models.Model):
    score = models.FloatField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
