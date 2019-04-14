#!/usr/bin/env python3
#-*- coding: utf8 -*-

import random
import pprint
import spacy

from pathlib import Path
from spacy.util import minibatch, compounding

def load_model_base(model):
    if model is not None:
        nlp = spacy.load(model)  # load existing spaCy model
        print(f"Loaded model {model}")
    else:
        nlp = spacy.blank("fr")  # create blank Language class
        print("Création modèle vierge 'fr'")
    
    return nlp
    
def phase_training(nlp, model, TRAIN_DATA):
    
    """Load the model, set up the pipeline and train the entity recognizer."""

    # create the built-in pipeline components and add them to the pipeline
    # nlp.create_pipe works for built-ins that are registered with spaCy
    if "ner" not in nlp.pipe_names:
        ner = nlp.create_pipe("ner")
        nlp.add_pipe(ner, last=True)
    # otherwise, get it so we can add labels
    else:
        ner = nlp.get_pipe("ner")

    # add labels
    for _, annotations in TRAIN_DATA:
        for ent in annotations.get("entities"):
            ner.add_label(ent[2])

    # print(f"{nlp.pipe_names}")
    # get names of other pipes to disable them during training
    pipes_a_ne_pas_entrainer = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
    
    with nlp.disable_pipes(*pipes_a_ne_pas_entrainer):  # only train NER
    
        # reset and initialize the weights randomly – but only if we're
        # training a new model
        if model is None:
            nlp.begin_training()
        
        n_iteration = 100
        
        print(f"Pertes : ")
        for i in range(n_iteration):
            random.shuffle(TRAIN_DATA)
            pertes = {}
            
            # paquet up the examples using spaCy's minipaquet
            paquets = minibatch(TRAIN_DATA, size=compounding(4.0, 32.0, 1.001))
            
            for paquet in paquets:
                texts, annotations = zip(*paquet)
                nlp.update(
                    texts,  # paquet of texts
                    annotations,  # paquet of annotations
                    drop=0.5,  # dropout - make it harder to memorise data
                    losses=pertes,
                )
            print(f" - {pertes}", end=' ')
    
    list_special_cases = {
        "y'a" : [
            {'ORTH': "y'", 'LEMMA': "y", 'POS': "PRO"},
            {'ORTH': "a"}
        ],
        "disoit" : [
            {'ORTH': "disoit", 'LEMMA': "dire", 'POS': "VERB"}
        ],
        "Nostre" : [
            {'ORTH': 'Nostre', 'LEMMA': "notre", 'POS': "PRO", 'NORM': "notre",}
        ],
        "Roy" : [
            {'ORTH': 'Roy', 'LEMMA': "roi", 'POS': "NOUN", 'NORM': "roi",}
        ],
        "Heur" : [
            {'ORTH': 'Heur', 'LEMMA': "bonheur", 'POS': "NOUN", 'NORM': "bonheur"}
        ],
        "enfans" : [
            {'ORTH': 'enfans', 'LEMMA': "enfant", 'POS': " ", 'NORM': "enfants"}
        ],
        "sçavent" : [
            {'ORTH': 'sçavent', 'LEMMA': "savoir", 'POS': "VERB", 'NORM': "savent"}
        ],
        "tantost" : [
            {'ORTH': 'tantost', 'LEMMA': "tantôt", 'POS': "PROP",}
        ],
        "esté" : [
            {'ORTH': 'esté', 'LEMMA': "être", 'POS': "AUX", 'NORM': "était"}
        ],
        "faict" : [
            {'ORTH': 'faict', 'LEMMA': "faire", 'POS': "VERB", 'NORM': "fait"}
        ],
        "s’escria" : [
            {'ORTH': "s'", 'LEMMA': "se", 'POS': " "},
            {'ORTH': "escria", 'LEMMA': "écrier", 'POS': "VERB"}
        ],
        "s’estant" : [
            {'ORTH': "s'", 'LEMMA': "se", 'POS': " "},
            {'ORTH': "estant", 'LEMMA': "être", 'POS': "AUX"}
        ],
        "enquis" : [
            {'ORTH': 'enquis', 'LEMMA': "enquérir", 'POS': "VERB", 'NORM': "enquit"}
        ],
        "c’estoit" : [
            {'ORTH': "c'", 'LEMMA': "ce", 'POS': " "},
            {'ORTH': "estoit", 'LEMMA': "être", 'POS': "VERB", 'NORM':"était"}
        ],
        "luy" : [
            {'ORTH': 'luy', 'LEMMA': "lui", 'POS': "PRO", 'NORM': "lui"}
        ],
        "fist" : [
            {'ORTH': 'fist', 'LEMMA': "faire", 'POS': "VERB", 'NORM': "fait"}
        ],
        "verifioit" : [
            {'ORTH': 'verifioit', 'LEMMA': "vérifier", 'POS': "VERB", 'NORM': "vérifiait"}
        ],
        "despens" : [
            {'ORTH': 'despens', 'LEMMA': "dépend", 'POS': "NOUN", 'NORM': "dépens"}
        ],
        "l’advertissement" : [
            {'ORTH': "l'", 'LEMMA': "le"}, {'ORTH': "advertissement", 'LEMMA': "avertissement", 'POS': "NOUN"}
        ],
        "estat" : [
            {'ORTH' : 'estat', 'LEMMA': "état", 'POS': "NOUN", 'NORM': "état"}
        ],
        "dixiesme" : [
            {'ORTH' : 'dixiesme', 'LEMMA': "dixième", 'POS': "NUM", 'NORM': "dixième"}
        ],
        "avoit" : [
            {'ORTH' : 'avoit', 'LEMMA': "avoir", 'POS': "AUX", 'NORM': "avait"}
        ],
        "estat" : [
            {'ORTH' : 'estat', 'LEMMA': "état", 'POS': "NOUN", 'NORM': "état"}
        ],
        "branslé" : [
            {'ORTH' : 'branslé', 'LEMMA': "branler", 'POS': "VERB", 'NORM': "branlé"}
        ],
        "veu" : [
            {'ORTH' : 'veu', 'LEMMA': "voir", 'POS': "VERB", 'NORM': "vu"}
        ]
    }

    for mot_ancien in list_special_cases.keys():
        nlp.tokenizer.add_special_case(mot_ancien, list_special_cases[mot_ancien])

