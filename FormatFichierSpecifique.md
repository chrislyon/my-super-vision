# Introduction #

Description du format de fichier d'echanges


# Details #

Voici un exemple :

```
#>>>:GET_DATA-DEB:#
#>>>:ENT-DEB:#
GET_DATA V0.0Alpha
Genere le  12-09-12 18:19:27
#>>>:ENT-FIN:#
#>>>:SERVEUR-DEB:#
SERVER_NAME: chris-R61i.local
SERVER IP: 127.0.1.1
SERVER UNAME: Linux chris-R61i 2.6.32-42-generic #95-Ubuntu SMP Wed Jul 25 15:57:54 UTC 2012 i686 GNU/Linux
cat: /etc/system-release: Aucun fichier ou dossier de ce type
SERVER RELEASE:
#>>>:SERVEUR-FIN:#
#>>>:GET_DATA-FIN:#
```

En gros des marqueurs debut / fin qui englobe des infos