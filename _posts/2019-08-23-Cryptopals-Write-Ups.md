---
layout: post
title: Cryptopals - Set 1
subtitle: Challenges de cryptographie - Write-Ups 
gh-repo: 0xSs0rZ/0xSs0rZ.github.io
gh-badge: [star]
tags: [Cryptopals, Cryptographie, Write-Up, solutions, Python]
comments: false
---

**Vous vous intéressez à la cryptographie ? Cryptopals est l'endroit pour tester vos connaissances.**

Cryptopals: [https://cryptopals.com/](https://cryptopals.com/)

## Challenge 1 - Convert hex to base64

The string:

    49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d

Should produce:

    SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t

So go ahead and make that happen. You'll need to use this code for the rest of the exercises. 

**Solution:**

~~~
#1. En décomposant les étapes
# Hex to Ascii
┌─[xor@parrot]─[~]
└──╼ $echo -n 49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d | xxd -r -p
I'm killing your brain like a poisonous mushroom
#Ascii to base64
┌─[✗]─[xor@parrot]─[~]
└──╼ $echo -n "I'm killing your brain like a poisonous mushroom" | base64
SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t
#2. En une commande
┌─[xor@parrot]─[~]
└──╼ $echo -n 49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d | xxd -r -p | base64
SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t
~~~

## Challenge 2 - Fixed XOR

Write a function that takes two equal-length buffers and produces their XOR combination.

If your function works properly, then when you feed it the string:

    1c0111001f010100061a024b53535009181c

... after hex decoding, and when XOR'd against:

    686974207468652062756c6c277320657965

... should produce:

    746865206b696420646f6e277420706c6179
    
**Solution:**

~~~
┌─[xor@parrot]─[~]
└──╼ $python
Python 2.7.16+ (default, Jul  8 2019, 09:45:29) 
[GCC 8.3.0] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> s1 = "1c0111001f010100061a024b53535009181c"
>>> s2 = "686974207468652062756c6c277320657965"
>>> xor = hex(int(s1, 16) ^ int(s2, 16))
>>> print xor
0x746865206b696420646f6e277420706c6179L
>>> 
~~~

Source: [https://stackoverflow.com/questions/17390050/xoring-two-hex-strings-in-python-which-method-is-correct](https://stackoverflow.com/questions/17390050/xoring-two-hex-strings-in-python-which-method-is-correct)

## Challenge 3 - Single-byte XOR cipher

The hex encoded string:

    1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736

... has been XOR'd against a single character. Find the key, decrypt the message.

You can do this by hand. But don't: write code to do it for you.

How? Devise some method for "scoring" a piece of English plaintext. Character frequency is a good metric. Evaluate each output and choose the one with the best score. 

**Solution:**

Script singlebytexor.py:

{% highlight javascript linenos %}
# Source: https://laconicwolf.com/2018/05/29/cryptopals-challenge-3-single-byte-xor-cipher-in-python/

def get_english_score(input_bytes):
    """Compares each input byte to a character frequency 
    chart and returns the score of a message based on the
    relative frequency the characters occur in the English
    language
    """

    # From https://en.wikipedia.org/wiki/Letter_frequency
    # with the exception of ' ', which I estimated.
    character_frequencies = {
        'a': .08167, 'b': .01492, 'c': .02782, 'd': .04253,
        'e': .12702, 'f': .02228, 'g': .02015, 'h': .06094,
        'i': .06094, 'j': .00153, 'k': .00772, 'l': .04025,
        'm': .02406, 'n': .06749, 'o': .07507, 'p': .01929,
        'q': .00095, 'r': .05987, 's': .06327, 't': .09056,
        'u': .02758, 'v': .00978, 'w': .02360, 'x': .00150,
        'y': .01974, 'z': .00074, ' ': .13000
    }
    return sum([character_frequencies.get(chr(byte), 0) for byte in input_bytes.lower()])


def single_char_xor(input_bytes, char_value):
    """Returns the result of each byte being XOR'd with a single value.
    """
    output_bytes = b''
    for byte in input_bytes:
        output_bytes += bytes([byte ^ char_value])
    return output_bytes


def main():
    hexstring = '1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'
    ciphertext = bytes.fromhex(hexstring)
    potential_messages = []
    for key_value in range(256):
        message = single_char_xor(ciphertext, key_value)
        score = get_english_score(message)
        data = {
            'message': message,
            'score': score,
            'key': key_value
            }
        potential_messages.append(data)
    best_score = sorted(potential_messages, key=lambda x: x['score'], reverse=True)[0]
    for item in best_score:
        print("{}: {}".format(item.title(), best_score[item]))

if __name__ == '__main__':
    main()
% endhighlight %}

Résultat:

~~~
┌─[xor@parrot]─[~]
└──╼ $python3 singlebytexor.py 
Message: b"Cooking MC's like a pound of bacon"
Score: 2.14329
Key: 88
~~~

**Poursuivez avec: [PicoCTF 2018 - Cryptography](https://0xss0rz.github.io/2019-08-22-picoCTF-Cryptography-Write-Ups/)**

[![CC-BY](https://mirrors.creativecommons.org/presskit/buttons/88x31/svg/by.svg)](https://creativecommons.org/licenses/by/4.0/)

This work is licensed under a [Creative Commons Attribution 4.0 International License](https://creativecommons.org/licenses/by/4.0/).


