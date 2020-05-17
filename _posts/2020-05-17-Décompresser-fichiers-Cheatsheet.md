---
layout: post
title: Cheatsheet - Décompresser des fichiers
subtitle: RAR, ZIP, TAR, etc 
gh-repo: 0xSs0rZ/0xSs0rZ.github.io
gh-badge: [star]
tags: [Cheatsheet, archive, décompression, extraction, Rar, Tar, Zip, Gzip, Bz2, Xz,  Commandes, Linux]
comments: false
---

**Une petite synthèse pour décompresser/extraire des fichiers sous Linux**

# Zip

~~~
unzip myzip.zip
~~~

# Rar

~~~
unrar x archive.rar
~~~

# Gunzip

~~~
gzip -d filename.gz
gunzip -k filename.gz   //-k keep (don't delete) original file .gz
zcat filename.gz > filename
~~~

# Bzip2

~~~
bzip2 -d filename.bz2 // This command will not preserve original archive file
bzip2 -dk filename.bz2 // To preserve the original file
~~~

# Tar

~~~
tar xvf file.tar
~~~

# Tar + Gzip

~~~
tar -xzvf archive.tar.gz
~~~

# Tar + Bz2

~~~
tar -xjvf archive.tar.bz2
~~~

# Tar + Xz

~~~
tar -xJvf archive.tar.xz
~~~

[![CC-BY](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by.svg)](https://creativecommons.org/licenses/by/4.0/)

This work is licensed under a [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).

