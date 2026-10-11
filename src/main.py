import os
from read_write import *

#Goruntuler kod klasorunde durmuyor: girdiler img/, uretilenler output/ altinda.
IMG = os.path.join("..", "img")
OUT = os.path.join("..", "output")
os.makedirs(OUT, exist_ok = True)

# ---------------------------------------------------------------- LAB00

mypgm = [10, 40, 70, 100, 130, 160, 190, 220, 250]

#Madde 1 - 3x3 goruntu olustur ve test.pgm olarak yaz
mypgmwrite("P5", mypgm, os.path.join(OUT, "test.pgm"), 3, 3, 255)

#Madde 2 - test.pgm'i geri oku ve ilk iki pikseli dogrula
f_test, column, row, greyval = mypgmread(os.path.join(OUT, "test.pgm"))

if f_test[0] == 10 :
    print("Dogru ilk deger")
else :
    print("Yanlis ilk deger")

if f_test[1] == 40 :
    print("Dogru ikinci deger")
else :
    print("Yanlis ikinci deger")

#Madde 3 - 100x100 pattern: i. satirin j. pikseli i + j + 1
f_pattern = []
for i in range(100):
    for j in range(100):
        f_pattern.append(i + j + 1)

mypgmwrite("P5", f_pattern, os.path.join(OUT, "pattern.pgm"), 100, 100, 255)

#Madde 4 - lena.pgm oku, 50-79 arasi satirlari sifirla, myLena2.pgm olarak yaz
f_lena, column, row, greyval = mypgmread(os.path.join(IMG, "lena.pgm"))
print("lena w ", column, "lena h", row)

for i in range(50, 80):
    for j in range(column):
        f_lena[i * column + j] = 0

mypgmwrite("P5", f_lena, os.path.join(OUT, "myLena2.pgm"), column, row, 255)

# ---------------------------------------------------------------- LAB01

#Kitaptaki sekillerin PGM'e cevrilmis halleri.
FIG_3_4  = os.path.join(IMG, "fig0304a.pgm")      #dijital mamografi        -> negatif
FIG_3_5  = os.path.join(IMG, "fig0305a.pgm")      #Fourier spektrumu        -> log
FIG_3_8  = os.path.join(IMG, "fig0308a.pgm")      #kirik omurga MR          -> gamma 0.6 / 0.4 / 0.3
FIG_3_33 = os.path.join(IMG, "fig0333a.pgm")      #500x500 test deseni      -> ortalama m = 3/5/9/15/35
FIG_3_35 = os.path.join(IMG, "fig0335a.pgm")      #tuz-biberli devre karti  -> 3x3 ortalama + 3x3 medyan


def lab01():
    #Sekil 3.4 - negatif
    if os.path.exists(FIG_3_4) :
        f_negative, column, row, greyval = myImageNegative(FIG_3_4)
        mypgmwrite("P5", f_negative, os.path.join(OUT, "fig0304b_negative.pgm"), column, row, greyval)
        print("3.4(b) yazildi")

    #Sekil 3.5 - log donusumu
    if os.path.exists(FIG_3_5) :
        f_log, column, row, greyval = myImageLogTransformation(FIG_3_5)
        mypgmwrite("P5", f_log, os.path.join(OUT, "fig0305b_log.pgm"), column, row, greyval)
        print("3.5(b) yazildi")

    #Sekil 3.8 - power-law, uc farkli gamma
    if os.path.exists(FIG_3_8) :
        for gamma in (0.6, 0.4, 0.3) :
            f_gamma, column, row, greyval = myImageGammaTransformation(FIG_3_8, gamma)
            mypgmwrite("P5", f_gamma, os.path.join(OUT, "fig0308_gamma_%s.pgm" % gamma), column, row, greyval)
            print("3.8 gamma=%s yazildi" % gamma)

    #Sekil 3.33 - bes farkli boyutta ortalama maskesi
    if os.path.exists(FIG_3_33) :
        for m in (3, 5, 9, 15, 35) :
            f_average, column, row, greyval = myImageCorrelation(FIG_3_33, myAverageMask(m))
            mypgmwrite("P5", f_average, os.path.join(OUT, "fig0333_avg_%d.pgm" % m), column, row, greyval)
            print("3.33 m=%d yazildi" % m)

    #Sekil 3.35 - ayni gurultulu goruntuye ortalama ve medyan, karsilastirma icin
    if os.path.exists(FIG_3_35) :
        f_average_3x3, column, row, greyval = myImageCorrelation(FIG_3_35, myAverageMask(3))
        mypgmwrite("P5", f_average_3x3, os.path.join(OUT, "fig0335b_avg3.pgm"), column, row, greyval)
        f_median_3x3, column, row, greyval = myImageMedian(FIG_3_35, 3)
        mypgmwrite("P5", f_median_3x3, os.path.join(OUT, "fig0335c_median3.pgm"), column, row, greyval)
        print("3.35(b) ve 3.35(c) yazildi")


