from django.db import models
from django.contrib.auth.models import User



departments=[('Cardiologist','Cardiologist'),
('Dermatologists','Dermatologists'),
('Emergency Medicine Specialists','Emergency Medicine Specialists'),
('Allergists/Immunologists','Allergists/Immunologists'),
('Anesthesiologists','Anesthesiologists'),
('Colon and Rectal Surgeons','Colon and Rectal Surgeons')
]
class Doctor(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=True)
    department= models.CharField(max_length=50,choices=departments,default='Cardiologist')
    status=models.BooleanField(default=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return "{} ({})".format(self.user.first_name,self.department)



class Patient(models.Model):
    """
    Patient model for the clinic system.

    Attributes
    ----------
    user : User
        Linked Django user.
    address : str
        Patient's address.
    mobile : str
        Patient's phone number.
    symptoms : str
        Patient's symptoms.
    assignedDoctorId : int, optional
        Assigned doctor's ID.
    admitDate : date
        Admission date (auto-set).
    status : bool
        Account status (approved or not).

    Properties
    ----------
    get_name : str
        Full name of the patient.
    get_id : int
        User ID.
    """
    user=models.OneToOneField(User,on_delete=models.CASCADE)
 
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=False)
    symptoms = models.CharField(max_length=100,null=False)
    assignedDoctorId = models.PositiveIntegerField(null=True)
    admitDate=models.DateField(auto_now=True)
    status=models.BooleanField(default=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return self.user.first_name+" ("+self.symptoms+")"


class Appointment(models.Model):
    patientId=models.PositiveIntegerField(null=True)
    doctorId=models.PositiveIntegerField(null=True)
    patientName=models.CharField(max_length=40,null=True)
    doctorName=models.CharField(max_length=40,null=True)
    appointmentDate=models.DateField(auto_now=True)
    description=models.TextField(max_length=500)
    status=models.BooleanField(default=False)



class PatientDischargeDetails(models.Model):
    """
    Stores discharge details for a patient.

    Attributes
    ----------
    patientId : int, optional
        ID of the patient.
    patientName : str
        Name of the patient.
    assignedDoctorName : str
        Name of the assigned doctor.
    address : str
        Patient's address.
    mobile : str, optional
        Patient's phone number.
    symptoms : str, optional
        Patient's symptoms.
    admitDate : date
        Admission date.
    releaseDate : date
        Discharge date.
    daySpent : int
        Number of days spent in hospital.
    roomCharge : int
        Room charges.
    medicineCost : int
        Cost of medicines.
    doctorFee : int
        Doctor's fee.
    OtherCharge : int
        Other charges.
    total : int
        Total bill amount.
    """

    patientId=models.PositiveIntegerField(null=True)
    patientName=models.CharField(max_length=40)
    assignedDoctorName=models.CharField(max_length=40)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=True)
    symptoms = models.CharField(max_length=100,null=True)

    admitDate=models.DateField(null=False)
    releaseDate=models.DateField(null=False)
    daySpent=models.PositiveIntegerField(null=False)

    roomCharge=models.PositiveIntegerField(null=False)
    medicineCost=models.PositiveIntegerField(null=False)
    doctorFee=models.PositiveIntegerField(null=False)
    OtherCharge=models.PositiveIntegerField(null=False)
    total=models.PositiveIntegerField(null=False)



