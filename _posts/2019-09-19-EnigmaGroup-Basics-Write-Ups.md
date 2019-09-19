---
layout: post
title: Enigma Group - Basics
subtitle: Enigma Group - Basics - Write-Ups 
gh-repo: 0xSs0rZ/0xSs0rZ.github.io
gh-badge: [star]
tags: [CTF, Enigma Group, Basics, Commandes, Javascript, Web App, Local Fi SQLi, Write-Up]
comments: false
---

**Voici quelques solutions pour la catégorie Basics de Enigma Group.**

Enigma Group: [https://www.enigmagroup.org/](https://www.enigmagroup.org/)

# Basics - Starter

##1 Basic 1

Level 1 - The Infamous Noob Test

Find the password to complete this mission.

**Solution:**

Clic droit - code source, on trouve le mot de passe dans un commentaire

##2 Basic 2

fopen: could not open file '/www/htdocs/challenges/basics/pre/2/dontlookinhere/password.txt';

FYI, the mission isn't broken, the above error is part of the mission.

**Solution:**

On regarde: http://challenges.enigmagroup.org/basics/pre/2/dontlookinhere/password.txt

404 Not Found

On visite http://challenges.enigmagroup.org/basics/pre/2/dontlookinhere/

Il y a un fichier nommé password.inc on le consulte on trouve un mot de passe pour le compte admin

##3 Basic 3

Tip: robot

**Solution:**

On visite http://challenges.enigmagroup.org/basics/pre/3/robots.txt. Résultat: 

User-agent:	*
Disallow:       /f0rk/

On visite http://challenges.enigmagroup.org/basics/pre/3/f0rk/

Il y a un fichier config.inc, on le consulte et on trouve des credentials

# Basics - Javascript

## Basic 4

Log in with the name Jane

**Solution:**

Ouvrir l'inspecteur, Changer le champ:

~~~
<option value="Jack">Jack</option>
~~~

pour value="Jane" et cliquer sur Submit

## Basic 5

Bypass login - Prompt Password

**Solution:**

Dans le code source on trouve:

~~~
<script language="JavaScript" type="text/javascript">
<!--
var password= "hax0r";

password=prompt("Please enter the Password!","");
if (password=="skriptkid") {

window.location.href="http://challenges.enigmagroup.org/basics/js/2/"+password+".php";
}
//-->
</script>
~~~

## Basic 6 

Bypass login - Prompt Password

**Solution:**

Dans le code source on trouve: 

~~~
<!--The Source Has Been Disabled To Stop All Of You From Hacking My Shit.-->
~~~

En ouvrant l'inspecteur on trouve:

~~~
<script type="text/javascript">
<!--

password=prompt("Please enter the Password!","");
var  pasword= "hax0r";
if (password=="Sauc3") {
window.location.href="http://challenges.enigmagroup.org/basics/js/3/"+password+".php";

}
//-->
</script>
~~~

## Basic 7

Bypass login - Prompt Password

**Solution:**

Dans l'inspecteur on trouve:

~~~
<!--

password=prompt("Please enter the Password!","");
if (password=="leethaxor") {

window.location.href="http://challenges.enigmagroup.org/basics/js/4/"+password+".php";
}

-->
<br>

	<font color="red">Wrong!</font>
	<br><br>
	<form>
		<input value="Try Again" onclick="window.location='http://challenges.enigmagroup.org/basics/js/4/index.php'" type="button">
	</form>
~~~

On essaye avec 'leethaxor' mais  ne fonctionne pas. On consulte view-source:http://challenges.enigmagroup.org/basics/js/4/index.php . On trouve: 

~~~
<!--
var password= "hax0r";

password=prompt("Please enter the Password!","");
if (password=="shifted") {

window.location.href="http://challenges.enigmagroup.org/basics/js/4/"+password+".php";
}
else
{
window.location.href="http://challenges.enigmagroup.org/basics/js/4/lndex.php";
}
//-->
~~~

## Basic 8

Bypass login - Prompt Password

**Solution:**

Dans le code source, on trouve: 

~~~
<script language="javaScript">
var pass = "%41%53%43%49%49%2D%43%68%61%72%74"
password=prompt("Please enter the Password!","");
if (password==unescape(pass)) {
window.location.href="http://challenges.enigmagroup.org/basics/js/5/"+unescape(pass)+".php";
}
</script>
~~~

On décode %41%53%43%49%49%2D%43%68%61%72%74 encodé en HTML URL. [https://www.urldecoder.org/](https://www.urldecoder.org/)

#Spoofing

## Basic 16 

Se connecter en utilisant un proxy transparent.


Use an Anonymous or Transparent proxy to view this page.

IMPORTANT: Do not use an "Elite" or "High Anonymity" proxy, this script is set to detect the HTTP_X_FORWARDED_FOR variables used by low anonymity proxies. 

**Solution:**

Chercher une liste de transparent proxy. Utiliser FoxyProxy et revisiter la page.

## Basic 17

Info: You must be using the "EnigmaFox" web browser.

**Solution:**

Spoofing du user-agent en utilisant Burp

#SQL Injection

## Basic 21

**Solution:**

x' or 1=1--

#URL Manipulation

## Basic 27

Prompt

**Solution:**

Entrer n'importe quel mot de passe. Il s'affiche: 'Error finding in password.php'

L'url est: http://challenges.enigmagroup.org/basics/um/1/index.php?file=login.php

Visiter http://challenges.enigmagroup.org/basics/um/1/index.php?file=password.php

## Basic 30

Tip: Local File Inclusion

 Warning: main(pages/$page): failed to open stream: No such file or directory in /home/enigmagroup/public_html/challenges/basics/vm/1/index.php on line 14

FYI, This error message is part of the mission.

Login 

**Solution:**

Références: 

[https://www.wpwhitesecurity.com/securing-wordpress-wp-admin-htaccess/](https://www.wpwhitesecurity.com/securing-wordpress-wp-admin-htaccess/)

[https://httpd.apache.org/docs/2.4/programs/htpasswd.html](https://httpd.apache.org/docs/2.4/programs/htpasswd.html)

[https://www.owasp.org/index.php/Testing_for_Local_File_Inclusion](https://www.owasp.org/index.php/Testing_for_Local_File_Inclusion)

Le lien 'Login' nous amène sur la page http://challenges.enigmagroup.org/basics/vm/1/admin

Il s'agit d'une page d'authentification de type htaccess. Dans ce cas, les mots de passe se trouvent dans un fichier nommé .htpasswd 

Local file inclusion

http://challenges.enigmagroup.org/basics/vm/1/index.php?page=../admin/.htpasswd

On trouve: 

admin:dXWxIS6i6irN6

On crack le hash avec John

~~~
root@Host-001:~/Bureau# john hash
Created directory: /root/.john
Using default input encoding: UTF-8
Loaded 1 password hash (descrypt, traditional crypt(3) [DES 256/256 AVX2])
Will run 8 OpenMP threads
Proceeding with single, rules:Single
Press 'q' or Ctrl-C to abort, almost any other key for status
Almost done: Processing the remaining buffered candidate passwords, if any.
Warning: Only 664 candidates buffered for the current salt, minimum 2048 needed for performance.
Proceeding with wordlist:/usr/share/john/password.lst, rules:Wordlist
***              (admin)
1g 0:00:00:01 DONE 2/3 (2019-09-16 14:30) 0.8064g/s 27496p/s 27496c/s 27496C/s 123456..thebest3
Use the "--show" option to display all of the cracked passwords reliably
Session completed
~~~

## Basic 31

Tip: Redirection Evasion

What are you doing here?

**Solution:**

L'url est: http://challenges.enigmagroup.org/basics/vm/2/index2.php

Essayons: http://challenges.enigmagroup.org/basics/vm/2/index.php

Nous sommes redirigé sur index2.php après avoir vu un message à l'écran. 

Dans le code source de index.php view-source:http://challenges.enigmagroup.org/basics/vm/2/index.php on voit:

~~~
<div style="padding:150px">
    <div id="outer">
        <div id="inner"><!--             911_411.php                -->
<br />
<center>
	<font size="2" color="red"><i>Off you go, my child!</i></font>
</center>

<meta http-equiv="refresh" content="0;url=http://challenges.enigmagroup.org/basics/vm/2/index+2.php" />
~~~

Consultons le contenu de 911_411.php

view-source:http://challenges.enigmagroup.org/basics/vm/2/911_411.php

Mission completed

**Poursuivez avec:**

- [PicoCTF 2018 - Forensics](https://0xss0rz.github.io/2019-08-21-picoCTF-Forensics-Write-Ups/)

- [PicoCTF 2018 - General Skills](https://0xss0rz.github.io/2019-08-22-picoCTF-General-Skills-Write-Ups/)

- [PicoCTF 2018 - Cryptography](https://0xss0rz.github.io/2019-08-22-picoCTF-Cryptography-Write-Ups/)

[![CC-BY](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by.svg)](https://creativecommons.org/licenses/by/4.0/)

This work is licensed under a [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).
























































**Poursuivez avec:**

- [PicoCTF 2018 - Forensics](https://0xss0rz.github.io/2019-08-21-picoCTF-Forensics-Write-Ups/)

- [PicoCTF 2018 - General Skills](https://0xss0rz.github.io/2019-08-22-picoCTF-General-Skills-Write-Ups/)

- [PicoCTF 2018 - Cryptography](https://0xss0rz.github.io/2019-08-22-picoCTF-Cryptography-Write-Ups/)

[![CC-BY](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by.svg)](https://creativecommons.org/licenses/by/4.0/)

This work is licensed under a [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).


