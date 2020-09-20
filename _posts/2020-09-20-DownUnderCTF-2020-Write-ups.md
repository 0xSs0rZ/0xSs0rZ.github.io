---
layout: post
title: DownUnder CTF 2020 - Write-Ups
subtitle: Web, crypto, stegano, etc. 
gh-repo: 0xSs0rZ/0xSs0rZ.github.io
gh-badge: [star]
tags: [CTF, DUCTF, Web, Crypto, Stegano, Write-up, Rot-i, RSA, RsaCtfTool, Audacity, wav, Audio, Spectrum, Stegcracker, Pickle, Command Injection]
comments: false
---

![Logo](/img/DUCTF_logo.png){: .center-block :}

DownUnder est la “premiere compétition australienne en cybersécurité”. L'édition 2020 s'est déroulée en ligne du 18 au 20 septembre.

{: .box-warning}
DownUnderCTF is a online world-wide Capture The Flag (CTF) competition targeted at Australian secondary and tertiary students though is open to everyone to compete. Its main goal is to try to up-skill the next-generation of potential Cyber Security Professionals, as well as increase the size of the CTF community here in Australia. This event is a cross collaboration between 13 different Cyber Security Societies around the country trying to make a difference in the Cyber Security community by providing a national cyber security competition within Australia, which is also open to the world - Source: [CTFTime](https://ctftime.org/event/1084)

Voici quelques write-up des épreuves proposées lors du DownUnder CTF 2020

# Crypto

## Rot-i - 100 - beginner

![Rot-i](/img/DUCTF_rot-i_1.png){: .center-block :}

**challenge.txt** 

~~~
Ypw'zj zwufpp hwu txadjkcq dtbtyu kqkwxrbvu! Mbz cjzg kv IAJBO{ndldie_al_aqk_jjrnsxee}. Xzi utj gnn olkd qgq ftk ykaqe uei mbz ocrt qi ynlu, etrm mff'n wij bf wlny mjcj :).
~~~

Nous observons `IAJBO{ndldie_al_aqk_jjrnsxee}`

On va utiliser [Cryptii](https://cryptii.com/pipes/caesar-cipher)

en sachant que le format du flag est `DUCTF{flag}` on débute avec un décalage de +5: a ->f , ..., d -> i, etc

la version décodée devient:

~~~
Tkr'ue urpakk crp osvyefxl yowotp flfrsmwqp! Hwu xeub fq DVEWJ{iygydz_vg_vlf_eeminszz}. Sud poe bii jgfy lbl aof tfvlz pzd hwu jxmo ld tigp, zomh haa'i rde wa rgit hexe :)

# D
~~~

Continuons avec un décalage de 6: a->g, ..., u -> v, etc

~~~
Sjq'td tqozjj bqo nruxdewk xnvnso ekeqrlvpo! Gvt wdta ep CUDVI{hxfxcy_uf_uke_ddlhmryy}. Rtc ond ahh ifex kak zne seuky oyc gvt iwln kc shfo, ynlg gzz'h qcd vz qfhs gdwd :).

# DU
~~~

Décalage de 7

~~~
Rip'sc spnyii apn mqtwcdvj wmumrn djdpqkuon! Fus vcsz do BTCUH{gwewbx_te_tjd_cckglqxx}. Qsb nmc zgg hedw jzj ymd rdtjx nxb fus hvkm jb rgen, xmkf fyy'g pbc uy pegr fcvc :).

# DUC
~~~

Décalage de 8

~~~
Qho'rb romxhh zom lpsvbcui vltlqm cicopjtnm! Etr ubry cn ASBTG{fvdvaw_sd_sic_bbjfkpww}. Pra mlb yff gdcv iyi xlc qcsiw mwa etr gujl ia qfdm, wlje exx'f oab tx odfq ebub :).

# DUCT
~~~

Décalage de 9

~~~
Pgn'qa qnlwgg ynl koruabth ukskpl bhbnoisml! Dsq taqx bm ZRASF{eucuzv_rc_rhb_aaiejovv}. Oqz lka xee fcbu hxh wkb pbrhv lvz dsq ftik hz pecl, vkid dww'e nza sw ncep data :).

# DUCTF
~~~

Décalage de 10

~~~
Ofm'pz pmkvff xmk jnqtzasg tjrjok agamnhrlk! Crp szpw al YQZRE{dtbtyu_qb_qga_zzhdinuu}. Npy kjz wdd ebat gwg vja oaqgu kuy crp eshj gy odbk, ujhc cvv'd myz rv mbdo czsz :).

