---
layout: post
title: PicoCTF 2018 - General Skills
subtitle: PicoCTF 2018 - General Skills - Write-Ups 
gh-repo: 0xSs0rZ/0xSs0rZ.github.io
gh-badge: [star]
tags: [CTF, picoCTF, General Skills, Write-Up, Commandes, Réseautique]
comments: false
---

**Le terminal est votre meilleur allié. Voici quelques solutions pour la catégorie _"General Skills"_ de picoCTF.**

Avant de commencer, si vous ne connaissez pas encore les commandes essentielles en ligne de commande, ça vaut la peine de jeter un coup d'oeil à cette article: [Commandes essentielles](https://0xss0rz.github.io/2019-08-19-commandes-essentieles/)

picoCTF 2018: [https://2018game.picoctf.com/](https://2018game.picoctf.com/)

## General Warmup 1

{: .box-note}
If I told you your grade was 0x41 in hexadecimal, what would it be in ASCII? 

**Solution:** [https://www.rapidtables.com/convert/number/hex-to-ascii.html](https://www.rapidtables.com/convert/number/hex-to-ascii.html)

## General Warmup 2

{: .box-note}
Can you convert the number 27 (base 10) to binary (base 2)? 

**Solution:** [https://www.rapidtables.com/convert/number/decimal-to-binary.html](https://www.rapidtables.com/convert/number/decimal-to-binary.html)

## General Warmup 3

{: .box-note}
What is 0x3D (base 16) in decimal (base 10). 

**Solution: [https://www.rapidtables.com/convert/number/index.html](https://www.rapidtables.com/convert/number/index.html)

##  Resources

{: .box-note}
We put together a bunch of resources to help you out on our website! If you go over there, you might even find a flag! https://picoctf.com/resources

**Solution:** Clic droit - Code source

~~~
<p><br /> 
<br /> 
Thanks for reading the resources page! Here’s a flag for your time: picoCTF{quelquechose}</p>
~~~

## grep 1

{: .box-note}
Can you find the flag in file? This would be really obnoxious to look through by hand, see if you can find a faster way. You can also find the file in /problems/grep-1_3_8d9cff3d178c231ab735dfef3267a1c2 on the shell server. 

**Solution:**

~~~
┌─[xor@parrot]─[~/Téléchargements]
└──╼ $strings file | grep picoCTF
picoCTF{quelquechose}
~~~

## net cat 

{: .box-note}
Using netcat (nc) will be a necessity throughout your adventure. Can you connect to 2018shell.picoctf.com at port 10854 to get the flag? 

**Solution:**

~~~
┌─[xor@parrot]─[~/Téléchargements]
└──╼ $nc -h
[v1.10-41.1]
connect to somewhere:	nc [-options] hostname port[s] [ports] ... 
listen for inbound:	nc -l -p port [-options] [hostname] [port]
(...)
┌─[✗]─[xor@parrot]─[~/Téléchargements]
└──╼ $nc 2018shell.picoctf.com 10854
That wasn't so hard was it?
picoCTF{quelquechose}
~~~

## strings

{: .box-note}
Can you find the flag in this file without actually running it? You can also find the file in /problems/strings_3_1dbaafa1f8f0556872cad33e16bc8dc7 on the shell server.

**Solution:**

~~~
┌─[xor@parrot]─[~/Téléchargements]
└──╼ $strings strings | grep picoCTF
picoCTF{quelques chose}
~~~

## pipe

{: .box-note}
During your adventure, you will likely encounter a situation where you need to process data that you receive over the network rather than through a file. Can you find a way to save the output from this program and search for the flag? Connect with 2018shell.picoctf.com 37542. 

**Solution:**

~~~
┌─[✗]─[xor@parrot]─[~/Téléchargements]
└──╼ $nc 2018shell.picoctf.com 37542 | grep picoCTF
picoCTF{quelquechose}
~~~

## grep 2

{: .box-note}
This one is a little bit harder. Can you find the flag in /problems/grep-2_3_826f886f547acb8a9c3fccb030e8168d/files on the shell server? Remember, grep is your friend. 

**Solution:**

~~~
0xSs0rZ@pico-2018-shell:~$ cd /problems/grep-2_3_826f886f547acb8a9c3fccb030e8168d/files                        
0xSs0rZ@pico-2018-shell:/problems/grep-2_3_826f886f547acb8a9c3fccb030e8168d/files$ ls -la                      
total 48                                                                                                       
drwxr-xr-x 12 root root 4096 Mar 25 19:18 .
drwxr-xr-x  3 root root 4096 Mar 25 19:18 ..
drwxr-xr-x  2 root root 4096 Mar 25 19:18 files0
drwxr-xr-x  2 root root 4096 Mar 25 19:18 files1
drwxr-xr-x  2 root root 4096 Mar 25 19:18 files2
drwxr-xr-x  2 root root 4096 Mar 25 19:18 files3
drwxr-xr-x  2 root root 4096 Mar 25 19:18 files4
drwxr-xr-x  2 root root 4096 Mar 25 19:18 files5
drwxr-xr-x  2 root root 4096 Mar 25 19:18 files6
drwxr-xr-x  2 root root 4096 Mar 25 19:18 files7
drwxr-xr-x  2 root root 4096 Mar 25 19:18 files8
drwxr-xr-x  2 root root 4096 Mar 25 19:18 files9
0xSs0rZ@pico-2018-shell:/problems/grep-2_3_826f886f547acb8a9c3fccb030e8168d/files$ grep -Ril "picoCTF"         
files6/file16
0xSs0rZ@pico-2018-shell:/problems/grep-2_3_826f886f547acb8a9c3fccb030e8168d/files$ cat files6/file16 | grep pic
oCTF
picoCTF{quelquechose}
~~~

## Aca-Shell-A

{: .box-note}
It's never a bad idea to brush up on those linux skills or even learn some new ones before you set off on this adventure! Connect with nc 2018shell.picoctf.com 6903. 

**Solution:**

~~~
$nc 2018shell.picoctf.com 6903
Sweet! We have gotten access into the system but we aren't root.
It's some sort of restricted shell! I can't see what you are typing
but I can see your output. I'll be here to help you along.
If you need help, type "echo 'Help Me!'" and I'll see what I can do
There is not much time left!
~/$ ls
blackmail
executables
passwords
photos
secret
~/$ cd secret
Now we are cookin'! Take a look around there and tell me what you find!
~/secret$ ls
intel_1
intel_2
intel_3
intel_4
intel_5
profile_ahqueith5aekongieP4ahzugi
profile_ahShaighaxahMooshuP1johgo
profile_aik4hah9ilie9foru0Phoaph0
profile_AipieG5Ua9aewei5ieSoh7aph
profile_bah9Ech9oa4xaicohphahfaiG
profile_ie7sheiP7su2At2ahw6iRikoe
profile_of0Nee4laith8odaeLachoonu
profile_poh9eij4Choophaweiwev6eev
profile_poo3ipohGohThi9Cohverai7e
profile_Xei2uu5suwangohceedaifohs
Sabatoge them! Get rid of all their intel files!
~/secret$ rm intel*
Nice! Once they are all gone, I think I can drop you a file of an exploit!
Just type "echo 'Drop it in!' " and we can give it a whirl!
~/secret$ echo 'Drop it in!
Drop it in!
I placed a file in the executables folder as it looks like the only place we can execute from!
Run the script I wrote to have a little more impact on the system!
~/secret$ cd ..
~/$ cd executables
~/executables$ ls
dontLookHere
~/executables$ ./dontLookHere
 7011 8828 cc1a c30e f0d3 35a7 d821 9c7c 9312 4af1 5655 5b70 ec4a 8c79 0d6f 9912 d309 a65c 89a5 9dea b9f6 f893 8101 7089 a169
 .....
 .....
 7c62 624e ff26 0655 145e e9b7 9a98 7947 70f2 25af a8a4 2976 58ea 801c 2ccb 4e7f 8f0c a16a 0d5a 594f 875a ad2c 4f33 14aa 6dce
Looking through the text above, I think I have found the password. I am just having trouble with a username.
Oh drats! They are onto us! We could get kicked out soon!
Quick! Print the username to the screen so we can close are backdoor and log into the account directly!
You have to find another way other than echo!
~/executables$ whoami
l33th4x0r
Perfect! One second!
Okay, I think I have got what we are looking for. I just need to to copy the file to a place we can read.
Try copying the file called TopSecret in tmp directory into the passwords folder.
~/executables$ cp /tmp/TopSecret passwords
Server shutdown in 10 seconds...
Quick! go read the file before we lose our connection!
~/executables$ cd ..
~/$ cd passwords
~/passwords$ ls
TopSecret
~/passwords$ cat TopSecret
Major General John M. Schofield's graduation address to the graduating class of 1879 at West Point is as follows: The discipline which makes the soldiers of a free country reliable in battle is not to be gained by harsh or tyrannical treatment.On the contrary, such treatment is far more likely to destroy than to make an army.It is possible to impart instruction and give commands in such a manner and such a tone of voice as to inspire in the soldier no feeling butan intense desire to obey, while the opposite manner and tone of voice cannot fail to excite strong resentment and a desire to disobey.The one mode or other of dealing with subordinates springs from a corresponding spirit in the breast of the commander.He who feels the respect which is due to others, cannot fail to inspire in them respect for himself, while he who feels,and hence manifests disrespect towards others, especially his subordinates, cannot fail to inspire hatred against himself.
picoCTF{quelquechose}
~~~

## environ

{: .box-note}
Sometimes you have to configure environment variables before executing a program. Can you find the flag we've hidden in an environment variable on the shell server? 

_Ref:_ [https://www.digitalocean.com/community/tutorials/how-to-read-and-set-environmental-and-shell-variables-on-a-linux-vps](https://www.digitalocean.com/community/tutorials/how-to-read-and-set-environmental-and-shell-variables-on-a-linux-vps)

**Solution:**

~~~
0xSs0rZ@pico-2018-shell:~$ printenv                                                                            
SECRET_FLAG=picoCTF{eNv1r0nM3nT_v4r14Bl3_fL4g_3758492}                                                         
FLAG=Finding the flag wont be that easy...                                                                     
TERM=xterm                                                                                                     
SHELL=/bin/bash                                                                                                
SSH_CLIENT=127.0.0.1 50576 22                                                                                  
SSH_TTY=/dev/pts/167                                                                                           
USER=0xSs0rZ                                                                                                   
LS_COLORS=rs=0:di=01;34:ln=01;36:mh=00:pi=40;33:so=01;35:do=01;35:bd=40;33;01:cd=40;33;01:or=40;31;01:mi=00:su=
37;41:sg=30;43:ca=30;41:tw=30;42:ow=34;42:st=37;44:ex=01;32:*.tar=01;31:*.tgz=01;31:*.arc=01;31:*.arj=01;31:*.t
az=01;31:*.lha=01;31:*.lz4=01;31:*.lzh=01;31:*.lzma=01;31:*.tlz=01;31:*.txz=01;31:*.tzo=01;31:*.t7z=01;31:*.zip
=01;31:*.z=01;31:*.Z=01;31:*.dz=01;31:*.gz=01;31:*.lrz=01;31:*.lz=01;31:*.lzo=01;31:*.xz=01;31:*.bz2=01;31:*.bz
=01;31:*.tbz=01;31:*.tbz2=01;31:*.tz=01;31:*.deb=01;31:*.rpm=01;31:*.jar=01;31:*.war=01;31:*.ear=01;31:*.sar=01
;31:*.rar=01;31:*.alz=01;31:*.ace=01;31:*.zoo=01;31:*.cpio=01;31:*.7z=01;31:*.rz=01;31:*.cab=01;31:*.jpg=01;35:
*.jpeg=01;35:*.gif=01;35:*.bmp=01;35:*.pbm=01;35:*.pgm=01;35:*.ppm=01;35:*.tga=01;35:*.xbm=01;35:*.xpm=01;35:*.
tif=01;35:*.tiff=01;35:*.png=01;35:*.svg=01;35:*.svgz=01;35:*.mng=01;35:*.pcx=01;35:*.mov=01;35:*.mpg=01;35:*.m
peg=01;35:*.m2v=01;35:*.mkv=01;35:*.webm=01;35:*.ogm=01;35:*.mp4=01;35:*.m4v=01;35:*.mp4v=01;35:*.vob=01;35:*.q
t=01;35:*.nuv=01;35:*.wmv=01;35:*.asf=01;35:*.rm=01;35:*.rmvb=01;35:*.flc=01;35:*.avi=01;35:*.fli=01;35:*.flv=0
1;35:*.gl=01;35:*.dl=01;35:*.xcf=01;35:*.xwd=01;35:*.yuv=01;35:*.cgm=01;35:*.emf=01;35:*.ogv=01;35:*.ogx=01;35:
*.aac=00;36:*.au=00;36:*.flac=00;36:*.m4a=00;36:*.mid=00;36:*.midi=00;36:*.mka=00;36:*.mp3=00;36:*.mpc=00;36:*.
ogg=00;36:*.ra=00;36:*.wav=00;36:*.oga=00;36:*.opus=00;36:*.spx=00;36:*.xspf=00;36:                            
MAIL=/var/mail/0xSs0rZ                                                                                         
PATH=/home/0xSs0rZ/bin:/home/0xSs0rZ/.local/bin:/home/0xSs0rZ/:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bi
n:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin                                                             
PWD=/home/0xSs0rZ                                                                                              
LANG=en_US.UTF-8                                                                                               
SHLVL=1                                                                                                        
HOME=/home/0xSs0rZ                                                                                             
PICOCTF_FLAG=Nice try... Keep looking!                                                                         
LOGNAME=0xSs0rZ                                                                                                
XDG_DATA_DIRS=/usr/local/share:/usr/share:/var/lib/snapd/desktop                                               
SSH_CONNECTION=127.0.0.1 50576 127.0.0.1 22                                                                    
LESSOPEN=| /usr/bin/lesspipe %s                                                                                
LESSCLOSE=/usr/bin/lesspipe %s %s                                                                              
_=/usr/bin/printenv                                                                                            
0xSs0rZ@pico-2018-shell:~$                                                                                     
~~~

## ssh-keyz

{: .box-note}
As nice as it is to use our webshell, sometimes its helpful to connect directly to our machine. To do so, please add your own public key to ~/.ssh/authorized_keys, using the webshell. The flag is in the ssh banner which will be displayed when you login remotely with ssh to with your username. 

_Ref_: [https://www.maketecheasier.com/generate-public-private-ssh-key/](https://www.maketecheasier.com/generate-public-private-ssh-key/)

**Solution:**

~~~
0xSs0rZ@pico-2018-shell:~$ ssh-keygen -t rsa                                                                   
Generating public/private rsa key pair.                                                                        
Enter file in which to save the key (/home/0xSs0rZ/.ssh/id_rsa):                                               
Enter passphrase (empty for no passphrase):                                                                    
Enter same passphrase again:                                                                                   
Your identification has been saved in /home/0xSs0rZ/.ssh/id_rsa.                                               
Your public key has been saved in /home/0xSs0rZ/.ssh/id_rsa.pub.                                               
The key fingerprint is:                                                                                        
SHA256:YPsf7PTkrxc7owo8NkyxQVnfL3ZOS3xf+YDmJNVcMR0 0xSs0rZ@pico-2018-shell                                     
The key's randomart image is:                                                                                  
+---[RSA 2048]----+                                                                                            
|        .o.    E=|                                                                                            
|       ..  . + .o|                                                                                            
|      o o   o +  |                                                                                            
|     . o + . ....|                                                                                            
|      . S . + ++*|                                                                                            
|       = . = .o**|                                                                                            
|        O + o  ++|                                                                                            
|       . B =  =  |                                                                                            
|          +.==.o |                                                                                            
+----[SHA256]-----+                                                                                            
0xSs0rZ@pico-2018-shell:~$ cd /home/0xSs0rZ/.ssh                                                               
0xSs0rZ@pico-2018-shell:~/.ssh$                                                                                
0xSs0rZ@pico-2018-shell:~/.ssh$  ls                                                                            
id_rsa  id_rsa.pub                                                                                             
0xSs0rZ@pico-2018-shell:~/.ssh$ cp id_rsa.pub ~/.ssh/authorized_keys                                           
0xSs0rZ@pico-2018-shell:~/.ssh$ ssh -i id_rsa 0xSs0rZ@localhost                                                
The authenticity of host 'localhost (127.0.0.1)' can't be established.                                         
ECDSA key fingerprint is SHA256:1/2OUR2IggrhZwLysFuJlUZ169yf1BFVeTIDW8Fo5XU.                                   
Are you sure you want to continue connecting (yes/no)? yes                                                     
Warning: Permanently added 'localhost' (ECDSA) to the list of known hosts.                                     
picoCTF{quelquechose}  
~~~                                                                          

## what base is this?

{: .box-note}
To be successful on your mission, you must be able read data represented in different ways, such as hexadecimal or binary. Can you get the flag from this program to prove you are ready? Connect with nc 2018shell.picoctf.com 15853.

**Tools:**

- [https://www.asciitohex.com/](https://www.asciitohex.com/)
- [https://onlineasciitools.com/convert-octal-to-ascii](https://onlineasciitools.com/convert-octal-to-ascii)

**Solution:**

~~~
┌─[xor@parrot]─[~/Téléchargements]
└──╼ $nc 2018shell.picoctf.com 15853
We are going to start at the very beginning and make sure you understand how data is stored.
bottle
Please give me the 01100010 01101111 01110100 01110100 01101100 01100101 as a word.
To make things interesting, you have 30 seconds.
Input:
bottle
Please give me the 726f626f74 as a word.
Input:
robot
Please give me the  163 164 151 164 143 150 as a word.
Input:
stitch
You got it! You're super quick!
Flag: picoCTF{quelquechose}
~~~

## you can't see me

{: .box-note}
'...reading transmission... Y.O.U. .C.A.N.'.T. .S.E.E. .M.E. ...transmission ended...' Maybe something lies in /problems/you-can-t-see-me_4_8bd1412e56df49a3c3757ebeb7ead77f.

**Solution:**

~~~
0xSs0rZ@pico-2018-shell:/problems/you-can-t-see-me_4_8bd1412e56df49a3c3757ebeb7ead77f$ cat .                   
cat: .: Is a directory                                                                                         
0xSs0rZ@pico-2018-shell:/problems/you-can-t-see-me_4_8bd1412e56df49a3c3757ebeb7ead77f$ cat .*                  
cat: .: Is a directory                                                                                         
picoCTF{j0hn_c3na_paparapaaaaaaa_paparapaaaaaa_22f627d9}                                                       
cat: ..: Permission denied                                                                                     
0xSs0rZ@pico-2018-shell:/problems/you-can-t-see-me_4_8bd1412e56df49a3c3757ebeb7ead77f$                         
~~~

**Poursuivez avec: [PicoCTF 2018 - Forensics](https://0xss0rz.github.io/2019-08-21-picoCTF-Forensics-Write-Ups/)**

**Pour continuer à tester ses connaissances en ligne de commandes et en réseautique: [OverTheWire - Bandit 1](https://0xss0rz.github.io/2019-08-20-OverTheWire-Bandit-1-Write-Ups/)**


[![CC-BY](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by.svg)](https://creativecommons.org/licenses/by/4.0/)

This work is licensed under a [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).


