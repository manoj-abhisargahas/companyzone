from django.shortcuts import render, redirect, get_object_or_404
from django.db import IntegrityError, transaction
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
# from django.utils.decorators import method_decorator
from empapp.models import Employee, Department, Location
from django.db.models import Count, Min, Max, Sum, Avg, Q, F, Value, IntegerField, CharField
from django.db.models.functions import Cast
from django.views import View
from .exceptions import NegativeValueError, ZeroValueError
import os
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import permission_required

# DB Activities:
# 1. One Time - Database Design
# 2. Multiple Times - insert, update, delete, search

# Here not checked for empty values as they are ensuring through html required attribute in front-end

# Create your views here.

# We can also use method_decorator instead of "LoginRequiredMixin" for Class-based Views:
# This tells Django to apply the function decorator to the class dispatch engine
# @method_decorator(login_required, name='dispatch')
class EmployeeInsertView(LoginRequiredMixin, PermissionRequiredMixin, View):
    res_filename = 'empapp/new_employee.html'
    permission_required = 'empapp.add_employee'
    raise_exception = True  #Automatically throws a 403 Forbidden to unauthorized users

    def get(self, request):
        return EmployeeInsertView.response(request, result='', result_type='', filename=EmployeeInsertView.res_filename)
    
    def post(self, request):
        query_set = request.POST
        result = ''
        result_type = 'noerror'
        
        emp_name = query_set.get('emp_name', "")
        emp_pfpic = request.FILES.get('emp_pfpic', None)
        emp_intvid = request.FILES.get('emp_intvid', None)
        emp_resume = request.FILES.get('emp_resume', None)
        emp_dept = query_set.get('emp_dept', None)
        emp_loc = query_set.get('emp_loc', None)

        try:
            emp_no = int(query_set.get('emp_no', ""))
            if emp_no == 0:
                raise ZeroValueError("Employee No.")
            elif emp_no < 0:
                raise NegativeValueError("Employee No.")
        except (ValueError, NegativeValueError):
            result = "Error: Please enter a positive integer value for Employee No."
            result_type = "error"
            return EmployeeInsertView.response(request, result, result_type, EmployeeInsertView.res_filename)
        except ZeroValueError as e:
            result = str(e)
            result_type = "error"
            return EmployeeInsertView.response(request, result, result_type, EmployeeInsertView.res_filename)
        
        try:
            emp_sal = int(query_set.get('emp_sal', ""))
            if emp_sal < 0:
                raise NegativeValueError("Employee Salary")
        except (ValueError, NegativeValueError):
            result = "Error: Please enter a positive integer value for Employee Salary."
            result_type = "error"
            return EmployeeInsertView.response(request, result, result_type, EmployeeInsertView.res_filename)
        
        try:
            fields_kwargs = {'eno':emp_no, 'ename':emp_name, 'esal':emp_sal}
            if emp_pfpic!=None and emp_pfpic!='':
                fields_kwargs['epfpic'] = emp_pfpic
            if emp_intvid!=None and emp_intvid!='':
                fields_kwargs['eintvid'] = emp_intvid
            if emp_resume!=None and emp_resume!='':
                fields_kwargs['eresume'] = emp_resume
            if emp_dept!=None and emp_dept!='':
                fields_kwargs['edept'] = Department.objects.get(dept_id=int(emp_dept))
            if emp_loc!=None and emp_loc!='':
                fields_kwargs['eloc'] = Location.objects.get(loc_id=int(emp_loc))

            Employee.objects.create(**fields_kwargs)
        except IntegrityError:
            result = f"Error: Employee No. ({emp_no}) already exists!"
            result_type = "error"
        except Exception as e:
            result = f"Error: Employee No. ({emp_no}) insertion failed due to System Error, Try Again!. Message: {e}"
            result_type = "error"
        else:
            result = f"{emp_no}. {emp_name} - New Employee inserted Successfully!"
            result_type = 'success'
        
        return EmployeeInsertView.response(request, result, result_type, EmployeeInsertView.res_filename)
        
    @classmethod
    def response(cls, request, result, result_type, filename, context = None):
        if context is None:
            context = {}
        context["result"] = result
        context["result_type"]= result_type
        context["depts"] = Department.objects.all()
        context["locations"] = Location.objects.all()
        
        if result_type == 'error':
            context["emp_name"]= request.POST.get('emp_name', "")
            context["emp_sal"] = request.POST.get('emp_sal', "")
            if context.get("emp_no")==None:
                context["emp_no"] = request.POST.get('emp_no', "")
            if request.POST.get('emp_dept')!='':
                context["emp_dept"] = int(request.POST.get('emp_dept'))
            if request.POST.get('emp_loc')!='':
                context["emp_loc"] = int(request.POST.get('emp_loc'))

        return render(request, filename, context)

