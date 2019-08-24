---
layout: post
title: CTFLearn - Cryptography
subtitle: Challenges de cryptographie - Write-Ups 
gh-repo: 0xSs0rZ/0xSs0rZ.github.io
gh-badge: [star]
tags: [CTF, CTFLearn, Cryptographie , Write-Up]
comments: false
---

**Voici quelques solutions pour la catégorie _Cryptography_ de CTFLearn**

CTFlearn: [https://ctflearn.com](https://ctflearn.com/)

# Easy

## Morse Code

..-. .-.. .- --. ... .- -- ..- . .-.. -- --- .-. ... . .. ... -.-. --- --- .-.. -... -.-- - .... . .-- .- -.-- .. .-.. .. -.- . -.-. .... . . ...

**Solution:** [http://www.unit-conversion.info/texttools/morse-code/](http://www.unit-conversion.info/texttools/morse-code/)

## Vigenere Cipher

The vignere cipher is a method of encrypting alphabetic text by using a series of interwoven Caesar ciphers based on the letters of a keyword.<br /> I’m not sure what this means, but it was left lying around: blorpy gwox{RgqssihYspOntqpxs}

**Solution:** Clé = blorpy [https://cryptii.com/pipes/vigenere-cipher](https://cryptii.com/pipes/vigenere-cipher)

## HyperStream Test 2

I love the smell of bacon in the morning! ABAAAABABAABBABBAABBAABAAAAAABAAAAAAAABAABBABABBAAAAABBABBABABBAABAABABABBAABBABBAABB

**Solution:** Baconian cipher [http://rumkin.com/tools/cipher/baconian.php](http://rumkin.com/tools/cipher/baconian.php)

## BruXOR

There is a technique called bruteforce. Message: q{vpln'bH_varHuebcrqxetrHOXEj No key! Just brute .. brute .. brute ... :D

_Ref:_ The Cyber Swiss Army Knife [https://github.com/gchq/CyberChef](https://github.com/gchq/CyberChef)

**Solution:** XOR Brute Force [https://gchq.github.io/](https://gchq.github.io/)

## Base 2 2 the 6

There are so many different ways of encoding and decoding information nowadays... One of them will work! Q1RGe0ZsYWdneVdhZ2d5UmFnZ3l9

**Solution:** [https://www.base64decode.org/](https://www.base64decode.org/)

## Hextroadinary

Meet ROXy, a coder obsessed with being exclusively the worlds best hacker. She specializes in short cryptic hard to decipher secret codes. The below hex values for example, she did something with them to generate a secret code, can you figure out what? Your answer should start with 0x. 0xc4115 0x4cf8

**Solution:** 

~~~
Python 2.7.16+ (default, Jul  8 2019, 09:45:29) 
[GCC 8.3.0] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> s1 = "c4115"
>>> s2 = "4cf8"
>>> xor = hex(int(s1, 16) ^ int(s2, 16))
>>> print xor
~~~

Ou en ligne: [http://xor.pw](http://xor.pw)

# Medium

## ALEXCTF CR2: Many time secrets

This time Fady learned from his old mistake and decided to use onetime pad as his encryption technique, but he never knew why people call it one time pad! Flag will start with ALEXCTF{. https://mega.nz/#!DGxBjaDR!tMWkHf0s0svmkboGd-IASHsS9jACxSYx4zi_ETsyzyQ

Onetime pad - Contenu du fichier msg:

~~~
0529242a631234122d2b36697f13272c207f2021283a6b0c7908
2f28202a302029142c653f3c7f2a2636273e3f2d653e25217908
322921780c3a235b3c2c3f207f372e21733a3a2b37263b313012
2f6c363b2b312b1e64651b6537222e37377f2020242b6b2c2d5d
283f652c2b31661426292b653a292c372a2f20212a316b283c09
29232178373c270f682c216532263b2d3632353c2c3c2a293504
613c37373531285b3c2a72273a67212a277f373a243c20203d5d
243a202a633d205b3c2d3765342236653a2c7423202f3f652a18
2239373d6f740a1e3c651f207f2c212a247f3d2e65262430791c
263e203d63232f0f20653f207f332065262c3168313722367918
2f2f372133202f142665212637222220733e383f2426386b
~~~

**Solution:**

Utilisation de cribdrag [https://github.com/SpiderLabs/cribdrag](https://github.com/SpiderLabs/cribdrag)

~~~
$cat msg | tr -d '\n'; echo
0529242a631234122d2b36697f13272c207f2021283a6b0c79082f28202a302029142c653f3c7f2a2636273e3f2d653e25217908322921780c3a235b3c2c3f207f372e21733a3a2b37263b3130122f6c363b2b312b1e64651b6537222e37377f2020242b6b2c2d5d283f652c2b31661426292b653a292c372a2f20212a316b283c0929232178373c270f682c216532263b2d3632353c2c3c2a293504613c37373531285b3c2a72273a67212a277f373a243c20203d5d243a202a633d205b3c2d3765342236653a2c7423202f3f652a182239373d6f740a1e3c651f207f2c212a247f3d2e65262430791c263e203d63232f0f20653f207f332065262c31683137223679182f2f372133202f142665212637222220733e383f2426386b
$./cribdrag/cribdrag.py 0529242a631234122d2b36697f13272c207f2021283a6b0c79082f28202a302029142c653f3c7f2a2636273e3f2d653e25217908322921780c3a235b3c2c3f207f372e21733a3a2b37263b3130122f6c363b2b312b1e64651b6537222e37377f2020242b6b2c2d5d283f652c2b31661426292b653a292c372a2f20212a316b283c0929232178373c270f682c216532263b2d3632353c2c3c2a293504613c37373531285b3c2a72273a67212a277f373a243c20203d5d243a202a633d205b3c2d3765342236653a2c7423202f3f652a182239373d6f740a1e3c651f207f2c212a247f3d2e65262430791c263e203d63232f0f20653f207f332065262c31683137223679182f2f372133202f142665212637222220733e383f2426386b
Your message is currently:
0	________________________________________
40	________________________________________
80	________________________________________
120	________________________________________
160	________________________________________
200	________________________________________
240	________________________________________
280	____
Your key is currently:
0	________________________________________
40	________________________________________
80	________________________________________
120	________________________________________
160	________________________________________
200	________________________________________
240	________________________________________
280	____
Please enter your crib: ALEXCTF{
*** 0: "Dear Fri"
1: "hho;Q`TV"
2: "ef&JwFkP"
3: "k/WlQymM"
4: ""^qJnp"
5: "SxWuhb/"
6: "u^hsu=9h"
7: "Sann*+U\"
8: "lgs1<GaW"
9: "jz,'Psj["
(...)
Enter the correct position, 'none' for no match, or 'end' to quit: 0
Is this crib part of the message or key? Please enter 'message' or 'key': message
Your message is currently:
0	ALEXCTF{________________________________
40	________________________________________
80	________________________________________
120	________________________________________
160	________________________________________
200	________________________________________
240	________________________________________
280	____
Your key is currently:
0	Dear Fri________________________________
40	________________________________________
80	________________________________________
120	________________________________________
160	________________________________________
200	________________________________________
240	________________________________________
280	____
# Guess: Dear Friend
Please enter your crib: Dear Friend, 
0: "ALEXCTF{HERE"
S" "mAK2r`DNX
2: "`O`T_BS"
3: "nsF2kY_
(...)
Enter the correct position, 'none' for no match, or 'end' to quit: 0
Is this crib part of the message or key? Please enter 'message' or 'key': key
Your message is currently:
0	ALEXCTF{HERE____________________________
40	________________________________________
80	________________________________________
120	________________________________________
160	________________________________________
200	________________________________________
240	________________________________________
280	____
Your key is currently:
0	Dear Friend,____________________________
40	________________________________________
80	________________________________________
120	________________________________________
160	________________________________________
200	________________________________________
240	________________________________________
280	____
#Guess: ALEXCTF{HERE_      format du flag
*** 0: "Dear Friend, "
(...)
259: "YcjobgfT\c7dy"
*** 260: "ncryption sch"
261: "n{dkc{R]-dtr}"
(...)
Enter the correct position, 'none' for no match, or 'end' to quit: 260
Is this crib part of the message or key? Please enter 'message' or 'key': message
Your message is currently:
0	ALEXCTF{HERE____________________________
40	________________________________________
80	________________________________________
120	________________________________________
160	________________________________________
200	________________________________________
240	____________________ALEXCTF{HERE________
280	____
Your key is currently:
0	Dear Friend,____________________________
40	________________________________________
80	________________________________________
120	________________________________________
160	________________________________________
200	________________________________________
240	____________________ncryption sch_______
280	____
#Guess
Please enter your crib: encryption scheme
(...)
259: "}ALEXCTF{HERE_GOE"
(...)
Enter the correct position, 'none' for no match, or 'end' to quit: 259
Is this crib part of the message or key? Please enter 'message' or 'key': key
Your message is currently:
0	ALEXCTF{HERE____________________________
40	________________________________________
80	________________________________________
120	________________________________________
160	________________________________________
200	________________________________________
240	___________________}ALEXCTF{HERE_GOE____
280	____
Your key is currently:
0	Dear Friend,____________________________
40	________________________________________
80	________________________________________
120	________________________________________
160	________________________________________
200	________________________________________
240	___________________encryption scheme____
280	____
(...)
233: "]j{x~7eTGe7z8|e6"
*** 234: "gree with me to u"
235: "lx;`{I[-zr:lg*c"
(...)
Enter the correct position, 'none' for no match, or 'end' to quit: 234
Is this crib part of the message or key? Please enter 'message' or 'key': message
Your message is currently:
0	ALEXCTF{HERE____________________________
40	________________________________________
80	________________________________________
120	________________________________________
160	________________________________________
200	__________________________________ALEXCT
240	F{HERE_GOES________}ALEXCTF{HERE_GOE____
280	____
Your key is currently:
0	Dear Friend,____________________________
40	________________________________________
80	________________________________________
120	________________________________________
160	________________________________________
200	__________________________________gree w
240	ith me to u________encryption scheme____
280	____
Please enter your crib: agree with me to us
(...)
233: "}ALEXCTF{HERE_GOES_"
(...)
Enter the correct position, 'none' for no match, or 'end' to quit: 233
Is this crib part of the message or key? Please enter 'message' or 'key': key
Your message is currently:
0	ALEXCTF{HERE____________________________
40	________________________________________
80	________________________________________
120	________________________________________
160	________________________________________
200	_________________________________}ALEXCT
240	F{HERE_GOES________}ALEXCTF{HERE_GOE____
280	____
Your key is currently:
0	Dear Friend,____________________________
40	________________________________________
80	________________________________________
120	________________________________________
160	________________________________________
200	_________________________________agree w
240	ith me to us_______encryption scheme____
280	____
Please enter your crib: ALEXCTF{HERE_GOES_
(...)
25: "IcmxidfR\i7zc8ecex"
*** 26: "nderstood my mista"
27: "ilohc}RW-zn:uaybm`"
(...)
Enter the correct position, 'none' for no match, or 'end' to quit: 26
Is this crib part of the message or key? Please enter 'message' or 'key': message
Your message is currently:
0	ALEXCTF{HERE______________ALEXCTF{HERE_G
40	OES_____________________________________
80	________________________________________
120	________________________________________
160	________________________________________
200	_________________________________}ALEXCT
240	F{HERE_GOES________}ALEXCTF{HERE_GOE____
280	____
Your key is currently:
0	Dear Friend,______________nderstood my m
40	ista____________________________________
80	________________________________________
120	________________________________________
160	________________________________________
200	_________________________________agree w
240	ith me to us_______encryption scheme____
280	____
Please enter your crib: understood my mistake
(...)
25: "}ALEXCTF{HERE_GOES_TH"
(...)
Enter the correct position, 'none' for no match, or 'end' to quit: 25
Is this crib part of the message or key? Please enter 'message' or 'key': key
Your message is currently:
0	ALEXCTF{HERE_____________}ALEXCTF{HERE_G
40	OES_TH__________________________________
80	________________________________________
120	________________________________________
160	________________________________________
200	_________________________________}ALEXCT
240	F{HERE_GOES________}ALEXCTF{HERE_GOE____
280	____
Your key is currently:
0	Dear Friend,_____________understood my m
40	istake__________________________________
80	________________________________________
120	________________________________________
160	________________________________________
200	_________________________________agree w
240	ith me to us_______encryption scheme____
280	____
Please enter your crib: ALEXCTF{HERE_GOES_THE_
(...)
155: "E-yotawSyx7x}(dyx+{"
*** 156: " proven to be not crac"
157: "}{rmr|Gb7u8feb,hnly"
(...)
Enter the correct position, 'none' for no match, or 'end' to quit: 156
Is this crib part of the message or key? Please enter 'message' or 'key': message
Your message is currently:
0	ALEXCTF{HERE_____________}ALEXCTF{HERE_G
40	OES_TH__________________________________
80	________________________________________
120	____________________________________ALEX
160	CTF{HERE_GOES_THE_______________________
200	_________________________________}ALEXCT
240	F{HERE_GOES________}ALEXCTF{HERE_GOE____
280	____
Your key is currently:
0	Dear Friend,_____________understood my m
40	istake__________________________________
80	________________________________________
120	____________________________________ pro
160	ven to be not crac______________________
200	_________________________________agree w
240	ith me to us_______encryption scheme____
280	____
Please enter your crib: proven to be not crack
(...)
57: "LEXCTF{HERE_GOES_THE_K"
(...)
Enter the correct position, 'none' for no match, or 'end' to quit: 157
Is this crib part of the message or key? Please enter 'message' or 'key': key
Your message is currently:
0	ALEXCTF{HERE_____________}ALEXCTF{HERE_G
40	OES_TH__________________________________
80	________________________________________
120	____________________________________ALEX
160	CTF{HERE_GOES_THE_K_____________________
200	_________________________________}ALEXCT
240	F{HERE_GOES________}ALEXCTF{HERE_GOE____
280	____
Your key is currently:
0	Dear Friend,_____________understood my m
40	istake__________________________________
80	________________________________________
120	____________________________________ pro
160	ven to be not crack_____________________
200	_________________________________agree w
240	ith me to us_______encryption scheme____
280	____
Please enter your crib: ALEXCTF{HERE_GOES_THE_KEY 
(...)
*** 52: "sed One time pad encrypti"
(...)
Enter the correct position, 'none' for no match, or 'end' to quit: 52
Is this crib part of the message or key? Please enter 'message' or 'key': message
Your message is currently:
0	ALEXCTF{HERE_____________}ALEXCTF{HERE_G
40	OES_TH______ALEXCTF{HERE_GOES_THE_KEY___
80	________________________________________
120	____________________________________ALEX
160	CTF{HERE_GOES_THE_K_____________________
200	_________________________________}ALEXCT
240	F{HERE_GOES________}ALEXCTF{HERE_GOE____
280	____
Your key is currently:
0	Dear Friend,_____________understood my m
40	istake______sed One time pad encrypti___
80	________________________________________
120	____________________________________ pro
160	ven to be not crack_____________________
200	_________________________________agree w
240	ith me to us_______encryption scheme____
280	____
Please enter your crib: sed One time pad encryption
(...)
52: "ALEXCTF{HERE_GOES_THE_KEY}A"
(...)
Enter the correct position, 'none' for no match, or 'end' to quit: 52
Is this crib part of the message or key? Please enter 'message' or 'key': key
Your message is currently:
0	ALEXCTF{HERE_____________}ALEXCTF{HERE_G
40	OES_TH______ALEXCTF{HERE_GOES_THE_KEY}A_
80	________________________________________
120	____________________________________ALEX
160	CTF{HERE_GOES_THE_K_____________________
200	_________________________________}ALEXCT
240	F{HERE_GOES________}ALEXCTF{HERE_GOE____
280	____
Your key is currently:
0	Dear Friend,_____________understood my m
40	istake______sed One time pad encryption_
80	________________________________________
120	____________________________________ pro
160	ven to be not crack_____________________
200	_________________________________agree w
240	ith me to us_______encryption scheme____
280	____
Please enter your crib: ALEXCTF{HERE_GOES_THE_KEY}
(...)
*** 182: "ever if the key is kept se"
(...)
Enter the correct position, 'none' for no match, or 'end' to quit: 182
Is this crib part of the message or key? Please enter 'message' or 'key': message
Your message is currently:
0	ALEXCTF{HERE_____________}ALEXCTF{HERE_G
40	OES_TH______ALEXCTF{HERE_GOES_THE_KEY}A_
80	________________________________________
120	____________________________________ALEX
160	CTF{HERE_GOES_THE_K___ALEXCTF{HERE_GOES_
200	THE_KEY}_________________________}ALEXCT
240	F{HERE_GOES________}ALEXCTF{HERE_GOE____
280	____
Your key is currently:
0	Dear Friend,_____________understood my m
40	istake______sed One time pad encryption_
80	________________________________________
120	____________________________________ pro
160	ven to be not crack___ever if the key is
200	 kept se_________________________agree w
240	ith me to us_______encryption scheme____
280	____
Please enter your crib: ever if the key is kept secret
(...)
182: "ALEXCTF{HERE_GOES_THE_KEY}AKRI"
(...)
Enter the correct position, 'none' for no match, or 'end' to quit: 182
Is this crib part of the message or key? Please enter 'message' or 'key': key
Your message is currently:
0	ALEXCTF{HERE_____________}ALEXCTF{HERE_G
40	OES_TH______ALEXCTF{HERE_GOES_THE_KEY}A_
80	________________________________________
120	____________________________________ALEX
160	CTF{HERE_GOES_THE_K___ALEXCTF{HERE_GOES_
200	THE_KEY}AKRI_____________________}ALEXCT
240	F{HERE_GOES________}ALEXCTF{HERE_GOE____
280	____
Your key is currently:
0	Dear Friend,_____________understood my m
40	istake______sed One time pad encryption_
80	________________________________________
120	____________________________________ pro
160	ven to be not crack___ever if the key is
200	 kept secret_____________________agree w
240	ith me to us_______encryption scheme____
280	____
Please enter your crib: ALEXCTF{HERE_GOES_THE_KEY}
(...)
*** 234: "gree with me to use this e"
(...)
Enter the correct position, 'none' for no match, or 'end' to quit: 234
Is this crib part of the message or key? Please enter 'message' or 'key': message
Your message is currently:
0	ALEXCTF{HERE_____________}ALEXCTF{HERE_G
40	OES_TH______ALEXCTF{HERE_GOES_THE_KEY}A_
80	________________________________________
120	____________________________________ALEX
160	CTF{HERE_GOES_THE_K___ALEXCTF{HERE_GOES_
200	THE_KEY}AKRI_____________________}ALEXCT
240	F{HERE_GOES_THE_KEY}ALEXCTF{HERE_GOE____
280	____
Your key is currently:
0	Dear Friend,_____________understood my m
40	istake______sed One time pad encryption_
80	________________________________________
120	____________________________________ pro
160	ven to be not crack___ever if the key is
200	 kept secret_____________________agree w
240	ith me to use this encryption scheme____
280	____
Please enter your crib: ALEXCTF{HERE_GOES_THE_KEY}
(...)
*** 156: " proven to be not cracked "
(...)
Enter the correct position, 'none' for no match, or 'end' to quit: 156
Is this crib part of the message or key? Please enter 'message' or 'key': message
Your message is currently:
0	ALEXCTF{HERE_____________}ALEXCTF{HERE_G
40	OES_TH______ALEXCTF{HERE_GOES_THE_KEY}A_
80	________________________________________
120	____________________________________ALEX
160	CTF{HERE_GOES_THE_KEY}ALEXCTF{HERE_GOES_
200	THE_KEY}AKRI_____________________}ALEXCT
240	F{HERE_GOES_THE_KEY}ALEXCTF{HERE_GOE____
280	____
Your key is currently:
0	Dear Friend,_____________understood my m
40	istake______sed One time pad encryption_
80	________________________________________
120	____________________________________ pro
160	ven to be not cracked ever if the key is
200	 kept secret_____________________agree w
240	ith me to use this encryption scheme____
280	____
Please enter your crib: ALEXCTF{HERE_GOES_THE_KEY}
*** 0: "Dear Friend, This time I u"
(...)
Enter the correct position, 'none' for no match, or 'end' to quit: 0
Is this crib part of the message or key? Please enter 'message' or 'key': message
Your message is currently:
0	ALEXCTF{HERE_GOES_THE_KEY}ALEXCTF{HERE_G
40	OES_TH______ALEXCTF{HERE_GOES_THE_KEY}A_
80	________________________________________
120	____________________________________ALEX
160	CTF{HERE_GOES_THE_KEY}ALEXCTF{HERE_GOES_
200	THE_KEY}AKRI_____________________}ALEXCT
240	F{HERE_GOES_THE_KEY}ALEXCTF{HERE_GOE____
280	____
Your key is currently:
0	Dear Friend, This time I understood my m
40	istake______sed One time pad encryption_
80	________________________________________
120	____________________________________ pro
160	ven to be not cracked ever if the key is
200	 kept secret_____________________agree w
240	ith me to use this encryption scheme____
280	____
Please enter your crib: ALEXCTF{HERE_GOES_THE_KEY}
(...)
*** 130: "hod that is mathematically"
(...)
Enter the correct position, 'none' for no match, or 'end' to quit: 130
Is this crib part of the message or key? Please enter 'message' or 'key': message
Your message is currently:
0	ALEXCTF{HERE_GOES_THE_KEY}ALEXCTF{HERE_G
40	OES_TH______ALEXCTF{HERE_GOES_THE_KEY}A_
80	________________________________________
120	__________ALEXCTF{HERE_GOES_THE_KEY}ALEX
160	CTF{HERE_GOES_THE_KEY}ALEXCTF{HERE_GOES_
200	THE_KEY}AKRI_____________________}ALEXCT
240	F{HERE_GOES_THE_KEY}ALEXCTF{HERE_GOE____
280	____
Your key is currently:
0	Dear Friend, This time I understood my m
40	istake______sed One time pad encryption_
80	________________________________________
120	__________hod that is mathematically pro
160	ven to be not cracked ever if the key is
200	 kept secret_____________________agree w
240	ith me to use this encryption scheme____
280	____
Please enter your crib: ALEXCTF{HERE_GOES_THE_KEY}
(...)
*** 208: "cure, Let Me know if you a"
(...)
Enter the correct position, 'none' for no match, or 'end' to quit: 208
Is this crib part of the message or key? Please enter 'message' or 'key': message
Your message is currently:
0	ALEXCTF{HERE_GOES_THE_KEY}ALEXCTF{HERE_G
40	OES_TH______ALEXCTF{HERE_GOES_THE_KEY}A_
80	________________________________________
120	__________ALEXCTF{HERE_GOES_THE_KEY}ALEX
160	CTF{HERE_GOES_THE_KEY}ALEXCTF{HERE_GOES_
200	THE_KEY}ALEXCTF{HERE_GOES_THE_KEY}ALEXCT
240	F{HERE_GOES_THE_KEY}ALEXCTF{HERE_GOE____
280	____
Your key is currently:
0	Dear Friend, This time I understood my m
40	istake______sed One time pad encryption_
80	________________________________________
120	__________hod that is mathematically pro
160	ven to be not cracked ever if the key is
200	 kept secure, Let Me know if you agree w
240	ith me to use this encryption scheme____
280	____
Please enter your crib
#Continuer comme ça jusqu'à tout remplire. De toute façon nous avonc trouvé le flag depuis longtemps :)
~~~

**Poursuivez avec:**

- [CTFlearn - Forensics](https://0xss0rz.github.io/2019-08-23-CTFlearn-Forensics-Write-Ups/)
- [Cryptopals - Set 1](https://0xss0rz.github.io/2019-08-23-Cryptopals-Write-Ups/)
- [PicoCTF 2018 _ Cryptography](https://0xss0rz.github.io/2019-08-22-picoCTF-Cryptography-Write-Ups/)

[![CC-BY](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by.svg)](https://creativecommons.org/licenses/by/4.0/)

This work is licensed under a [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).


