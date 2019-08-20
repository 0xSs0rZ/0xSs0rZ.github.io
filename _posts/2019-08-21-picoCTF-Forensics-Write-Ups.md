---
layout: post
title: PicoCTF 2018 - Forensics
subtitle: PicoCTF 2018 - Forensics - Write-Ups 
gh-repo: 0xSs0rZ/0xSs0rZ.github.io
gh-badge: [star]
tags: [CTF, picoCTF, Forensics, Write-Up]
comments: false
---

**Et si on se prenait pour un investigateur numérique ? Voici quelques solutions pour la catégorie _"Forensics"_ de picoCTF.**

picoCTF: [https://2018game.picoctf.com/](https://2018game.picoctf.com/)

## Forensics Warmup 1

{: .box-note}
Can you unzip this file for me and retreive the flag? 

**Solution:** Télécharger le fichier, le dézipper et ouvrir la photo

## Forensics Warmup 2

{: .box-note}
Hmm for some reason I can't open this PNG? Any ideas? 

**Solution:** 

Regarder l'hexadécimal du fichier:

~~
$xxd flag.png 
00000000: ffd8 ffe0 0010 4a46 4946 0001 0101 004b  ......JFIF.....K
00000010: 004b 0000 ffdb 0043 0002 0101 0201 0102  .K.....C........
(...)
~~

On voit: JFIF. L'extension du fichier a été modifiée, il ne s'agit pas d'un fichier PNG mais JPEG. Modifier l'extension en jpeg et ouvrir la photo

## Desrouleaux 

{: .box-note}
Our network administrator is having some trouble handling the tickets for all of of our incidents. Can you help him out by answering all the questions? Connect with nc 2018shell.picoctf.com 54782. incidents.json

**Solution:**

Se connecter à l'adresse indiquer: 

~~~
$nc 2018shell.picoctf.com 54782
You'll need to consult the file `incidents.json` to answer the following questions.

#Faire quelques calculs simple pour répondre aux questions

What is the most common source IP address? If there is more than one IP address that is the most common, you may give any of the most common ones.
##########
Correct!


How many unique destination IP addresses were targeted by the source IP address 251.165.34.242?
#
Correct!


What is the number of unique destination ips a file is sent, on average? Needs to be correct to 2 decimal places.
###
Correct!


Great job. You've earned the flag: 
#####################
~~~

### Reading Between the Eyes 

{: .box-note}
Stego-Saurus hid a message for you in this image, can you retreive it? 

On observe l'image en  zoomant au max mais on ne trouve rien, on recherche dans l'hexadécimal un chaine "picoCTF", on trouve rien non plus...

_Hint:_ Maybe you can find an online decoder?

**Solution:** On utilise [http://stylesuxx.github.io/steganography/](http://stylesuxx.github.io/steganography/)

## Recovering From the Snap

{: .box-note}
There used to be a bunch of animals here, what did Dr. Xernon do to them? 

**Solution:**

Ouvrir le fichier avec [Autopsy](https://autopsy.com/).

Dans _$CarvedFiles_ il y a 4 fichiers jpg, le flag est dans f0002388.jpg

## admin panel

{: .box-note}
We captured some traffic logging into the admin panel, can you find the password? 

**Solution:** On ouvre le fichier pcap avec Wireshark. On fait un recherche de la chaine 'password'. On voit que la trame 68 est un _POST /LOGIN_, on trouve le username et le password = flag

## hex editor

{: .box-note}
This cat has a secret to teach you. You can also find the file in /problems/hex-editor_4_0a7282b29fa47d68c3e2917a5a0d726b on the shell server. 

**Solution:**

~~~
# 1. 
┌─[xor@parrot]─[~/Téléchargements]
└──╼ $xxd hex_editor.jpg 

# On trouve le flag à la fin du fichier: c'est un classique !

# 2.  
┌─[xor@parrot]─[~/Téléchargements]
└──╼ $strings hex_editor.jpg | grep "picoCTF"
~~~

## Truly an Artist

{: .box-note}
Can you help us find the flag in this Meta-Material? You can also find the file in /problems/truly-an-artist_3_066d6319e350c1d579e5cf32e326ba02. 
 
**Solution:** [https://www.extractmetadata.com/](https://www.extractmetadata.com/)

## now you don't

{: .box-note}
We heard that there is something hidden in this picture. Can you find it?  

**Solution:**
 
Utiliser Stegsolve: [http://www.caesum.com/handbook/Stegsolve.jar](http://www.caesum.com/handbook/Stegsolve.jar)
 
_Red_ _Plane_ _1_ ou _Red_ _Plane_ _0_

## Lying Out

{: .box-note}
Some odd traffic has been detected on the network, can you identify it? More info here. Connect with nc 2018shell.picoctf.com 27108 to help us answer some questions. 

**Solution:**

Comparer les logs avec le graph

~~~
#nc 2018shell.picoctf.com 27108
You'll need to consult the file `traffic.png` to answer the following questions.


Which of these logs have significantly higher traffic than is usual for their time of day? You can see usual traffic on the attached plot. There may be multiple logs with higher than usual traffic, so answer all of them! Give your answer as a list of `log_ID` values separated by spaces. For example, if you want to answer that logs 2 and 7 are the ones with higher than usual traffic, type 2 7.
    log_ID      time  num_IPs
0        0  03:30:00    10199
1        1  04:45:00    10121
2        2  05:30:00     9858
3        3  05:45:00    11625
4        4  05:45:00     9880
5        5  06:00:00    10036
6        6  07:30:00    13145
7        7  09:45:00    10121
8        8  09:45:00     9935
9        9  14:15:00    11632
10      10  15:15:00     9899
11      11  15:45:00    11630
12      12  22:15:00    10090
13      13  23:15:00     9669
3 6 9 11 
Correct!


Great job. You've earned the flag: 
#######
~~~

## What's My Name?

{: .box-note}
Say my name, say my name. 

**Solution:** Ouvrir le fichier pcap avec Wireshark. A la trame 43 on voit une requête DNS _thisismyname.com_, la réponse à cette requête est située à la trame 55. On trouve le flag dans cette réponse.

[![CC-BY](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by.svg)](https://creativecommons.org/licenses/by/4.0/)

This work is licensed under a [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).


