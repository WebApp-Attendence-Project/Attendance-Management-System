import json
from django.http.response import JsonResponse
from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .models import Contact, Employee, Take_attendence
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from json import dumps
import datetime
import xlwt
import datetime

# Create your views here.
def index(request):
    return render(request, 'info/index.html')

# Contact Page
def contact(request):
    
    if request.method == "POST":
        name = request.POST.get('name', '')
        phone = request.POST.get('phone', '')
        email = request.POST.get('email', '')
        content = request.POST.get('content', '')
        contact=Contact(name=name, email=email, phone=phone, content=content)
        contact.save()
        messages.success(request, "Your message has been successfully sent")
    else:
        messages.success(request, 'Welcome to contact')
    return render(request, "info/contact.html")
    
# About Page
@csrf_exempt
def about(request):
    return render(request, 'info/about.html')

# Login
@csrf_exempt
def handleLogin(request):
    if request.method=="POST":
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']
        user = authenticate(username=loginusername, password=loginpassword)

        if user is not None:
            login(request, user)
            
            return redirect('attendence')
        else:
            messages.error(request, "Invalid Login")
            check=True
            return redirect('home')

# Logout 
def handleLogout(request):
    logout(request)
    return redirect('home')


# Marking attendence 
@login_required
def attendence(request):
    # messages.success(request, "Welcome to Attendence")
    all_employee = Employee.objects.all()
    # print(all_employee)
    # context = {'context':all_employee}
    # context = serializers.serialize('json', self.get_queryset())
    return render(request, 'info/attendence_new.html')


@csrf_exempt
def get_attendence(request):
    position = request.POST.get('position')
    if position=='All':
        position_data = Employee.objects.all()
    else:
        position_data = Employee.objects.filter(post=position)
   
    list_data = []

    for Employe in position_data:
        staff_sno = Employee.objects.filter(name=Employe.name)[0]
      
        data_small = {"id": Employe.sno, "name": Employe.name, "post":Employe.post}
        list_data.append(data_small)
    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


# Saving attendence Data 
@csrf_exempt
def save_data(request):
    if request.method == 'POST':
            Employe_ids = request.POST.get("Employe_ids")
            attendence_date = request.POST.get("attendance_date")
        
            json_Employe = json.loads(Employe_ids)
           

            try:
        # First Attendance Data is Saved on Attendance Model
       
                for stud in json_Employe:

                    # Attendance of Individual Employe saved on AttendanceReport Model
                    employe = Employee.objects.get(sno=stud['id'])
                    attendance_report = Take_attendence(name=employe.name, status=stud['status'], attendence_date=attendence_date, employe=employe)
                    attendance_report.save()
                messages.success(request, "Attendance is added Successfully")
                return HttpResponse("OK")
            except:
     
                return HttpResponse("Error")


# Adding Employees Details 
@login_required
def add_staff(request):
    if request.method == "POST":
        name = request.POST.get('name', '')
        phone = request.POST.get('phone', '')
        gender = request.POST.get('gender', '')
        bloodgroup = request.POST.get('bloodgroup', '')
        email = request.POST.get('email', '')
        position = request.POST.get('position', '')
     
        employe=Employee(name=name, email=email, phone=phone,gender=gender, bloodgroup=bloodgroup, post=position)
        employe.save()
        messages.success(request, "Your message has been successfully sent")
    else:
        messages.success(request, 'Welcome to Add Staff')
    return render(request, "info/add_staff.html")


# Showing attendence Report 
@login_required
def attendence_report(request):
    messages.success(request, 'Welcome to Attendence Report')
    all_attendence= Take_attendence.objects.all()
   
    context = {'context':all_attendence}
    return render(request, "info/attendence_report.html", context)

