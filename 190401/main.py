#!/usr/bin/env/ python3
# -*- coding : utf-8 -*-

import spacy

def analyse_svo(phrase, nlp):
    """ docstring of the function """

    sujet = ''
    obj = ''
    verbe = ''

    print(f"\n====== {phrase} =======\n")

    doc = nlp(phrase)

    for token in doc:
        print(f"{token} - {token.pos_} - {token.dep_}", end=" | ")

        if token.pos_ == "VERB":
            verbe = token
            sujet = [eltSub for child in token.children for eltSub in child.subtree if child.dep_ == "nsubj" ]
            obj = [eltSub for child in token.children for eltSub in child.subtree if child.dep_ == "obj" ]

    sujet = ' '.join(map(str, sujet))
    obj = ' '.join(map(str, obj))

    print(f"\n\nS : {sujet}, V : {verbe}, O : {obj}")

def main():
    # nlp = spacy.load("fr_core_news_sm")
    nlp = spacy.load("fr_core_news_md")

    listePhrases = [
        "Le chat mange la souris.",
        "Les enfants n’aiment pas trop les asperges.",
        "Les enfants aiment les asperges.",
	"Les Français réclament moins d’impôts.",
	"Ils réclament moins d’impôts.",
	"Ils réclament des impôts.",
	"Les Français réclament des impôts.",
	"Les acacias donnent un miel ambré, limpide et fluide.",
	"L’équipe fait porter le chapeau à l’arbitrage."
    ]

    for phrase in listePhrases:
        analyse_svo(phrase, nlp)

if __name__ == '__main__':
    main()

