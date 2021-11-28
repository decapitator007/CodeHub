from django.shortcuts import render,get_object_or_404,redirect
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .forms import signin,signup,QForm,AForm
from .models import Question,Answer,cfid
from django.contrib import messages
from django.conf import settings
import requests,datetime
from django.http import HttpResponse
#About
def about(request):
    return render(request,'CodeHub/about.html',{})
#List of Users
def list(request):
    userlist=User.objects.all().order_by('first_name')
    return render(request,'CodeHub/list.html',{'userlist':userlist})
#Schedule
def myFunc(e):
    return e['start']
def kontests(url,list):
    response=requests.get(url)
    for i in response.json():
        str=i['start_time'][0:19]
        i['start']=datetime.datetime.strptime(str,'%Y-%m-%dT%H:%M:%S')+datetime.timedelta(hours=5,minutes=30)
        if i['start']>datetime.datetime.now():
            list.append(i)
def schedule(request):
    list1=[]
    list2=[]
    list3=[]
    list4=[]
    list5=[]
    list=[]
    kontests("https://kontests.net/api/v1/codeforces",list1)
    kontests("https://kontests.net/api/v1/leet_code",list3)
    kontests("https://kontests.net/api/v1/kick_start",list4)
    kontests("https://kontests.net/api/v1/at_coder",list5)
    for i in list1:
        i['site']='Codeforces'
        list.append(i)
    for i in list3:
        i['site']='Leetcode'
        list.append(i)
    for i in list4:
        i['site']='Kickstart'
        list.append(i)
    for i in list5:
        i['site']='Atcoder'
        list.append(i)
    list.sort(key=myFunc)
    return render(request,'CodeHub/schedule.html',{'list':list})
#Profile
def profile(request,string):
    userob=get_object_or_404(User,username=string)
    cf=get_object_or_404(cfid,username=userob)
    apikey="dddd2a31aa144fa1b23a0cfe4d0b57c166f9cd91"
    url="https://codeforces.com/api/user.info/"
    handle=cf.cfusername
    params={'apikey':apikey,'handles':[handle]}
    response=requests.get(url,params=params)
    if cf.cfusername=="":
        details={}
    else:
        details=response.json()['result'][0]
    return render(request,'CodeHub/profile.html',{'cf':details,'userob':userob,'contri':cf})
#Delete Answer
def delete_ans(request,pk,ak):
    answer=get_object_or_404(Answer,pk=ak)
    if request.user.is_authenticated and request.user==answer.author:
        if request.method=="POST":
            if 'yes' in request.POST:
                answer.delete()
                cf=get_object_or_404(cfid,username=request.user)
                cf.no_of_a=cf.no_of_a-1
                cf.save()
                messages.success(request,'Answer Deleted!')
            return redirect('ques_detail',pk=pk)
        else:
            return render(request,'CodeHub/delete_ans.html',{})
    else:
        return redirect('identify')
#Delete Question
def delete_ques(request,pk):
    question=get_object_or_404(Question,pk=pk)
    if request.user.is_authenticated and request.user==question.author:
        if request.method=="POST":
            if 'yes' in request.POST:
                del_ans=Answer.objects.filter(link_to_ques=question)
                for answer in del_ans:
                    user=User.objects.get(username=answer.author)
                    cf=cfid.objects.get(username=user)
                    cf.no_of_a=cf.no_of_a-1
                    cf.save()
                question.delete()
                messages.success(request,'Question Deleted!')
                cf=get_object_or_404(cfid,username=request.user)
                cf.no_of_q=cf.no_of_q-1
                cf.save()
            return redirect('home')
        else:
            return render(request,'CodeHub/delete_ques.html',{})
    else:
        return redirect('identify')
#Delete Account
def delete_acc(request,string):
    user=get_object_or_404(User,username=string)
    if request.user.is_authenticated and request.user==user:
        if request.method=="POST":
            if 'yes' in request.POST:
                logout(request)
                user.delete()
                messages.success(request,'Account Deleted!')
                return redirect('home')
            else:
                return redirect('profile',string=string)
        else:
            return render(request,'CodeHub/delete_acc.html',{})
    else:
        return redirect('identify')
