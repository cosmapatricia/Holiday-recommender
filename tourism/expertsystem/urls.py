from django.urls import path
from . import views 

app_name = 'expertsystem'

urlpatterns = [
	path('', views.index, name = 'index'),
	path('<int:question_id>/', views.detail, name='detail'),
	path('results/', views.results, name='results'),
]