#  Showing attendance of a particular date
@csrf_exempt
def admin_get_attendence(request):
    attendance_date = request.POST.get('attendance_date')
    attendance_data = Take_attendence.objects.filter(attendence_date=attendance_date)
 
    list_data = []

    for Employe in attendance_data:
        staff_sno = Employee.objects.filter(name=Employe.name)[0]
 
        data_small={"id":Employe.sno, "name":Employe.name, "date":Employe.attendence_date, "status":Employe.status, "staff_sno":staff_sno.sno}
        list_data.append(data_small)
    
    return JsonResponse(json.dumps(list_data), content_type="application/json", safe=False)


@login_required
def all_staff(request):
    staff = Employee.objects.all()
    return render(request, 'info/all_staff.html', {'staff_detail':staff})


#  Showing Employee Details
@login_required
def staff_details(request):
    sno = request.POST.get('staff_sno')
    detail = Employee.objects.filter(sno=sno)[0]
    attendance_detail = Take_attendence.objects.filter(name=detail.name)

    list = []
    for data in attendance_detail:
        data_small={"name":data.name, "date":data.attendence_date, "status":data.status}
        list.append(data_small)

    return render(request, 'info/staff_details.html', {'detail':detail, 'attendance_detail':attendance_detail})

#  Searching attendence between two dates
@login_required
@csrf_exempt
def from_to_staff_attendance(request):
    date_from = request.POST.get('date_from')
  
    date_to = request.POST.get('date_to')
    employee_name = request.POST.get('Employe_name')
    get_data = Take_attendence.objects.filter(attendence_date__range=[date_from, date_to], name=employee_name)
   
    list = []
    for data in get_data:
        data_small = {"name": data.name, "date": data.attendence_date, "status": data.status}
        list.append(data_small)

    return JsonResponse(json.dumps(list), content_type="application/json", safe=False)


    

# Exporting attendance in Excel File
@login_required
@csrf_exempt
def export_excel(request):
    month = request.POST.get('month')
    year = request.POST.get('year')
    datetime_object = datetime.datetime.strptime(month, "%m")
    month_name = datetime_object.strftime("%b")
    
    if month == '02':
        total_days = 29
    elif int(month) % 2 == 0 and int(month)<= 7:
        total_days = 31
    elif int(month) % 2 != 0 and int(month)>= 8:
        total_days = 31
    else :
        total_days = 32

# 1 2 3 4 5 6 7 8 9 10
# j f m a m j j a s o
# 1 8 1 0 1 0 1 1 0 1
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename=AttendenceData' + \
        str(datetime.datetime.now())+'.xls' 
    wb = xlwt.Workbook(encoding='utf-8')  
    ws = wb.add_sheet('AttendenceData')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    i = 0
    
    ws.write(row_num, 0, 'Name', font_style)
    for col_num in range(1, total_days):
        ws.write(row_num, col_num, f'{col_num}-{month_name}-{year}', font_style)

    font_style = xlwt.XFStyle()

    
    
    # rows = Take_attendence.objects.all().values_list('name', 'date', 'status')
    rows = Employee.objects.all().values_list('name')
    for name in rows:
        row_num += 1
        list = []
        dates = Take_attendence.objects.filter(attendence_date__range=[f'20{year}-{month}-01', f'20{year}-{month}-{total_days-1}'], name=f'{name[0]}')
        for data in dates:
            data_small = {"date": data.attendence_date, "status": data.status}
            list.append(data_small)
        ws.write(row_num, 0, f'{name[0]}', font_style)
        # print(list)
        for col_num in range(1, total_days):
            check = 0
            for l in list:
                if l['date'][8] == '0': # 2021-01-01
                    if l['date'] == f'20{year}-{month}-0{col_num}':
                        ws.write(row_num, col_num, f'{l["status"]}', font_style)
                        check = 1
                
                else:
                    if l['date'] == f'20{year}-{month}-{col_num}':
                        ws.write(row_num, col_num, f'{l["status"]}', font_style)
                        check = 1
            if check == 0:
                ws.write(row_num, col_num, f'NA', font_style)

    wb.save(response)

    return response
