import serial
import Funcoes_Braco as funcB #importariamos o novo módulo chamado Funcoes_Braco

import time

serBraco = serial.Serial('COM6', 115200, timeout=None)
time.sleep(50)


while True:
    funcB.movimentaPecaTeste(serBraco)
    