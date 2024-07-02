import io
import sklearn
import pickle
import pandas as pd
from django.shortcuts import render,redirect,get_object_or_404
from django.http.response import HttpResponseRedirect,HttpResponse,JsonResponse
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import FileUpload
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import precision_score
from sklearn.ensemble import RandomForestClassifier
from django.core.mail import send_mail



def base(request):
    return render(request,'homeApp/landing_page.html')


def account_details(request):
    return render(request,'homeApp/account_details.html')
def change_password(request):
    return render(request,'homeApp/change_password.html')

def view_data(request,id):
    obj = FileUpload.objects.get(id=id)
    df = pd.read_csv(obj.actual_file.path)
    columns = df.columns.tolist()
    return render(request,'homeApp/view_data.html', {'id': id, 'columns': columns})
def delete_data(request,id):
    obj=FileUpload.objects.get(id=id)
    obj.delete()
    messages.success(request, "File Deleted succesfully",extra_tags = 'alert alert-success alert-dismissible show')
    return HttpResponseRedirect('/report')

from django.http import HttpResponseRedirect
from django.contrib import messages

def upload_data(request):
    if request.method == 'POST':
        try:
            actual_file = request.FILES['actual_file_name']
            data = pd.read_csv(actual_file)
            cc_nums=data['cc_num']
            cc_nums=cc_nums.values.tolist()
            #print(cc_nums)
            #data=usecols=['', col2, ...]
            #data["cc_num"] = data["cc_num"].astype(float)
            sc = StandardScaler()
            data = sc.fit_transform(data)
            model= joblib.load("model_save2")
            predictions = model.predict(data)
            statuses = ["Fraudulent Transaction" if pred == 1 else "Non-Fraudulent Transaction" for pred in predictions]
            #print(statuses)
            for i in range(len(statuses)):
                if statuses[i]=="Fraudulent Transaction":
                    message = f"Here we see that you got an unusual transaction in your account. CC: {cc_nums[i]}"
                    send_mail(
                        "Unusual Transaction Detection",
                        message,
                        "for400c@gmail.com",
                        ["mirsadalhossain5712@gmail.com"],
                        fail_silently=False
                    )
                    print("mail send")
                FileUpload.objects.create(
                        cc_num=cc_nums[i],
                        actual_file=actual_file,
                        status=statuses[i]
                )

            messages.success(request, "File Uploaded successfully", extra_tags='alert alert-success alert-dismissible show')
            return HttpResponseRedirect('/upload_file')

        except Exception as e:
            messages.warning(request, f"Error: {e}. Please upload a valid file.")
            return HttpResponseRedirect('/upload_file')
    return render(request, 'homeApp/fraud_detection.html')

            
def show_report(request):
    data = FileUpload.objects.all()  
    return render(request, 'homeApp/reports.html', {'data': data})

def userLogout(request):
    try:
      del request.session['username']
    except:
      pass
    logout(request)
    return HttpResponseRedirect('/') 
    

def login2(request):
    data = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        print(user)
        if user:
            login(request, user)
            return HttpResponseRedirect('/')
        
        else:    
            data['error'] = "Username or Password is incorrect"
            res = render(request, 'homeApp/login.html', data)
            return res
    else:
        return render(request, 'homeApp/login.html', data)


def about(request):
    return render(request,'homeApp/about.html')

def dashboard(request):
    return render(request,'homeApp/dashboard.html')
