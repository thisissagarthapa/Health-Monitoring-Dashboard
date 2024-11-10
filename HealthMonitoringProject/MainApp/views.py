import joblib
import numpy as np
import pandas as pd
import os
from django.conf import settings
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import DataEntry
from .models import HealthReport
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import DataEntry, HealthReport
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib import colors
from django.core.cache import cache


# Create your views here.
def health(request):
    return render(request,"Health/health.html")

def feature(request):
    return render(request,"Health/features.html")

def working(request):
    return render(request,"Health/working.html")

def testimonials(request):
    return render(request,"Health/testimonials.html")

def security(request):
    return render(request,"Health/security.html")

def register(request):
    if request.method=="POST":
        name=request.POST["name"]
        username=request.POST["username"]
        email=request.POST["email"]
        password=request.POST["password1"]
        password1=request.POST["password1"]
        if password==password1:
            if User.objects.filter(username=username).exists():
                messages.info(request,f"hello{name},your username already exists.")
            elif User.objects.filter(email=email).exists():
                messages.info(request,f"hello {name},your email alreaady exists.")
            else:
                User.objects.create_user(first_name=name,username=username,email=email,password=password)
                messages.success(request,f"hello {name}, your have registered successfully.")
                return redirect('health')
        else:
            messages.error(request,"passwords do not match.")    
    return render(request,"Auth/register.html")

