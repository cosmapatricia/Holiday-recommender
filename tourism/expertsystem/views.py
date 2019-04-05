from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.http import Http404
from .models import Question, Result
# Create your views here.

question_list = Question.objects.all()
database_conclusions_list = Result.objects.all() #retrieve all objects from table Result which contains all possible conclusions and their descriptions
result_list = {} # resulted conclusion name - conclusion description mapping

i=0

# parser data
premises = []
partial_conclusions = []
final_conclusions = []
rules = {}

# user data
user_premises = []
user_partial_conclusions = []
user_results = [] # inference results (with zeros for unactivated conclusions)
user_results2 = [] 
final_results = [] # results without description

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
	user_results2 = list(set(user_results))
	no_result = True
	for result in user_results2:
		if result != 0:
			final_results.append(result)
			no_result = False
	if no_result:
		final_results.append('No matches found')
	return final_results

q1_answer = []
q2_answer = []
q10_answer = []

def append_choices(choices_list, list):
	for choice in choices_list:
		list.append(choice)

def clear_session():
	user_premises.clear()
	user_partial_conclusions.clear()
	user_results.clear()
	user_results2.clear()
	final_results.clear()
	result_list.clear()
	q1_answer.clear()
	q2_answer.clear()
	q10_answer.clear()

	
def index(request):
	clear_session()
	parse('D:\\An IV CTI 2018\\SE\\Holiday-recommender\\rules.txt')
	#parse('D:\\AC\\4th_year\\SE\\Holiday-recommender\\rules.txt')
	if request.method == 'POST':
		data = request.POST.copy()
		choices = data.getlist('choice')
		append_choices(choices, user_premises)
	context = {'question': question_list[i], 'next_question': question_list[i+1]}
	return render(request, 'expertsystem/index.html', context)

def detail(request, question_id):
	question = get_object_or_404(Question, pk=question_id)

	if request.method == 'POST':
		data = request.POST.copy()
		choices = data.getlist('choice')
		append_choices(choices, user_premises)
		if question_id == 2:
			append_choices(choices, q1_answer)
			print(q1_answer)
		elif question_id == 3:
			append_choices(choices, q2_answer)
			print(q2_answer)
			if 'mountain' in q2_answer:
				return render(request, 'expertsystem/detail.html', {'question': question, 'next_question': question_id+4})
		elif question_id == 11:
			append_choices(choices, q10_answer)
			print(q10_answer)
			if 'exotic' not in q10_answer:
				results(request)
				return render(request, 'expertsystem/results.html', {'final_results': final_results, 'result_list': result_list})
		elif question_id == 8 and ('Europe' not in q1_answer):
			question = get_object_or_404(Question, pk=(question_id+1))
			return render(request, 'expertsystem/detail.html', {'question': question, 'next_question': question_id+2})
		elif question_id == 4 and 'city-break' in q2_answer:
			return render(request, 'expertsystem/detail.html', {'question': question, 'next_question': question_id+2})
		elif question_id == 6 and 'city-break' in q2_answer:
			return render(request, 'expertsystem/detail.html', {'question': question, 'next_question': question_id+2})
		elif question_id == 9 and ('city-break' in q2_answer or 'mountain' in q2_answer):
			results(request)
			return render(request, 'expertsystem/results.html', {'final_results': final_results, 'result_list': result_list})
		elif question_id == 5 and 'sea' in q2_answer:
			return render(request, 'expertsystem/detail.html', {'question': question, 'next_question': question_id+3})
			
	if question_id == Question.objects.count():
		if 'exotic' in q10_answer:
			return render(request, 'expertsystem/last_question.html', {'question': question})
	else:
		return render(request, 'expertsystem/detail.html', {'question': question, 'next_question': question_id+1})

def results(request):
	if request.method == 'POST':
		data = request.POST.copy()
		choices = data.getlist('choice')
		append_choices(choices, user_premises)
	get_recommendations()
	for result in final_results:
		for res in database_conclusions_list:
			if result == res.result_name:
				result_list[result] = res.result_text
	return render(request, 'expertsystem/results.html', {'final_results': final_results, 'result_list': result_list})