eksik = [f for f in (FIG_3_4, FIG_3_5, FIG_3_8, FIG_3_33, FIG_3_35) if not os.path.exists(f)]
if eksik :
    print()
    print("LAB01 atlandi, su goruntuler yok:", ", ".join(eksik))
    print("DIP3E_CH03_Original_Images.zip icinden cikarip PGM'e cevirdikten sonra tekrar calistir.")
else :
    lab01()

# ---------------------------------------------------------------- LAB02

FIG_3_38 = os.path.join(IMG, "fig0338a.pgm")     #bulanik ay goruntusu  -> Laplacian keskinlestirme
FIG_3_40 = os.path.join(IMG, "fig0340a.pgm")     #DIP-XE yazisi         -> unsharp masking / highboost


def lab02_sekil338():
    #Sekil 3.38 (b)-(e): Laplacian ile keskinlestirme.
    #(b) ve (c) ayni ham Laplacian ciktisindan turer, sadece sonraki islem farklidir:
    #(b) kirpilir, (c) olceklenir.
    laplacian_4, column, row, greyval = myImageCorrelation(FIG_3_38, myLaplacianMask(4))

    f_laplacian_clipped = myImageClip(laplacian_4, greyval)
    mypgmwrite("P5", f_laplacian_clipped, os.path.join(OUT, "fig0338b_lap_clipped.pgm"), column, row, greyval)

    f_laplacian_scaled = myImageScale(laplacian_4, greyval)
    mypgmwrite("P5", f_laplacian_scaled, os.path.join(OUT, "fig0338c_lap_scaled.pgm"), column, row, greyval)

    #(d) ve (e): g = f + c * laplacian,  iki farkli maske ile
    f_sharpened_4, column, row, greyval = myImageSharpen(FIG_3_38, myLaplacianMask(4))
    mypgmwrite("P5", f_sharpened_4, os.path.join(OUT, "fig0338d_sharp4.pgm"), column, row, greyval)

    f_sharpened_8, column, row, greyval = myImageSharpen(FIG_3_38, myLaplacianMask(8))
    mypgmwrite("P5", f_sharpened_8, os.path.join(OUT, "fig0338e_sharp8.pgm"), column, row, greyval)

    print("3.38 (b)(c)(d)(e) yazildi")


def lab02_not1_sekil338():
    #Not-1: keskinlestirmeyi artirmak icin |c| buyutulur. Cok buyurse kenarlarda
    #halka (halo) etkisi ve doygunluk olusur, yani goruntu bozulur.
    for komsu in (4, 8) :
        for c in (-1, -2, -3, -5, -8) :
            f_sharpened, column, row, greyval = myImageSharpen(FIG_3_38, myLaplacianMask(komsu), c)
            mypgmwrite("P5", f_sharpened,
                       os.path.join(OUT, "fig0338_c%d_k%d.pgm" % (abs(c), komsu)),
                       column, row, greyval)
    print("3.38 Not-1 (c = -1,-2,-3,-5,-8 / 4 ve 8 komsu) yazildi")


