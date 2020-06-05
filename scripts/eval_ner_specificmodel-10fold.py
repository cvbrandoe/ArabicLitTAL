# -*- coding: UTF-8 -*-

from __future__ import unicode_literals, print_function
import plac, random, spacy, os, glob, ast, datetime
from pathlib import Path
from spacy.util import minibatch, compounding 
from spacy import displacy
import codecs, json, sys
from spacy.gold import GoldParse
from spacy.scorer import Scorer

def evaluate(ner_model, examples):
	scorer = Scorer()
	for input_, annot in examples:
		doc_gold_text = ner_model.make_doc(input_)
		gold = GoldParse(doc_gold_text, entities=annot['entities'])
		pred_value = ner_model(input_)
		scorer.score(pred_value, gold)
	return scorer.scores
	
# MAIN PROGRAM	
# Execution: 
# python eval_ner_specificmodel-10.py <eval_dataset> <models_folder> <cats> 

# for instance:
# python3 eval_ner_specificmodel-10fold.py ../CorpusAnnote1cat/groupsTahtaoui/  ../Models/Tahtaoui/ LOC 
# python3 eval_ner_specificmodel-10fold.py ../CorpusAnnote3cat/groupsTahtaoui/  ../Models/Tahtaoui/ LOC-Admin,LOC-Natur,LOC-Build

eval_data_dir=sys.argv[1]
model_data_dir=sys.argv[2]
cats=sys.argv[3]

log_exp_measures = open(model_data_dir+"log-measures.txt","w")
log_exp_error_ana = open(model_data_dir+"log-error-analysis.csv","w")
print("debut : "+str(datetime.datetime.now()))
log_exp_measures.write("debut : "+str(datetime.datetime.now())+"\n")
log_exp_error_ana.write("debut : "+str(datetime.datetime.now())+"\n")
	
for x in range(10):
	dataset_train = []
	# set train datasets
	for y in range(10):
		if x != y:
			dataset_train.append(y)
			
	print("Loading model from"+model_data_dir+"model"+str(dataset_train).replace("[","").replace("]","").replace(" ","").replace(",","-"))	
	#log_exp_error_ana.write("Loading model from" +model_data_dir+"model"+str(dataset_train).replace("[","").replace("]","").replace(" ","").replace(",","-")+"\n")

	nlp2 = spacy.load(model_data_dir+"model"+str(dataset_train).replace("[","").replace("]","").replace(" ","").replace(",","-"))		

	EVAL_DATA = []
	dataset_eval = []

	# set eval dataset file identifiers
	dataset_eval.append(x)
	print("Evaluation data set is:" +str(dataset_eval))
	log_exp_error_ana.write("Evaluation data set is:" +str(dataset_eval)+"\n")

			
	# add the actual data to the eval dataset
	print("Evaluation data set is:"+eval_data_dir+"group"+str(dataset_eval[0]))
	log_exp_error_ana.write("Evaluation data set is:"+eval_data_dir+"group"+str(dataset_eval[0])+"\n")
	log_exp_measures.write("\n")
	log_exp_measures.write("Evaluation data set is:"+eval_data_dir+"group"+str(dataset_eval[0])+"\n")
	
	eval_d = glob.glob(eval_data_dir+"group"+str(dataset_eval[0])+"/*.txt")
	for i in eval_d:
		with codecs.open(i, 'r+', encoding='utf8') as eval_f:
			eval_l = ast.literal_eval('[{0}]'.format(eval_f.read()))
			EVAL_DATA.extend(eval_l[0]) 
	print("nb of sentences in the evaluation dataset: "+str(len(EVAL_DATA)))
	#log_exp_error_ana.write("nb of sentences in the evaluation dataset: "+str(len(EVAL_DATA))+"\n")
	
	for i in cats.split(","):
		print("cat:"+i)
		EVAL_DATA_CAT = []
		for sent, anns in EVAL_DATA:
			anns_loc_adm_list = [el for el in anns.get("entities") if el[2]==str(i)]
			#print(anns_loc_adm_list)
			EVAL_DATA_CAT.append((sent,{'entities': anns_loc_adm_list}))			
	
		#print(EVAL_DATA_CAT)
		log_exp_measures.write("Type\tP\tR\tF\t\n")
	
		print("Evaluation "+i+" per category")
		results = evaluate(nlp2, EVAL_DATA_CAT)
		log_exp_measures.write(i+"\t"+str(results['ents_p'])+"\t"+str(results['ents_r'])+"\t"+str(results['ents_f'])+"\n")
		log_exp_measures.write("")
	
	# test the eval data
	print("Looking at errors in group"+str(x))
	ent_refs=[]
	ent_test=[]
	for text, anns2 in EVAL_DATA:
		#print (text)
		doc = nlp2(text)
		ent_test = [(ent.start_char, ent.end_char, ent.text, ent.label_) for ent in doc.ents]
		for ref_ent in anns2.get('entities'):
			ent_refs.append((ref_ent[0], ref_ent[1], text[ref_ent[0]:ref_ent[1]], ref_ent[2]))		
		#comparer les listes et sortir les VP, FN, TP non-matchs.
		#log_exp_error_ana.write("REF:")
		#log_exp_error_ana.write(str(ent_refs)+"\t")
		#log_exp_error_ana.write("TEST:")
		
		#print("REF:"+str(ent_refs)+"\n")
		#print("TEST:"+str(ent_test)+"\n")

		vp = [x for x in ent_refs if x in ent_test]
		if vp:
			log_exp_error_ana.write("true positives:"+"\t") # ils sont dans le ref et dans le test 
			log_exp_error_ana.write(str(vp[0][0])+"\t"+str(vp[0][1])+"\t"+str(vp[0][2])+"\t"+str(vp[0][3]))
			log_exp_error_ana.write("\n")
			
		fp = [x for x in ent_refs if x not in ent_test]
		if fp:
			log_exp_error_ana.write("False positives:"+"\t") # ils sont dans le ref mais pas dans le test 
			log_exp_error_ana.write(str(fp[0][0])+"\t"+str(fp[0][1])+"\t"+str(fp[0][2])+"\t"+str(fp[0][3]))
			log_exp_error_ana.write("\n")
		
		fn = [x for x in ent_test if x not in ent_refs]
		if fn:
			log_exp_error_ana.write("False negatives:"+"\t") # ils ne sont pas dans le ref ils ont été répérés par le systeme  
			log_exp_error_ana.write(str(fn[0][0])+"\t"+str(fn[0][1])+"\t"+str(fn[0][2])+"\t"+str(fn[0][3]))
			log_exp_error_ana.write("\n")
		ent_refs=[]
	
print("fin : "+str(datetime.datetime.now()))
log_exp_measures.write("fin : "+str(datetime.datetime.now())+"\n")
log_exp_error_ana.write("fin : "+str(datetime.datetime.now())+"\n")
log_exp_measures.close()
log_exp_error_ana.close()
