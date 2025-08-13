from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from . import forms,models
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth.models import Group
from django.db.models import Q

# Create your views here.
def index(request):
    """
Show the home page.
    """
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'base.html')
def patientclick_view(request):

    """
    Display the patient login and registration page.

    If the user is already authenticated, they are redirected to the
    :func:`afterlogin_view`. Otherwise, the `patientclick.html` template is rendered.

    :param request: The HTTP request object.
    :type request: django.http.HttpRequest
    :return: HTTP redirect to ``afterlogin`` if authenticated, otherwise renders the patient click page.
    :rtype: django.http.HttpResponse
    """
   
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'patientclick.html')

# Signup-patient
def patient_signup_view(request):

    """
    Handle patient sign-up requests.

    Displays the patient registration form and processes the form submission.
    Creates a new user and patient profile, assigns them to the ``PATIENT`` group,
    and redirects to the patient login page upon successful registration.

    :param request: The HTTP request object.
    :type request: django.http.HttpRequest
    :return: Renders the signup page on GET, redirects to ``patientlogin`` on successful POST.
    :rtype: django.http.HttpResponse
    """

    userForm=forms.PatientUserForm()
    patientForm=forms.PatientForm()
    mydict={'userForm':userForm,'patientForm':patientForm}
    if request.method=='POST':
        userForm=forms.PatientUserForm(request.POST)
        patientForm=forms.PatientForm(request.POST,request.FILES)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            patient=patientForm.save(commit=False)
            patient.user=user
            patient.assignedDoctorId=request.POST.get('assignedDoctorId')
            patient=patient.save()
            my_patient_group = Group.objects.get_or_create(name='PATIENT')
            my_patient_group[0].user_set.add(user)
        return HttpResponseRedirect('patientlogin')
    return render(request,'patientsignup.html',context=mydict)

def is_patient(user):
    """
    Check if a user belongs to the ``PATIENT`` group.

    :param user: The user instance to check.
    :type user: django.contrib.auth.models.User
    :return: ``True`` if the user is in the patient group, otherwise ``False``.
    :rtype: bool
    """
    return user.groups.filter(name='PATIENT').exists()

@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_dashboard_view(request):

    """
    Display the patient dashboard.

    Retrieves the patient and their assigned doctor, and passes relevant
    details to the dashboard template.

    :param request: The HTTP request object.
    :type request: django.http.HttpRequest
    :return: Rendered dashboard template with patient and doctor details.
    :rtype: django.http.HttpResponse
    """

    patient=models.Patient.objects.get(user_id=request.user.id)
    doctor=models.Doctor.objects.get(user_id=patient.assignedDoctorId)
    mydict={
    'patient':patient,
    'doctorName':doctor.get_name,
    'doctorMobile':doctor.mobile,
    'doctorAddress':doctor.address,
    'symptoms':patient.symptoms,
    'doctorDepartment':doctor.department,
    'admitDate':patient.admitDate,
    }
    return render(request,'patient_dashboard.html',context=mydict)

def afterlogin_view(request):

    """
    Redirect user to the appropriate dashboard after login.

    Depending on the user's role (admin, doctor, or patient), they are
    redirected to their respective dashboards. If a doctor or patient account
    is pending approval, they are shown a base page.

    :param request: The HTTP request object.
    :type request: django.http.HttpRequest
    :return: HTTP redirect or base template.
    :rtype: django.http.HttpResponse
    """


    if is_admin(request.user):
        return redirect('admin-dashboard')
    elif is_doctor(request.user):
        accountapproval=models.Doctor.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('doctor-dashboard')
        else:
            return render(request,'base.html')
    elif is_patient(request.user):
        accountapproval=models.Patient.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('patient-dashboard')
        else:
            return render(request,'base.html')
        
@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_appointment_view(request):
    """
    Display the patient appointment page.

    Used to show patient profile information in the sidebar when booking
    appointments.

    :param request: The HTTP request object.
    :type request: django.http.HttpRequest
    :return: Rendered appointment page template.
    :rtype: django.http.HttpResponse
    """
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    return render(request,'patient_appointment.html',{'patient':patient})



@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_book_appointment_view(request):
    """
    Allow patients to book an appointment.

    Displays the appointment form and handles appointment creation on POST.

    :param request: The HTTP request object.
    :type request: django.http.HttpRequest
    :return: Renders booking page on GET, redirects to appointment view on POST.
    :rtype: django.http.HttpResponse
    """
    appointmentForm=forms.PatientAppointmentForm()
    patient=models.Patient.objects.get(user_id=request.user.id) 
    message=None
    mydict={'appointmentForm':appointmentForm,'patient':patient,'message':message}
    if request.method=='POST':
        appointmentForm=forms.PatientAppointmentForm(request.POST)
        if appointmentForm.is_valid():
            print(request.POST.get('doctorId'))
            desc=request.POST.get('description')

            doctor=models.Doctor.objects.get(user_id=request.POST.get('doctorId'))
            
            appointment=appointmentForm.save(commit=False)
            appointment.doctorId=request.POST.get('doctorId')
            appointment.patientId=request.user.id 
            appointment.doctorName=models.User.objects.get(id=request.POST.get('doctorId')).first_name
            appointment.patientName=request.user.first_name 
            appointment.status=False
            appointment.save()
        return HttpResponseRedirect('patient-view-appointment')
    return render(request,'patient_book_appointment.html',context=mydict)

@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_view_appointment_view(request):
    """
    View all appointments for the logged-in patient.

    :param request: The HTTP request object.
    :type request: django.http.HttpRequest
    :return: Rendered appointment list template.
    :rtype: django.http.HttpResponse
    """
    patient=models.Patient.objects.get(user_id=request.user.id)
    appointments=models.Appointment.objects.all().filter(patientId=request.user.id)
    return render(request,'patient_view_appointment.html',{'appointments':appointments,'patient':patient})

@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_discharge_view(request):
     
    """
    Display discharge details for the logged-in patient.

    Shows the most recent discharge record, including cost breakdown.
    If the patient is not discharged, shows a placeholder message.

    :param request: The HTTP request object.
    :type request: django.http.HttpRequest
    :return: Rendered discharge details template.
    :rtype: django.http.HttpResponse
    """
    patient=models.Patient.objects.get(user_id=request.user.id)
    dischargeDetails=models.PatientDischargeDetails.objects.all().filter(patientId=patient.id).order_by('-id')[:1]
    patientDict=None
    if dischargeDetails:
        patientDict ={
        'is_discharged':True,
        'patient':patient,
        'patientId':patient.id,
        'patientName':patient.get_name,
        'assignedDoctorName':dischargeDetails[0].assignedDoctorName,
        'address':patient.address,
        'mobile':patient.mobile,
        'symptoms':patient.symptoms,
        'admitDate':patient.admitDate,
        'releaseDate':dischargeDetails[0].releaseDate,
        'daySpent':dischargeDetails[0].daySpent,
        'medicineCost':dischargeDetails[0].medicineCost,
        'roomCharge':dischargeDetails[0].roomCharge,
        'doctorFee':dischargeDetails[0].doctorFee,
        'OtherCharge':dischargeDetails[0].OtherCharge,
        'total':dischargeDetails[0].total,
        }
        print(patientDict)
    else:
        patientDict={
            'is_discharged':False,
            'patient':patient,
            'patientId':request.user.id,
        }
    return render(request,'patient_discharge.html',context=patientDict)