def lab02_sekil340():
    #Sekil 3.40 (b)-(e): unsharp masking ve highboost.
    #Kitap (b) icin 5x5 Gauss, sigma = 3 kullaniyor.
    gauss_mask = myGaussianMask(5, 3)

    f_blurred, column, row, greyval = myImageCorrelation(FIG_3_40, gauss_mask)
    mypgmwrite("P5", f_blurred, os.path.join(OUT, "fig0340b_blurred.pgm"), column, row, greyval)

    #(c) maskenin kendisi: hem negatif hem pozitif deger tasir, gosterim icin olceklenir
    f_unsharp_mask, column, row, greyval = myImageUnsharpMask(FIG_3_40, gauss_mask)
    mypgmwrite("P5", myImageScale(f_unsharp_mask, greyval),
               os.path.join(OUT, "fig0340c_mask.pgm"), column, row, greyval)

    #(d) k = 1 -> unsharp masking
    f_unsharp_k1, column, row, greyval = myImageHighboost(FIG_3_40, gauss_mask, 1)
    mypgmwrite("P5", f_unsharp_k1, os.path.join(OUT, "fig0340d_unsharp_k1.pgm"), column, row, greyval)

    #(e) k = 4.5 -> highboost. Kitap bunu tum degerleri pozitif tutan en buyuk k olarak veriyor.
    f_highboost_k45, column, row, greyval = myImageHighboost(FIG_3_40, gauss_mask, 4.5)
    mypgmwrite("P5", f_highboost_k45, os.path.join(OUT, "fig0340e_highboost_k45.pgm"), column, row, greyval)

    print("3.40 (b)(c)(d)(e) yazildi")


def lab02_not1_sekil340():
    #Not-1: k buyudukce keskinlik artar. 4.5 ustune cikilinca negatif degerler dogar,
    #kirpilirlar ve kenarlarda koyu haleler olusur.
    gauss_mask = myGaussianMask(5, 3)
    for k in (1, 2, 4.5, 8, 15) :
        f_highboost, column, row, greyval = myImageHighboost(FIG_3_40, gauss_mask, k)
        mypgmwrite("P5", f_highboost,
                   os.path.join(OUT, "fig0340_k%s.pgm" % str(k).replace(".", "_")),
                   column, row, greyval)
    print("3.40 Not-1 (k = 1, 2, 4.5, 8, 15) yazildi")


#Sekil 3.20 girdi goruntuleri (Sekil 3.16'dan): karanlik, acik, dusuk ve yuksek kontrast
FIG_3_20 = {
    "dark":         os.path.join(IMG, "fig0320_dark.pgm"),
    "light":        os.path.join(IMG, "fig0320_light.pgm"),
    "lowcontrast":  os.path.join(IMG, "fig0320_lowcontrast.pgm"),
    "highcontrast": os.path.join(IMG, "fig0320_highcontrast.pgm"),
}


def lab02_sekil320():
    #Sekil 3.20 orta sutun: dort goruntunun histogram esitlenmis halleri.
    for ad, dosya in FIG_3_20.items() :
        f_equalized, column, row, greyval = myImageHistEqualization(dosya)
        mypgmwrite("P5", f_equalized,
                   os.path.join(OUT, "fig0320_%s_equalized.pgm" % ad),
                   column, row, greyval)
    print("3.20 dort esitlenmis goruntu yazildi")


eksik2 = [f for f in (FIG_3_38, FIG_3_40) if not os.path.exists(f)]
if eksik2 :
    print()
    print("LAB02 atlandi, su goruntuler yok:", ", ".join(eksik2))
else :
    lab02_sekil338()
    lab02_not1_sekil338()
    lab02_sekil340()
    lab02_not1_sekil340()
    if all(os.path.exists(d) for d in FIG_3_20.values()) :
        lab02_sekil320()
