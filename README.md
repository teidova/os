# Bounce
Vous voulez jouer au ping pong mais vous n'avez pas d'amis ? Faites jouer des containers docker entre eux.

## Comment jouer
> Pour jouer vous aurez besoin de **docker** avec **le plugin compose**. L'ancien ```docker-compose``` n'est pas supporte. Si vous avez un doute, si docker ne donne pas d'erreur si vous faites ```docker compose```, vous avez la bonne version.

### Avec un registry local
> On considere que vous avez un repository docker disponible a l'adresse ```localhost```, si votre depot a une adresse differente il faudras le changer dans les fichiers ```push.sh``` et ```docker-compose.yml```.

Clonez le repository
```
$ git clone https://github.com/teidova/os
```

Buildez l'image docker ```balles:dev```
```
$ ./build.sh
```

Lancez le jeu avec ```docker compose```
```
$ docker compose up
```

### Sans registry
Clonez le repository
```
$ git clone https://github.com/teidova/os
```

Modifiez le fichier ```docker-compose.yml```, commentez les lignes commencant par ```image:``` et decommentez les lignes commencant par ```build:```.

Lancez le jeu avec ```docker compose```
```
$ docker compose up
```

## Configuration
Les differentes variables d'environnement disponibles sont listees dans le fichier ```docker-compose.yml```