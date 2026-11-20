#!/usr/bin/env python3
"""Android launcher ve kısayol ikonlarını üretir."""
from PIL import Image, ImageDraw
import os

MARKA=(20,31,49); KREM=(241,247,247); YESIL=(48,144,72)
RES="android/app/src/main/res"

def motor(d,cx,cy,s,renk,k):
    r=s*0.30
    sol=(cx-s*0.52,cy+s*0.28); sag=(cx+s*0.52,cy+s*0.28)
    for (x,y) in (sol,sag):
        d.ellipse([x-r,y-r,x+r,y+r],outline=renk,width=k)
    d.line([sol[0]+r*0.7,sol[1]-r*0.35,cx,cy-s*0.10],fill=renk,width=k)
    d.line([cx,cy-s*0.10,sag[0]-r*0.7,sag[1]-r*0.35],fill=renk,width=k)
    d.line([cx-s*0.10,cy-s*0.10,cx+s*0.05,cy-s*0.52],fill=renk,width=k)
    d.line([cx-s*0.22,cy-s*0.52,cx+s*0.30,cy-s*0.52],fill=renk,width=k)
    d.line([cx-s*0.34,cy-s*0.30,cx-s*0.02,cy-s*0.30],fill=renk,width=k)

def kare(boyut, yuvarlak=False, oran=0.60):
    ss=4; W=boyut*ss
    im=Image.new("RGBA",(W,W),(0,0,0,0)); d=ImageDraw.Draw(im)
    if yuvarlak:
        d.ellipse([0,0,W-1,W-1],fill=MARKA)
    else:
        d.rounded_rectangle([0,0,W-1,W-1],radius=int(W*0.22),fill=MARKA)
    motor(d,W/2,W/2,W*oran*0.52,KREM,max(2,int(W*0.045)))
    return im.resize((boyut,boyut),Image.LANCZOS)

YOGUNLUK={"mdpi":1.0,"hdpi":1.5,"xhdpi":2.0,"xxhdpi":3.0,"xxxhdpi":4.0}
for ad,ol in YOGUNLUK.items():
    d=f"{RES}/mipmap-{ad}"; os.makedirs(d,exist_ok=True)
    n=int(48*ol)
    kare(n).save(f"{d}/ic_launcher.png")
    kare(n,yuvarlak=True).save(f"{d}/ic_launcher_round.png")

# ön plan katmanı (adaptive icon): saydam zemin + ortada glif
for ad,ol in YOGUNLUK.items():
    d=f"{RES}/mipmap-{ad}"; n=int(108*ol)
    ss=4; W=n*ss
    im=Image.new("RGBA",(W,W),(0,0,0,0)); dr=ImageDraw.Draw(im)
    motor(dr,W/2,W/2,W*0.38*0.52,KREM,max(2,int(W*0.038)))
    im.resize((n,n),Image.LANCZOS).save(f"{d}/ic_launcher_foreground.png")

# adaptive icon xml
os.makedirs(f"{RES}/mipmap-anydpi-v26",exist_ok=True)
aci='''<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@color/marka" />
    <foreground android:drawable="@mipmap/ic_launcher_foreground" />
</adaptive-icon>
'''
open(f"{RES}/mipmap-anydpi-v26/ic_launcher.xml","w").write(aci)
open(f"{RES}/mipmap-anydpi-v26/ic_launcher_round.xml","w").write(aci)

# kısayol çizimleri (drawable-xxhdpi, 96dp)
def kisa(n, ciz):
    ss=4; W=n*ss
    im=Image.new("RGBA",(W,W),(0,0,0,0)); d=ImageDraw.Draw(im)
    d.rounded_rectangle([0,0,W-1,W-1],radius=int(W*0.20),fill=KREM)
    ciz(d,W)
    return im.resize((n,n),Image.LANCZOS)

def c_gorev(d,W):
    k=max(2,int(W*0.055))
    d.rounded_rectangle([W*0.24,W*0.28,W*0.76,W*0.78],radius=int(W*0.06),outline=MARKA,width=k)
    d.line([W*0.40,W*0.20,W*0.60,W*0.20],fill=MARKA,width=k)
    d.line([W*0.36,W*0.54,W*0.46,W*0.64,W*0.66,W*0.42],fill=YESIL,width=k,joint="curve")

def c_kazanc(d,W):
    k=max(2,int(W*0.055))
    d.line([W*0.22,W*0.70,W*0.40,W*0.50,W*0.54,W*0.60,W*0.78,W*0.32],fill=MARKA,width=k,joint="curve")
    d.line([W*0.62,W*0.32,W*0.78,W*0.32,W*0.78,W*0.48],fill=MARKA,width=k)
    d.line([W*0.22,W*0.80,W*0.78,W*0.80],fill=YESIL,width=k)

def c_mesaj(d,W):
    k=max(2,int(W*0.055))
    d.rounded_rectangle([W*0.20,W*0.26,W*0.80,W*0.66],radius=int(W*0.10),outline=MARKA,width=k)
    d.line([W*0.34,W*0.66,W*0.30,W*0.78,W*0.46,W*0.66],fill=MARKA,width=k,joint="curve")
    for x in (0.36,0.47,0.58):
        d.ellipse([W*x,W*0.42,W*(x+0.06),W*0.48],fill=MARKA)

def c_yardim(d,W):
    k=max(2,int(W*0.055))
    d.ellipse([W*0.22,W*0.22,W*0.78,W*0.78],outline=MARKA,width=k)
    d.arc([W*0.38,W*0.32,W*0.64,W*0.56],start=200,end=20,fill=MARKA,width=k)
    d.line([W*0.51,W*0.54,W*0.51,W*0.60],fill=MARKA,width=k)
    d.ellipse([W*0.48,W*0.65,W*0.54,W*0.71],fill=MARKA)

dd=f"{RES}/drawable-xxhdpi"; os.makedirs(dd,exist_ok=True)
kisa(288,c_gorev).save(f"{dd}/sc_gorev.png")
kisa(288,c_kazanc).save(f"{dd}/sc_kazanc.png")
kisa(288,c_mesaj).save(f"{dd}/sc_mesaj.png")
kisa(288,c_yardim).save(f"{dd}/sc_yardim.png")

print("android ikonları üretildi")
for kok,_,dosyalar in os.walk(RES):
    for f in sorted(dosyalar):
        if f.endswith(".png"):
            y=os.path.join(kok,f)
            print(f"  {y.replace(RES+'/','')} {os.path.getsize(y)}")
