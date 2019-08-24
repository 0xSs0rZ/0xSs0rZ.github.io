---
layout: post
title: PicoCTF 2018 - Web Application
subtitle: PicoCTF 2018 - Web App - Write-Ups 
gh-repo: 0xSs0rZ/0xSs0rZ.github.io
gh-badge: [star]
tags: [CTF, picoCTF, Web App, SQLi, Write-Up]
comments: false
---

**Voici quelques solutions pour la catégorie applications Web de picoCTF 2018.**

picoCTF 2018: [https://2018game.picoctf.com/](https://2018game.picoctf.com/)

## Inspect Me

Inpect this code! http://2018shell.picoctf.com:28831

**Solution:** Page Intro: Clic Droit, Code source = première partie du flag. Ouvrir mycss.css = deuxième partie du flag. Ouvrir myjs.js = troisième partie du flag

## Client Side is Still Bad

I forgot my password again, but this time there doesn't seem to be a reset, can you help me? http://2018shell.picoctf.com:8249

**Solution:** Clic droit, code source:

~~~
<script type="text/javascript">
  function verify() {
    checkpass = document.getElementById("pass").value;
    split = 4;
    if (checkpass.substring(split*7, split*8) == '}') {
      if (checkpass.substring(split*6, split*7) == '17e9') {
        if (checkpass.substring(split*5, split*6) == 'd_91') {
         if (checkpass.substring(split*4, split*5) == 's_ba') {
          if (checkpass.substring(split*3, split*4) == 'nt_i') {
            if (checkpass.substring(split*2, split*3) == 'clie') {
              if (checkpass.substring(split, split*2) == 'CTF{') {
                if (checkpass.substring(0,split) == 'pico') {
                  alert("You got the flag!")
                  }
                }
              }
      
            }
          }
        }
      }
    }
    else {
      alert("Incorrect password");
    }
  }
</script>
~~~

Lire le code et recréer le flag

## Logon

I made a website so now you can log on to! I don't seem to have the admin password. See if you can't get to the flag. http://2018shell.picoctf.com:5477

**Solution:**

SQLi - User: ' Password: '

On est logué mais on a un message 'No flag for you'

On actualise la page en l'interceptant avec Burp, on voit un cookie admin=False on le modifie pour admin=True. On a le flag

## Irish Name Repo

There is a website running at http://2018shell.picoctf.com:52135 (link). Do you think you can log us in? Try to see if you can login! 

**Solution:**

On va sur la page 'Admin Login'. On essaye de se loguer en lançant une SQLi (user: admin password:'or'1'='1 ) et on intercepte la requête avec Burp. On voit un cookie debug=0, on le modifie debug=1. On a le flag 

## Mr. Robots

Do you see the same things I see? The glimpses of the flag hidden away? http://2018shell.picoctf.com:29568

**Solution:**

http://2018shell.picoctf.com:29568/robots.txt

~~~
User-agent: *
Disallow: /74efc.html
~~~

http://2018shell.picoctf.com:29568/74efc.html

On a le flag

## No Login

Looks like someone started making a website but never got around to making a login, but I heard there was a flag if you were the admin. http://2018shell.picoctf.com:39670

**Solution:** Créer un cookie admin=True à l'aide de l'inspecteur: [https://stackoverflow.com/questions/42011964/how-to-edit-or-remove-cookies-in-firefox-devtools](https://stackoverflow.com/questions/42011964/how-to-edit-or-remove-cookies-in-firefox-devtools)

## Secret Agent

Here's a little website that hasn't fully been finished. But I heard google gets all your info anyway. http://2018shell.picoctf.com:53383

**Solution:**

Quand on demande le flag on a cette réponse: 'You're not google! Mozilla/5.0 (X11; Linux x86_64; rv:68.0) Gecko/20100101 Firefox/68.0 '

Modifier le user_agent par: 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'. On a le flag

## Buttons

There is a website running at http://2018shell.picoctf.com:18342 (link). Try to see if you can push their buttons. 

**Solution:**

Le premier bouton utilise POST tandis que le deuxième bouton utilise GET. Modifier la requête de GET à POST pour le deuxième bouton, on a le flag

## The Vault 

There is a website running at http://2018shell.picoctf.com:64349 (link). Try to see if you can login! 

**Solution:**

Dans le code source on voit:

~~~
//validation check
  $pattern ="/.*['\"].*OR.*/i";
  $user_match = preg_match($pattern, $username);
  $password_match = preg_match($pattern, $username);
  if($user_match + $password_match > 0)  {
    echo "<h1>SQLi detected.</h1>";
  }
~~~

L'appli vérifie qu'on utilise pas de 'or' pour faire une SQLi... Mais on peut faire une SQLi autrement

Payload: User: admin ; Pass: ' union select 1 from users--


**Poursuivez avec:**

- [PicoCTF 2018 - Forensics](https://0xss0rz.github.io/2019-08-21-picoCTF-Forensics-Write-Ups/)

- [PicoCTF 2018 - General Skills](https://0xss0rz.github.io/2019-08-22-picoCTF-General-Skills-Write-Ups/)

- [PicoCTF 2018 - Cryptography](https://0xss0rz.github.io/2019-08-22-picoCTF-Cryptography-Write-Ups/)

[![CC-BY](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by.svg)](https://creativecommons.org/licenses/by/4.0/)

This work is licensed under a [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).