#Edit Answer
def edit_ans(request,pk,ak):
    answer=get_object_or_404(Answer,pk=ak)
    if request.user.is_authenticated and request.user==answer.author:
        if request.method=='POST':
            form=AForm(request.POST,instance=answer)
            if form.is_valid():
                answer=form.save(commit=False)
                answer.added_time=timezone.now()
                answer.save()
                messages.success(request,'Answer Edited!')
                return redirect('ques_detail',pk=pk)
        else:
            form=AForm(instance=answer)
        return render(request,'CodeHub/add_ans.html',{'form':form})
    else:
        return redirect('identify')
#All answers of a question
def ques_detail(request,pk):
    question=get_object_or_404(Question,pk=pk)
    answers=Answer.objects.filter(link_to_ques=question).order_by('-added_time')
    return render(request,'CodeHub/ques_detail.html',{'question':question,'answers':answers})
#Add a question
def new_ques(request):
    if request.user.is_authenticated:
        if request.method=='POST':
            form=QForm(request.POST)
            if form.is_valid():
                question=form.save(commit=False)
                question.author=request.user
                question.added_time=timezone.now()
                question.save()
                cf=get_object_or_404(cfid,username=request.user)
                cf.no_of_q=cf.no_of_q+1
                cf.save()
                messages.success(request,'Question Added!')
                return redirect('home')
        else:
            form=QForm()
        return render(request,'CodeHub/new_ques.html',{'form':form})
    else:
        messages.warning(request,'You must login to ask a question!')
        cur_path=request.path
        return redirect('/identify/?next='+cur_path)
#Add an answer
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
                cf=get_object_or_404(cfid,username=request.user)
                cf.no_of_a=cf.no_of_a+1
                cf.save()
                messages.success(request,'Answer Added!')
                return redirect('ques_detail',pk=pk)
        else:
            form=AForm()
        return render(request,'CodeHub/add_ans.html',{'form':form})
    else:
        messages.warning(request,'You must login to answer a question!')
        cur_path=request.path
        return redirect('/identify/?next='+cur_path)
#Home Page
def home(request):
    questions=Question.objects.order_by('-added_time')
    return render(request,'CodeHub/home.html',{'questions':questions})
#Login
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
                    messages.success(request,'Logged In!')
                    if 'next' in request.GET:
                        next=request.GET['next']
                        return redirect(next)
                    else:
                        return redirect('home')
                else:
                    messages.warning(request,'Invalid Credentials!')
                    return render(request,'CodeHub/identify.html',{'form':form})
        else:
            form=signin()
        return render(request,'CodeHub/identify.html',{'form':form})
#Signup
def isvalid(cf,email,username,password,cpassword):
    error=''
    apikey="dddd2a31aa144fa1b23a0cfe4d0b57c166f9cd91"
    url="https://codeforces.com/api/user.info/"
    params={'apikey':apikey,'handles':[cf]}
    response=requests.get(url,params=params)
    url="https://mailcheck.p.rapidapi.com/"
    params={"domain":email}
    headers={'x-rapidapi-key':"d1ef0714e4msh5108dce6969ee1ep1e4e75jsnb180e18e0179",'x-rapidapi-host':"mailcheck.p.rapidapi.com"}
    result=requests.get(url,headers=headers,params=params)
    if User.objects.filter(username=username).exists():
        error="This username is already registered!"
    elif result.json()['block']==True or result.json()['valid']==False or result.json()['disposable']==True:
        error="Invalid email!"
    elif User.objects.filter(email=email).exists():
        error="This email is already registered!"
    elif response.json()['status']!="OK" and len(cf)>0:
        error="Codeforces ID is incorrect!"
    elif len(password)<8 or len(password)>16:
        error='Invalid length of password!'
    elif password!=cpassword:
        error="Passwords did not match!"
    return error
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
                error=isvalid(cf,email,username,password,cpassword)
                if error!="":
                    messages.warning(request,error)
                    return render(request,'CodeHub/register.html',{'form':form})
                User.objects.create_user(first_name=firstname,last_name=lastname,username=username,email=email,password=password)
                user=User.objects.get(username=username)
                cfid.objects.create(username=user,cfusername=cf)
                messages.success(request,'Account Created!')
                return redirect('identify')
        else:
            form=signup()
        return render(request,'CodeHub/register.html',{'form':form})
#Logout
def out(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,'Logged Out!')
        if 'next' in request.GET:
            next=request.GET['next']
            return redirect(next)
        else:
            return redirect('home')
    return redirect('identify')
#404 Error
def error_404(request,exception):
    return render(request,'CodeHub/404.html')