def test_model_trained(nlp, TRAIN_DATA):
    # test the trained model
    print(f"\n\n=== Résultat du modèle entrainé ===")
    for text, _ in TRAIN_DATA:
        print(f"\n- Phrase de base : {text}")
        doc = nlp(text)
        ent = [(ent.text, ent.label_) for ent in doc.ents]
        print(f"\n* Entités repérées :")
        pprint.pprint(ent)
        tok = [(t.text, t.ent_type_, t.ent_iob, t.pos_, t.lemma_) for t in doc]
        print(f"\n* Tokens :")
        pprint.pprint(tok)

def save_model_trained(nlp, output_dir):
    # save model to output directory
    if output_dir is not None:
        output_dir = Path(output_dir)
        if not output_dir.exists():
            output_dir.mkdir()
        nlp.to_disk(output_dir)
        print(f"\n\nModèle sauvegardé sous : {output_dir}/\n")

def load_and_test_mymodel(dir_model, output_dir,  DATA_TO_TEST):
    # test the saved model
    nlp2 = spacy.load(dir_model)
    print(f"\n\nModèle importé de : {dir_model}/\n")

    if output_dir is not None:
        output_dir = Path(output_dir)
        if not output_dir.exists():
            output_dir.mkdir()

    print(f"=== Résultat du modèle sauvegardé ===")
    with open(str(output_dir.absolute())+'/output.txt', mode='w') as fileout:
        for phrase in DATA_TO_TEST:
            print(f"\n- Phrase de base : {phrase}")
            doc = nlp2(phrase)
        
            ent = [(ent.text, ent.label_) for ent in doc.ents]
            print(f"\n* Entités repérées :")
            pprint.pprint(ent)
        
            fileout.write(f"\n === Phrase de base : {phrase} === \n")
            
            print(f"\n* Les tokens et leurs informations ont été rajoutés au fichier {output_dir}/output.txt.\n")
            
            fileout.write(f"\n* Tokens :\n\n")
            for t in doc:
                fileout.write(f"- {t.text}\t{t.ent_type_} \t {t.ent_iob} \t {t.pos_} \t {t.lemma_}\n")
        
def main():
    
    #var
    TRAIN_DATA = [
        ("Stadia fonctionne grâce à des data centers", {"entities": [(0, 6, "MISC")]}),
        ("la firme de Mountain View a levé le voile sur Stadia", {"entities": [(12, 25, "LOC"), (46, 52, "MISC")]}),        
    ]
    
    model_base = 'fr_core_news_md'
    
    nlp = load_model_base(model_base)
    phase_training(nlp, model_base, TRAIN_DATA)
    test_model_trained(nlp, TRAIN_DATA)
    
    #var
    dir_model ='./sauv_modele'
    
    save_model_trained(nlp, dir_model)
    
    ##########################################################
    print(f"\n +++ À partir d'ici, on recommence en chargeant notre modèle, en lui demandant de repérer des entités sur de nouvelles phrases, et enfin de tokeniser les phrases (surtout pour celles de Montaigne).")
    
    #var
    DATA_TO_TEST = [
        "Stadia fonctionne sur du vent de mer de la marque Boss.",
        "La firme de Mountain View a levé le voile sur Marseille avec le comte de Monte Cristo et son ami Dwyane Wade.",
        "Les enfans sçavent le conte du Roy Croesus à ce propos : lequel, ayant esté pris par Cyrus et condamné à la mort, sur le point de l’execution, il s’escria : O Solon, Solon’.",
        "Cela rapporté à Cyrus, et s’estant enquis que c’estoit à dire, il luy fist entendre qu’il verifioit lors à ses despens l’advertissement qu’autrefois luy avoit donné Solon, que les hommes, quelque beau visage que fortune leur face, ne se peuvent appeller heureux, jusques à ce qu’on leur aye veu passer le dernier jour de leur vie.",
        "Cela pour l’incertitude et varieté des choses humaines, qui d’un bien leger mouvement se changent d’un estat en autre, tout divers.",
        "Et pourtant Agesilaus, à quelqu’un qui disoit heureux le Roy de Perse, de ce qu’il estoit venu fort jeune à un si puissant estat.",
        "Ouy mais, dit-il, Priam en tel age ne fut pas malheureux. ",
        "Tantost, des Roys de Macedoine, successeurs de ce grand Alexandre, il s’en faict des menuisiers et greffiers à Rome ; des tyrans de Sicile, des pedantes à Corinthe.",
        "D’un conquerant de la moitié du monde, et Empereur de tant d’armées, il s’en faict un miserable suppliant des belitres officiers d’un Roy d’Égypte : tant cousta à ce grand Pompeius la prolongation de cinq ou six mois de vie. ",
        "Et, du temps de nos peres, ce Ludovic Sforce, dixiesme Duc de Milan, soubs qui avoit si long temps branslé toute l’Italie, on l’a veu mourir prisonnier à Loches;"
    ]
    
    output_dir = './output'
    
    load_and_test_mymodel(dir_model, output_dir, DATA_TO_TEST)


if __name__ == "__main__":
    main()
