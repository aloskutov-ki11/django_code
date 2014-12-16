# -*- coding: utf-8 -*-
from django import forms

class encryptForm(forms.Form):
    data_file = forms.FileField(label="Файл с исходными данными")
    vigenere_key = forms.FileField(label="Файл с ключом для шифрования Виженера")
    aes_key = forms.FileField(label="Файл с ключом для шифрования AES")
    img_file = forms.FileField(label="Изображение для метода LSB")

class decryptForm(forms.Form):
    vigenere_key = forms.FileField(label="Файл с ключом для расшифрования Виженера")
    aes_key = forms.FileField(label="Файл с ключом для расшифрования AES")
    img_file = forms.FileField(label="Изображение, содержащее сообщение")
