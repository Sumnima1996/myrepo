from django.conf.urls import url

from question import views

urlpatterns=[
url(r'^$', views.questions, name='questions'),
url(r'^answered/$', views.answered, name='answered'),
url(r'^unanswered/$', views.unanswered, name='unanswered'),
url(r'^all/$', views.all, name='all'),
url(r'ques/$',views.askQuestion,name="quen"),
url(r'ans/$',views.writeAnswer,name="ans"),
url(r'^(\d+)/$', views.question, name='question'),
url(r'accept/$',views.answerAccept,name='accept'),
url(r'^favorite/$', views.favorite, name='favorite'),
url(r'^vote/$', views.vote, name='vote'),

]

