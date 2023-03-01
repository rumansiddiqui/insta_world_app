from rest_framework import serializers
from .models import User


class DivisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Division
        fields = '__all__'

    def validate(self, attrs):
        return attrs

    def create(self, validated_data):
        Division.objects.create(**validated_data)
        return validated_data


class DepartmentSerializer(serializers.ModelSerializer):
    Division = DivisionSerializer(source='Division_join')

    class Meta:
        model = Department
        fields = '__all__'

    def validate(self, attrs):
        return attrs

    def create(self, validated_data):
        Department.objects.create(**validated_data)
        return validated_data


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

    def validate(self, attrs):
        return attrs

    def create(self, validated_data):
        Course.objects.create(**validated_data)
        return validated_data


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'

    def validate(self, attrs):
        return attrs

    def create(self, validated_data):
        Teacher.objects.create(**validated_data)
        return validated_data


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'

    def validate(self, attrs):
        return attrs

    def create(self, validated_data):
        Student.objects.create(**validated_data)
        return validated_data


class CombinedSerializer(serializers.ModelSerializer):
    department = DepartmentSerializer(source='department_join')

    class Meta:
        model = Course
        fields = '__all__'
