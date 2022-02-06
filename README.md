# Categorisez automatiquement des questions
Moteur + API de suggestion de tag pour des questions

## Description
Ce projet a été réalisé dans le cadre de la formation Data Scientist par Openclassrooms/Centrale-Supelec.  

L'objectif du projet est de proposer un moteur de suggestion de tags pour toute question posée sur le site StackOverflow.

Le projet présente les étapes de:
* nettoyage
* exploration
* modélisation
* déploiement de l'api

## Contenu

├── P06_01_Categorisez_automatiquement_des_questions_Nettoyage.ipynb  
├── P06_02_Categorisez_automatiquement_des_questions_Exploration.ipynb  
├── P06_03_Categorisez_automatiquement_des_questions_Modelisation.ipynb  
├── P06_04_categorisez-automatiquement-des-questions_huiguan.pdf  
├── P06_05_Rapport-Categorisez automatiquement des questions.pdf  
├── questiontags-api  
│   ├── Dockerfile  
│   ├── models  
│   ├── requirements.txt  
│   ├── server.py  
│   └── templates  
└── README.md   

Les notebooks ont été créés avec Jupyter Notebook (Python 3.8).
L'api a été développée avec  python, fastapi et bootstrap puis dockerisée et déployée sur Heroku.
