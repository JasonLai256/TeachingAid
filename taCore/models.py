# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User


class Degree(models.Model):
    name = models.CharField(max_length=40)

    def __unicode__(self):
        return "Degree: {0}".format(self.id)

class College(models.Model):
    name = models.CharField(max_length=60)

    def __unicode__(self):
        return "College: {0}".format(self.id)

class Speciality(models.Model):
    name = models.CharField(max_length=60)
    college = models.ForeignKey(College)

    def __unicode__(self):
        return "Speciality: {0}".format(self.id)

class Class(models.Model):
    name = models.CharField(max_length=60)

    def __unicode__(self):
        return "Class: {0}".format(self.id)

class Teacher(models.Model):
    user = models.ForeignKey(User)
    title = models.CharField(max_length=50)
    college = models.ForeignKey(College)
    descript = models.CharField(max_length=1000)
    leading_class = models.ForeignKey(Class)

    def __unicode__(self):
        return "teacher - {0}", self.user


class Student(models.Model):
    user = models.ForeignKey(User)
    degree = models.ForeignKey(Degree)
    college = models.ForeignKey(College)
    speciality = models.ForeignKey(Speciality)
    stuclass = models.ForeignKey(Class)

    def __unicode__(self):
        return "Student - {0}", self.user

class Course(models.Model):
    name = models.CharField(max_length=80)
    teacher = models.ForeignKey(Teacher)
    students = models.ManyToManyField(Student)
    classes = models.ManyToManyField(Class)
    speciality = models.ForeignKey(Speciality)
    college = models.ForeignKey(College)

    def __unicode__(self):
        return "Course: {0}".format(self.id)
    
class Classroom(models.Model):
    name = models.CharField(max_length=50)
    capacity = models.PositiveSmallIntegerField(default=0)
    begintime = models.TimeField()  # time the classroom begin to use
    endtime = models.TimeField()
    status = models.CharField(max_length=30)  # 标识属于一天中的第几节课
    courses = models.ManyToManyField(Course)

    def __unicode__(self):
        return "Classroom: {0}".format(self.id)
    

