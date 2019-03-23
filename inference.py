from parser import *

user_premises = ['Europe', 'sea', 'relaxing', 'sightseeing', 'quiet', 'sunbathe', 'shop at designer boutiques', ' shop at bazaars', 'diving', 'visit historical places', 'italian food', 'greek food', 'capital', 'exotic', 'island', 'high-end']
user_partial_conclusions = []

#parse('D:\\An IV CTI 2018\\SE\\Holiday-recommender\\rules.txt') 
parse('D:\\AC\\4th_year\\SE\\Holiday-recommender\\rules.txt')

print('\nInference data: ')
print('\nRules: ')
print(rules)
print('\nPremises: ')
print(premises)
print('\nPartial conclusions: ')
print(partial_conclusions)
print('\nFinal conclusions: ')
print(final_conclusions)
print('\n')

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

results = []
for conclusion in final_conclusions:
	results.append(inference(conclusion))

results = list(set(results))
	
no_result = True
for result in results:
	if result != 0:
		print(result)
		no_result = False
if no_result:
	print('No matches found')
	
user_partial_conclusions.clear()
rules.clear()
premises.clear()
partial_conclusions.clear()
final_conclusions.clear()