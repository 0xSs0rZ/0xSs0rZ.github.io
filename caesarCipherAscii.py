# coding=utf-8

# caesar cipher 2 - picoCTF2018
# Inspiré de: https://www.tutorialspoint.com/cryptography_with_python/cryptography_with_python_caesar_cipher

message = 'PICO#4&[C!ESA2?#I0H%R3?JU34?A2%N4?S%C5R%]' #encrypted message

characters = list(map(chr, range(32,126)))
LETTERS = ''.join(characters)
#LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

for key in range(len(LETTERS)):
   translated = ''
   for symbol in message:
      if symbol in LETTERS:
         num = LETTERS.find(symbol)
         num = num - key
         if num < 0:
            num = num + len(LETTERS)
         translated = translated + LETTERS[num]
      else:
         translated = translated + symbol
   print('key #%s: %s' % (key, translated))
