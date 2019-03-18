from django.shortcuts import render
from django.http import HttpResponse
from .models import Question
# Create your views here.

def index(request):
    question_list = Question.objects.all()
    context = {'question_list': question_list}
    return render(request, 'expertsystem/index.html', context)

def results(request):
    response = "You're looking at the results."
    return HttpResponse(response)
