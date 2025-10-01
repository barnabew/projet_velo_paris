# Projet : Analyse des flux de vélos à Paris

## Contexte

Ce projet a pour objectif d'analyser les données de comptage de vélos à Paris pour l'année 2024. L'objectif est de mieux comprendre les comportements des cyclistes et d'identifier les tendances principales afin de fournir des éléments utiles pour les décisions en matière de mobilité urbaine.

## Analyses réalisées

L'étude s'est concentrée sur plusieurs dimensions des flux cyclistes. L'analyse horaire a permis de mettre en évidence les pics de circulation le matin entre 8h et 9h et en fin de journée entre 17h et 19h. L'analyse journalière a montré que l'activité est plus soutenue du mardi au jeudi, tandis que le lundi et le vendredi présentent des volumes légèrement plus faibles, probablement en lien avec le télétravail. Le week-end, les usages deviennent davantage récréatifs. L'examen des variations mensuelles a révélé une forte saisonnalité, avec un trafic plus important de mai à septembre et une baisse sensible en hiver. L'analyse géographique des sites de comptage a permis d'identifier une concentration des flux cyclistes dans le centre de Paris et autour des grands axes convergents, tandis que les zones périphériques présentent des volumes plus modérés.

## Résultats clés

Cette étude a permis d'identifier les jours et heures les plus chargés, de mettre en évidence la saisonnalité du trafic et de visualiser les zones de forte affluence cycliste. Les indicateurs synthétiques générés offrent un outil pratique pour suivre l'activité cycliste et orienter la planification des infrastructures à Paris.

## Organisation du projet

Le notebook `Projet_velo.ipynb` contient toutes les explications détaillées sur le traitement des données, le calcul des indicateurs et les analyses réalisées. Le dossier `streamlit/` reprend le même code, mais il a été divisé en différentes parties afin de rendre le code plus lisible et modulaire. Cette séparation facilite la maintenance et l'extension de l'application, alors qu'elle aurait également pu être appliquée directement dans le notebook.
