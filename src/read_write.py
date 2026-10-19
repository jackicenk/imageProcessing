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

# ---------------------------------------------------------------- LAB01

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
    #squeeze = False ile subplots her durumda 2 boyutlu dizi dondurur, tek goruntude de calisir
    fig, axes = plt.subplots(satir, sutun, figsize = (4.2 * sutun, 4.4 * satir), squeeze = False)
    axes = axes.ravel()
    for k in range(len(axes)) :
        if k < len(images) :
            axes[k].imshow(myImageTo2D(images[k], column, row), cmap = "gray", vmin = 0, vmax = greyval)
            axes[k].set_title(basliklar[k], fontsize = 10)
        axes[k].axis("off")
    plt.tight_layout()
    plt.show()


# ---------------------------------------------------------------- LAB02

def myLaplacianMask(komsu = 4):
    #Gonzalez Sekil 3.37'deki Laplacian cekirdekleri.
    #komsu = 4 -> Denklem (3.6-6), 90 derece katlarinda izotropik
    #komsu = 8 -> kosegen terimler de eklenmis hali, 45 derece katlarinda izotropik
    #Iki maskenin de toplami sifirdir, bu yuzden myImageCorrelation bolme yapmaz.
    #Merkez katsayi negatif oldugu icin keskinlestirmede c = -1 kullanilir.
    if komsu == 8 :
        return [1,  1, 1,
                1, -8, 1,
                1,  1, 1]
    return [0,  1, 0,
            1, -4, 1,
            0,  1, 0]

def myImageClip(img, greyval = 255):
    #Aralik disina tasan degerleri sinirlara kirpar: negatifler 0, greyval ustu greyval olur.
    #myImageScale'den farki, degerleri yeniden DAGITMAMASIDIR; sadece uclari keser.
    #Sekil 3.38(b)'de kitabin "negatif degerlerin hepsi ekran tarafindan 0'a kirpilir"
    #dedigi durum tam olarak budur.
    clip_pixel = []
    for pixel in img :
        if pixel < 0 :
            clip_pixel.append(0)
        elif pixel > greyval :
            clip_pixel.append(greyval)
        else :
            clip_pixel.append(round(pixel))
    return clip_pixel


def myImageSharpen(file, mask, c = -1):
    #Denklem (3.6-7):  g(x,y) = f(x,y) + c * laplacian(x,y)
    #c = -1 merkez katsayisi negatif olan maskeler icindir (Sekil 3.37 a ve b).
    #|c| buyudukce keskinlestirme artar; cok buyurse kenarlarda asiri vurgu ve bozulma olusur.
    old_pixel, column, row, greyval = mypgmread(file)
    #maskenin toplami sifir oldugu icin korelasyon ham degerleri dondurur (negatifler dahil)
    lap_pixel, column, row, greyval = myImageCorrelation(file, mask)

    sharp_pixel = []
    #iki listeyi ayni anda gezmek gerektigi icin deger degil indeks uzerinden donulur
    for k in range(len(old_pixel)) :
        sharp_pixel.append(old_pixel[k] + c * lap_pixel[k])

    #toplama sonucu 0-greyval araligi disina cikabilir, kirpilarak geri getirilir
    return myImageClip(sharp_pixel, greyval), column, row, greyval


def myGaussianMask(m, sigma):
    #m x m Gauss cekirdegi:  w(s,t) = e^(-(s^2 + t^2) / (2*sigma^2))
    #Merkezden uzaklastikca agirlik azalir; ortalama maskesinden farki budur.
    #Katsayilar normalize edilmez, cunku myImageCorrelation zaten maskenin
    #toplamina boluyor (mask_sum). Boylece agirliklarin toplami 1 olmus gibi davranir.
    a = m // 2
    mask = []
    for s in range(-a, a + 1) :
        for t in range(-a, a + 1) :
            mask.append(math.exp(-(s * s + t * t) / (2 * sigma * sigma)))
    return mask

def myImageUnsharpMask(file, mask):
    #Denklem (3.6-8):  g_mask(x,y) = f(x,y) - f_bulanik(x,y)
    #Sonuc hem negatif hem pozitif deger icerir; gosterilecekse myImageScale gerekir.
    old_pixel, column, row, greyval = mypgmread(file)
    blurred_pixel, column, row, greyval = myImageCorrelation(file, mask)

    unsharp_pixel = []
    for k in range(len(old_pixel)) :
        unsharp_pixel.append(old_pixel[k] - blurred_pixel[k])

    return unsharp_pixel, column, row, greyval

def myImageHighboost(file, mask, k = 1):
    #Denklem (3.6-9):  g(x,y) = f(x,y) + k * g_mask(x,y)
    #k = 1  -> unsharp masking
    #k > 1  -> highboost filtreleme
    #k < 1  -> maskenin katkisini azaltir
    #k buyudukce keskinlik artar; cok buyurse sonuc negatife duser ve kenarlarda
    #koyu haleler olusur (kitap k = 4.5'i tum degerleri pozitif tutan sinir olarak veriyor).
    old_pixel, column, row, greyval = mypgmread(file)
    unsharp_pixel, column, row, greyval = myImageUnsharpMask(file, mask)

    boost_pixel = []
    for n in range(len(old_pixel)) :
        boost_pixel.append(old_pixel[n] + k * unsharp_pixel[n])

    return myImageClip(boost_pixel, greyval), column, row, greyval

