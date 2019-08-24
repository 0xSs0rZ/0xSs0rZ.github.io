---
layout: post
title: CTFLearn - Miscellaneous
subtitle: Challenges - Write-Ups 
gh-repo: 0xSs0rZ/0xSs0rZ.github.io
gh-badge: [star]
tags: [CTF, CTFLearn, Misc , Write-Up]
comments: false
---

**Voici quelques solutions pour la catégorie _Miscellaneous_ de CTFLearn**

CTFlearn: [https://ctflearn.com](https://ctflearn.com/)

# Easy

## Where Can My Robot Go?

Hint: Where do robots find what pages are on a website? Hint 2: What does disallow tell a robot? Hint 3: The flag is not 70r3hnanldfspufdsoifnlds 

**Solution:** https://ctflearn.com/70r3hnanldfspufdsoifnlds.html

## Paste Those Binaries

I found this scratched on the side of an old mac pro, r44LxiXq I wonder what it means... Hint: Some Kind of Website is at play here...

**Solution:** https://pastebin.com/r44LxiXq

## Reversal of fortune

Our team of agents have been tracking a hacker that sends cryptic messages to other hackers about what he's doing. We intercepted the below message he sent recently, can you figure out what it says? He mentions his hacker name in it, that's the code you need. .nac uoy fi tIe$reveRpilF eldnah ym gnisu em egassem ,avaj yllacificeps ,gnidoc emos htiw pleh deen I ,deifitnedi tegrat txeN

**Solution:**

script reverseString.py:

{% highlight javascript linenos %}
#Given a string S as input. You have to reverse the given string.

if __name__ == '__main__':
    string = input()
    reverseString=''
    i = len(string)-1
    while i>=0:
       reverseString+=string[i]
       i-=1
    print(reverseString)
{% endhighlight %}

Usage:

~~~
$python reverseString.py 
" .nac uoy fi tIe$reveRpilF eldnah ym gnisu em egassem ,avaj yllacificeps ,gnidoc emos htiw pleh deen I ,deifitnedi tegrat txeN"
Next target identified, I need help with some coding, specifically java, message me using my handle ******* if you can. 
~~~

## Wikipedia

Not much to go off here, but it’s all you need: Wikipedia and 128.125.52.138. 

**Solution:** 

1/ https://en.wikipedia.org/wiki/Special:Contributions/128.125.52.138

2/ https://en.wikipedia.org/w/index.php?title=Flag&oldid=676540540

3/ 'In a certain CTF competition, the flag to a certain problem is ******'

# QR Code

Do you remember something known as QR Code? Simple. Here for you : <br /> https://mega.nz/#!eGYlFa5Z!8mbiqg3kosk93qJCP-DBxIilHH2rf7iIVY-kpwyrx-0

**Solution:**

Scanner le code. Le QR code donne: c3ludCB2ZiA6IGEwX29icWxfczBldHJnX2RlX3BicXI= 

C'est du base64. On le décode: [https://www.base64decode.org/](https://www.base64decode.org/)

Ca donne un ROT 13. On le décode: [https://cryptii.com/pipes/rot13](https://cryptii.com/pipes/rot13)

On a le flag

## QR Code v2

How well are you in the ways of the QR Code? https://mega.nz/#!JItR3aqI!QKGxexShAPt-HUU_2DAdJKUljXc69sx1fXuaGUeoKaY

**Solution:**

Scanner le QR Code. On a le flag

## IP Tracer

Bob is an amateur hacker and has collected the following IP Address: 159.167.16.5, but Bob needs help finding where the IP Address is located. Can you help Bob find where the IP Address is located. (Type the City name)

**Solution:** https://db-ip.com/159.167.16.5

# Medium

## Help Bity

Bity had the flag for his problem. Unfortunately, his negative friend Noty corrupted it. Help Bity retrieve his flag. He only remembers the first 4 characters of the flag: CTFL. Flag: BUGMd`sozc0o`sx^0r^`vdr1ld

_Indice:_ Bit Flip

_Tool:_ [https://mothereff.in/binary-ascii](https://mothereff.in/binary-ascii)

**Solution:**

BUGMd`so en binaire donne:

01000010 01010101 01000111 01001101 01100100 01100000 01110011 01101111 

CTFLearn en binaire donne:

01000011 01010100 01000110 01001100 01100101 01100001 01110010 01101110 

On remarque le dernier bit a été flippé

BUGMd`sozc0o`sx^0r^`vdr1ld donne: 

01000010 01010101 01000111 01001101 01100100 01100000 01110011 01101111 01111010 01100011 00110000 01101111 01100000 01110011 01111000 01011110 00110000 01110010 01011110 01100000 01110110 01100100 01110010 00110001 01101100 01100100 01111100

On flippe les bits et on a le flag:

01000011 01010100 01000110 01001100 01100101 01100001 01110010 01101110 01111011 01100010 00110001 01101110 01100001 01110010 01111001 01011111 00110001 01110011 01011111 01100001 01110111 01100101 01110011 00110000 01101101 01100101 01111101

## Ambush Mission

Hi, i can't tell you my name since now i'm in a mission. In case to arrest our fugitive target, our team had been intercepted communication between the target with his fellow and found this image (https://mega.nz/#!TKZ3DabY!BEUHD7VJvq_b-M22eD4VfHv_PPBnW2m7CZUfMbveZYw). It looks like they are going to meet in specific place, but we still don't know the time yet. Can you help me ?

**Solution:**

On ouvre l'image avec StegSolve, on utilise Red Plane 0 et on trouve un texte encodé en base64 écrit à l'envers. On le réécrit à l'endroit et on le décode

## What could this be?

It seems like someone really likes special characters… Or could it mean something more? https://mega.nz/#!SDQkUYQZ!b1Fu7iZ_wGiNX0aOjez95_74TYDCnLb3YSQfRzs0J-o

Contenu de what_can_this_be.txt:

~~~
[][(![]+[])[+[]]+([![]]+[][[]])[+!+[]+[+[]]]+(![]+[])[!+[]+!+[]]+(!![]+[])[+[]]+(!![]+[])[!+[]+!+[]+!+[]]+(!![]+[])[+!+[]]][([][(![]+[])[+[]]+([![]]+[][[]])[+!+[]+[+[]]]+(![]+[]
(...)
~~~

C'est encodé en JSFuck !! On le décode et on a le flag. Outil: [https://enkhee-osiris.github.io/Decoder-JSFuck/](https://enkhee-osiris.github.io/Decoder-JSFuck/)

**Poursuivez avec:**

- [CTFlearn - Forensics](https://0xss0rz.github.io/2019-08-23-CTFlearn-Forensics-Write-Ups/)
- [CTFlearn - Cryptography](https://0xss0rz.github.io/2019-08-24-CTFlearn-Cryptography-Write-Ups/)

[![CC-BY](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by.svg)](https://creativecommons.org/licenses/by/4.0/)

This work is licensed under a [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).


