import serial
import time

ser = serial.Serial('COM16', 115200, timeout=None)
time.sleep(50)


def confere():
    opa = 'hugostoso'
    while True:
        opa = str(ser.readline())
        # print(opa[2])
        if opa[2] == '1':
            ser.flush()
            break


# pegar peça
coorde = f"35,154,158,500,500,1"
ser.write(coorde.encode())
confere()
input("Pressione Enter para continuar...")


# subir
coorde = f"35,154,100,500,500,1"
ser.write(coorde.encode())
confere()

# levar 
coorde = f"45,130,100,500,500,1"
ser.write(coorde.encode())
confere()

# soltar
coorde = f"45,130,157,500,500,0"
ser.write(coorde.encode())
confere()

# subir
coorde = f"45,130,145,500,500,0"
ser.write(coorde.encode())
confere()

# segunda peça (cavalo g8-a6)

# pegar peça
coorde = f"100,169,158,500,500,1"
ser.write(coorde.encode())
confere()
input("Pressione Enter para continuar...")


# subir
coorde = f"100,169,100,500,500,1"
ser.write(coorde.encode())
confere()

# levar 
coorde = f"76,151,100,500,500,1"
ser.write(coorde.encode())
confere()

# soltar
coorde = f"76,151,157,500,500,0"
ser.write(coorde.encode())
confere()

# subir
coorde = f"76,151,145,500,500,0"
ser.write(coorde.encode())
confere()


# terceira peça (bispo c8-a6)

# pegar peça
coorde = f"46,173,158,500,500,1"
ser.write(coorde.encode())
confere()
input("Pressione Enter para continuar...")


# subir
coorde = f"46,173,100,500,500,1"
ser.write(coorde.encode())
confere()

# levar 
coorde = f"33,136,100,500,500,1"
ser.write(coorde.encode())
confere()

# soltar
coorde = f"33,136,157,500,500,0"
ser.write(coorde.encode())
confere()

# subir
coorde = f"33,136,145,500,500,0"
ser.write(coorde.encode())
confere()