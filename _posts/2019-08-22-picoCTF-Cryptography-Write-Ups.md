---
layout: post
title: PicoCTF 2018 - Cryptography
subtitle: PicoCTF 2018 - Cryptography - Write-Ups 
gh-repo: 0xSs0rZ/0xSs0rZ.github.io
gh-badge: [star]
tags: [CTF, picoCTF, Cryptographie, Write-Up]
comments: false
---

**Voici quelques solutions pour la catégorie de cryptographie de picoCTF 2018.**

picoCTF 2018: [https://2018game.picoctf.com/](https://2018game.picoctf.com/)

## Crypto Warmup 1

{: .box-note}
Crpyto can often be done by hand, here's a message you got from a friend, llkjmlmpadkkc with the key of thisisalilkey. Can you use this table to solve it?. 

**Solution:** chiffre de Vigenère [https://planetcalc.com/2468/](https://planetcalc.com/2468/)

## Crypto Warmup 2

{: .box-note}
Cryptography doesn't have to be complicated, have you ever heard of something called rot13? cvpbPGS{guvf_vf_pelcgb!}

**Solution:** En ligne [https://cryptii.com/pipes/rot13-decoder](https://cryptii.com/pipes/rot13-decoder) ou avec Python:

~~~
$python
Python 2.7.16+ (default, Jul  8 2019, 09:45:29) 
[GCC 8.3.0] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> import codecs
>>> codecs.decode("cvpbPGS{guvf_vf_pelcgb!}", "rot_13")
u'picoCTF{quelquechose}'
>>> 
~~~

## HEEEEEEERE'S Johnny!

{: .box-note}
Okay, so we found some important looking files on a linux computer. Maybe they can be used to get a password to the process. Connect with nc 2018shell.picoctf.com 5221. Files can be found here: passwd shadow. 

_Ref:_ [https://www.openwall.com/john/doc/EXAMPLES.shtml](https://www.openwall.com/john/doc/EXAMPLES.shtml)

**Solution:**

~~~
┌─[xor@parrot]─[~/Téléchargements]
└──╼ $ls
passwd  rockyou.txt  rockyou.txt.bz2  shadow
┌─[xor@parrot]─[~/Téléchargements]
└──╼ $unshadow passwd shadow > mypasswd
┌─[xor@parrot]─[~/Téléchargements]
└──╼ $john --wordlist=rockyou.txt mypasswd
Warning: detected hash type "sha512crypt", but the string is also recognized as "HMAC-SHA256"
Use the "--format=HMAC-SHA256" option to force loading these as that type instead
Using default input encoding: UTF-8
Loaded 1 password hash (sha512crypt, crypt(3) $6$ [SHA512 128/128 SSE2 2x])
Cost 1 (iteration count) is 5000 for all loaded hashes
Will run 2 OpenMP threads
Press 'q' or Ctrl-C to abort, almost any other key for status
password1        (root)
1g 0:00:00:01 DONE (2019-08-21 15:20) 0.9615g/s 123.0p/s 123.0c/s 123.0C/s 123456..diamond
Use the "--show" option to display all of the cracked passwords reliably
Session completed
┌─[xor@parrot]─[~/Téléchargements]
└──╼ $nc 2018shell.picoctf.com 5221
Username: root
Password: password1
picoCTF{quelquechose}
~~~

## caesar cipher 1

{: .box-note}
This is one of the older ciphers in the books, can you decrypt the message? You can find the ciphertext in /problems/caesar-cipher-1_2_73ab1c3e92ea50396ad143ca48039b86 on the shell server

_Cipher:_ picoCTF{payzgmuujurjigkygxiovnkxlcgihubb}

**Solution:** [https://cryptii.com/pipes/caesar-cipher](https://cryptii.com/pipes/caesar-cipher)

## hertz

{: .box-note}
Here's another simple cipher for you where we made a bunch of substitutions. Can you decrypt it? Connect with nc 2018shell.picoctf.com 43324. 

**Solution:** Substitution cipher [https://quipqiup.com/](https://quipqiup.com/)

##  blaise's cipher 

{: .box-note}
My buddy Blaise told me he learned about this cool cipher invented by a guy also named Blaise! Can you figure out what it says? Connect with nc 2018shell.picoctf.com 26039. 

_Tools_: [https://www.boxentriq.com/code-breaking/vigenere-cipher](https://www.boxentriq.com/code-breaking/vigenere-cipher)

*Solution:**

~~~
$nc 2018shell.picoctf.com 26039
Encrypted message:
(...)
pohzCZK{g1gt3w3_n1pn3wd_ax3s7_maj_901j13l1}
(...)
~~~

Déchiffrer avec l'outil en ligne

## caesar cipher 2

{: .box-note}
Can you help us decrypt this message? We believe it is a form of a caesar cipher. You can find the ciphertext in /problems/caesar-cipher-2_2_d9c42f8026f320079f3d4fcbaa410615 on the shell server. 

_Cipher:_ PICO#4&[C!ESA2?#I0H%R3?JU34?A2%N4?S%C5R%]

**Solution:** Un petit script python :)

{% highlight javascript linenos %}
# coding=utf-8

# caesar cipher 2 - picoCTF2018
# Inspiré de: https://www.tutorialspoint.com/cryptography_with_python/cryptography_with_python_caesar_cipher

message = 'PICO#4&[C!ESA2?#I0H%R3?JU34?A2%N4?S%C5R%]' #encrypted message

characters = list(map(chr, range(32,126)))
LETTERS = ''.join(characters)

for key in range(len(LETTERS)):
   translated = ''
   for symbol in message:
      if symbol in LETTERS:
         num = LETTERS.find(symbol)
         num = num - key
         if num < 0:
            num = num + len(LETTERS)
         translated = translated + LETTERS[num]
      else:
         translated = translated + symbol
   print('key #%s: %s' % (key, translated))
{% endhighlight %}

**Poursuivez avec:**

- [PicoCTF 2018 - Forensics](https://0xss0rz.github.io/2019-08-21-picoCTF-Forensics-Write-Ups/)

- [PicoCTF 2018 - General Skills](https://0xss0rz.github.io/2019-08-22-picoCTF-General-Skills-Write-Ups/)


[![CC-BY](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by.svg)](https://creativecommons.org/licenses/by/4.0/)

This work is licensed under a [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).