#Authentication
@login_required # Bounces users back to login page if they lack an active session
#Authorization - 'empapp.view_employee' getting this built-in permission from 'Employee' model class
@permission_required('empapp.view_employee', raise_exception=True)
def viewEmployees(request):
    res_filename = 'empapp/view_all_employees.html'
    if request.method == 'GET':
        eobjs = Employee.objects.all()
        context = {'eobjs': eobjs}
        
        return render(request, res_filename, context)

@login_required
#Authorization - 'empapp.view_detail_employee' Created this custom permission in 'Employee' model class
@permission_required('empapp.view_detail_employee', raise_exception=True)
def viewDetailEmployee(request, emp_no):
    eobj = get_object_or_404(Employee, eno=emp_no)
    res_filename = 'empapp/view_detail_employee.html'
    
    if request.method == 'GET':
        context = {'eobj':eobj}
        return render(request, res_filename, context)

@login_required
@permission_required('empapp.change_employee', raise_exception=True)
def updateEmployee(request, emp_no):
    eobj = get_object_or_404(Employee, eno=emp_no)
    res_filename = 'empapp/update_employee.html'
    
    if request.method == 'GET':
        context = {'emp_no': emp_no,
                    'emp_name': eobj.ename,
                    'emp_sal': eobj.esal,
                    'emp_dept': eobj.edept.dept_name if eobj.edept else None,
                    'emp_loc': eobj.eloc.loc_name if eobj.eloc else None,
                    'depts': Department.objects.all(),
                    'locations': Location.objects.all()}
        
        return render(request, res_filename, context)

    elif request.method == 'POST':
        query_set = request.POST
        result = ''
        result_type = 'noerror'

        emp_name = query_set.get('emp_name', "")
        emp_sal = int(query_set.get('emp_sal', "")) #ValueError
        emp_pfpic = request.FILES.get('emp_pfpic', None)
        emp_intvid = request.FILES.get('emp_intvid', None)
        emp_resume = request.FILES.get('emp_resume', None)
        emp_dept = query_set.get('emp_dept', None)
        emp_loc = query_set.get('emp_loc', None)
        
        try:
            # Everything inside this block is treated as a single, unbreakable unit
            with transaction.atomic():
                eobj.ename = emp_name
                eobj.esal = emp_sal
                eobj.edept = Department.objects.get(dept_id=int(emp_dept)) if emp_dept!='' else None
                eobj.eloc = Location.objects.get(loc_id=int(emp_loc)) if emp_loc!='' else None

                # 1. Backup old file targets before overwriting
                old_pfpic = eobj.epfpic if emp_pfpic else None
                old_intvid = eobj.eintvid if emp_intvid else None
                old_resume = eobj.eresume if emp_resume else None

                 # 2. Assign the new uploads
                if emp_pfpic: eobj.epfpic = emp_pfpic
                if emp_intvid: eobj.eintvid = emp_intvid
                if emp_resume: eobj.eresume = emp_resume

                # 3. Commit to the database
                eobj.save()
        except Exception as e:
            result = f"Error: Employee No. ({emp_no}) updation failed due to System Error, Try Again!. Message: {e}"
            result_type = "error"
        else:
            # 4. This block ONLY runs if the try block finishes with ZERO errors.
            # Deleting files in MEDIA_ROOT if it exits:
            # using old_pfpic.delete(save=False) instead of ".. and os.path.isfile(old_pfpic.path): os.remove(old_pfpic.path)"
            # Delete the physical file from storage without updating the database row
            if old_pfpic and old_pfpic.name: old_pfpic.delete(save=False)
            if old_intvid and old_intvid.name: old_intvid.delete(save=False)
            if old_resume and old_resume.name: old_resume.delete(save=False)

            result = f"Employee No. ({emp_no}) Updated Successfully!"
            result_type = 'success'
        
        return updateEmployee_response(request, result, result_type)

@login_required
def updateEmployee_response(request, result, result_type):
    if result_type == 'success':
        messages.success(request, result)
    elif result_type == 'error':
        messages.error(request, result)

    return redirect('viewemployees_url')

@login_required
@permission_required('empapp.delete_employee', raise_exception=True)
def deleteEmployee(request, emp_no):
    if request.method == 'GET':
        result = ""
        result_type = ""
        query_set = request.GET

        try:
            eobj = Employee.objects.get(eno=emp_no) #Employee.DoesNotExist

            with transaction.atomic():
                emp_name = eobj.ename #Exception - any DB error

                # 1. Backup old file targets before overwriting
                old_pfpic = eobj.epfpic
                old_intvid = eobj.eintvid
                old_resume = eobj.eresume

                # 2. Commit to the database
                eobj.delete() #Exception - any DB error
        except Employee.DoesNotExist:
            result = f"Error: Employee with No. ({emp_no}) doesn't exits!"
            result_type = 'error'
        except Exception as e:
            result = f"Error: Employee No. ({emp_no}) deletion failed due to System Error, Try Again!. Message: {e}"
            result_type = 'error'
        else:
            # 3. This block ONLY runs if the try block finishes with ZERO errors.
            # Deleting files in MEDIA_ROOT if it exits:
            if old_pfpic and old_pfpic.name: old_pfpic.delete(save=False)
            if old_intvid and old_intvid.name: old_intvid.delete(save=False)
            if old_resume and old_resume.name: old_resume.delete(save=False)

            result = f"{emp_no}. {emp_name} - Employee Deleted Successfully!"
            result_type = 'success'
        
        return updateEmployee_response(request, result, result_type)

