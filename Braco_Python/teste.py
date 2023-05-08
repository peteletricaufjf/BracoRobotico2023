import serial

import time

ser = serial.Serial('COM8', 115200, timeout=None)
time.sleep(50)


def confere():
    opa = 'hugostoso'
    while True:
        opa = str(ser.readline())
        # print(opa[2])
        if opa[2] == '1':
            ser.flush()
            break


while True:
    print('passo 1')
    coord = f"50, 50, 100, 500, 500, 0"
    ser.write(coord.encode())
    confere()
    print('descer')
    coord = f"50, 50, 225, 500, 500, 0"
    ser.write(coord.encode())
    confere()
    print('subir')
    coord = f"50, 50, 100, 500, 500, 0"
    ser.write(coord.encode())
    confere()

    print('passo 2')
    coord = f"200, 10, 100, 500, 500, 0"
    ser.write(coord.encode())
    confere()
    print('descer')
    coord = f"200, 10, 225, 500, 500, 0"
    ser.write(coord.encode())
    confere()
    print('subir')
    coord = f"200, 10, 100, 500, 500, 0"
    ser.write(coord.encode())
    confere()

    print('passo 3')
    coord = f"100, 100, 100, 500, 500, 0"
    ser.write(coord.encode())
    confere()
    print('descer')
    coord = f"100, 100, 225, 500, 500, 0"
    ser.write(coord.encode())
    confere()
    print('subir')
    coord = f"100, 100, 100, 500, 500, 0"
    ser.write(coord.encode())
    confere()
