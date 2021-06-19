from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .forms import signin,signup,QForm,AForm
from .models import Question,Answer,cfid
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
import requests,datetime
def list(request):
    userlist=User.objects.all()
    return render(request,'CodeHub/list.html',{'userlist':userlist})
def myFunc(e):
    return e['start']
def schedule(request):
    url="https://kontests.net/api/v1/codeforces"
    response=requests.get(url)
    list=[]
    for i in response.json():
        str=i['start_time'][0:19]
        i['start']=datetime.datetime.strptime(str,'%Y-%m-%dT%H:%M:%S')
        if i['start']>=datetime.datetime.now():
            i['start']+=datetime.timedelta(hours=5,minutes=30)
            list.append(i)
    url="https://kontests.net/api/v1/code_chef"
    response=requests.get(url)
    for i in response.json():
        str=i['start_time'][0:19]
        i['start']=datetime.datetime.strptime(str,'%Y-%m-%dT%H:%M:%S')
        if i['start']>=datetime.datetime.now():
            i['start']+=datetime.timedelta(hours=5,minutes=30)
            list.append(i)
    url="https://kontests.net/api/v1/leet_code"
    response=requests.get(url)
    for i in response.json():
        str=i['start_time'][0:19]
        i['start']=datetime.datetime.strptime(str,'%Y-%m-%dT%H:%M:%S')
        if i['start']>=datetime.datetime.now():
            i['start']+=datetime.timedelta(hours=5,minutes=30)
            list.append(i)
    list.sort(key=myFunc)
    return render(request,'CodeHub/schedule.html',{'list':list})
def profile(request,string):
    cf=get_object_or_404(cfid,username=string)
    userob=get_object_or_404(User,username=string)
    apikey="dddd2a31aa144fa1b23a0cfe4d0b57c166f9cd91"
    url="https://codeforces.com/api/user.info/"
    handle=cf.cfusername
    p={'apikey':apikey,'handles':[handle]}
    response=requests.get(url,params=p)
    details=response.json()['result'][0]
    return render(request,'CodeHub/profile.html',{'cf':details,'userob':userob})
def delete_ans(request,pk,ak):
    answer=get_object_or_404(Answer,pk=ak)
    if request.user.is_authenticated and request.user==answer.author:
        if request.method=="POST":
            if 'yes' in request.POST:
                answer.delete()
            return redirect('ques_detail',pk=pk)
        else:
            return render(request,'CodeHub/delete_ans.html',{})
    else:
        return redirect('home')
def edit_ans(request,pk,ak):
    answer=get_object_or_404(Answer,pk=ak)
    if request.user.is_authenticated and request.user==answer.author:
        if request.method=='POST':
            form=AForm(request.POST,instance=answer)
            if form.is_valid():
                answer=form.save(commit=False)
                answer.added_time=timezone.now()
                answer.save()
                messages.success(request,'Answer edited!')
                return redirect('ques_detail',pk=pk)
        else:
            form=AForm(instance=answer)
        return render(request,'CodeHub/add_ans.html',{'form':form})
    else:
        return redirect('home')
def ques_detail(request,pk):
    question=get_object_or_404(Question,pk=pk)
    answers=Answer.objects.filter(link_to_ques=question).order_by('-added_time')
    return render(request,'CodeHub/ques_detail.html',{'question':question,'answers':answers})
def new_ques(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            form=QForm(request.POST)
            if form.is_valid():
                question=form.save(commit=False)
                question.author=request.user
                question.added_time=timezone.now()
                question.save()
                messages.success(request,'Your question has been added!')
                return redirect('home')
        else:
            form=QForm()
        return render(request,'CodeHub/new_ques.html',{'form':form})
    else:
        messages.warning(request,'You must login to ask a question!')
        return redirect('identify')
def add_ans(request,pk):
    question=get_object_or_404(Question,pk=pk)
    if request.user.is_authenticated:
        if request.method=='POST':
            form=AForm(request.POST)
            if form.is_valid():
                answer=form.save(commit=False)
                answer.author=request.user
                answer.added_time=timezone.now()
                answer.link_to_ques=question
                answer.save()
                messages.success(request,'Your answer has been added!')
                return redirect('ques_detail',pk=pk)
        else:
            form=AForm()
        return render(request,'CodeHub/add_ans.html',{'form':form})
    else:
        messages.warning(request,'You must login to answer a question!')
        return redirect('identify')
def home(request):
    questions=Question.objects.order_by('-added_time')
    return render(request,'CodeHub/home.html',{'questions':questions})
def identify(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method=='POST':
            form=signin(request.POST)
            if form.is_valid():
                username=form.cleaned_data.get("username")
                password=form.cleaned_data.get("password")
                user=authenticate(request,username=username,password=password)
                if user is not None:
                    login(request,user)
                    messages.success(request,'Logged in!')
                    return redirect('home')
                else:
                    messages.warning(request,'Invalid Credentials!')
                    return render(request,'CodeHub/identify.html',{'form':form})
        else:
            form=signin()
        return render(request,'CodeHub/identify.html',{'form':form})
def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method=='POST':
            form=signup(request.POST)
            if form.is_valid():
                firstname=form.cleaned_data.get("firstname")
                lastname=form.cleaned_data.get("lastname")
                username=form.cleaned_data.get("username")
                email=form.cleaned_data.get("email")
                password=form.cleaned_data.get("password")
                cpassword=form.cleaned_data.get("cpassword")
                cf=form.cleaned_data.get("cf")
                error=""
                apikey="dddd2a31aa144fa1b23a0cfe4d0b57c166f9cd91"
                url="https://codeforces.com/api/user.info/"
                handle=cf
                p={'apikey':apikey,'handles':[handle]}
                response=requests.get(url,params=p)
                if User.objects.filter(username=username).exists():
                    error="This username is already registered!"
                elif User.objects.filter(email=email).exists():
                    error="This email is already registered!"
                elif response.json()['status']!="OK":
                    error="Codeforces ID is incorrect!"
                elif password!=cpassword:
                    error="Passwords did not match!"
                if error!="":
                    messages.warning(request,error)
                    return render(request,'CodeHub/register.html',{'form':form})
                User.objects.create_user(first_name=firstname,last_name=lastname,username=username,email=email,password=password)
                cfid.objects.create(username=username,cfusername=cf)
                messages.success(request,'Account created successfully!')
                send_mail('Welcome to CodeHub','Hi '+firstname+'! Thank you for registering on CodeHub.',settings.EMAIL_HOST_USER,[email])
                return redirect('identify')
        else:
            form=signup()
        return render(request,'CodeHub/register.html',{'form':form})
def out(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,'Logged out!')
    return redirect('identify')
