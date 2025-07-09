from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models import Student
from .serializers import StudentSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication

class StudentListCreateAPI(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        students = Student.objects.filter(user=request.user)
        serializer = StudentSerializer(students, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data.copy()
        data['user'] = request.user.id
        serializer = StudentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

class StudentUpdateDeleteAPI(APIView):
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, pk):
        try:
            student = Student.objects.get(pk=pk, user=request.user)
        except Student.DoesNotExist:
            return Response(status=404)
        serializer = StudentSerializer(student, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request, pk):
        try:
            student = Student.objects.get(pk=pk, user=request.user)
        except Student.DoesNotExist:
            return Response(status=404)
        student.delete()
        return Response(status=204)
