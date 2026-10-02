MAXVALOFGREY= 65536

mypgm = [10, 40, 70, 100, 130, 160, 190, 220, 250]


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

        return pikseller, column, row

        
mypgmwrite ("P5", mypgm,"test.pgm", 3, 3, 255)
img, w, h = mypgmread("test.pgm") 

if img[0] == 10 : 
    print ("Dogru ilk deger")
else :
    print ("Yanlis ilk deger")

if img[1] == 40 : 
    print ("Dogru ikinci deger")
else :
    print ("Yanlis ikinci deger")

pattern = []
for i in range(100):
    for j in range(100):
        pattern.append(i + j + 1)

mypgmwrite ("P5", pattern,"pattern.pgm", 100, 100, 255)
lenaimg, w, h = mypgmread("lena.pgm")
print ("lena w ", w, "lena h", h)

for i in range(50, 80):
    for j in range(w):
        lenaimg[i * w + j] = 0

mypgmwrite ("P5", lenaimg,"myLena2.pgm", w, h, 255)