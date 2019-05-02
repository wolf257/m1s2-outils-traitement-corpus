#!/usr/bin/env/ python3
# -*- coding : utf-8 -*-

# Syntaxe : python3 main.py

import sys
import treetaggerwrapper
import pprint

from collections import defaultdict


def taggingTreetagger(nameFileIn, nameFileOut, tagger):

    with open(nameFileIn, mode='r', encoding='utf-8') as filein:
        with open(nameFileOut, mode='w', encoding='utf-8') as fileout:

            for sentence in filein:

                #TAGGER LA PHRASE
                tags = tagger.TagText(sentence)
                tags2 = treetaggerwrapper.make_tags(tags)

                for elt in tags:
                    fileout.write(f"{str(elt)}\n")


def recupInfosPOSTagging(dico_eval_pos_total, dico_eval_error_total, nameFileReference, nameFileTreeTagger):
    ref = open(nameFileReference, mode="r").readlines()
    tag = open(nameFileTreeTagger, mode="r").readlines()
    
    if len(ref) != len(tag):
        print(f"On a probablement un problème d'alignement.")
    
    for index, (ligne_ref, ligne_tag) in enumerate(zip(ref, tag)):

        # Découpage lignes
        ligne_ref = ligne_ref.split('\t')
        ligne_tag = ligne_tag.strip().split('\t')

        # Extraction POS
        pos_ref = ligne_ref[1].strip()
        pos_ref = pos_ref.split(':')[0] if ":" in pos_ref else pos_ref
        pos_tag = ligne_tag[1].strip()
        pos_tag = pos_tag.split(':')[0] if ':' in pos_tag else pos_tag
        
        dico_eval_pos_total.setdefault(pos_ref, {})
        dico_eval_pos_total[pos_ref].setdefault("total", 0)
        dico_eval_pos_total[pos_ref].setdefault("correct", 0)
        
        
        # Comparaison et remplissage dicos
        dico_eval_pos_total[pos_ref]['total'] += 1
        
        if pos_ref == pos_tag :
            dico_eval_pos_total[pos_ref]['correct'] += 1
        else :
            dico_eval_error_total.setdefault( (pos_ref, pos_tag) , 0)
            dico_eval_error_total[(pos_ref, pos_tag)] +=1
        
def evaluationPOSTagging(dico_eval_pos_total, dico_eval_error_total):

    """ Calculs """
 
    # Précision Globale : nbCorrect / nbTotal    
    nbTotal = sum ( dico_eval_pos_total[pos]['total'] for pos in dico_eval_pos_total )
    nbCorrect = sum( dico_eval_pos_total[pos]['correct'] for pos in dico_eval_pos_total )
    
    precisionGlobale = round(float(nbCorrect/nbTotal)*100 , 2)
    
    print(f"* Precision Globale : {precisionGlobale}% ({nbCorrect}/{nbTotal})\n")

    # Précision par POS
    print("* Précision par POS (par ordre de fréquence décroissant):")
    sorted_pos = sorted( [ (dico_eval_pos_total[pos]['total'], pos) for pos in dico_eval_pos_total ], reverse = True )
    
    for (_, pos) in sorted_pos:
        nbCorrectPOS = dico_eval_pos_total[pos]['correct']
        nbTotalPOS = dico_eval_pos_total[pos]['total']
        precisionPOS = round(float(nbCorrectPOS/nbTotalPOS)*100 , 2)
        print(f"\t{pos} : {precisionPOS}% ({nbCorrectPOS}/{nbTotalPOS})")

    print("\n")

    # Erreurs, par frequence
    print(f"* Erreurs (par ordre de fréquence décroissant):")
    erreurs = sum( dico_eval_error_total.values() )
    sorted_errors = sorted( [ (dico_eval_error_total[erreur], erreur) for erreur in dico_eval_error_total ], reverse = True )
    
    if len(sorted_errors) == 0:
        print("\tApparemment, il n'y a aucune erreur.")
    else:
        for (nbErr, err) in sorted_errors:
            print(f"{err} - {nbErr}")
    

def main():

    TREETAGGER_ROOT = './treetagger/'
    fichiersDeBase = ['./bashung.txt', './sequoia.txt']

    # PARTIE TAGGING
    print(f"\n\n- Tagging des fichiers.\n")
    
    # Construction et configuration du wrapper
    tagger = treetaggerwrapper.TreeTagger(TAGLANG='fr', TAGINENC='utf-8',
                                          TAGOUTENC='utf-8' , TAGDIR=TREETAGGER_ROOT)

    for nameFileIn in fichiersDeBase:
        # NB : le '-new' pour éviter d'écraser les fichiers que nous avons manuellement modifiés 
        nameFileOut = nameFileIn.split('/')[-1].split('.')[0] + '-treetagger-new.txt'

        taggingTreetagger(nameFileIn, nameFileOut, tagger)


    # PARTIE EVALUATION (librement inspiré du script eval_pos_tagger.py)
    
    dico_eval_pos_total = {}
    # forme : dico_eval_pos_total = { 'VER' : { 'correct' : 13, 'total' : 14 }, 'NOM' ... }
    
    dico_eval_error_total = {}
    # forme : dico_eval_error_total = { ('NOM','ADJ') : 10, ... } c-a-d que 10 fois, un nom a été taggé comme adj.
    
    print(f"- Récupération des infos de POS (tagging + référence).\n")
    
    for nameFileIn in fichiersDeBase:
        dico_eval_pos_texte = {}
        dico_eval_error_texte = {}
        
        nameFileTreeTagger = nameFileIn.split('/')[-1].split('.')[0] + '-treetagger.txt'
        nameFileReference = nameFileIn.split('/')[-1].split('.')[0] + '-reference.txt'

        print(f"\n\n ******* Texte : {nameFileIn} ******* \n")
        
        recupInfosPOSTagging(dico_eval_pos_texte, dico_eval_error_texte, nameFileReference, nameFileTreeTagger)
        
        evaluationPOSTagging(dico_eval_pos_texte, dico_eval_error_texte)
        
        recupInfosPOSTagging(dico_eval_pos_total, dico_eval_error_total, nameFileReference, nameFileTreeTagger)

    print(f"\n\n ******* Évaluation globale ******* \n")

    evaluationPOSTagging(dico_eval_pos_total, dico_eval_error_total)
    
if __name__ == '__main__':
    main()

