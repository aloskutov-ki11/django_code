# -*- coding: utf-8 -*-
import Image, ImageDraw


def changeEndBits(byte, bits):
    byte = ((byte >> 2) << 2) + int(bits, 2)
    return byte

def getEndBits(byte):
    byte = bin(byte)[2:].rjust(8, '0')
    return byte[6:8]

#сокрытие сообщения внутри картинки  
def hide(img, data):                     # два пикселя берем для кодирования одного байта
                                         # для нагрузки будем использовать первые два байта пикселя (байты, отвечающие за красный и зеленый цвет (RGB)) 
                                         # третий байт будем использовать в качестве указателя окончания сообщения    
    imgSize = img.size
    dataSize = len(data)
   
    if dataSize > (imgSize[0]*imgSize[1])/2:
        print "Слишком большой размер текста для данного изображения"
        return None
    
    w = 0
    h = 0
    for byte in data:
        block = bin(ord(byte))[2:].rjust(8, '0')        #8 бит, то есть 1 байт
       
        if w == imgSize[0]:
            w = 0
            h += 1
        
        for i in range(2):
            w += i
            if w == imgSize[0]:
                w = 0
                h += 1
                
            pixel = img.getpixel((w, h))
       
            f_pix = changeEndBits(int(pixel[0]), block[4*i:4*i+2])
            s_pix = changeEndBits(int(pixel[1]), block[4*i+2:4*i+4])
        
            #Обнуление последних двух битов третьего байта пикселя, которые указывают на то, что сообщение еще не закончилось
            t_pix  = (int(pixel[2]) >> 2) << 2
 
            img.putpixel((w, h), (f_pix, s_pix, t_pix))
        w += 1
    
    #записываем в последние два бита третьего байта пикселя 11 для того, чтобы можно было увидеть окончание сообщения
    f_pixel = img.getpixel((w, h))
    f_t  = ((int(f_pixel[2]) >> 2) << 2) + 3
    img.putpixel((w, h), (int(f_pixel[0]), int(f_pixel[1]), f_t))
    
    return img
 
 
# извлечение скрытого сообщения из картинки
def extract(img):
    imgSize = img.size
    data = ''
    byte = ''
    
    w = 0
    h = 0
    
    f_t = ''
    while 1:       
        if w == imgSize[0]:
            w = 0
            h += 1
        
        for i in range(2):
            w += i
            if w == imgSize[0]:
                w = 0
                h += 1
                
            pixel = img.getpixel((w, h))
            
            f_bits = getEndBits(int(pixel[0]))
            s_bits = getEndBits(int(pixel[1]))
            t_bits = getEndBits(int(pixel[2]))          
            
            if t_bits != '11':
                byte += f_bits + s_bits
            else:
                return data
           
        data += ''.join(chr(int(byte,2)))  
        byte = ''  
        w += 1

def lsb_method(data, img, mode):

    if (mode == '-h'):
            img = hide(img, data)
            return img
            
    if (mode == '-e'):
        data = extract(img)
        return data
    
    
    
    
    
    
    
    
