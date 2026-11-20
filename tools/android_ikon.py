#!/usr/bin/env python3
"""Sezar Abi Kurye simgeleri: lacivert zemin + krem motosiklet glifi."""
from PIL import Image, ImageDraw
import os, math

MARKA = (20, 31, 49)      # #141F31
KREM = (241, 247, 247)    # #F1F7F7
YESIL = (48, 144, 72)     # #309048

def motor(d, cx, cy, s, renk, kalinlik):
    """Basit motosiklet silueti: iki teker + gövde + gidon."""
    k = kalinlik
    # tekerlekler
    r = s * 0.30
    sol = (cx - s*0.52, cy + s*0.28)
    sag = (cx + s*0.52, cy + s*0.28)
    for (x, y) in (sol, sag):
        d.ellipse([x-r, y-r, x+r, y+r], outline=renk, width=k)
    # gövde
    d.line([sol[0]+r*0.7, sol[1]-r*0.35, cx, cy - s*0.10], fill=renk, width=k)
    d.line([cx, cy - s*0.10, sag[0]-r*0.7, sag[1]-r*0.35], fill=renk, width=k)
    d.line([cx - s*0.10, cy - s*0.10, cx + s*0.05, cy - s*0.52], fill=renk, width=k)
    # gidon
    d.line([cx - s*0.22, cy - s*0.52, cx + s*0.30, cy - s*0.52], fill=renk, width=k)
    # sele
    d.line([cx - s*0.34, cy - s*0.30, cx - s*0.02, cy - s*0.30], fill=renk, width=k)

def ikon(boyut, zemin, glif, dolgu=False, oran=0.62):
    ss = 4
    im = Image.new("RGBA", (boyut*ss, boyut*ss), (0,0,0,0))
    d = ImageDraw.Draw(im)
    W = boyut*ss
    if dolgu:
        d.rectangle([0,0,W,W], fill=zemin)
    else:
        d.rounded_rectangle([0,0,W-1,W-1], radius=int(W*0.22), fill=zemin)
    motor(d, W/2, W/2, W*oran*0.52, glif, max(2, int(W*0.045)))
    return im.resize((boyut,boyut), Image.LANCZOS)

def yuvarlak(boyut, zemin, glif, oran=0.62):
    ss = 4
    im = Image.new("RGBA", (boyut*ss, boyut*ss), (0,0,0,0))
    d = ImageDraw.Draw(im)
    W = boyut*ss
    d.ellipse([0,0,W-1,W-1], fill=zemin)
    motor(d, W/2, W/2, W*oran*0.52, glif, max(2,int(W*0.045)))
    return im.resize((boyut,boyut), Image.LANCZOS)

os.makedirs("icons", exist_ok=True)

# ana simgeler
for b in (192, 512):
    ikon(b, MARKA, KREM).save(f"icons/icon-{b}.png")

# maskable: güvenli alan için glif küçültülür, zemin tam kare
ss = 4
W = 512*ss
im = Image.new("RGBA", (W,W), MARKA)
d = ImageDraw.Draw(im)
motor(d, W/2, W/2, W*0.40*0.52, KREM, max(3,int(W*0.038)))
im.resize((512,512), Image.LANCZOS).save("icons/maskable-512.png")

# apple-touch
ikon(180, MARKA, KREM).save("icons/apple-touch-icon.png")

# kısayol simgeleri (krem zemin + lacivert glif)
def kisa(boyut, ciz):
    ss = 4
    W = boyut*ss
    im = Image.new("RGBA", (W,W), KREM)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([0,0,W-1,W-1], radius=int(W*0.20), fill=KREM)
    ciz(d, W)
    return im.resize((boyut,boyut), Image.LANCZOS)

def ciz_gorev(d, W):
    k = max(2, int(W*0.055))
    # pano/kutu
    d.rounded_rectangle([W*0.24, W*0.28, W*0.76, W*0.78], radius=int(W*0.06), outline=MARKA, width=k)
    d.line([W*0.40, W*0.20, W*0.60, W*0.20], fill=MARKA, width=k)
    # onay
    d.line([W*0.36, W*0.54, W*0.46, W*0.64, W*0.66, W*0.42], fill=YESIL, width=k)

def ciz_kazanc(d, W):
    k = max(2, int(W*0.055))
    d.line([W*0.22, W*0.70, W*0.40, W*0.50, W*0.54, W*0.60, W*0.78, W*0.32], fill=MARKA, width=k, joint="curve")
    d.line([W*0.62, W*0.32, W*0.78, W*0.32, W*0.78, W*0.48], fill=MARKA, width=k)
    d.line([W*0.22, W*0.80, W*0.78, W*0.80], fill=YESIL, width=k)

def ciz_mesaj(d, W):
    k = max(2, int(W*0.055))
    d.rounded_rectangle([W*0.20, W*0.26, W*0.80, W*0.66], radius=int(W*0.10), outline=MARKA, width=k)
    d.line([W*0.34, W*0.66, W*0.30, W*0.78, W*0.46, W*0.66], fill=MARKA, width=k, joint="curve")
    d.ellipse([W*0.36, W*0.42, W*0.42, W*0.48], fill=MARKA)
    d.ellipse([W*0.47, W*0.42, W*0.53, W*0.48], fill=MARKA)
    d.ellipse([W*0.58, W*0.42, W*0.64, W*0.48], fill=MARKA)

def ciz_yardim(d, W):
    k = max(2, int(W*0.055))
    d.ellipse([W*0.22, W*0.22, W*0.78, W*0.78], outline=MARKA, width=k)
    d.arc([W*0.38, W*0.32, W*0.64, W*0.56], start=200, end=20, fill=MARKA, width=k)
    d.line([W*0.51, W*0.54, W*0.51, W*0.60], fill=MARKA, width=k)
    d.ellipse([W*0.48, W*0.65, W*0.54, W*0.71], fill=MARKA)

kisa(192, ciz_gorev).save("icons/sc-gorev.png")
kisa(192, ciz_kazanc).save("icons/sc-kazanc.png")
kisa(192, ciz_mesaj).save("icons/sc-mesaj.png")
kisa(192, ciz_yardim).save("icons/sc-yardim.png")

print("simgeler üretildi:")
for f in sorted(os.listdir("icons")):
    print("  ", f, os.path.getsize(os.path.join("icons",f)), "bayt")
