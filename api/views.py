from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import FacultySerializer, StudentSerializers, AttendanceSerializers, SessionSerializer
from .models import Faculty, Session, Student, Attendance
from django.contrib.auth.hashers import make_password, check_password
from datetime import datetime
from openpyxl import Workbook
from io import BytesIO

# To add student
@api_view(['POST'])
def CreateStudent(request):
    student_data = StudentSerializers(data=request.data)
    print(student_data)
    if student_data.is_valid():
        student_data.save()
        return Response(student_data.data, status=status.HTTP_201_CREATED)
    return Response(student_data.errors, status=status.HTTP_400_BAD_REQUEST)



# To SignUp student
@api_view(['PATCH'])
def SignUp(request):
    username = request.data.get("username")
    password = request.data.get("password")
    # <------------------ For Faculty ------------------>
    if(len(username) == 7):
        try:
            instance = Faculty.objects.get(employee_id=username)
            if instance.password:
                return Response({"message": "Already registered"}, status=status.HTTP_400_BAD_REQUEST)
        except Faculty.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        hashed_password = make_password(password)
        print(hashed_password)
        serializer = FacultySerializer(instance, data={"password" : hashed_password}, partial= True)
        if serializer.is_valid():
            serializer.validated_data['password'] = hashed_password
            # serializer.validated_data['image'] = image 
            serializer.save()
            return Response({"message": "Signup Successfully"}, status=status.HTTP_201_CREATED)
        return Response({"message" : "Signup failed"}, status=status.HTTP_400_BAD_REQUEST)
    # <------------------ For Student ------------------>
    else:
        try:
            instance = Student.objects.get(enrollment_no=username)
            if instance.password:
                return Response({"message": "Already registered"}, status=status.HTTP_400_BAD_REQUEST)
        except Student.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        password = request.data.get("password")
        hashed_password = make_password(password)
        print(hashed_password)
        serializer = StudentSerializers(instance, data={"password" : hashed_password}, partial= True)
        if serializer.is_valid():
            serializer.validated_data['password'] = hashed_password
            # serializer.validated_data['image'] = image 
            serializer.save()
            return Response({"message": "Signup Successfully"}, status=status.HTTP_201_CREATED)
        return Response({"message" : "Signup failed"}, status=status.HTTP_400_BAD_REQUEST)




# Login
@api_view(['POST'])
def Login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    # <------------------ For Faculty ------------------>
    if(len(username) == 7):
        try:
            faculty = Faculty.objects.get(employee_id=username)
        except Faculty.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        if faculty is not None and check_password(password, faculty.password):
            # Authentication successful
            faculty_data = FacultySerializer(faculty)
            return Response({"message": "Authentication successful", "data": faculty_data.data}, status=status.HTTP_200_OK)
        else:
            # Authentication failed
            return Response({"message": "Password is incorrect"}, status=status.HTTP_401_UNAUTHORIZED)
    # <------------------ For Student ------------------>
    try:
        student = Student.objects.get(enrollment_no=username)
    except Student.DoesNotExist:
        return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    if student is not None and check_password(password, student.password):
        # Authentication successful
        student_data = StudentSerializers(student)
        return Response({"message": "Authentication successful", "data": student_data.data}, status=status.HTTP_200_OK)
    else:
        # Authentication failed
        return Response({"message": "Password is incorrect"}, status=status.HTTP_401_UNAUTHORIZED)




# To add attendance 
@api_view(['POST'])
def CreateAttendance(request):
    attendance_data = AttendanceSerializers(data=request.data)
    print(attendance_data)
    if attendance_data.is_valid():
        attendance_data.save()
        return Response(attendance_data.data, status=status.HTTP_201_CREATED)
    return Response(attendance_data.errors, status=status.HTTP_400_BAD_REQUEST)




# To get attendance
@api_view(['POST'])
def GetAttendance(request):
    start_date = datetime.strptime(request.data.get('start_date'), '%Y-%m-%d').date()
    end_date = datetime.strptime(request.data.get('end_date'), '%Y-%m-%d').date()
    queryset = Attendance.objects.filter(date__gte=start_date, date__lt=end_date)
    serializer = AttendanceSerializers(queryset, many=True)

    # Create Excel file
    workbook = Workbook()
    sheet = workbook.active
    sheet.append(['ID', 'Enrollment No', 'Date', 'Status', 'Subject Code'])
    for item in serializer.data:
        sheet.append([item['id'], item['enrollment_no'], item['date'], item['status'], item['subject_code']])

    excel_data = BytesIO()
    workbook.save(excel_data)
    excel_data.seek(0)

    response = Response(excel_data, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=attendance_data.xlsx'
    return response




# Upload image
@api_view(['PATCH'])
def UploadImage(request):
    enrollment_no = request.data.get("enrollment_no")
    image = request.data.get("image")
    try:
        instance = Student.objects.get(enrollment_no = enrollment_no)
    except Student.DoesNotExist:
        return Response({"error": "Object not found"}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = StudentSerializers(instance, data={"image" : image}, partial= True)
    if serializer.is_valid():
        serializer.validated_data['image'] = image 
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# Add Session
@api_view(['POST'])
def AddSession(request):
    session = SessionSerializer(data = request.data)
    if session.is_valid():
        session.save()
        return Response(session.data, status=status.HTTP_201_CREATED)
    return Response(session.errors, status=status.HTTP_400_BAD_REQUEST)


# Delete Session
@api_view(['DELETE'])
def DeleteSession(request, session_id):
    try:
        session = Session.objects.get(session_id=session_id)
    except Session.DoesNotExist:
        return Response({"message": "Session not found"}, status=status.HTTP_404_NOT_FOUND)

    session.delete()
    return Response({"message": "Session deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
