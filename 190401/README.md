# Observations

On remarque que l'analyse n'aboutit pas dans deux cas :
- La négation du verbe.
- La présence d'adverbes.

On s'est posé la question du pourquoi ?

## Première piste : modèle utilisé par spacy pour son analyse des dépendances ?

Ici, il s'agit du fr_core_news_sm (captures c1-1 et c1-2).

On en a essayé un autre, le fr_core_news_md (captures c2-1 et c2-2).

### Négation : `Les enfants n'aiment pas les asperges.`

On voit que fr_core_news_sm n'arrive à détecter aucun de nos groupes (S,V,O), là où fr_core_news_md en trouve.

Cependant, dépendamment de notre point de vue, on pourrait dire que fr_core_news_md ne restitue pas tout le sens. En effet, il manque le 'pas'. 

De même, le 'ne' de négation a été placé sous le S, au lieu du V. 

### Adverbes : `Les Français réclament moins d'impôts.`

Là encore, fr_core_news_md fait un peu mieux. Il tag le 'd' comme déterminant, là où fr_core_news_sm en fait un NUM, et au niveau des dépendances, fr_core_news_md reconnait réclament comme ROOT de l'arbre, là où fr_core_news_sm choisit 'impôts' comme ROOT.

## Seconde hypothèse : script pas assez affiné

Si ceci est une première analyse, on concède n'avoir pas assez d'expérience sur spacy pour prétendre en démonter la mécanique.

C'est pourquoi, nous estimons que d'ici peu, notre analyse sera pour être plus poussée et juste.