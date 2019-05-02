# Exercice sem 15/04/19

## Consignes

`Étiquetez manuellement puis avec l’étiqueteur de votre choix les deux textes suivants. Calculez la précision globale pour chacun des textes et commentez.`

## Syntaxe

`python3 main.py`

## Données

Les 2 fichiers :
- bashung.txt
- sequoia.txt

## Procédure

### 1 - Partie tagging

Pour chaque fichier :
- Tagger tout le fichier.
- Enregistrer les informations dans un nouveau fichier (nom+'-treetagger.txt').

### 2- Partie récupération d'information

Pour chaque couple (fichier de référence, fichier taggé par TreeTagger) :
- Comparer ligne à ligne les POS :
    - Si différents : capturer l'erreur.
    - Sinon : incrémenter le compteur de POS correct.
    - Dans tous les cas : incrémenter le compteur de POS total.

### 3- Partie calcul

- Calcul précision globale.
- Précision par POS.
- Erreurs, par frequence

## Résultats et commentaires

L'étiquetage automatique a été réalisé par le module treetagger.

Pour Bashung, elle est de 83.33% (40/48).
Pour Sequoia, la précision globale est de 100% (90/90).
En tenant en compte les proportions, on a une précision globale de 94.2% (130/138).

Vous avez tous les détails dans [lien-vers-résultats](./resultats.txt).

Les principales erreurs sont conséquence d'une mauvaise tokenisation de treetagger, surtout pour les mots contenant une apostrophe (ex : j'en, c'est, qu'on) que le taggeur a systématiquement mal étiqueté.

Si la précision globale des taggeurs tournent aujourd'hui autour des 95%, on voit que nous avons deux extrêmes (83% qui est très faible, et 100% qui est parfait).

Est-ce du au type de texte (vers dans Bashung, prose dans Sequoia) ? Possible, mais surtout, il nous faut noter que nos textes sont bien trop courts (environ 110 mots à eux 2). C'est très clairement insuffisant pour évaluer un outil correctement.

Néanmoins, la démarche pourrait être la même à grande échelle, et nous pensons que c'est là que se trouve le plus important : le fait d'avoir pu se confronter à l'évaluation de nos outils.

## Remarques

En l'état, notre script exige un alignement strict entre les fichiers de référence et les fichiers de treetager, ainsi, on a du parfois manuellement modifier nos fichiers.

