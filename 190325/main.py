#!/usr/bin/env/ python3
# -*- coding : utf-8 -*-

import pprint
import spacy

listeFicIn = ['./stateoftheunion2016.txt', './stateoftheunion2017.txt']
setOfTokens = set()
listOfTokens = []

def main():
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(u"Apple is looking at buying U.K. startup Apple for $1 billion")
    for token in doc:
        content = token.text
        setOfTokens.add(content)
        listOfTokens.append(content)
        # print(token.text)

    print(f"- Le set est : {setOfTokens} de longueur {len(setOfTokens)}. \n")

    print(f"- La liste est : {listOfTokens} de longueur {len(listOfTokens)}. \n")
if __name__ == '__main__':
    main()


