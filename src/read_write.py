import math
import matplotlib.pyplot as plt

MAXVALOFGREY= 65536



def mypgmwrite (frm, img, imgname, column, row, greyval) :

    with open(imgname, "wb") as test:
        test.write(frm.encode())
        test.write(b"\n")
        test.write(str(column).encode())
        test.write(b"\n")
        test.write(str(row).encode())
        test.write(b"\n")
        test.write(str(greyval).encode())
        test.write(b"\n")

        for pixel in img:
            test.write(bytes([pixel]))
    return 

def mypgmread (file) :

    with open(str(file), "rb") as test:
        tokens = []
        while len(tokens) < 4 :
            line = test.readline().strip()
            if not line.startswith(b"#") :
                tokens.extend(line.split())

        frm, column, row, greyval = tokens[0], int(tokens[1]), int(tokens[2]), int(tokens[3])
        if frm != b"P5" :
            return

        pikseller = []
        if greyval >= MAXVALOFGREY :
            print ("Hatali PGM : Grey Val maksimum siniri asmis")
            return
        kalan = test.read()
        for byte in kalan :
            pikseller.append(byte)

        return pikseller, column, row, greyval

def myImageScale(orj_pixel, greyval = 255):
    #olcekleme:  fm = f - min(f)   ve   fs = K * (fm / max(fm))
    min_of_pixel = min(orj_pixel)

    #1. adim: en kucuk deger 0 olsun
    fm = []
    for pixel in orj_pixel :
        fm.append(pixel - min_of_pixel)

    max_of_pixel = max(fm)
    if max_of_pixel == 0 :          #tum pikseller ayni degerdeyse bolme yapilamaz
        return [0] * len(orj_pixel)

    #2. adim: en buyuk deger greyval olsun
    scale_pixel = []
    for pixel in fm :
        scale_pixel.append(round(pixel / max_of_pixel * greyval))

    return scale_pixel

def myImageNegative(file):
    old_pixel, column, row, greyval = mypgmread(file)
    neg_pixel = []
    #PGM basligindaki greyval zaten L - 1 degerine esit.
    for pixel in old_pixel :
        neg_pixel.append(greyval - pixel)

    return neg_pixel, column, row, greyval

def myImageLogTransformation(file):
    old_pixel, column, row, greyval = mypgmread(file)
    log_pixel = []

    for pixel in old_pixel :
        log_pixel.append(math.log( 1 + pixel))

    return myImageScale(log_pixel, greyval), column, row, greyval

def myImageGammaTransformation(file, gamma, c = 1):
    old_pixel, column, row, greyval = mypgmread(file)
    gamma_pixel = []
    
    for pixel in old_pixel :
        gamma_pixel.append(round(greyval * c * ((pixel / greyval) ** gamma)))

    return gamma_pixel, column, row, greyval

def myAverageMask(m):
    #m x m ortalama (box) maskesi. Katsayilar 1 tutulur; bolme islemi
    #myImageCorrelation icinde maskenin toplamina (m*m) bolunerek yapilir.
    return [1] * (m * m)

def myImageCorrelation(file, mask, border = "replicate"):
    #Uzamsal korelasyon:  g(i,j) = toplam( w(s,t) * f(i+s, j+t) )
    #mask duz bir liste olarak verilir (m*m eleman), m bu listeden hesaplanir.
    #border: kenarda maskenin disari tasan kismi icin
    #   "replicate" -> en yakin kenar pikseli tekrarlanir (varsayilan)
    #   "zero"      -> disarisi 0 kabul edilir, kenarlar koyulasir
    old_pixel, column, row, greyval = mypgmread(file)
    m = math.isqrt(len(mask))        #maske m x m boyutunda
    a = m // 2                       #merkeze olan uzaklik, m tek sayi oldugu icin tam bolunur
    mask_sum = sum(mask)

    corr_pixel = []
    for i in range(row) :
        for j in range(column) :
            toplam = 0
            for s in range(-a, a + 1) :
                for t in range(-a, a + 1) :
                    ii = i + s
                    jj = j + t
                    if ii < 0 or ii >= row or jj < 0 or jj >= column :
                        if border == "zero" :
                            deger = 0
                        else :
                            #en yakin gecerli satir/sutuna kaydir
                            ii = min(max(ii, 0), row - 1)
                            jj = min(max(jj, 0), column - 1)
                            deger = old_pixel[ii * column + jj]
                    else :
                        deger = old_pixel[ii * column + jj]
                    toplam = toplam + mask[(s + a) * m + (t + a)] * deger

            #ortalama maskesinde mask_sum = m*m olur, yani bolme ortalamayi verir.
            #Toplami sifir olan maskelerde (Laplacian vb) bolme yapilmaz, cagiran taraf myImageScale kullanmali.
            if mask_sum != 0 :
                corr_pixel.append(round(toplam / mask_sum))
            else :
                corr_pixel.append(toplam)

    return corr_pixel, column, row, greyval

def myImageMedian(file, m, border = "replicate"):
    #Medyan filtresi: komsulugu buyukten kucuge siralar ve ortadaki degeri secer.
    old_pixel, column, row, greyval = mypgmread(file)
    a = m // 2

    med_pixel = []
    for i in range(row) :
        for j in range(column) :
            komsuluk = []
            for s in range(-a, a + 1) :
                for t in range(-a, a + 1) :
                    ii = i + s
                    jj = j + t
                    if ii < 0 or ii >= row or jj < 0 or jj >= column :
                        if border == "zero" :
                            komsuluk.append(0)
                            continue
                        ii = min(max(ii, 0), row - 1)
                        jj = min(max(jj, 0), column - 1)
                    komsuluk.append(old_pixel[ii * column + jj])

            komsuluk.sort()
            #m tek sayi oldugu icin komsuluk eleman sayisi (m*m) da tektir, ortanca tek bir eleman olur
            med_pixel.append(komsuluk[len(komsuluk) // 2])

    return med_pixel, column, row, greyval

def myImageTo2D(img, column, row):
    #imshow iki boyutlu bir yapi bekler; duz piksel listesini satir satir bolerek
    iki_boyut = []
    for i in range(row) :
        iki_boyut.append(img[i * column : (i + 1) * column])
    return iki_boyut

def myImageShow(img, column, row, baslik = "", greyval = 255):
    #Goruntuyu Jupyter Notebook icinde gosterir.
    plt.imshow(myImageTo2D(img, column, row), cmap = "gray", vmin = 0, vmax = greyval)
    plt.title(baslik)
    plt.axis("off")
    plt.show()

def myImageShowMulti(images, basliklar, column, row, greyval = 255, sutun = 3):
    #Birden fazla goruntuyu yan yana gosterir. 
    satir = (len(images) + sutun - 1) // sutun
    fig, axes = plt.subplots(satir, sutun, figsize = (4.2 * sutun, 4.4 * satir))
    axes = axes.ravel() if len(images) > 1 else [axes]
    for k in range(len(axes)) :
        if k < len(images) :
            axes[k].imshow(myImageTo2D(images[k], column, row), cmap = "gray", vmin = 0, vmax = greyval)
            axes[k].set_title(basliklar[k], fontsize = 10)
        axes[k].axis("off")
    plt.tight_layout()
    plt.show()

