# -*- coding: UTF-8 -*-

import json, codecs, ast

#GoldStandard_Bin_Nabi.json - ok
#GoldStandard_Mubarak.json - ok
#GoldStandard_Shidiaq.json - ok
#GoldStandard_Tahtaoui.json - ok
#GoldStandard_Zaki.json - ok
#GoldStandard_Zidan.json - ok

with codecs.open('../annotated-data-original/GoldStandard_Tahtaoui.json', 'r+', encoding='utf-8') as json_file:
	content = ast.literal_eval('[{0}]'.format(json_file.read()))
	# phrase, EN
	dico = {}
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
		
count = 0
for dic in dico:
	out_file = codecs.open("../"+str(count)+".txt", "w", encoding='utf-8')
	out_file.write("[(")
	out_file.write("\""+str(dic)+"\"")
	out_file.write(","+str(dico[dic]))	
	out_file.write(")]")
	out_file.write("\n")
	out_file.close()
	count = count + 1
		