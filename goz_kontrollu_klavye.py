import cv2
import numpy as np
import dlib
from math import hypot
import keyboard
from textblob import TextBlob

cap = cv2.VideoCapture(0)
board = np.zeros((500, 500), np.uint8)     #Klavyeden seçilen harflerin yazılacağı ekran 500x500 boyutunda
board[:] = 255      #Yazı kısmı beyaz renk olacak 

detector = dlib.get_frontal_face_detector()   # Dlib içindeki yüz algılama 
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# Klavye Ayarları
keyboard = np.zeros((300, 900, 3), np.uint8)  #Klavyenin sol tarafı
keys_set_1 = {0: "Q", 1: "W", 2: "E", 3: "R", 4: "T",      
              5: "Y", 6: "U", 7: "O", 8: "P", 9: "A",
              10: "S", 11: "D", 12: "F", 13: "G", 14: "H",
              15: "J",16: "K", 17: "L", 18: "I", 19: "Z",
              20: "X", 21: "C", 22: "V", 23: "B", 24: "N", 25: "M", 26: "<"}

def letter(letter_index, text, letter_light):
    # Harfler
    if letter_index == 0:           #Harflerin Yerleşimi
        x = 0
        y = 0
    elif letter_index == 1:
        x = 100
        y = 0
    elif letter_index == 2:
        x = 200
        y = 0
    elif letter_index == 3:
        x = 300
        y = 0
    elif letter_index == 4:
        x = 400
        y = 0
    elif letter_index == 5:
        x = 500
        y = 0
    elif letter_index == 6:
        x = 600
        y = 0
    elif letter_index == 7:
        x = 700
        y = 0
    elif letter_index == 8:
        x = 800
        y = 0
    elif letter_index == 9:
        x = 0 
        y = 100
    elif letter_index == 10:
        x = 100
        y = 100
    elif letter_index == 11:
        x = 200
        y = 100
    elif letter_index == 12:
        x = 300
        y = 100
    elif letter_index == 13:
        x = 400
        y = 100
    elif letter_index == 14:
        x = 500
        y = 100
    elif letter_index == 15:
        x = 600
        y = 100
    elif letter_index == 16:
        x = 700
        y = 100
    elif letter_index == 17:
        x = 800
        y = 100
    elif letter_index == 18:
        x = 0
        y = 200
    elif letter_index == 19:
        x = 100
        y = 200
    elif letter_index == 20:
        x = 200
        y = 200
    elif letter_index == 21:
        x = 300
        y = 200
    elif letter_index == 22:
        x = 400
        y = 200
    elif letter_index == 23:
        x = 500
        y = 200
    elif letter_index == 24:
        x = 600
        y = 200
    elif letter_index == 25:
        x = 700
        y = 200
    elif letter_index == 26:
        x = 800
        y = 200

    width = 100
    height = 100
    th = 3 # Kalınlık
    if letter_light is True:     #letter_light true ise klavye ekranı beyaz
        cv2.rectangle(keyboard, (x + th, y + th), (x + width - th, y + height - th), (255, 255, 255), -1)
    else:    #klavye ekranı siyah
        cv2.rectangle(keyboard, (x + th, y + th), (x + width - th, y + height - th), (255, 0, 0), th)

    # Yazı Ayarları
    font_letter = cv2.FONT_HERSHEY_PLAIN
    font_scale = 8
    font_th = 4
    text_size = cv2.getTextSize(text, font_letter, font_scale, font_th)[0]
    width_text, height_text = text_size[0], text_size[1]
    text_x = int((width - width_text) / 2) + x    #Harfleri ortalamak için
    text_y = int((height + height_text) / 2) + y
    cv2.putText(keyboard, text, (text_x, text_y), font_letter, font_scale, (255, 0, 0), font_th)

def orta_nokta_bul(p1 ,p2):  # Verilen noktaların ortasını bulan fonksiyon
    return int((p1.x + p2.x)/2), int((p1.y + p2.y)/2) #piksel ondalık olamayacağı için int 

font = cv2.FONT_HERSHEY_PLAIN

