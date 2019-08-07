---
layout: post
title: Installer LAMP sous Ubuntu 19.04 Disco Dingo
subtitle: 
gh-repo: 0xSs0rZ/0xSs0rZ.github.io
gh-badge: [star, fork, follow]
tags: [Ubuntu, Disco Dingo, LAMP]
comments: true
---

**Vous venez d'installer Ubuntu 19. 04 Disco Dingo et voulez passer à l'étape suivante en installant LAMP sur votre machine. Voici les étapes à suivre.**

## Préalables: Installer Ubuntu

Si vous ne disposez pas encore d'une distribution Ubuntu, une manière simple pour se familiariser avec cet OS consiste à créer une machine virtuelle (VM). Vous pouvez trouver l'ISO d'Ubuntu sur le site de Canonical [1] ou encore utiliser l'image d'une machine virtuelle [2].

## Pourquoi LAMP ?

LAMP signifie Linux, Apache, MySQL, PHP. Cette pile vous permettra de développer vos sites en suivant une architecture trois tiers [3] et pourquoi pas d'installer Damn Vulnerable Web Application, DVWA, pour commencer à apprendre les bases des tests d'intrusion

## Installer LAMP

**1-Installer Apache**

~~~
$ sudo apt update
$ sudo apt install apache2 -y
~~~

Si utilisation d'un pare feu, autoriser le traffic entrant http et https. Voir [5]

Lancer Apache à chaque démarrage d'Ubuntu:

~~~
$ sudo sytemctl enable apache2
~~~

Vérifier qu'Apache fonctionne correctement. Visiter http://votre_adresse_ip   

==> page par défault d'Ubuntu

Trouver son IP:

~~~
$ ip address
~~~

**2-Installer MySQL**

~~~
$ sudo apt install mysql-server -y 
~~~

Pas de mot de passe par défaut pour le compte root. Modifier le mot de passe du compte root :

~~~
$ sudo mysql_secure_installation
~~~

Pour se connecter à MySQL en utilisant le compte root et son mot de passe il faut modifier sa méthode d'authentification de auth_socket à mysql_native_password:

~~~
$ sudo mysql -uroot -p
Enter password: 

mysql> USE mysql; 
mysql> SELECT User, Host, plugin FROM mysql.user; 
~~~

L'utilisateur root utilise la méthode auth_socket. Modifier cette méthode: 

~~~
mysql> UPDATE user SET plugin='mysql_native_password' WHERE User='root'; 
mysql> FLUSH PRIVILEGES; 
mysql> exit; 
~~~

**3-Installer PHP**

~~~
$ sudo apt install php libapache2-mod-php php-mysql 
~~~

Vérifier que PHP fonctionne. Créer un document test.php dans le fichier /var/www/html et insérer le code suivant:

~~~
$sudo vim /var/www/html/test.php
~~~


~~~
<?php phpinfo(); ?>  
~~~

Sauvegarder et relancer Apache:

~~~
# systemctl restart apache2  
~~~

Visiter http://votre_adresse_ip/test.php  

Version de PHP:

~~~
$ php -v
~~~

Supprimer test.php:

~~~
$ sudo rm -rf /var/www/html/test.php
~~~

**Références:**

[1] Canonical, [Ubuntu]( https://ubuntu.com/)

[2] OSBoxes, [Ubuntu]( https://www.osboxes.org/ubuntu/)

[3] Wikiversity, [Three-Tier Architecture]( https://en.wikiversity.org/wiki/Three-Tier_Architecture)

[4] DigitalOcean, [How To Install Linux, Apache, MySQL, PHP (LAMP) stack on Ubuntu 18.04] ( https://www.digitalocean.com/community/tutorials/how-to-install-linux-apache-mysql-php-lamp-stack-ubuntu-18-04)


