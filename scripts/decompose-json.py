# -*- coding: UTF-8 -*-

import json, codecs, ast, os
import random

#GoldStandard_Bin_Nabi.json - ok
#GoldStandard_Mubarak.json - ok
#GoldStandard_Shidiaq.json - ok
#GoldStandard_Tahtaoui.json - ok
#GoldStandard_Zaki.json - ok
#GoldStandard_Zidan.json - ok

directory = '../annotated-data-original'
dico = {}
for filename in os.listdir(directory):
	if filename.endswith(".json"): 
		print(os.path.join(directory, filename))
		with codecs.open(os.path.join(directory, filename), 'r+', encoding='utf-8') as json_file:
			content = ast.literal_eval('[{0}]'.format(json_file.read()))
			print(len(content[0]))
			for i in range(len(content[0])):
				ent = (content[0][i][1]['entities'][0][0],content[0][i][1]['entities'][0][1],str(content[0][i][1]['entities'][0][2]))		
				if str(content[0][i][0]) in dico:
					#print("add entity to existing list")
					if ent not in dico[str(content[0][i][0])]['entities']:
						dico[str(content[0][i][0])]['entities'].append(ent)
				else:
					#print("create list and add entity")
					dico[str(content[0][i][0])] = {'entities':[]}
					dico[str(content[0][i][0])]['entities'].append(ent)
print(len(dico))

my_list = list(range(0,len(dico))) # list of integers from 1 to 99
random.shuffle(my_list)

count = 0
for dic in dico:
	out_file = codecs.open("../CorpusAnnote3cat/groupsAll/"+str(my_list[count])+".txt", "w", encoding='utf-8')
	out_file.write("[(")
	out_file.write("\""+str(dic)+"\"")
	out_file.write(","+str(dico[dic]))	
	out_file.write(")]")
	out_file.write("\n")
	out_file.close()
	count = count + 1	