#!/usr/bin/env/ python3
# -*- coding : utf-8 -*-

import pprint
import spacy

listeFicIn = ['./stateoftheunion2016.txt', './stateoftheunion2017.txt']

def main():
    nlp = spacy.load("en_core_web_sm")

    print("Bienvenue. Pour notre travail, nous avons utilisé le module spacy sur nos deux fichiers. \n")

    for file in listeFicIn:

        setOfTypes = set()
        listOfTokens = []

        print(f"=== Fichier : {file} === \n")

        # on récupére le contenu du fichier, que l'on prendra soin de fermer.
        myfile = open(file, mode="r", encoding="utf8")
        textmyfile = myfile.read()
        myfile.close()

        doc = nlp(textmyfile)

        # on parcourt le texte, tout en remplissant notre ensemble de types et notre liste de tokens.
        for token in doc:
            content = token.text.strip()

            # enlevons les éléments vides.
            if not content:
                continue
            # enlevons les ponctuations
            if len(content) == 1 and not content.isalnum():
                continue

            # type
            setOfTypes.add(content)
            # tokens
            listOfTokens.append(content)

        V = len(setOfTypes)
        N = len(listOfTokens)
        TTR = (V/N)*100

        print(f"- Le vocabulaire est constitué de {V} types différents.")

        print(f"- La texte a une taille de {N} tokens (hors ponctuation.).")

        print(f"- Cela nous donne un TTR de {round(TTR, 3)}. \n")


if __name__ == '__main__':
    main()


