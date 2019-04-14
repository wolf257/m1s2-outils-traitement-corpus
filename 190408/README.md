# Exercice sem 13/04/19

## Consigne

`Ré-entraînez un modèle pour l’adapter à : soit deux textes de chansons en français « non standard » (hip-hop, français de la francophonie, …), soit deux poésies de François Villon (exemple) ou de textes de la même époque.`

## Syntaxe

**python3 main.py**

## Déroulement du script

- Phase1
    - Chargement du module 'fr_core_news_md' ou création d'un nouveau 'fr'
    - Entrainement sur les entités à partir de (liste TRAIN_DATA).
    - Ajout de cas spéciaux de tokenisation concernant l'ancien français (dico list_special_cases).
    - Test sur la (liste TRAIN_DATA).
    - Sauvegarde du modèle modifié.
- Phase2
    - Rechargement du modèle sauvegardé.
    - Test de tokenisation, repérage d'entités sur le jeu de donnée (liste DATA_TO_TEST)
        - Affichage des entités sur le terminal.
        - Enregistrement des données sur tokens dans le fichier './output/output.txt'.

## Input

Pour l'ancien français, nous avons choisi un extrait des Essais de Montaigne (T1 Chap 19, ed de la Pléiade).

## Remarques

Pour la tokenisation, une fois les règles ajoutées, tout se passe très bien.

Pour le repérage d'entités, si spacy les reconnait plutôt bien, parfois il a bien du mal à dire quel type d'entité c'est. Ainsi, plusieurs personnes deviennent LOC, des lieux MISC, etc.

Cela pourrait influencer l'analyse, donc on doit y faire attention. Puis disons que l'extrait soumis n'est pas des plus facile, même pour nous.