from parser import *

user_premises = ['sea', 'sunbathe', 'greek food', 'Europe', 'diving', 'island']
user_partial_conclusions = []

parse('C:\\Users\\Melissa\\Desktop\\SE\\rules.txt')

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

for conclusion in final_conclusions:
	print(inference(conclusion))
	
user_partial_conclusions.clear()
rules.clear()
premises.clear()
partial_conclusions.clear()
final_conclusions.clear()