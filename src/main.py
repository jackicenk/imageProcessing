import os
from read_write import *

# ---------------------------------------------------------------- LAB00

mypgm = [10, 40, 70, 100, 130, 160, 190, 220, 250]

#Madde 1 - 3x3 goruntu olustur ve test.pgm olarak yaz
mypgmwrite("P5", mypgm, "test.pgm", 3, 3, 255)

#Madde 2 - test.pgm'i geri oku ve ilk iki pikseli dogrula
f_test, column, row, greyval = mypgmread("test.pgm")

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

mypgmwrite("P5", f_pattern, "pattern.pgm", 100, 100, 255)

#Madde 4 - lena.pgm oku, 50-79 arasi satirlari sifirla, myLena2.pgm olarak yaz
f_lena, column, row, greyval = mypgmread("lena.pgm")
print("lena w ", column, "lena h", row)

for i in range(50, 80):
    for j in range(column):
        f_lena[i * column + j] = 0

mypgmwrite("P5", f_lena, "myLena2.pgm", column, row, 255)

# ---------------------------------------------------------------- LAB01

#Kitaptaki sekillerin PGM'e cevrilmis halleri.
FIG_3_4  = "fig0304a.pgm"      #dijital mamografi        -> negatif
FIG_3_5  = "fig0305a.pgm"      #Fourier spektrumu        -> log
FIG_3_8  = "fig0308a.pgm"      #kirik omurga MR          -> gamma 0.6 / 0.4 / 0.3
FIG_3_33 = "fig0333a.pgm"      #500x500 test deseni      -> ortalama m = 3/5/9/15/35
FIG_3_35 = "fig0335a.pgm"      #tuz-biberli devre karti  -> 3x3 ortalama + 3x3 medyan


def lab01():
    #Sekil 3.4 - negatif
    if os.path.exists(FIG_3_4) :
        f_negative, column, row, greyval = myImageNegative(FIG_3_4)
        mypgmwrite("P5", f_negative, "fig0304b_negative.pgm", column, row, greyval)
        print("3.4(b) yazildi")

    #Sekil 3.5 - log donusumu
    if os.path.exists(FIG_3_5) :
        f_log, column, row, greyval = myImageLogTransformation(FIG_3_5)
        mypgmwrite("P5", f_log, "fig0305b_log.pgm", column, row, greyval)
        print("3.5(b) yazildi")

    #Sekil 3.8 - power-law, uc farkli gamma
    if os.path.exists(FIG_3_8) :
        for gamma in (0.6, 0.4, 0.3) :
            f_gamma, column, row, greyval = myImageGammaTransformation(FIG_3_8, gamma)
            mypgmwrite("P5", f_gamma, "fig0308_gamma_%s.pgm" % gamma, column, row, greyval)
            print("3.8 gamma=%s yazildi" % gamma)

    #Sekil 3.33 - bes farkli boyutta ortalama maskesi
    if os.path.exists(FIG_3_33) :
        for m in (3, 5, 9, 15, 35) :
            f_average, column, row, greyval = myImageCorrelation(FIG_3_33, myAverageMask(m))
            mypgmwrite("P5", f_average, "fig0333_avg_%d.pgm" % m, column, row, greyval)
            print("3.33 m=%d yazildi" % m)

    #Sekil 3.35 - ayni gurultulu goruntuye ortalama ve medyan, karsilastirma icin
    if os.path.exists(FIG_3_35) :
        f_average_3x3, column, row, greyval = myImageCorrelation(FIG_3_35, myAverageMask(3))
        mypgmwrite("P5", f_average_3x3, "fig0335b_avg3.pgm", column, row, greyval)
        f_median_3x3, column, row, greyval = myImageMedian(FIG_3_35, 3)
        mypgmwrite("P5", f_median_3x3, "fig0335c_median3.pgm", column, row, greyval)
        print("3.35(b) ve 3.35(c) yazildi")


eksik = [f for f in (FIG_3_4, FIG_3_5, FIG_3_8, FIG_3_33, FIG_3_35) if not os.path.exists(f)]
if eksik :
    print()
    print("LAB01 atlandi, su goruntuler yok:", ", ".join(eksik))
    print("DIP3E_CH03_Original_Images.zip icinden cikarip PGM'e cevirdikten sonra tekrar calistir.")
else :
    lab01()
