# ArabicLitTAL

This repository contains:
- a literary corpus in Arabic annotated in spatial named entities
- named entity recognition models for Spacy created from these data


**Authors**

Motasem ALRAHABI, Carmen BRANDO, Muhamed ALKHALIL, Joseph DICHY

Sorbonne Université, France, motasem.alrahabi@paris-sorbonne.fr

École des Hautes Études en Sciences Sociales, France, carmen.brando@ehess.fr

Université de New York, Abou Dhabi, EAU, muhamed.alkhalil@nyu.edu

Université Canadienne de Doubaï (CUD), EAU, joseph.dichy@yahoo.fr


**The corpus**

- A Paris Profile (1834) by Rifa'a al-Tahtawi
- The Uncovering of Europe (1857) by A. Fares Al-Shidyaq
- The World in Paris (1900) by Ahmad Zaki
- A Trip to Europe (1912) by Jurji Zaydan
- The Paris Days (1931) by Zaki Mubarak
- Memoirs of a Witness to the Century (1965) by Malek Bin Nabi

These texts were annotated in spatial named entites (administrative places, buildings, natural places) by : 

Motasem ALRAHABI, 
Muhamed ALKHALIL, 
Joseph DICHY.

Anotations are standoff at the phrase level, the format is Spacy's JSON (https://spacy.io/api/annotation).


**The NER models**

There are ten models created for a 10-fold cross validation. Performances for each models is provided as well as errors found in terms of false positives and false negatives.