# DUCTF{
~~~

Décalage de 11

~~~
Nel'oy oljuee wlj impsyzrf siqinj zfzlmgqkj! Bqo ryov zk XPYQD{csasxt_pa_pfz_yygchmtt}. Mox jiy vcc dazs fvf uiz nzpft jtx bqo drgi fx ncaj, tigb buu'c lxy qu lacn byry :).

# DUCTF{c
~~~

etc, etc. 

ce qui donne au final  `DUCTF{crypto_is_fun_kjqlptzy}`

Aussi possible de créer un script pour automatiser

## babyrsa - 294 - easy

![BabyRSA](/img/DUCTF_babyrsa_1.png){: .center-block :}

**babyrsa.py:**

~~~
from Crypto.Util.number import bytes_to_long, getPrime

flag = open('flag.txt', 'rb').read().strip()

p, q = getPrime(1024), getPrime(1024)
n = p*q
e = 0x10001

s = pow(557*p - 127*q, n - p - q, n)

c = pow(bytes_to_long(flag), e, n)

print(f'n = {n}')
print(f's = {s}')
print(f'c = {c}')
~~~

**output.txt**

~~~
n = 19574201286059123715221634877085223155972629451020572575626246458715199192950082143183900970133840359007922584516900405154928253156404028820410452946729670930374022025730036806358075325420793866358986719444785030579682635785758091517397518826225327945861556948820837789390500920096562699893770094581497500786817915616026940285194220703907757879335069896978124429681515117633335502362832425521219599726902327020044791308869970455616185847823063474157292399830070541968662959133724209945293515201291844650765335146840662879479678554559446535460674863857818111377905454946004143554616401168150446865964806314366426743287
s = 3737620488571314497417090205346622993399153545806108327860889306394326129600175543006901543011761797780057015381834670602598536525041405700999041351402341132165944655025231947620944792759658373970849932332556577226700342906965939940429619291540238435218958655907376220308160747457826709661045146370045811481759205791264522144828795638865497066922857401596416747229446467493237762035398880278951440472613839314827303657990772981353235597563642315346949041540358444800649606802434227470946957679458305736479634459353072326033223392515898946323827442647800803732869832414039987483103532294736136051838693397106408367097
c = 7000985606009752754441861235720582603834733127613290649448336518379922443691108836896703766316713029530466877153379023499681743990770084864966350162010821232666205770785101148479008355351759336287346355856788865821108805833681682634789677829987433936120195058542722765744907964994170091794684838166789470509159170062184723590372521926736663314174035152108646055156814533872908850156061945944033275433799625360972646646526892622394837096683592886825828549172814967424419459087181683325453243145295797505798955661717556202215878246001989162198550055315405304235478244266317677075034414773911739900576226293775140327580
~~~

