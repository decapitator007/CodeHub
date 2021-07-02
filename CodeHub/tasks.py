import requests,datetime
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
def myFunc(e):
    return e['start']
def kontests(url,list):
    response=requests.get(url)
    for i in response.json():
        str=i['start_time'][0:19]
        i['start']=datetime.datetime.strptime(str,'%Y-%m-%dT%H:%M:%S')+datetime.timedelta(hours=5,minutes=30)
        if i['in_24_hours']=='Yes':
            list.append(i)
list=[]
kontests("https://kontests.net/api/v1/codeforces",list)
kontests("https://kontests.net/api/v1/code_chef",list)
kontests("https://kontests.net/api/v1/leet_code",list)
list.sort(key=myFunc)
subject='Reminder from CodeHub'
html_message=render_to_string('CodeHub/mail.html',{'list':list})
plain_message=strip_tags(html_message)
send_mail(subject,plain_message,settings.EMAIL_HOST_USER,['suryanshsingh.civ18@itbhu.ac.in'],html_message=html_message)
