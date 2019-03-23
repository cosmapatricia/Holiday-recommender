premises = []
partial_conclusions = []
final_conclusions = []
rules = {}

def parse(path):
	try:
		with open(path,'r') as f:
			lines = f.readlines()  
			print("File has been opened")
			# print(lines) 
	except:
		print("Cannot open ") + path
		return

	final_conclusions.extend(lines[0].split(', '))
	final_conclusions[len(final_conclusions)-1] = final_conclusions[len(final_conclusions)-1].rstrip()
# 	print(final_conclusions)

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

# print("Partial conclusions: ")
# print(partial_conclusions)
# print("Rules: ")
# print(rules)