def log_in(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        if not User.objects.filter(username=username).exists():
            messages.error(request,"username not found")
            return redirect(log_in)
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('dashboard')
        else:
            messages.error(request,"Invalid credentials")
    return render(request,"Auth/login.html")

@login_required(login_url='log_in')
def log_out(request):
    logout(request)
    return redirect('health')

@login_required(login_url='log_in')
def dashboard(request):
    return render(request,"Dashboard/dashboard.html")

@login_required(login_url='log_in')
def overview(request):
    return render(request,"Dashboard/overview.html")

@login_required(login_url='log_in')
def healthHistory(request):
    data=DataEntry.objects.all()
    return render(request,"Dashboard/healthHistory.html",{"health_records":data})

@login_required(login_url='log_in')
def recommendation(request):
    return render(request,"Dashboard/recommendation.html")

@login_required(login_url='log_in')
def Health_report(request):
    entries = HealthReport.objects.all()  # Changed to entries for clarity
    return render(request, "Dashboard/report.html", {"entries": entries})



def generate_report(request, data_entry_id):
    data_entry = get_object_or_404(DataEntry, id=data_entry_id)
    health_report = data_entry.health_reports.first()  # Get the related HealthReport
    
    # Create a PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="health_report_{data_entry.name}.pdf"'
    
    # Create a canvas
    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter
    
    # Set the title style
    p.setFont("Helvetica-Bold", 24)
    p.setFillColor(colors.darkblue)
    p.drawString(100, height - 50, f"Health Report for {data_entry.name}")
    
    # Set a subtitle style
    p.setFont("Helvetica-Bold", 18)
    p.setFillColor(colors.black)
    p.drawString(100, height - 100, "Health Parameters:")
    
    # Set a regular text style for report content
    p.setFont("Helvetica", 14)
    p.setFillColor(colors.black)

    # Add health parameters with spacing
    spacing = 30  # Vertical space between lines
    y_position = height - 130  # Starting position for the first parameter

    parameters = [
        f"Heart Rate: {data_entry.heart_rate} bpm",
        f"Blood Pressure: {data_entry.blood_pressure}",
        f"Sleep Duration: {data_entry.sleep_duration} hours",
        f"Oxygen Saturation: {data_entry.oxygen_saturation}%",
        f"Body Temperature: {data_entry.body_temperature} °C",
        f"BMI: {data_entry.bmi}",
        f"Status: {health_report.status}"
    ]

    for param in parameters:
        p.drawString(100, y_position, param)
        y_position -= spacing  # Move down for the next parameter
    
    # Draw a footer
    p.setFont("Helvetica-Oblique", 10)
    p.setFillColor(colors.grey)
    p.drawString(100, 50, "This report is generated for personal health monitoring purposes.")

    # Finish the PDF
    p.showPage()
    p.save()
    
    return response


@login_required(login_url='log_in')
def dataEntry(request):
    model_path = os.path.join(settings.BASE_DIR, 'MainApp', 'ML', 'model_voting_classifier.pkl')
    
    try:
        model = joblib.load(model_path)
    except Exception as e:
        print("Error loading model:", e)
        messages.error(request, "Error loading the model. Please check the server logs.")
        return redirect('dashboard')
    
    if request.method == "POST":
        # Get data from the form
        name = request.POST.get("name")
        heart_rate = float(request.POST.get("heart_rate"))
        blood_pressure = float(request.POST.get("blood_pressure").split('/')[0])  # Get systolic pressure
        sleep_duration = float(request.POST.get("sleep_duration"))
        oxygen_saturation = float(request.POST.get("oxygen_saturation"))
        body_temperature = float(request.POST.get("body_temperature"))
        bmi = float(request.POST.get("bmi"))

        # Prepare data for model prediction as DataFrame
        input_data = pd.DataFrame([{
            'heart_rate': heart_rate,
            'blood_pressure': blood_pressure,
            'sleep_duration': sleep_duration,
            'oxygen_saturation': oxygen_saturation,
            'body_temperature': body_temperature,
            'bmi': bmi
        }])

        # Make the prediction
        prediction = model.predict(input_data)[0]
        status_label = "Healthy" if prediction == 1 else "At Risk"

        # Save data entry and report
        data_entry = DataEntry.objects.create(
            name=name,
            heart_rate=heart_rate,
            blood_pressure=blood_pressure,
            sleep_duration=sleep_duration,
            oxygen_saturation=oxygen_saturation,
            body_temperature=body_temperature,
            bmi=bmi
        )
        HealthReport.objects.create(data_entry=data_entry, status=status_label)

        # Generate recommendations
        health_metrics = {
            "heart_rate": heart_rate,
            "blood_pressure": blood_pressure,
            "sleep_duration": sleep_duration,
            "oxygen_saturation": oxygen_saturation,
            "body_temperature": body_temperature,
            "bmi": bmi
        }
        recommendations = get_recommendations(status_label, health_metrics)

        # Pass all data and recommendations to the template
        return render(request, "Dashboard/recommendation.html", {
            "name": name,
            "status": status_label,
            "heart_rate": heart_rate,
            "blood_pressure": blood_pressure,
            "sleep_duration": sleep_duration,
            "oxygen_saturation": oxygen_saturation,
            "body_temperature": body_temperature,
            "bmi": bmi,
            "recommendations": recommendations
        })

    return render(request, "Dashboard/dataEntry.html")


def get_recommendations(status, health_metrics):
    recommendations = []
    
    if status == "Healthy":
        recommendations.append("Keep up the good work! Maintain your regular exercise and balanced diet.")
    elif status == "At Risk":
        # Provide specific recommendations based on health metrics
        if health_metrics['heart_rate'] > 100:
            recommendations.append("Consider incorporating stress-reducing activities like meditation or yoga.")
        if health_metrics['blood_pressure'] > 130:
            recommendations.append("Monitor your blood pressure regularly and reduce salt intake.")
        if health_metrics['sleep_duration'] < 6:
            recommendations.append("Try to maintain a regular sleep schedule with at least 7-8 hours of sleep.")
        if health_metrics['oxygen_saturation'] < 95:
            recommendations.append("Consult with a healthcare provider regarding your oxygen saturation levels.")
        if health_metrics['body_temperature'] > 37.5:
            recommendations.append("Monitor your temperature and consider consulting a healthcare professional if it remains high.")
        if health_metrics['bmi'] < 18.5:
            recommendations.append("Consider gaining weight through a balanced diet and regular exercise.")
        elif health_metrics['bmi'] > 24.9:
            recommendations.append("Consider adopting a weight loss plan focusing on healthy eating and exercise.")
    return recommendations