@login_required
@permission_required('empapp.view_dept_status', raise_exception=True)
def viewDeptStats(request):
    res_filename = 'empapp/view_dept_stats.html'
    if request.method == 'GET':
        q1 = Department.objects.values('dept_id', 
                                       'dept_name', 
                                       emp_count=Count('dept_emp__eno'), 
                                       emp_min_sal=Min('dept_emp__esal'), 
                                       emp_max_sal=Max('dept_emp__esal'), 
                                       emp_avg_sal=Cast(Avg('dept_emp__esal'), output_field=IntegerField()))
        q2 = Employee.objects.filter(edept__isnull=True)\
                             .values(dept_id=Value(0, output_field=IntegerField()), 
                                     dept_name=Value(None, output_field=CharField()))\
                             .annotate(emp_count=Count('eno'), 
                                       emp_min_sal=Min('esal'), 
                                       emp_max_sal=Max('esal'), 
                                       emp_avg_sal=Cast(Avg('esal'), output_field=IntegerField()))\
                             .values('dept_id','dept_name','emp_count','emp_min_sal','emp_max_sal','emp_avg_sal')
        context = {'depts_stats':q1.union(q2).order_by('dept_id')}
        
        return render(request, res_filename, context)
    """
    Returns a list of dictionaries with statistics 
    grouped by dept_id along with unassigned grouped employees
    order by 'dept_id' in descending order.

    >>> for dept in context['dept_stats']:
    ...     print(dept)
    ... 
    {'dept_id': 0, 'dept_name': 'unassigned', 'emp_count': 2, 'emp_min_sal': 1331, 'emp_max_sal': 1597, 'emp_avg_sal': 1464}
    {'dept_id': 1, 'dept_name': 'Management', 'emp_count': 3, 'emp_min_sal': 799, 'emp_max_sal': 2130, 'emp_avg_sal': 1420}
    {'dept_id': 2, 'dept_name': 'Designing', 'emp_count': 2, 'emp_min_sal': 1664, 'emp_max_sal': 23100, 'emp_avg_sal': 12382}
    {'dept_id': 3, 'dept_name': 'Marketing', 'emp_count': 0, 'emp_min_sal': None, 'emp_max_sal': None, 'emp_avg_sal': None}
    {'dept_id': 4, 'dept_name': 'Testing', 'emp_count': 0, 'emp_min_sal': None, 'emp_max_sal': None, 'emp_avg_sal': None}
    {'dept_id': 5, 'dept_name': 'Business Analysis', 'emp_count': 0, 'emp_min_sal': None, 'emp_max_sal': None, 'emp_avg_sal': None}
    {'dept_id': 6, 'dept_name': 'Development', 'emp_count': 0, 'emp_min_sal': None, 'emp_max_sal': None, 'emp_avg_sal': None}
    {'dept_id': 7, 'dept_name': 'Support Team', 'emp_count': 0, 'emp_min_sal': None, 'emp_max_sal': None, 'emp_avg_sal': None}
    """

# Not using:
# * because of only giving departments info that are used in employee table
# * not giving departments info that are not used yet
# * because data is only fetching from Employee Table
@login_required
def viewDeptStats_FromEmployeeTableSide(request):
    res_filename = 'empapp/view_dept_stats.html'
    if request.method == 'GET':
        context = {'depts_stats': Employee.objects.values(dept_id = F('edept_id'))\
                                                  .annotate(dept_name = F('edept__dept_name'), 
                                                            emp_count = Count('eno'), 
                                                            emp_min_sal = Min('esal'), 
                                                            emp_max_sal = Max('esal'), 
                                                            emp_avg_sal = Cast(Avg('esal'), output_field = IntegerField()))\
                                                  .order_by('dept_id')}

        return render(request, res_filename, context)
    """
    >>> for dept in context['dept_stats']:
    ...     print(dept)
    ...
    {'dept_id': None, 'dept_name': None, 'emp_count': 2, 'emp_min_sal': 1331, 'emp_max_sal': 1597, 'emp_avg_sal': 1464}
    {'dept_id': 1, 'dept_name': 'Management', 'emp_count': 3, 'emp_min_sal': 799, 'emp_max_sal': 2130, 'emp_avg_sal': 1420}
    {'dept_id': 2, 'dept_name': 'Designing', 'emp_count': 2, 'emp_min_sal': 1664, 'emp_max_sal': 23100, 'emp_avg_sal': 12382}
    """