def myImageHistogram(img, greyval = 255):
    #Denklem (3.3-7):  p_r(r_k) = n_k / MN
    #Her gri seviyenin goruntudeki goreli sikligi. Toplami 1'dir.
    #Donen liste greyval + 1 elemanlidir (8 bit icin 0..255 arasi 256 seviye).
    sayim = [0] * (greyval + 1)
    for pixel in img :
        sayim[pixel] = sayim[pixel] + 1

    MN = len(img)
    hist = []
    for n in sayim :
        hist.append(n / MN)
    return hist

def myImageCDF(hist):
    #Kumulatif dagilim: cdf[k] = hist[0] + hist[1] + ... + hist[k]
    #Normalize histogramin toplami 1 oldugu icin cdf 0 ile 1 arasinda artar.
    cdf = []
    toplam = 0
    for p in hist :
        toplam = toplam + p
        cdf.append(toplam)
    return cdf

def myImageHistEqualization(file):
    #Denklem (3.3-8):  s_k = (L-1) * cdf(r_k)
    #Donusum fonksiyonunun kendisi CDF'tir; CDF'in dik oldugu yerde (piksellerin
    #yogunlastigi seviyelerde) cikis degerleri genis bir araliga yayilir, yatay
    #oldugu yerde sikisir. Sonucta histogram tum skalaya dagilir.
    old_pixel, column, row, greyval = mypgmread(file)
    cdf = myImageCDF(myImageHistogram(old_pixel, greyval))

    #her gri seviye icin cikis degerini bir kez hesapla (256 deger), sonra tabloyu kullan
    donusum = []
    for k in range(greyval + 1) :
        donusum.append(round(greyval * cdf[k]))

    eq_pixel = []
    for pixel in old_pixel :
        eq_pixel.append(donusum[pixel])

    return eq_pixel, column, row, greyval

def myImageHistShow(hists, basliklar, sutun = 4):
    #Normalize histogramlari cubuk grafik olarak yan yana cizer (Sekil 3.20 sag sutunu gibi).
    #Her cubuk bir gri seviyeyi, yuksekligi o seviyenin goreli sikligini (n_k / MN) gosterir.
    satir = (len(hists) + sutun - 1) // sutun
    fig, axes = plt.subplots(satir, sutun, figsize = (4.2 * sutun, 3.2 * satir), squeeze = False)
    axes = axes.ravel()
    for k in range(len(axes)) :
        if k < len(hists) :
            axes[k].bar(range(len(hists[k])), hists[k], width = 1, color = "black")
            axes[k].set_xlim(0, len(hists[k]) - 1)
            axes[k].set_title(basliklar[k], fontsize = 10)
            axes[k].set_xlabel("gri seviye")
        else :
            axes[k].axis("off")
    plt.tight_layout()
    plt.show()

def myImageHistCdfShow(f_in, f_out, baslik, greyval = 255):
    #Not-2: giris ve cikis goruntulerinin normalize histogramlari ve CDF'leri yan yana.
    #Ucuncu grafikte iki CDF ust uste cizilir. Kesikli cizgi duzgun dagilimin CDF'idir;
    #esitlenmis goruntunun CDF'i bu dogruya ne kadar yakinsa histogram o kadar yayilmistir.
    hist_in = myImageHistogram(f_in, greyval)
    hist_out = myImageHistogram(f_out, greyval)
    cdf_in = myImageCDF(hist_in)
    cdf_out = myImageCDF(hist_out)
    seviye = range(greyval + 1)
    #iki histogram ayni dikey olcekte cizilmeli, yoksa yukseklikler karsilastirilamaz
    ust_sinir = max(max(hist_in), max(hist_out)) * 1.05

    fig, axes = plt.subplots(1, 3, figsize = (15, 3.6))
    axes[0].bar(seviye, hist_in, width = 1, color = "black")
    axes[0].set_ylim(0, ust_sinir)
    axes[0].set_title(baslik + " - giriş histogramı", fontsize = 10)
    axes[1].bar(seviye, hist_out, width = 1, color = "black")
    axes[1].set_ylim(0, ust_sinir)
    axes[1].set_title(baslik + " - çıkış histogramı", fontsize = 10)
    axes[2].plot(seviye, cdf_in, label = "giriş CDF")
    axes[2].plot(seviye, cdf_out, label = "çıkış CDF")
    axes[2].plot([0, greyval], [0, 1], linestyle = ":", color = "gray", label = "düzgün dağılım")
    axes[2].set_title(baslik + " - CDF", fontsize = 10)
    axes[2].legend(fontsize = 8)
    for ax in axes :
        ax.set_xlim(0, greyval)
        ax.set_xlabel("gri seviye")
    plt.tight_layout()
    plt.show()
