# Le projet en lui-même
Ce projet consiste en le développement dans une architecture en microservices d’un service d'annuaire. 

Voici les différentes fonctionnalités présentées :

- Interface utilisateur web
- Possibilité de s’inscrire, se connecter, se deconnecter, supprimer son compte et de changer son mot de passe.
- Consultation de l'annuaire de tous les utilisateurs
- Possibilités de promouvoir, retrograder, supprimer un compte et changer le mot de passe des membres en étant admin

# Données
Les bases de données sont remplies de X utilisateurs membre et admin.
## Identifiants :



Il est évidemment possible de créer de nouveaux utilisateurs, posts et abonnements durant votre navigation.
# Application

## Pour lancer l'application sur Windows :

```bash
docker-compose up

ou sans docker

cd front/
pip3 install -r requirements.txt
set FLASK_APP=front
cd ..
flask run

cd user/
pip3 install -r requirements.txt
set FLASK_APP=user
cd ..
flask run -p 5001
```

# Pour lancer l'application sur MacOS ou Linux :

```shell
sudo docker-compose up
```

## Puis aller à l'adresse suivante :

[Lien](http://127.0.0.1:5000/)