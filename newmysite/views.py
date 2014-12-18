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
    errors = []
    if request.method == 'POST':
        form = encryptForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            
            data_puth = 'newmysite/media/' + request.FILES['data_file'].name
            img_puth = 'newmysite/media/' + request.FILES['img_file'].name
                     
            handle_uploaded_file(request.FILES['data_file'], data_puth)
            handle_uploaded_file(request.FILES['img_file'], img_puth)
                                 
            data = read_from_file(data_puth)
            vigenere_key = request.POST['vigenere_key']
            aes_key = request.POST['aes_key']
            
            if len(aes_key) != 16:
                errors.append('Неверная длина ключа для шифрования AES!')
                return render_to_response('encrypt.html', {'form': form, 'errors': errors})
                
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
    errors = []
    if request.method == 'POST':
        form = decryptForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data
            
            img_puth = 'newmysite/media/' + request.FILES['img_file'].name
            
            vigenere_key = request.POST['vigenere_key']
            aes_key = request.POST['aes_key']
            handle_uploaded_file(request.FILES['img_file'], img_puth)
        
            if len(aes_key) != 16:
                errors.append('Неверная длина ключа для шифрования AES!')
                return render_to_response('dencrypt.html', {'form': form, 'errors': errors})
            
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
