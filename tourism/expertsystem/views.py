from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.http import Http404
from .models import Question
# Create your views here.

question_list = Question.objects.all()
i=0

premises = []
partial_conclusions = []
final_conclusions = []
rules = {}

user_premises = []
user_partial_conclusions = []

user_results = []
final_results = []

def parse(path):
	try:
		with open(path,'r') as f:
			lines = f.readlines()   
	except:
		return

	final_conclusions.extend(lines[0].split(', '))
	final_conclusions[len(final_conclusions)-1] = final_conclusions[len(final_conclusions)-1].rstrip()

	for i in range (1, len(lines)):
		if not lines[i] or lines[i].startswith('#'):
			continue
		elif lines[i].startswith('IF'):
			sides = lines[i].replace('IF ','').split(' THEN ')
			current_premises = sides[0].split(' AND ')
			for current_premise in current_premises:
				if current_premise not in premises:
					premises.append(current_premise)
			sides[1] = sides[1].rstrip()
			rules[sides[1]] = current_premises
			if sides[1] not in final_conclusions:
				partial_conclusions.append(sides[1])

def inference(conclusion):
	if conclusion in final_conclusions and conclusion in user_partial_conclusions:
		return conclusion
	for concl, premise_list in rules.items():
		found = 1
		for premise in premise_list:
			if not (premise in user_premises or premise in user_partial_conclusions):
				found = 0
		if found == 1:
			if concl not in user_partial_conclusions:
				user_partial_conclusions.append(concl)
				if concl in final_conclusions:
					return concl
				else:
					for c,p in rules.items():
						if concl in p:
							inference(c)
	return 0

def get_recommendations():
	for conclusion in final_conclusions:
		user_results.append(inference(conclusion))
	no_result = True
	for result in user_results:
		if result != 0:
			final_results.append(result)
			no_result = False
	if no_result:
		final_results.append('No matches found')
	return final_results
	
# user_partial_conclusions.clear()

# rules.clear()
# premises.clear()
# partial_conclusions.clear()
# final_conclusions.clear()

def index(request):
	user_premises.clear()
	user_partial_conclusions.clear()
	user_results.clear()
	final_results.clear()
	parse('D:\\An IV CTI 2018\\SE\\Holiday-recommender\\rules.txt')
	if request.method == 'POST':
		data = request.POST.copy()
		choices = data.getlist('choice')
		for choice in choices:
			user_premises.append(choice)
	context = {'question': question_list[i], 'next_question': question_list[i+1]}
	return render(request, 'expertsystem/index.html', context)

def detail(request, question_id):
	if request.method == 'POST':
		data = request.POST.copy()
		choices = data.getlist('choice')
		for choice in choices:
			user_premises.append(choice)
	question = get_object_or_404(Question, pk=question_id)
	if question_id == Question.objects.count():
		return render(request, 'expertsystem/last_question.html', {'question': question})
	else:
		return render(request, 'expertsystem/detail.html', {'question': question, 'next_question': question_id+1})

def results(request):
	if request.method == 'POST':
		data = request.POST.copy()
		choices = data.getlist('choice')
		for choice in choices:
			user_premises.append(choice)
	#response = "You're looking at the results."
	#return HttpResponse(user_premises)
	get_recommendations()
	#return HttpResponse(final_results) #daca pun aici apelul la get_recommandations se apeleaza de mai multe ori aiurea no idea why
	return render(request, 'expertsystem/results.html', {'final_results': final_results})