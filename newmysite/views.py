# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.http import HttpResponseRedirect

import operator
import Image, ImageDraw

from .forms import *

from .vigenere import *
from .aes import *
from .lsb import *

def start(request):
    return render_to_response('start.html')
  
def handle_uploaded_file(f, name):
    with open(name, 'w+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
            
def read_from_file(file_puth):
    F = open(file_puth, "r")
    data = F.read()
    F.close()
    return data
            
def encrypt(request):
    if request.method == 'POST':
        form = encryptForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            
            data_puth = 'newmysite/media/' + request.FILES['data_file'].name
            vigenere_key_path = 'newmysite/media/' + request.FILES['vigenere_key'].name
            aes_key_path = 'newmysite/media/' + request.FILES['aes_key'].name
            img_puth = 'newmysite/media/' + request.FILES['img_file'].name
                     
            handle_uploaded_file(request.FILES['data_file'], data_puth)
            handle_uploaded_file(request.FILES['vigenere_key'], vigenere_key_path)
            handle_uploaded_file(request.FILES['aes_key'], aes_key_path)
            handle_uploaded_file(request.FILES['img_file'], img_puth)
                                 
            data = read_from_file(data_puth)
            vigenere_key = read_from_file(vigenere_key_path)
            aes_key = read_from_file(aes_key_path)
            
            aes_key = aes_key[0:len(aes_key)-1]
            if len(aes_key) != 16:
                return render_to_response('encrypt.html', {'form': form, 'errors': 'Неверная длина ключа для шифрования AES!'})
                
            result = vigenere_cipher(data, vigenere_key, operator.add)
            result = aes_cipher(result, aes_key, '-c')
            
            img = Image.open(img_puth)
            img.save("newmysite/static/img_before.bmp")
               
            if len(result) > (img.size[0]*img.size[1])/2:
                return render_to_response('encrypt.html', {'form': form, 'errors': 'Слишком маленькое изображение для внедрения в него такого количества данных!'})
                
            img = lsb_method(result, img, '-h')
            img.save("newmysite/static/img_after.bmp")
            
            return render_to_response('encryption_result.html',)
    else:
        form = encryptForm()

    return render_to_response('encrypt.html', {'form': form})
               
def dencrypt(request):
    if request.method == 'POST':
        form = decryptForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            
            vigenere_key_path = 'newmysite/media/' + request.FILES['vigenere_key'].name
            aes_key_path = 'newmysite/media/' + request.FILES['aes_key'].name
            img_puth = 'newmysite/media/' + request.FILES['img_file'].name
            
            handle_uploaded_file(request.FILES['vigenere_key'], vigenere_key_path)
            handle_uploaded_file(request.FILES['aes_key'], aes_key_path)
            handle_uploaded_file(request.FILES['img_file'], img_puth)
            
            vigenere_key = read_from_file(vigenere_key_path)
            aes_key = read_from_file(aes_key_path)
            
            aes_key = aes_key[0:len(aes_key)-1]
            if len(aes_key) != 16:
                return render_to_response('dencrypt.html', {'form': form, 'errors': 'Неверная длина ключа для шифрования AES!'})
            
            img = Image.open(img_puth)
            result = lsb_method('', img, '-e')

            result = aes_cipher(result, aes_key, '-d')
            result = vigenere_cipher(result, vigenere_key, operator.sub)

            outF = open("newmysite/static/decrypted", "w")
            outF.write(result)
            outF.close()
        
            return render_to_response('dencryption_result.html',)
    else:
        form = decryptForm()

    return render_to_response('dencrypt.html', {'form': form})










