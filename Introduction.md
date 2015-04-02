# Introduction #

Super vision est un peu exagéré, le but est que certain serveur paramétré
pour transmette des infos sur leur etat de santé :
- CPU / RAM / DISQUE / ERREUR

Le but est d'effectuer des rapports réguliers

# Details #

Pour être plus précis :

avec un l'aide de cron je génère un fichier avec get\_data.sh régulièrement
En gros je fait un df -kP, je récolte+ d'autres infos sur le système
j'emballe le tout et hop je transfert sur un serveur.

Fréquence maximum 1 fois / jour

Le format de ce fichier est spécifique voir FormatFichierSpecifique

Le serveur réceptionne ce fichier le stocke dans une base de données

Par la suite on utilisera ces informations pour générer des rapports
Le format de sortie par défaut sera du RestructuredText pour sa simplicité
mais aussi pour sa capacité à être traduit en pdf odt html