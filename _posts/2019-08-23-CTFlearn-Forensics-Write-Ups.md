---
layout: post
title: CTFLearn - Forensics
subtitle: Challenges d'investigation numérique - Write-Ups 
gh-repo: 0xSs0rZ/0xSs0rZ.github.io
gh-badge: [star]
tags: [CTF, CTFLearn, Forensics, Stéganographie, Write-Up]
comments: false
---

**Voici quelques solutions pour la catégorie _Forensics_ de CTFLearn**

CTFlearn: [https://ctflearn.com](https://ctflearn.com/)

# Easy

## Forensics 101

Think the flag is somewhere in there. Would you help me find it? https://mega.nz/#!OHohCbTa!wbg60PARf4u6E6juuvK9-aDRe_bgEL937VO01EImM7c

**Solution:**

~~~
┌─[xor@parrot]─[~/Téléchargements]
└──╼ $strings 95f6edfb66ef42d774a5a34581f19052.jpg | grep flag
flag{flag}
~~~

## Taking LS

Just take the Ls. Check out this zip file and I be the flag will remain hidden. https://mega.nz/#!mCgBjZgB!_FtmAm8s_mpsHr7KWv8GYUzhbThNn0I8cHMBi4fJQp8

**Solution:**

On trouve un pdf protégé par un mot de passe...

~~~
┌─[xor@parrot]─[~/Téléchargements/The Flag/The Flag]
└──╼ $ls
'The Flag.pdf'
┌─[xor@parrot]─[~/Téléchargements/The Flag/The Flag]
└──╼ $ls -la
total 40
drwxr-xr-x 3 xor xor  4096 août  22 09:51  .
drwxr-xr-x 4 xor xor  4096 août  22 09:20  ..
-rw-r--r-- 1 xor xor  6148 oct.  30  2016  .DS_Store
-rw-r--r-- 1 xor xor 16647 oct.  30  2016 'The Flag.pdf'
drwxr-xr-x 2 xor xor  4096 oct.  30  2016  .ThePassword
┌─[✗]─[xor@parrot]─[~/Téléchargements/The Flag/The Flag]
└──╼ $cd .ThePassword/
┌─[xor@parrot]─[~/Téléchargements/The Flag/The Flag/.ThePassword]
└──╼ $ls -la
total 12
drwxr-xr-x 2 xor xor 4096 oct.  30  2016 .
drwxr-xr-x 3 xor xor 4096 août  22 09:51 ..
-rw-r--r-- 1 xor xor   42 oct.  30  2016 ThePassword.txt
┌─[xor@parrot]─[~/Téléchargements/The Flag/The Flag/.ThePassword]
└──╼ $cat ThePassword.txt 
Nice Job!  The Password is "******".
~~~

## WOW.... So Meta

This photo was taken by our target. See what you can find out about him from it. https://mega.nz/#!ifA2QAwQ!WF-S-MtWHugj8lx1QanGG7V91R-S1ng7dDRSV25iFbk

**Solution:** [https://www.get-metadata.com/](https://www.get-metadata.com/)

## A CAPture of a Flag

This isn't what I had in mind, when I asked someone to capture a flag... can you help? You should check out WireShark. https://mega.nz/#!3WhAWKwR!1T9cw2srN2CeOQWeuCm0ZVXgwk-E2v-TrPsZ4HUQ_f4

**Solution:**

On filtre pour avoir les trames http. A la trame 247, on voit GET /?msg=ZmxhZ3tBRmxhZ0luUENBUH0= HTTP/1.1 ... Bizarement l'hote est www.hazy.co.uk soit le même nom que l'auteur de ce CTF. Le message est en base 64, on le décode et on a le flag

~~~
$echo ZmxhZ3tBRmxhZ0luUENBUH0= | base64 -d
flag{******}
~~~

ou en ligne: [https://www.base64decode.org/](https://www.base64decode.org/)

## Binwalk

Here is a file with another file hidden inside it. Can you extract it? https://mega.nz/#!qbpUTYiK!-deNdQJxsQS8bTSMxeUOtpEclCI-zpK7tbJiKV0tXY

_Ref:_ [https://securityonline.info/introduction-to-binwalk-firmware-analysis-tool/](https://securityonline.info/introduction-to-binwalk-firmware-analysis-tool/)

**Solution:**

~~~
┌─[xor@parrot]─[~/Téléchargements]
└──╼ $binwalk -e PurpleThing.jpeg 

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             PNG image, 780 x 720, 8-bit/color RGBA, non-interlaced
41            0x29            Zlib compressed data, best compression
153493        0x25795         PNG image, 802 x 118, 8-bit/color RGBA, non-interlaced
┌─[xor@parrot]─[~/Téléchargements]
└──╼ $cd _PurpleThing.jpeg.extracted/
┌─[xor@parrot]─[~/Téléchargements/_PurpleThing.jpeg.extracted]
└──╼ $ls
29  29.zlib
#Il manque les PNG :(
┌─[xor@parrot]─[~/Téléchargements/_PurpleThing.jpeg.extracted]
└──╼ $cd ..
┌─[xor@parrot]─[~/Téléchargements]
└──╼ $binwalk -D 'png image:png' PurpleThing.jpeg 

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             PNG image, 780 x 720, 8-bit/color RGBA, non-interlaced
41            0x29            Zlib compressed data, best compression
153493        0x25795         PNG image, 802 x 118, 8-bit/color RGBA, non-interlaced
┌─[xor@parrot]─[~/Téléchargements]
└──╼ $cd _PurpleThing.jpeg-0.extracted/
┌─[xor@parrot]─[~/Téléchargements/_PurpleThing.jpeg-0.extracted]
└──╼ $ls
0.png  25795.png  29  29.zlib
#Flag dans 25795.png
~~~

# Medium

## Up For A Little Challenge?

https://mega.nz/#!LoABFK5K!0sEKbsU3sBUG8zWxpBfD1bQx_JY_MuYEWQvLrFIqWZ0 You Know What To Do ...

**Solution:**

On utilise strings:

~~~
┌─[✗]─[xor@parrot]─[~/Téléchargements]
└──╼ $strings Begin\ Hack.jpg | grep flag
flag{Not_So_Simple...}
~~~

On essaye et effectivement c'est pas si simple...

On regarde les autres chaines de caractères:

~~~
┌─[xor@parrot]─[~/Téléchargements]
└──╼ $strings Begin\ Hack.jpg | more
(...)
`- https://mega.nz/#!*************** -N17hG
nFBfJliykJxXu8 -
(...)
Mp real_unlock_key: *******
(...)
~~~

Deux chaînes de caractères sont intéressantes.

On ouvre le lien qu'on vient de trouver et on télécharge le dossier nommé 'Up For A Little Challenge'. Dedans il y a un dossier nommé 'Did I Forget Again ?' qui fait penser au challenge précédent 'Taking LS'. On vérifie son contenu:

~~~
┌─[xor@parrot]─[~/Téléchargements/Up For A Little Challenge/Did I Forget Again?]
└──╼ $ls -la
total 132
drwxr-xr-x 3 xor xor  4096 août  22 12:35  .
drwxr-xr-x 4 xor xor  4096 août  22 12:22  ..
-rw-r--r-- 1 xor xor 83736 nov.  30  2016 'Loo Nothing Becomes Useless ack.jpg'
-rw-r--r-- 1 xor xor 32822 nov.  30  2016  .Processing.cerb4
┌─[xor@parrot]─[~/Téléchargements/Up For A Little Challenge/Did I Forget Again?]
└──╼ $cat .Processing.cerb4 
(...)
�2�1����>s�4D�P�|�yx��PKȦ�����|L�~I�|�yx����D<�*�&=P�J���d)/H@J�Kyv�Pdǭ>�#-��V�
                                          ��skycoder.jpgUT�?Xux
~~~

Il y a donc un fichier skycoder.jpg quelquepart !

~~~
$binwalk .Processing.cerb4

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             Zip archive data, encrypted at least v2.0 to extract, compressed size: 32632, uncompressed size: 46482, name: skycoder.jpg
32800         0x8020          End of Zip archive, footer length: 22

┌─[xor@parrot]─[~/Téléchargements/Up For A Little Challenge/Did I Forget Again?]
└──╼ $binwalk -e .Processing.cerb4

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             Zip archive data, encrypted at least v2.0 to extract, compressed size: 32632, uncompressed size: 46482, name: skycoder.jpg
32800         0x8020          End of Zip archive, footer length: 22
┌─[xor@parrot]─[~/Téléchargements/Up For A Little Challenge/Did I Forget Again?]
└──╼ $cd _.Processing.cerb4.extracted/
┌─[xor@parrot]─[~/Téléchargements/Up For A Little Challenge/Did I Forget Again?/_.Processing.cerb4.extracted]
└──╼ $ls
0.zip  skycoder.jpg
~~~

Ok on a un jpg et un zip. Il n'y a rien dans le jpg, le zip est protégé par un mot de passe. Utiliser le mot de passe trouvé initialement avec la commande strings ('real_unlock_key:') pour le dévérouiller.

On a maintenant un fichier 'skycoder.jpg (2)' avec du contenu. Ouvrir l'image. Zoomer. En bas à droite en rouge on trouve le flag :)

## The adventures of Boris Ivanov. Part 1.

The KGB agent Boris Ivanov got information about an attempt to sell classified data. He quickly reacted and intercepted the correspondence. Help Boris understand what exactly they were trying to sell. Here is the interception data: https://mega.nz/#!HfAHmKQb!zg6EPqfwes1bBDCjx7-ZFR_0O0-GtGg2Mrn56l5LCkE

_Indice:_ _Magic_ _Eye_

**Solution:**

Après avoir testé plusieurs outils en ligne de stéganographie, le seul à avoir donné un résultat plus ou moins est probant a été: [http://magiceye.ecksdee.co.uk/](http://magiceye.ecksdee.co.uk/). Toutefois, bien qu'on puisse distinguer le flag celui-ci reste illisible avec cet outil :(

Nous avons aussi essayez d'utiliser le script magiceye_solver [https://github.com/thearn/magiceye-solver](https://github.com/thearn/magiceye-solver) mais là encore nous n'avons pas réussi à trouver le flag avec cet outil...

Nous avons donc à faire à un stéréogramme et nous allons donc devoir le décoder manuellement, ou plutôt avec l'aide de GIMP.

Les étapes pour décoder un stéréogramme avec GIMP sont exposées dans cet article: [https://georgik.rocks/how-to-decode-stereogram-by-gimp/](https://georgik.rocks/how-to-decode-stereogram-by-gimp/)

**Etages à suivre:**

1. Ouvrir le fichier dans GIMP. Dupliquer le calque.

![Crepe](/img/gimp-duplicate-layers.png){: .center-block :}

2. Changer le mode, de Normal à Différence

![Crepe](/img/gimp-difference.png){: .center-block :}

3. Sélectionner l'Outil de déplacement

![Crepe](/img/gimp-move-tool.png){: .center-block :}

4. Déplacer le calque sur la droite à l'aide de la flèche droite jusqu'à ce qu'on trouve le flag

## 07601

https://mega.nz/#!CXYXBQAK!6eLJSXvAfGnemqWpNbLQtOHBvtkCzA7-zycVjhHPYQQ I think I lost my flag in there. Hopefully, it won't get attacked...

**Solution:**

~~~
┌─[xor@parrot]─[~/Téléchargements]
└──╼ $binwalk -e AGT.png 

DECIMAL       HEXADECIMAL     DESCRIPTION
--------------------------------------------------------------------------------
0             0x0             JPEG image data, JFIF standard 1.01
9584          0x2570          Zip archive data, at least v1.0 to extract, name: Secret Stuff.../
9646          0x25AE          Zip archive data, at least v2.0 to extract, name: Secret Stuff.../.DS_Store
10270         0x281E          Zip archive data, at least v1.0 to extract, name: __MACOSX/
10325         0x2855          Zip archive data, at least v1.0 to extract, name: __MACOSX/Secret Stuff.../
10396         0x289C          Zip archive data, at least v2.0 to extract, name: __MACOSX/Secret Stuff.../._.DS_Store
10546         0x2932          Zip archive data, at least v1.0 to extract, name: Secret Stuff.../Don't Open This.../
10627         0x2983          Zip archive data, at least v2.0 to extract, name: Secret Stuff.../Don't Open This.../.DS_Store
10988         0x2AEC          Zip archive data, at least v1.0 to extract, name: __MACOSX/Secret Stuff.../Don't Open This.../
11078         0x2B46          Zip archive data, at least v2.0 to extract, name: __MACOSX/Secret Stuff.../Don't Open This.../._.DS_Store
11247         0x2BEF          Zip archive data, at least v2.0 to extract, name: Secret Stuff.../Don't Open This.../I Warned You.jpeg
150550        0x24C16         Zip archive data, at least v2.0 to extract, name: __MACOSX/Secret Stuff.../Don't Open This.../._I Warned You.jpeg
151810        0x25102         End of Zip archive, footer length: 22
151832        0x25118         Zip archive data, at least v1.0 to extract, name: Secret Stuff.../
151894        0x25156         Zip archive data, at least v2.0 to extract, name: Secret Stuff.../.DS_Store
152518        0x253C6         Zip archive data, at least v1.0 to extract, name: __MACOSX/
152573        0x253FD         Zip archive data, at least v1.0 to extract, name: __MACOSX/Secret Stuff.../
152644        0x25444         Zip archive data, at least v2.0 to extract, name: __MACOSX/Secret Stuff.../._.DS_Store
152794        0x254DA         Zip archive data, at least v1.0 to extract, name: Secret Stuff.../Don't Open This.../
152875        0x2552B         Zip archive data, at least v2.0 to extract, name: Secret Stuff.../Don't Open This.../.DS_Store
153236        0x25694         Zip archive data, at least v1.0 to extract, name: __MACOSX/Secret Stuff.../Don't Open This.../
153326        0x256EE         Zip archive data, at least v2.0 to extract, name: __MACOSX/Secret Stuff.../Don't Open This.../._.DS_Store
153495        0x25797         Zip archive data, at least v2.0 to extract, name: Secret Stuff.../Don't Open This.../I Warned You.jpeg
292768        0x477A0         Zip archive data, at least v2.0 to extract, name: __MACOSX/Secret Stuff.../Don't Open This.../._I Warned You.jpeg
294028        0x47C8C         End of Zip archive, footer length: 22
294050        0x47CA2         Zip archive data, at least v1.0 to extract, name: Secret Stuff.../
294112        0x47CE0         Zip archive data, at least v2.0 to extract, name: Secret Stuff.../.DS_Store
294736        0x47F50         Zip archive data, at least v1.0 to extract, name: Secret Stuff.../Don't Open This.../
294817        0x47FA1         Zip archive data, at least v2.0 to extract, name: Secret Stuff.../Don't Open This.../.DS_Store
295162        0x480FA         Zip archive data, at least v2.0 to extract, name: Secret Stuff.../Don't Open This.../I Warned You.jpeg
434433        0x6A101         Zip archive data, at least v1.0 to extract, name: __MACOSX/
434488        0x6A138         Zip archive data, at least v1.0 to extract, name: __MACOSX/Secret Stuff.../
434559        0x6A17F         Zip archive data, at least v1.0 to extract, name: __MACOSX/Secret Stuff.../Don't Open This.../
434649        0x6A1D9         Zip archive data, at least v2.0 to extract, name: __MACOSX/Secret Stuff.../Don't Open This.../._I Warned You.jpeg
435702        0x6A5F6         End of Zip archive, footer length: 22
┌─[xor@parrot]─[~/Téléchargements]
└──╼ $cd _AGT.png.extracted/
┌─[xor@parrot]─[~/Téléchargements/_AGT.png.extracted]
└──╼ $ls
 25118.zip   47CA2.zip            __MACOSX
 2570.zip   'I Warned You.jpeg'  'Secret Stuff...'
┌─[xor@parrot]─[~/Téléchargements/_AGT.png.extracted]
└──╼ $unzip 25118.zip -d 25118
Archive:  25118.zip
warning [25118.zip]:  142218 extra bytes at beginning or within zipfile
  (attempting to process anyway)
   creating: 25118/Secret Stuff.../
  inflating: 25118/Secret Stuff.../.DS_Store  
   creating: 25118/Secret Stuff.../Don't Open This.../
  inflating: 25118/Secret Stuff.../Don't Open This.../.DS_Store  
  inflating: 25118/Secret Stuff.../Don't Open This.../I Warned You.jpeg  
   creating: 25118/__MACOSX/
   creating: 25118/__MACOSX/Secret Stuff.../
   creating: 25118/__MACOSX/Secret Stuff.../Don't Open This.../
  inflating: 25118/__MACOSX/Secret Stuff.../Don't Open This.../._I Warned You.jpeg  
┌─[xor@parrot]─[~/Téléchargements/_AGT.png.extracted]
└──╼ $ls
 25118       2570.zip   'I Warned You.jpeg'  'Secret Stuff...'
 25118.zip   47CA2.zip   __MACOSX
┌─[xor@parrot]─[~/Téléchargements/_AGT.png.extracted]
└──╼ $cd 25118/
┌─[xor@parrot]─[~/Téléchargements/_AGT.png.extracted/25118]
└──╼ $ls
 __MACOSX  'Secret Stuff...'
┌─[xor@parrot]─[~/Téléchargements/_AGT.png.extracted/25118]
└──╼ $cd Secret\ Stuff.../
┌─[xor@parrot]─[~/Téléchargements/_AGT.png.extracted/25118/Secret Stuff...]
└──╼ $ls
"Don't Open This..."
┌─[xor@parrot]─[~/Téléchargements/_AGT.png.extracted/25118/Secret Stuff...]
└──╼ $cd Don\'t\ Open\ This.../
┌─[xor@parrot]─[~/Téléchargements/_AGT.png.extracted/25118/Secret Stuff.../Don't Open This...]
└──╼ $ls
'I Warned You.jpeg'
┌─[✗]─[xor@parrot]─[~/Téléchargements/_AGT.png.extracted/25118/Secret Stuff.../Don't Open This...]
└──╼ $strings I\ Warned\ You.jpeg | grep ABC
ABCTF{*******}1r
┌─[xor@parrot]─[~/Téléchargements/_AGT.png.extracted/25118/Secret Stuff.../Don't Open This...]
└──╼ $
~~~

# Hard

## Exif

If only the password were in the image? https://mega.nz/#!SDpF0aYC!fkkhBJuBBtBKGsLTDiF2NuLihP2WRd97Iynd3PhWqRw You could really ‘own’ it with exif.

**Solution:**

On regarde rapidement l'hexadécimal et on trouve le flag (offset: 00000090), ou on utilise strings... Pas si difficile que ça en fait 

~~~
#1.
┌─[xor@parrot]─[~/Téléchargements]
└──╼ $xxd Computer-Password-Security-Hacker\ -\ Copy.jpg
#2. 
┌─[xor@parrot]─[~/Téléchargements]
└──╼ $strings Computer-Password-Security-Hacker\ -\ Copy.jpg | grep flag
flag{*********}
~~~

Vous pouvez aussi consulter les données EXIF pour trouver le flag: [https://onlineexifviewer.com/](https://onlineexifviewer.com/)

## Seeing is believing

My colleague's an astronaut who's currently on a mission orbiting in space. Just a few hours ago, unfortunately, his communication device caught fire so he's unable to report back to base. I did, however, receive a strange file that I can't seem to open. I think it may shed some light on his situation. Can you help me save poor boy Johnny? File: https://mega.nz/#!LTRUTaZb!9Nh0NwDONJQiOThif3G62evP8H_W9eIJSu0PdBQWKyg

_Ref:_

- [https://en.wikipedia.org/wiki/Ogg](https://en.wikipedia.org/wiki/Ogg)

**Solution:**

~~~
┌─[xor@parrot]─[~/Téléchargements/seeingisbelieving]
└──╼ $xxd help.me 
00000000: 4f67 6753 0002 0000 0000 0000 0000 9200  OggS............
00000010: 0000 0000 0000 7d85 db4b 011e 0176 6f72  ......}..K...vor
00000020: 6269 7300 0000 0001 44ac 0000 0000 0000  bis.....D.......
00000030: b0ad 0100 0000 0000 b801 4f67 6753 0000  ..........OggS..
00000040: 0000 0000 0000 0000 9200 0000 0100 0000  ................
(...)
~~~

Le fichier est un fichier audio ogg (_Magic_ _number:_ OggS). Copier le et renommer le en lui donnant l'extension .ogg.

Le fichier produit un son incompréhensible. Ca doit être de la stéganographie audio.

On ouvre le fichier avec Sonic Visualiser [https://www.sonicvisualiser.org/download.html](https://www.sonicvisualiser.org/download.html). On ajoute un spectogramme (Pane>Add Spectogram) et on observe un QR Code.

On scan le code avec une application comme QR Scanner et on à le flag :)

## Music To My Ears

This audio file is supposed to say the flag, but it's corrupted! ): <br> https://mega.nz/#!jexRzTzD!Fd3tD8ZcLquXJrsycMFUzozC9MHqaG-srUBfGREtL-0 <br /> <br />Can you fix it and input the flag? <br>

**Solution:** Procédure sous Windows, voir [http://sysfrontier.com/en/2014/12/31/hello-world/](http://sysfrontier.com/en/2014/12/31/hello-world/)

**Poursuivez avec: [PicoCTF 2018 - Forensics](https://0xss0rz.github.io/2019-08-21-picoCTF-Forensics-Write-Ups/)**

[![CC-BY](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by.svg)](https://creativecommons.org/licenses/by/4.0/)

This work is licensed under a [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).