On a `n`, on a `c` (on pourrait aussi utiliser s mais ici c'est c qui nous intéresse :) ) et `e` e =  0x10001 = 65537

On va utiliser RsaCtfTool. 

Ref:

- [https://stackoverflow.com/questions/60896984/ctf-rsa-decrypt-using-n-c-e](https://stackoverflow.com/questions/60896984/ctf-rsa-decrypt-using-n-c-e)
- [RsaCtfTool](https://github.com/Ganapati/RsaCtfTool)

~~~
root@Host-001:~/Bureau/OTA/DownUnder/RsaCtfTool# python3 RsaCtfTool.py -n 19574201286059123715221634877085223155972629451020572575626246458715199192950082143183900970133840359007922584516900405154928253156404028820410452946729670930374022025730036806358075325420793866358986719444785030579682635785758091517397518826225327945861556948820837789390500920096562699893770094581497500786817915616026940285194220703907757879335069896978124429681515117633335502362832425521219599726902327020044791308869970455616185847823063474157292399830070541968662959133724209945293515201291844650765335146840662879479678554559446535460674863857818111377905454946004143554616401168150446865964806314366426743287 -e 65537 --uncipher 7000985606009752754441861235720582603834733127613290649448336518379922443691108836896703766316713029530466877153379023499681743990770084864966350162010821232666205770785101148479008355351759336287346355856788865821108805833681682634789677829987433936120195058542722765744907964994170091794684838166789470509159170062184723590372521926736663314174035152108646055156814533872908850156061945944033275433799625360972646646526892622394837096683592886825828549172814967424419459087181683325453243145295797505798955661717556202215878246001989162198550055315405304235478244266317677075034414773911739900576226293775140327580
private argument is not set, the private key will not be displayed, even if recovered.

[*] Testing key /tmp/tmp341tt366.
[*] Performing smallfraction attack on /tmp/tmp341tt366.
[*] Performing noveltyprimes attack on /tmp/tmp341tt366.
[*] Performing cube_root attack on /tmp/tmp341tt366.
[*] Performing boneh_durfee attack on /tmp/tmp341tt366.
[*] Performing qicheng attack on /tmp/tmp341tt366.
Exception ignored in: <_io.TextIOWrapper name='<stdout>' mode='w' encoding='UTF-8'>
BrokenPipeError: [Errno 32] Broken pipe
[*] Performing comfact_cn attack on /tmp/tmp341tt366.
[*] Performing fermat attack on /tmp/tmp341tt366.
Exception ignored in: <_io.TextIOWrapper name='<stdout>' mode='w' encoding='UTF-8'>
BrokenPipeError: [Errno 32] Broken pipe
[*] Performing smallq attack on /tmp/tmp341tt366.
[*] Performing partial_q attack on /tmp/tmp341tt366.
[*] Performing ecm2 attack on /tmp/tmp341tt366.
[*] ECM2 Method can run forever and may never succeed, timeout set to 30sec. Hit Ctrl-C to bail out.
[*] Performing factordb attack on /tmp/tmp341tt366.

Results for /tmp/tmp341tt366:

Unciphered data :
HEX : 0x0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000044554354467b653473795f5253415f6368346c6c5f74305f6733745f737434727433647d
INT (big endian) : 132748507276301415390301942147815134336593703255400548711964080454286372643976697308285
INT (little endian) : 15829199073247604524471237805592804169128196475871082569476417023601722338231656685468837592997900577790923699171534087954919631213703023711961059186330207829454106455302666975098707358780043052942624619777166563446504122747411012925394443317770259823055620895536661530674671341652253899311425180305611044762554757343060526644668218063118685650683435257254542407836808304940172115798101797929675856569673066773607713082197584731479341748823605000803234438563509960460190169609698043022123967736287121317395963248038222658141347766002113290332320623106392021317711049212999174765622308416374378059628281299898371932160
STR : b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00DUCTF{e4sy_RSA_ch4ll_t0_g3t_st4rt3d}'
root@Host-001:~/Bureau/OTA/DownUnder/RsaCtfTool# 
~~~

![BabyRSA](/img/DUCTF_babyrsa_2.png){: .center-block :}

`DUCTF{e4sy_RSA_ch4ll_t0_g3t_st4rt3d}`

# Forensics 

## On The Spectrum - 100 - Beginner

![Spectrum](/img/DUCTF_spectrum_1.png){: .center-block :}

~~~
My friend has been sending me lots of WAV files, I think he is trying to communicate with me, what is the message he sent?
Author: scsc
~~~

On ouvre message_1.wav avec Audacity. 

On applique un 'Spectrum' avec les paramètres suivants: 

![Spectrum](/img/DUCTF_spectrum_2.png){: .center-block :}

Ref: [http://cedric.cnam.fr/~bouchati/enseignement/STMN_TDS/TP3_TFetSpectre.pdf](http://cedric.cnam.fr/~bouchati/enseignement/STMN_TDS/TP3_TFetSpectre.pdf)

**Résultat:**

![Spectrum](/img/DUCTF_spectrum_3.png){: .center-block :}

DUCTF{m4h?3_n0t_s0_h1dd3n}

Plus d'outils et de méthodes en stéganographie disponibles ici: [0xSs0rZ - GitBook](https://0xss0rz.gitbook.io/0xss0rz/ctf/steganography-1/tools) :)

##  I Love Scomo - 482 - medium (Incomplet)

![Scomo](/img/DUCTF_scomo_1.png){: .center-block :}

~~~
I really do love Scott Morrison! <3 <3 <3
However, some people don't like me because of my secret crush :(. So I have to hide my secrets using steganography. This is my hidden space, where I can dream about being with Scomo and I really appreciate that no one tries to reveal my secret message for him.
 Author: ghostccamm
~~~

On utilise stegcracker

~~~
root@Host-001:~/Bureau/OTA/DownUnder# stegcracker ilovescomo.jpg /usr/share/wordlists/rockyou.txt 
StegCracker 2.0.9 - (https://github.com/Paradoxis/StegCracker)
Copyright (c) 2020 - Luke Paris (Paradoxis)

Counting lines in wordlist..
Attacking file 'ilovescomo.jpg' with wordlist '/usr/share/wordlists/rockyou.txt'..
Successfully cracked file with password: iloveyou
Tried 5 passwords
Your file has been written to: ilovescomo.jpg.out
iloveyou
root@Host-001:~/Bureau/OTA/DownUnder# 
~~~

Le résultat est l'hymne australienne

~~~
root@Host-001:~/Bureau/OTA/DownUnder# cat ilovescomo.jpg.out | head
Australians all let us rejoice,
For we are young and free; 
We've golden soil and wealth for toil;
Our home is girt by sea;
Our land abounds in nature's gifts
Of beauty rich and rare; 
In history's page, let every stage
Advance Australia Fair.
In joyful strains then let us sing,
Advance Australia Fair. 
root@Host-001:~/Bureau/OTA/DownUnder# 
~~~

{: .box-warning}
Australians all let us rejoice,
For we are young and free; 
We've golden soil and wealth for toil;
Our home is girt by sea;
Our land abounds in nature's gifts 
Of beauty rich and rare;
In history's page, let every stage
Advance Australia Fair.
In joyful strains then let us sing, 
Advance Australia Fair. 
Beneath our radiant Southern Cross
We'll toil with hearts and hands; 
To make this Commonwealth of ours 
Renowned of all the lands;
For those who've come across the seas 
We've boundless plains to share; 
With courage let us all combine
To Advance Australia Fair. 
In joyful strains then let us sing, 
Advance Australia Fair.
Ref: https://en.wikipedia.org/wiki/Advance_Australia_Fair

A compléter

# Reversing

## formating  - 100 - formatting (Incomplet)

![Formating](/img/DUCTF_formating_1.png){: .center-block :}

Le fichier est un exécutable ELF 64-bit

![Formating](/img/DUCTF_formating_2.png){: .center-block :}

On ouvre le fichier avec IDA. Dans la fonction main on trouve `this crap is too easy what the heck`

![Formating](/img/DUCTF_formating_3.png){: .center-block :}

![Formating](/img/DUCTF_formating_4.png){: .center-block :}

A compléter 

# Web

## Robotsss - 499 - medium

![Robots](/img/DUCTF_robots_1.png){: .center-block :}

~~~
Author: donfran
Us robot devs use better templates than those stupid humans!
https://chal.duc.tf:30106
~~~

![Robots](/img/DUCTF_robots_2.png){: .center-block :}

On crée un compte et on se log. On tombe sur:

![Robots](/img/DUCTF_robots_3.png){: .center-block :}

**MESSAGE TO THE ROBOT REBELS:**

![Robots](/img/DUCTF_robots_4.png){: .center-block :}

**MESSAGE TO THE ROBOT DEVELOPERS:**

![Robots](/img/DUCTF_robots_5.png){: .center-block :}

**humans.txt**

![Robots](/img/DUCTF_robots_6.png){: .center-block :}

**/4dm1n_Cr3ds**

![Robots](/img/DUCTF_robots_7.png){: .center-block :}

~~~
Good day robot rebel. The admin cred is 6zMLV46JRp6kAmTs3nx5AG4WJgYeY.     
~~~

**/s3cr3t_p4th/robot_fl4g.txt**

![Robots](/img/DUCTF_robots_8.png){: .center-block :}

Dans le code source des pages de blog on trouve

![Robots](/img/DUCTF_robots_9.png){: .center-block :}

01101000 01110101 01101101 01100101 01101110 00101110 01110100 01111000 01110100

== humen.txt

**/humen.txt**

![Robots](/img/DUCTF_robots_10.png){: .center-block :}

**/Bender**

![Robots](/img/DUCTF_robots_11.png){: .center-block :}

On télécharge l'image pour l'analyser

![Robots](/img/DUCTF_robots_12.png){: .center-block :}

01100001 01100100 01101101 01101001 01101110 00111010 01010100 01101000 01101001 01110011 00101101 01001001 01110011 00101101 01010100 01101000 01100101 00101101 01000001 01100100 01101101 01101001 01101110 00101101 01010000 01100001 01110011 01110011 01110111 01101111 01110010 01100100 00101101 01011000 01000100 00100001

== admin:This-Is-The-Admin-Password-XD!

On peut se loguer en tant qu'admin avec ce mdp

![Robots](/img/DUCTF_robots_13.png){: .center-block :}

On essaye plusieurs payload de 'command injection' sans succès :( 

**Ref:** 

- [PayloadsAllTheThings](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Command%20Injection)
- [HackTricks](https://book.hacktricks.xyz/pentesting-web/command-injection)

**Réponse:**

À priori il suffisait de lancer: {{ get_file("/fl4g.txt") }} ![Robots](/img/DUCTF_robots_14.png)

:(

# Misc

## Twitter

![Twitter](/img/DUCTF_twitter_1.png){: .center-block :}

Compte twitter: [https://twitter.com/downunderctf](https://twitter.com/downunderctf)

On trouve:

![Twitter](/img/DUCTF_twitter_2.png){: .center-block :}

On décode le base64: 

`DUCTF{https://www.youtube.com/watch?v=XfR9iY5y94s}`

## Discord

![Discord](/img/DUCTF_discord_1.png){: .center-block :}

[https://downunderctf.com/rules/](https://downunderctf.com/rules/) en bas il y a un lien vers un Discord

![Discord](/img/DUCTF_discord_2.png){: .center-block :}

En haut on trouve un lien https://duc.tf/flag En cliquant sur ce lien on est redirigé vers https://www.youtube.com/watch?v=dQw4w9WgXcQ

`DUCTF{https://www.youtube.com/watch?v=dQw4w9WgXcQ}`

## Welcome

![Welcome](/img/DUCTF_welcome_1.png){: .center-block :}

On se connecte et on se retrouve avec l'écran suivant qui arrête pas de bouger et de changer de couleur !!! ÇA FAIT MAL AUX YEUX !!! EPILEPSY WARNING !!!

On prend un screenshot pour pouvoir mieux lire ce qui est écrit

![Welcome](/img/DUCTF_welcome_2.png){: .center-block :}

On voit à la huitième ligne en partant du haut `DUCTF{w3lc0m3_t0_DUCTF_h4v3_fun!}`

## Home Runs - 100 points - beginner

~~~
$echo 'RFVDVEZ7MTZfaDBtM19ydW41X20zNG41X3J1bm4xbjZfcDQ1N182NF9iNDUzNX0=' | base64 -d
DUCTF{16_h0m3_run5_m34n5_runn1n6_p457_64_b4535}
~~~

## In a pickle - 200 - easy

![Pickle](/img/DUCTF_pickle_1.png){: .center-block :}

~~~
Author: n00bmaster
We managed to intercept communication between und3rm4t3r and his  hacker friends. However it is obfuscated using something. We just can't  figure out what it is. Maybe you can help us find the flag?
~~~

**data:**

~~~
(dp0
I1
S'D'
p1
sI2
S'UCTF'
p2
sI3
S'{'
p3
sI4
I112
sI5
I49
sI6
I99
sI7
I107
sI8
I108
sI9
I51
sI10
I95
sI11
I121
sI12
I48
sI13
I117
sI14
I82
sI15
I95
sI16
I109
sI17
I51
sI18
I53
sI19
I53
sI20
I52
sI21
I103
sI22
I51
sI23
S'}'
p4
sI24
S"I know that the intelligence agency's are onto me so now i'm using ways to evade them: I am just glad that you know how to use pickle. Anyway the flag is "
p5
s.
~~~

On se réfère à cet [article](https://stackoverflow.com/questions/7501947/understanding-pickling-in-python) pour lire data

~~~
$cp data data.pkl
~~~

script readpickle.py:

~~~
root@Host-001:~/Bureau/OTA/DownUnder# cat readpickle.py 
import pprint, pickle

pkl_file = open('data.pkl', 'rb')

data1 = pickle.load(pkl_file)
pprint.pprint(data1)

data2 = pickle.load(pkl_file)
pprint.pprint(data2)

pkl_file.close()
~~~

**Résultat:**

![Pickle](/img/DUCTF_pickle_2.png){: .center-block :}

Encodé en ASCII. Ref: [http://www.asciitable.com/](http://www.asciitable.com/)

`DUCTF{p1ckl3_y0uR_m3554g3}` 

# Survey

![Survey](/img/DUCTF_survey_1.png){: .center-block :}

Just complete the survey

![Survey](/img/DUCTF_survey_2.png){: .center-block :}

**Poursuivez avec :** 

[- CSAW CTF Quals 2020 - Write-ups](https://0xss0rz.github.io/2020-09-14-CSAW-CTF-Quals-2020/)

[- Pwnable.kr - Write-ups](https://0xss0rz.github.io/2020-08-04-HTB-Write-Up/)

**Facilitez vos recherches avec mon [GitBook](https://0xss0rz.gitbook.io/0xss0rz/)**

[![CC-BY](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by.svg)](https://creativecommons.org/licenses/by/4.0/)

This work is licensed under a [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).
