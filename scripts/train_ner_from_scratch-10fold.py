# -*- coding: UTF-8 -*-

from __future__ import unicode_literals, print_function
import plac, random, spacy, os, glob, ast, datetime
from pathlib import Path
from spacy.util import minibatch, compounding 
from spacy import displacy
import codecs, json, sys, os

def train_mod(output_dir, train, iterations):
	
	nlp = spacy.blank('ar')  # create blank Language class
	# create the built-in pipeline components and add them to the pipeline
	# nlp.create_pipe works for built-ins that are registered with spaCy
	if 'ner' not in nlp.pipe_names:
		ner = nlp.create_pipe('ner')
		nlp.add_pipe(ner, last=True)
       
    # add labels
	for _, annotations in train:
		for ent in annotations.get('entities'):
			ner.add_label(ent[2])

    # get names of other pipes to disable them during training
	other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
	with nlp.disable_pipes(*other_pipes):  # only train NER
		optimizer = nlp.begin_training()
		for itn in range(iterations):
			#print("Statring iteration " + str(itn))
			losses = {}
			for text, annotations in train:
				nlp.update(
			 		[text],  # batch of texts
					[annotations],  # batch of annotations
					drop=0.2,  # dropout - make it harder to memorise data
					sgd=optimizer,  # callable to update weights
					losses=losses)
	print(str(datetime.datetime.now())+": training is finished")
	
	# save model to output directory
	output_dir = Path(output_dir)
	if not output_dir.exists():
		print(output_dir)
		output_dir.mkdir(parents=True, exist_ok=True)
	nlp.to_disk(output_dir)
	print("Saved model to", output_dir)
	
	return nlp
	
# MAIN PROGRAM	
# Execution: 
# python train_ner_from_scratch-10.py <name_folder_train_data> <model_save_folder>
# for instance:
#  python3 train_ner_from_scratch-10fold.py ../CorpusAnnote3cat/groupsTahtaoui/ ../Models/Tahtaoui/

base_in_dir=sys.argv[1]
out_dir=sys.argv[2]

print("debut : "+str(datetime.datetime.now()))
# from X groups, take out one group and train with the rest of the groups, this results in X runs of experiments
for x in range(10):
	TRAIN_DATA = []
	dataset_train = []
	
	# set train datasets
	for y in range(10):
		if x != y:
			dataset_train.append(y)
	print("training datasets: "+str(dataset_train))
		
	# add the actual data to train datasets
	for dossier_nb in dataset_train:
		train_d = glob.glob(base_in_dir+"group"+str(dossier_nb)+"/*.txt")
		for j in train_d:
			#print("reading "+j)
			with codecs.open(j, 'r+', encoding='utf8') as train_f:
				train_l = ast.literal_eval('[{0}]'.format(train_f.read()))
				TRAIN_DATA.extend(train_l[0]) 
	#print("nb of sentences in the training dataset: "+str(len(TRAIN_DATA)))
	
	# execute experiment
	#print(out_dir+"model"+str(dataset_train).replace("[","").replace("]","").replace(" ","").replace(",","-"))
	#print(TRAIN_DATA)
	train_mod(out_dir+"model"+str(dataset_train).replace("[","").replace("]","").replace(" ","").replace(",","-"), TRAIN_DATA, 20)

print("fin : "+str(datetime.datetime.now()))
	

