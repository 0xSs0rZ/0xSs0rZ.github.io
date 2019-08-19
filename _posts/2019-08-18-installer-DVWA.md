---
layout: post
title: Installer DVWA
subtitle: Damn Vulnerable Web Application
gh-repo: 0xSs0rZ/0xSs0rZ.github.io
gh-badge: [star]
tags: [DVWA, Damn Vulnerable Web Application, Pentest]
comments: false
---

**Damn Vulnerable Web Application, DVWA, est un incontournable pour tester ses connaissances en hacking d'application web. Voici comment l'installer:**

## 1-Description

Damn Vulnerable Web App (DVWA) est une application Web PHP / MySQL extrêmement vulnérable. Ses principaux objectifs sont d'aider les professionnels de la sécurité à tester leurs compétences et leurs outils en toute légalité, d'aider les développeurs Web à mieux comprendre les processus de sécurisation des applications Web et d'aider les enseignants / étudiants à enseigner / apprendre la sécurité des applications Web dans un environnement de salle de classe. [1]

## 2-Installation

Avant de commencer l'installation de DVWA, vous devez avoir configuré LAMP sur votre machine. Si ce n'est pas encore fait, consultez [Installer LAMP sur Ubuntu](https://0xss0rz.github.io/2019-08-07-installer-LAMP-Ubuntu/)

**2-1 Télécharger DVWA**

Nous allons installer DVWA dans le dossier racine du serveur Apache /var/www/html. Nous devons donc supprimer le fichier par défaut index.html:

~~~
# rm -r /var/www/html/index.html
~~~
 
Cloner DVWA

~~~ 
# git clone https://github.com/ethicalhack3r/DVWA /tmp/DVWA  
~~~
 
Déplacer DVWA dans le dossier /var/www/html

~~~ 
# rsync -avP /tmp/DVWA/ /var/www/html/  
~~~

**2-2 Configurer DVWA**

**2-2-1 Établir la connection avec la base de données**

Renommer le fichier de configuration

~~~ 
# cp /var/www/html/config/config.inc.php.dist /var/www/html/config/config.inc.php  

# vim /var/www/html/config/conf
~~~

Ajuster la configuration de la base de données:

~~~
 ... $_DVWA[ 'db_server' ] = '127.0.0.1'; #Si la connection ne fonctionne pas, essayez avec 'localhost'
 $_DVWA[ 'db_database' ] = 'dvwa'; 
$_DVWA[ 'db_user' ] = 'root'; 
$_DVWA[ 'db_password' ] = ''; ... #Il n'y a pas de mot de passe par défaut pour l'utilisateur root dans MySQL. Si vous avez défini un mot de passe pour cet utilisateur utiliser le ici
~~~

Sauvegarder la configurarion et relancer MySQL:

~~~
# systemctl restart mysql 
~~~

**2-2-2 Configurer PHP**

Nous utilisons la version 7.2 de PHP. Pour connaitre la version installée sur votre machine:

~~~
# php -v  
~~~

Éditer le fichier /etc/php/7.2/apache2/php.ini et effectuer les modifications suivantes:

• allow_url_include = on – Permettre les Remote File Inclusions (RFI)

• allow_url_fopen = on – Permettre les Remote File Inclusions (RFI)

• safe_mode = off – (Si PHP <= v5.4) Permettre les injections SQL (SQLi)

• magic_quotes_gpc = off – (Si PHP <= v5.4) Permettre les injections SQL (SQLi)

• display_errors = off – (Optionnel) Cacher les messages d'alertes PHP, moins verbeux

Modifier le propriétaire du fichier racine d'Apache:

~~~
# chown -R www-data.www-data /var/www/html/
~~~

Connecter vous à DVWA (votre adresse IP) avec votre navigateur web:  

Si 'PHP module gd: Missing', installer le module php-gd:

~~~
# apt install php-gd -y
~~~
   
relancer Apache et MySQL:

~~~
# systemctl restart apache2 
# systemctl restart mysql 
~~~

Retourner sur la page de DVWA avec votre navigateur web, tout devrait fonctionner.

Pour compléter l'installation, il faut créer la base de données de DVWA. Cliquer sur le bouton Create/Reset Database en bas de la page.

L'installation est terminée. Vous pouvez vous connecter en utilisant les credentials suivants:

user: admin 
passord: password.  

**Références:**
 
[1] Damn Vulnerable Web Application (DVWA), [http://www.dvwa.co.uk/](http://www.dvwa.co.uk/)