def kapalilik_orani_bul(goz_noktalari, facial_landmarks): #Göz kapalılık oranını bulan fonksiyon. ilk parametre landmark noktalarını tutan dizidir.
    sol_nokta = (facial_landmarks.part(goz_noktalari[0]).x, facial_landmarks.part(goz_noktalari[0]).y)
    sag_nokta = (facial_landmarks.part(goz_noktalari[3]).x, facial_landmarks.part(goz_noktalari[3]).y)
    ust_orta = orta_nokta_bul(facial_landmarks.part(goz_noktalari[1]), facial_landmarks.part(goz_noktalari[2])) # gözün üst orta noktasıdır
    alt_orta = orta_nokta_bul(facial_landmarks.part(goz_noktalari[5]), facial_landmarks.part(goz_noktalari[4])) # gözün alt orta noktasıdır

  

    yatay_uzunluk = hypot((sol_nokta[0] - sag_nokta[0]), (sol_nokta[1] - sag_nokta[1]))   # yatay çizginin uzunluğu
    dikey_uzunluk = hypot((ust_orta[0] - alt_orta[0]), (ust_orta[1] - alt_orta[1])) # dikey çizginin uzunluğu
                              #x koordinatı  #x koordinatı         #y koordinatı   #y koordinatı
    kapalilik =  yatay_uzunluk / dikey_uzunluk  # yatay/dikey oranı ne kadar büyükse göz o kadar kapalıdır
    return kapalilik
    #return dikey_uzunluk




frames = 0
letter_index = 0
blinking_frames = 0
del_frames = 0
text = ""
ilk_yazi=""


while True:
    _, frame = cap.read()
    frame = cv2.resize(frame, None, fx=0.5, fy=0.5)
    keyboard[:] = (0, 0, 0)
    frames += 1
    new_frame = np.zeros((500, 500, 3), np.uint8)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    active_letter = keys_set_1[letter_index]

    faces = detector(gray)
    for face in faces:
        """x, y = face.left(), face.top()
        x1, y1 = face.right(), face.bottom()
        cv2.rectangle(frame, (x, y), (x1, y1), (0, 255, 0), 2)"""
        
        landmarks = predictor(gray, face)

        # Göz kapalı mı değil mi?
        sol_goz_oran = kapalilik_orani_bul([36, 37, 38, 39, 40, 41], landmarks) # Sol göz kapalılık oranı
        sag_goz_oran = kapalilik_orani_bul([42, 43, 44, 45, 46, 47], landmarks)# Sağ göz kapalılık oranı
        kapalilik_orani = (sol_goz_oran + sag_goz_oran) / 2 # İki gözünde kapalılık ortalaması

        if kapalilik_orani > 5.7:
            cv2.putText(frame, "YAZ", (50, 150), font, 4, (255, 0, 0), thickness=3)
            blinking_frames += 1
            frames -= 1

            if blinking_frames == 5:
                text += active_letter
                ilk_yazi += active_letter
                print(ilk_yazi)

        else:
            blinking_frames = 0


        """if sag_goz_oran > 5.7:
            cv2.putText(frame, "SİL", (50, 150), font, 4, (255, 0, 0), thickness=3)
            del_frames += 1
            frames -= 1

            if del_frames == 5:
                ilk_yazi = ilk_yazi[:-1]
                print("Harf silindi")
                print(ilk_yazi)

        else:
            del_frames = 0"""
                
            


        

    
        
    key1 = cv2.waitKey(1)
    if key1 == 8: # backspace'e basınca son harf silinir
        ilk_yazi = ilk_yazi[:-1]
        print("Harf silindi")
        print(ilk_yazi)
        """cv2.putText(board, ilk_yazi, (10, 100), font, 4, 0, 3)
        cv2.imshow("Board", board)"""
        

    # Letters
    if frames == 30:    #Geçiş hızı ayarı
        letter_index += 1
        frames = 0
    if letter_index == 27:
        letter_index = 0


    for i in range(27):   #Harfleri ekrana yazan fonksiyonu çalıştıran döngü
        if letter_index == 26 and blinking_frames == 5:
            ilk_yazi = ilk_yazi[:-1]
            print("Harf silindi")
            print(ilk_yazi)
            
        if i == letter_index:
            light = True
        else:
            light = False
        letter(i, keys_set_1[i], light)

    cv2.putText(board, text, (10, 100), font, 4, 0, 3) # Klavyeden seçilen harfi board'a yazar
    

    cv2.imshow("Frame", frame)
    #cv2.imshow("New frame", new_frame)
    cv2.imshow("Virtual keyboard", keyboard)
    #cv2.imshow("Board", board)

    key = cv2.waitKey(1)
    if key == 27:
        #cv2.putText(board, kaydedilecek_yazi, (50, 300), font, 4, 0, 3)
        break

cap.release()


"""dosya=open("yazi.txt","w")
dosya.write(kaydedilecek_yazi)
dosya.close()"""
keyboard = np.zeros((1, 1, 1), np.uint8)
cv2.imshow("Virtual keyboard", keyboard)
#cv2.imshow("Board", board)
duzeltilecek_yazi=TextBlob(ilk_yazi)
print("ORIGINAL TEXT : "+str(ilk_yazi))
print("CORRECTED TEXT : "+str(duzeltilecek_yazi.correct()))
while True:
    1==1
cv2.destroyAllWindows()
