from django.urls import path
from . import views
urlpatterns=[
    path('',views.home,name='home'),
    path('identify/',views.identify,name='identify'),
    path('newques/',views.new_ques,name='new_ques'),
    path('question/<int:pk>/',views.ques_detail,name='ques_detail'),
    path('question/<int:pk>/ans/',views.add_ans,name='add_ans'),
    path('question/<int:pk>/edit/<int:ak>/',views.edit_ans,name='edit_ans'),
    path('question/<int:pk>/delete/<int:ak>/',views.delete_ans,name='delete_ans'),
    path('question/<int:pk>/delete/',views.delete_ques,name='delete_ques'),
    path('out/',views.out,name='out'),
    path('register/',views.register,name='register'),
    path('profile/<string>/',views.profile,name='profile'),
    path('profile/<string>/delete/',views.delete_acc,name='delete_acc'),
    path('schedule/',views.schedule,name='schedule'),
    path('list/',views.list,name='list'),
    path('about/',views.about,name='about'),
]
