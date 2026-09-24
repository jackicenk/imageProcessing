GREYVAL = 255

mypgm = [
    [10, 40, 70],
    [100, 130, 160],
    [190, 220, 250]
]

def mypgmwrite (frm, img, row, column) :

    with open("test.pgm", "wb") as test:
        test.write(frm.encode())
        test.write(b"\n")
        test.write(str(column).encode())
        test.write(b"\n")
        test.write(str(row).encode())
        test.write(b"\n")
        test.write(str(GREYVAL).encode())
        test.write(b"\n")
        for rw in img:
            for pixel in rw:
                test.write(bytes([pixel]))
    return 

mypgmwrite ("P5", mypgm, 3, 3)