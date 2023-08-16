import serial
import time


# timeout é o tempo que o python irá esperar para receber o dado do arduino, nesse caso coloquei o tempo como indefinido
# ajuste a porta serial e a taxa de transmissão de acordo com as configurações do seu Arduino
serBraco = serial.Serial('COM16', 115200, timeout=None) 

def confere(serBraco):
    opa = 'hugostoso'
    while True:
        opa = str(serBraco.readline())
        # print(opa[2])
        if opa[2] == '1':
            serBraco.flush()
            break

ferrarezi = 70
bernardo = 140

def seComeu(pacman,theta2,phi2):
    if pacman is False:
        # Manda o braço subir somente o eixo z para evitar de esbarrar nas peças
        coord = f"0, 0 ,133, 500, 500, 0"  # (angulo 1, angulo 2, z, vel, acel, eletroimã)
        serBraco.write(coord.encode())
        confere(serBraco)
    
        # Manda o braço ir até a peça que será removida do jogo
        coord = f"{theta2}, {phi2}, 133, 500, 500, 0"
        serBraco.write(coord.encode())
        confere(serBraco)

        # Manda o braço descer somente o eixo z para encostar na peça
        coord = f"{theta2}, {phi2}, {bernardo}, 500, 500, 1"
        serBraco.write(coord.encode())
        confere(serBraco)

        # Manda o braço subir somente o eixo z antes de mover a peça
        coord = f"{theta2}, {phi2}, {ferrarezi}, 500, 500, 1"
        serBraco.write(coord.encode())
        confere(serBraco)

        # Manda o braço levar a peça para fora do jogo
        coord = f"0, 0 ,{ferrarezi}, 500, 500, 0"
        serBraco.write(coord.encode())
        confere(serBraco)


def movimentaPeca(theta1,phi1,theta2,phi2):
    # Manda o braço subir somente o eixo z para evitar de esbarrar nas peças
    coord = f"0, 0 , 133, 500, 500, 0"
    serBraco.write(coord.encode())
    confere(serBraco)

    # Manda o braço ir até a peça que será mexida 
    coord = f"{theta1}, {phi1}, {ferrarezi}, 500, 500, 0"
    serBraco.write(coord.encode())
    confere(serBraco)
      
    # Manda o braço descer somente o eixo z para encostar na peça
    coord = f"{theta1}, {phi1}, {bernardo}, 500, 500, 1"
    serBraco.write(coord.encode())
    confere(serBraco)

    # Manda o braço subir somente o eixo z antes de mover a peça
    coord = f"{theta1}, {phi1}, {ferrarezi}, 500, 500, 1"
    serBraco.write(coord.encode())
    confere(serBraco)

    # Manda o braço levar a peça pra casa desejada 
    coord = f"{theta2}, {phi2}, {ferrarezi}, 500, 500, 1"
    serBraco.write(coord.encode())
    confere(serBraco)

    # Manda o braço descer somente o eixo z para colocar a peça no lugar
    coord = f"{theta2}, {phi2}, {bernardo}, 500, 500, 0"
    serBraco.write(coord.encode())
    confere(serBraco)

    # Manda o braço para uma posição inicial
    coord = f"0, 0, '200', 500, 500, 0"
    serBraco.write(coord.encode())
    confere(serBraco)

def movimentaPecaTeste():
    print('passo 1')
    
    coord = f"50, 50, 100, 500, 500, 0"
    serBraco.write(coord.encode())
    confere(serBraco)
    print('descer')
    coord = f"50, 50, 225, 500, 500, 0"
    serBraco.write(coord.encode())
    confere(serBraco)
    print('subir')
    coord = f"50, 50, 225, 500, 500, 0"
    serBraco.write(coord.encode())
    confere(serBraco)

    print('passo 2')
    coord = f"200, 10, 100, 500, 500, 0"
    serBraco.write(coord.encode())
    confere(serBraco)
    print('descer')
    coord = f"200, 10, 225, 500, 500, 0"
    serBraco.write(coord.encode())
    confere(serBraco)
    print('subir')
    coord = f"200, 10, 100, 500, 500, 0"
    serBraco.write(coord.encode())
    confere(serBraco)

    print('passo 3')
    coord = f"100, 100, 100, 500, 500, 0"
    serBraco.write(coord.encode())
    confere(serBraco)
    print('descer')
    coord = f"100, 100, 225, 500, 500, 0"
    serBraco.write(coord.encode())
    confere(serBraco)
    print('subir')
    coord = f"100, 100, 100, 500, 500, 0"
    serBraco.write(coord.encode())
    confere(serBraco)