from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED,\
HTTP_400_BAD_REQUEST
from rest_framework.views import APIView
from .serializers import EmpSerializer, CustomEmpSerializer, UserSerializer,\
    DepartmentSerializer, LocationSerializer
from empapp.models import Employee, Department, Location
from django.db.utils import IntegrityError
from .pagination import StandardPagination
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser, DjangoModelPermissions
from .permissions import UserPermissionsChecker

# Create your views here.

# Function-based APIViews
@api_view(["GET","POST"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def employee(request):
    if request.method == 'GET':
        queryset_emps = Employee.objects.all()
        ser_emps = EmpSerializer(queryset_emps, many=True)
        json_data_response = Response(ser_emps.data)
        return json_data_response

    if request.method == 'POST':
        py_dict_emp = request.data #in request array, Json data converted to Python Dictionary
        ser_emps = EmpSerializer(data=py_dict_emp)
        if ser_emps.is_valid():
            ser_emps.save()
            return Response(ser_emps.validated_data, status=HTTP_201_CREATED)
        else:
            return Response(ser_emps.errors, status=HTTP_400_BAD_REQUEST)

@api_view(["PUT","PATCH","DELETE"])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def employeeModify(request, pk):
    if request.method == 'PUT':
        pass
    if request.method == 'PATCH':
        pass
    if request.method == 'DELETE':
        pass

class NewEmpFormData(APIView):
    def get(self, request):
        depts = DepartmentSerializer(Department.objects.all(), many=True)
        locs = LocationSerializer(Location.objects.all(), many=True)
        combined_data = {
            'depts':depts.data,
            'locs':locs.data
        }
        return Response(combined_data)

# Class-based views
# For GET, POST
class EmployeeAPI(APIView):
    # 1. THIS IS MANDATORY: It tells your permission class which model checkboxes to check!
    queryset = Employee.objects.all()
    
    # authentication_classes = [JWTAuthentication, SessionAuthentication]

    # if we use "DjangoModelPermissions" => POST, PUT, PATCH, DELETE only restricts but GET will not restrict 
    # so we are using our custom permission class "GroupPermissionsRequired"
    # which will retrict GET request also if not allowed for the user in admin panel
    # permission_classes = [IsAuthenticated, UserPermissionsChecker]

    # permissions_required_actions_map = {
    #     'get': ['empapp.view_employee'],
    #     'post': ['empapp.add_employee'],
    # }

    def get(self, request):
        queryset_emps = Employee.objects.all()
        ser_emps = EmpSerializer(queryset_emps, many=True)
        
        # print(ser_emps.data)
        json_data_response = Response(ser_emps.data)
        return json_data_response

    def post(self, request):
        py_dict_emp = request.data
        ser_emps = EmpSerializer(data=py_dict_emp)
        if ser_emps.is_valid():
            ser_emps.save()
            # print(ser_emps.data)
            # We cannot access ser_emps.data before ser_emps.is_valid() or ser_emps.save()
            return Response(ser_emps.data, status=HTTP_201_CREATED)
        return Response(ser_emps.errors, status=HTTP_400_BAD_REQUEST)


# Class-based APIViews
# for GET_ONE, PUT, PATCH, DELETE
class EmployeeModifyAPI(APIView):
    queryset = Employee.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, UserPermissionsChecker]

    permissions_required_actions_map = {
        'get': ['empapp.view_detail_employee'],
        'put': ['empapp.change_employee'],
        'patch': ['empapp.change_employee'],
        'delete': ['empapp.delete_employee'],
    }

    # Get one
    def get(self, request, pk):
        try:
            emp_obj = Employee.objects.get(eno=pk)
            ser_emp = EmpSerializer(emp_obj)
            json_data_response = Response(ser_emp.data)
            return json_data_response
        except Employee.DoesNotExist:
            return Response({'msg':f'Employee with id:{pk} does not exist.'}, status=HTTP_400_BAD_REQUEST)

    # PUT (Full Replacement)
    # Complete resource replacement.
    # Must include all required fields.
    # Triggers validation errors or reverts fields to defaults.
    # partial=False (default behavior).
    # Use PUT when a user fills out a form and saves the whole thing at once.
    def put(self, request, pk):
        try:
            emp_obj = Employee.objects.get(eno=pk)
            py_dict_emp = request.data
            ser_emp = EmpSerializer(emp_obj, data=py_dict_emp)
            if ser_emp.is_valid():
                ser_emp.save()
                return Response(ser_emp.validated_data)
            return Response(ser_emp.errors, HTTP_400_BAD_REQUEST)
        except Employee.DoesNotExist:
            return Response({'msg':f'Employee with id:{pk} does not exist.'}, status=HTTP_400_BAD_REQUEST)

    # PATCH (Partial Update)
    # Partial resource modification.
    # Only include fields you want to change.
    # Left entirely untouched.
    # partial=True (under the hood).
    # Use PATCH when a user updates just one input box (like changing a password or updating a profile bio).
    def patch(self, request, pk):
        try:
            emp_obj = Employee.objects.get(eno=pk)
            py_dict_emp = request.data
            ser_emp = EmpSerializer(emp_obj, data=py_dict_emp, partial=True)
            if ser_emp.is_valid():
                ser_emp.save()
                return Response(ser_emp.validated_data)
            return Response(ser_emp.errors, HTTP_400_BAD_REQUEST)
        except Employee.DoesNotExist:
            return Response({'msg':f'Employee with id:{pk} does not exist.'}, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        # Here try-except no need as we cannot send delete request directly through url
        # we can send only through button
        queryset_emp = Employee.objects.get(eno=pk)
        queryset_emp.delete()
        return Response(status=HTTP_200_OK)

class CustomEmployeeAPI(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset_emps = Employee.objects.all()

        paginator = StandardPagination()
        paginator_queryset_emps = paginator.paginate_queryset(queryset_emps, request, view=self)

        ser_emps = EmpSerializer(paginator_queryset_emps, many=True)

        json_data_response = paginator.get_paginated_response(ser_emps.data)
        return json_data_response
    
    def post(self, request):
        py_dict_emp = request.data
        ser_emp = CustomEmpSerializer(data=py_dict_emp)
        if ser_emp.is_valid():
            try:
                ser_emp.save()
            except IntegrityError as e:
                ser_emp._errors = {'msg': e.args[1]}
                return Response(ser_emp.errors, status=HTTP_400_BAD_REQUEST)
            return Response(ser_emp.validated_data)
        return Response(ser_emp.errors, status=HTTP_400_BAD_REQUEST)

class CustomEmployeeModifyAPI(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            emp_obj = Employee.objects.get(eno=pk)
            ser_emp = EmpSerializer(emp_obj)
            return Response(ser_emp.data)
        except Employee.DoesNotExist:
            return Response({'msg':f'Employee with id:{pk} does not exist.'}, status=HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            emp_obj = Employee.objects.get(eno=pk)
            py_dict_emp = request.data
            ser_emp = CustomEmpSerializer(emp_obj, data=py_dict_emp)
            if ser_emp.is_valid():
                ser_emp.save()
                return Response(ser_emp.validated_data, status=HTTP_200_OK)
            return Response(ser_emp.errors, status=HTTP_400_BAD_REQUEST)
        except Employee.DoesNotExist:
            return Response({'msg':f'Employee with id:{pk} does not exist.'}, status=HTTP_400_BAD_REQUEST)

class ModelViewSetEmployeeAPI(ModelViewSet):
    authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated, UserPermissionsChecker]

    permissions_required_actions_map = {
        'list': ['empapp.view_employee'],
        'retrieve': ['empapp.view_detail_employee'],
        'create': ['empapp.add_employee'],
        'update': ['empapp.change_employee'],
        'partial_update': ['empapp.change_employee'],
        'delete': ['empapp.delete_employee'],
    }

    queryset = Employee.objects.all()
    serializer_class = EmpSerializer

    # ---------------------------------------------------------
    # Customizing ModelViewSet:
    # While ModelViewSet handles standard CRUD out of the box, 
    # you can customize its behavior using hooks and decorators.

    # 1. Overriding Core Methods:
    # You can intercept data before it gets saved or deleted by overriding the saving mixin hooks:
    def perform_create(self, serializer):
        print('<Testing Create Data>', self.request.data)
        print('<Testing Validated Data>', serializer.validated_data)
        super().perform_create(serializer)

    def perform_update(self, serializer):
        print('<Testing Update>', self.request)
        super().perform_update(serializer)
    
    def perform_destroy(self, instance):
        print('<Testing Delete>', self.request)
        super().perform_destroy(instance)

    # 2. Adding Custom Endpoints (@action)
    # If you need an endpoint that falls outside standard CRUD operations, use the @action decorator.
    
    # GET
    # Accessible at: GET /ViewSetEmployee/management/
    @action(methods=['GET'], detail=False)
    def management(self, request):
        management_staff = Employee.objects.filter(edept=Department.objects.get(dept_name='management'))
        emp_ser = self.get_serializer(management_staff, many=True)
        return Response(emp_ser.data)
    
    # RETRIVE
    @action(methods=['GET'], detail=True)
    def preview(self, request, pk=None):
        return Response({'msg': f"Previewing Single Employee(ID-{pk})."})
    
    # POST
    @action(methods=['POST'], detail=False)
    def bulk_create(self, request):
        return Response({"msg": "Bulk Employees created."})
    
    # PUT, PATCH
    @action(methods=['PUT', 'PATCH'], detail=True)
    def change_status(self, request, pk=None):
        return Response({"msg": f"Employee(ID-{pk}) Status Updated."})
    
    # DELETE
    @action(methods=['DELETE'], detail=True)
    def remove_archive(self, request, pk=None):
        return Response({"msg": f"Employee(ID-{pk}) Deleted whch is archived."})

class RegisterToAPI(APIView):
    def post(self, request):
        u_obj = UserSerializer(data=request.data)
        if u_obj.is_valid():
            u_obj.save()
            # Returns the safe data (username, email) along with the success status
            return Response(u_obj.data, status=HTTP_201_CREATED)
        # Returns validation error details (e.g., "username already exists")
        return Response(u_obj.errors, status=HTTP_400_BAD_REQUEST)