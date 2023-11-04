from rest_framework import serializers
from .models import Faculty, Session, Student, Attendance


class AttendanceSerializers(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'


class StudentSerializers(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

    # # Name validation   
    # def validate(self, data):
    #     special_character = '!@#$%^&*()_+<>?=,:[]/'
    #     if any(c in special_character for c in data['name']):
    #         raise serializers.ValidationError('Name cannot contain special characters')
    #     return data
    

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['image']


class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Faculty
        fields = '__all__'

class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = '__all__'
    


