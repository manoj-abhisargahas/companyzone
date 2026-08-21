from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from empapp.models import Employee, Department, Location
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class EmpSerializer(serializers.ModelSerializer):
    # Overriding fields to use nested serializers
    # By adding read_only=True, you tell Django:
    #     For GET requests: Use the nested serializer to display the 
    #                       full department details (ID, name, etc.).
    #     For POST/PUT requests: Completely ignore this field during data validation.
    edept = DepartmentSerializer(read_only=True)
    eloc = LocationSerializer(read_only=True)
    class Meta:
        model = Employee
        fields = ['eno','ename','esal','edept','eloc','epfpic']

class CustomEmpSerializer(serializers.Serializer):
    empno = serializers.IntegerField()
    firstname = serializers.CharField(max_length=20)
    lastname = serializers.CharField(max_length=20)
    salary = serializers.IntegerField()
    bonus = serializers.IntegerField()

    # for POST
    def create(self, validated_data):
        empno = validated_data['empno']
        fname = validated_data['firstname']
        lname = validated_data['lastname']
        sal = validated_data['salary']
        bonus = validated_data['bonus']

        emp_obj = Employee.objects.create(
            eno = empno,
            ename = fname+' '+lname,
            esal = sal + bonus
        )

        return emp_obj

    # for PUT
    def update(self, instance, validated_data):
        fname = validated_data['firstname']
        lname = validated_data['lastname']
        sal = validated_data['salary']
        bonus = validated_data['bonus']

        instance.ename = fname+' '+lname
        instance.esal = sal + bonus

        return instance

    # for POST, PUT, PATCH
    def validate(self, data_to_validate):
        errors = []

        if data_to_validate['empno'] < 0:
            errors.append({'empno':'Negative values cannot be accepted for Employee No.'})
        if data_to_validate['salary'] < 0:
            errors.append({'salary':'Negative values cannot be accepted for Salary.'})
        if data_to_validate['bonus'] < 0:
            errors.append({'bonus':'Negative values cannot be accepted for Bonus.'})
        
        if errors:
            raise ValidationError(errors)
        
        return data_to_validate #validated_data

User = get_user_model()
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        extra_kwargs = {
            # Makes password write-only so it never leaks in responses
            'password': {'write_only':True}
        }

    def create(self, validated_data):
        # Appropriately hashes the password instead of saving it in plain text
        user =  User.objects.create_user(**validated_data)

        # Automated Production Lockdowns
        user.is_api_user = True
        user.is_staff = False
        user.is_superuser = False
        user.save()

        # Automatically fetch and assign the 'Api User' group
        try:
            api_group = Group.objects.get(name='Api User')
            user.groups.add(api_group) # Links the user to the group permissions
        except Group.DoesNotExist:
            # Safe fallback if you haven't created the group in the admin panel yet
            pass

        return user