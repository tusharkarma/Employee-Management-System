from django.shortcuts import render,HttpResponse,redirect
from .models import Employee,Role,Department
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

@csrf_exempt
def admin_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_staff:  # Allow only admin users
            login(request, user)
            return redirect("/admin/")  # Redirect to dashboard
        else:
            return render(request, "emp_app/admin_login.html", {"error": "Invalid credentials or not an admin!"})

    return render(request, "emp_app/admin_login.html")

@login_required
def admin_dashboard(request):
    return render(request, "emp_app/admin_dashboard.html")

def admin_logout(request):
    logout(request)
    return redirect("admin_login")

def index(request):
    return render(request, 'emp_app/index.html')

def removeEmp(request):
    if request.method == "POST":
        emp_id = request.POST.get("emp_id", None)

        if emp_id:
            try:
                emp = Employee.objects.get(id=int(emp_id))
                emp.delete()
                return redirect('removeEmp')  # Refresh page after deletion
            except Employee.DoesNotExist:
                return HttpResponse("Employee not found.", status=404)
            except ValueError:
                return HttpResponse("Invalid Employee ID.", status=400)

    employees = Employee.objects.all()
    return render(request, "emp_app/removeEmp.html", {"employees": employees})
    


def addEmp(request):
    if request.method=='POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        salary = request.POST.get('salary', '0')
        bonus = request.POST.get('bonus', '0')
        phone = request.POST.get('phone', '').strip()
        dept_id = request.POST.get('dept', None)  # Ensure dept_id is None if not provided
        role_id = request.POST.get('role', None) 

        # Validate input fields
        if not first_name or not last_name or not phone or not dept_id or not role_id:
            return HttpResponse("All fields are required.", status=400)

        # Convert numeric fields safely
        try:
            salary = int(salary)
            bonus = int(bonus)
        except ValueError:
            return HttpResponse("Invalid salary or bonus value.", status=400)

        # Fetch department and role safely
        try:
            dept = Department.objects.get(id=dept_id)
        except Department.DoesNotExist:
            return HttpResponse("Invalid Department ID.", status=400)

        try:
            role = Role.objects.get(id=role_id)
        except Role.DoesNotExist:
            return HttpResponse("Invalid Role ID.", status=400)
        new_emp=Employee(first_name=first_name, last_name=last_name, salary=salary,bonus=bonus, phone=phone, dept=dept, role=role, hire_date=datetime.now())
        new_emp.save()
        return redirect('viewEmp')
        
    elif request.method=='GET':
        departments = Department.objects.all()
        roles = Role.objects.all()
        return render(request, 'emp_app/addEmp.html', {'departments': departments, 'roles': roles})
    else:
        return HttpResponse('An exception occured')
    


def filterEmp(request):
    employees = Employee.objects.all()
    departments = Department.objects.all()
    roles = Role.objects.all()

    if request.method == "GET":
        name = request.GET.get("name", "")
        dept_id = request.GET.get("dept_id", "")
        role_id = request.GET.get("role_id", "")

        if name:
            employees = employees.filter(first_name__icontains=name) | employees.filter(last_name__icontains=name)

        if dept_id:
            employees = employees.filter(dept_id=dept_id)  

        if role_id:
            employees = employees.filter(role_id=role_id)  

    return render(request, "emp_app/filterEmp.html", {
        "employees": employees,
        "departments": departments,
        "roles": roles,
    })

    
def viewEmp(request):
    emps= Employee.objects.all()
    context= {
        'emps': emps
    }
    print(context)
    return render(request, 'emp_app/viewEmp.html', context)
