# -*- coding: utf-8 -*-
def vigenere_cipher(inText, key, func):
    result = ''
    index = 0
    for char in inText:
        result += chr((func(ord(char), ord(key[index])) + 256) % 256 )
        index += 1
        
        if index == len (key):
            index = 0
    return result
