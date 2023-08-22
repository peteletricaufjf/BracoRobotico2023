import serial
import time

ferrarezi = 100
bernardo = 150

# timeout é o tempo que o python irá esperar para receber o dado do arduino, nesse caso coloquei o tempo como indefinido
# ajuste a porta serial e a taxa de transmissão de acordo com as configurações do seu Arduino
serBraco = serial.Serial('COM5', 115200, timeout=None) 

def confere(serBraco):
    opa = 'hugostoso'
    while True:
        opa = str(serBraco.readline())
        # print(opa[2])
        if opa[2] == '1':
            serBraco.flush()
            break


def seComeu(pacman,theta2,phi2,z2):
    if pacman is True:
        # Manda o braço subir somente o eixo z para evitar de esbarrar nas peças
        # coord = f"0, 0 ,133, 500, 500, 0"  # (angulo 1, angulo 2, z, vel, acel, eletroimã)
        # serBraco.write(coord.encode())
        # confere(serBraco)
    
        # Manda o braço ir até a peça que será removida do jogo
        coord = f"{theta2}, {phi2}, {bernardo}, 500, 500, 0"
        serBraco.write(coord.encode())
        confere(serBraco)

        # Manda o braço descer somente o eixo z para encostar na peça
        coord = f"{theta2}, {phi2}, {z2}, 500, 500, 1"
        serBraco.write(coord.encode())
        confere(serBraco)

        # Manda o braço subir somente o eixo z antes de mover a peça
        coord = f"{theta2}, {phi2}, {ferrarezi}, 500, 500, 1"
        serBraco.write(coord.encode())
        confere(serBraco)

        # Manda o braço levar a peça para fora do jogo
        coord = f"115, 75 ,{ferrarezi}, 500, 500, 0"
        serBraco.write(coord.encode())
        confere(serBraco)


def movimentaPeca(theta1,phi1,z1,theta2,phi2,z2,roque):
    # Manda o braço subir somente o eixo z para evitar de esbarrar nas peças
    # coord = f"0, 0 , 133, 500, 500, 0"
    # serBraco.write(coord.encode())
    # confere(serBraco)

    # Manda o braço ir até a peça que será mexida 
    coord = f"{theta1}, {phi1}, {bernardo}, 500, 500, 0"
    serBraco.write(coord.encode())
    confere(serBraco)
    
    # Manda o braço descer somente o eixo z para encostar na peça
    coord = f"{theta1}, {phi1}, {z1}, 500, 500, 1"
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
    coord = f"{theta2}, {phi2}, {z2}, 500, 500, 0"
    serBraco.write(coord.encode())
    confere(serBraco)
    
    # sobe um pouco
    coord = f"{theta2}, {phi2}, {bernardo}, 500, 500, 0"
    serBraco.write(coord.encode())
    confere(serBraco)

    if roque == False:
        # Manda o braço para uma posição inicial
        coord = f"30, 180, {bernardo}, 500, 500, 0"
        serBraco.write(coord.encode())
        confere(serBraco)
    

def fazroque(roque_curto,roque_longo,tabuleiro):
    if roque_curto == True:
        jogadabraco = "h8f8"
        c1 = jogadabraco[0]
        l1 = float(jogadabraco[1])
        c2 = jogadabraco[2]
        l2 = float(jogadabraco[3])

        theta1 = tabuleiro.loc[l1, c1][0]
        phi1 = tabuleiro.loc[l1, c1][1]
        z1 = tabuleiro.loc[l1, c1][2]

        theta2 = tabuleiro.loc[l2, c2][0]
        phi2 = tabuleiro.loc[l2, c2][1]
        z2 = tabuleiro.loc[l2, c2][2]
        
        movimentaPeca(theta1,phi1,z1,theta2,phi2,z2)
        
    if roque_longo == True:
        jogadabraco = "a8d8"
        c1 = jogadabraco[0]
        l1 = float(jogadabraco[1])
        c2 = jogadabraco[2]
        l2 = float(jogadabraco[3])

        theta1 = tabuleiro.loc[l1, c1][0]
        phi1 = tabuleiro.loc[l1, c1][1]
        z1 = tabuleiro.loc[l1, c1][2]

        theta2 = tabuleiro.loc[l2, c2][0]
        phi2 = tabuleiro.loc[l2, c2][1]
        z2 = tabuleiro.loc[l2, c2][2]
        
        movimentaPeca(theta1,phi1,z1,theta2,phi2,z2)