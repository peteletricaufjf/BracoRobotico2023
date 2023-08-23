import serial
import time

ferrarezi = 100
bernardo = 150

# timeout é o tempo que o python irá esperar para receber o dado do arduino, nesse caso coloquei o tempo como indefinido
# ajuste a porta serial e a taxa de transmissão de acordo com as configurações do seu Arduino
serBraco = serial.Serial('COM5', 115200, timeout=None) 

def confere(serBraco):
    """Função para fazer o python esperar o arduino terminar de execultar o movimento, para só depois disso dar prosseguimento no código

    Args:
        serBraco (Serial): comunicação serial com o arduino
    """
    opa = 'hugostoso'
    while True:
        opa = str(serBraco.readline())
        # print(opa[2])
        if opa[2] == '1':
            serBraco.flush()
            break


def seComeu(pacman,theta2,phi2,z2):
    """Função que realiza o movimento de retirar a peça que vai ser comida

    Args:
        pacman (bolean): Indica se o movimento vai ser de comer peça ou não
        theta2 (int): Indica o primeiro ângulo da casa que o braço precisa de ir para remover a peça
        phi2 (int): Indica o segundo ângulo da casa que o braço precisa de ir para remover a peça
        z2 (int): Indica a altura necessária para pegar uma peça nessa casa
    """
    if pacman is True:
        # Manda o braço ir até a peça que será removida do jogo
        coord = f"{theta2}, {phi2}, {bernardo}, 500, 500, 0"  # (angulo 1, angulo 2, z, vel, acel, eletroimã)
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
    """Função que realiza o movimento de levar uma peça de uma casa para outra

    Args:
        theta1 (int): O primeiro ângulo da casa de origem que o braço precisa de ir para pegar a peça
        phi1 (int): O segundo ângulo da casa de origem que o braço precisa de ir para pegar a peça
        z1 (int): A altura da casa de origem que o braço precisa de descer para pegar a peça
        theta2 (int): O primeiro ângulo da casa de destino que o braço precisa de ir para levar a peça
        phi2 (int): O segundo ângulo da casa de destino que o braço precisa de ir para levar a peça
        z2 (int): A altura da casa de destino que o braço precisa de descer para levar a peça
        roque (bolean): Caso vá ocorrer o roque (True), o braço não precisa de voltar para uma posição inicial,
        uma vez que ele ainda vai movimentar a torre, então usamos essa informação para verificar se o braço precisa ou não
        voltar para origem
    """
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

    # Se for ocorrer o roque ele não precisa voltar para a posição inical, pois ainda vai movimentar a torre
    if roque == False:
        # Manda o braço para uma posição inicial
        coord = f"30, 180, {bernardo}, 500, 500, 0"
        serBraco.write(coord.encode())
        confere(serBraco)
    

def fazroque(roque_curto,roque_longo,tabuleiro):
    """Função responsável por movimentar a torre quando o braço fizer o roque, uma vez que até então ele terá movimentado
    somente o rei, logo essa função começa depois desse movimento, e termina a jogada movimentando o rei

    Args:
        roque_curto (bolean): Váriavel que informa se é um roque curto  
        roque_longo (bolean): Váriavel que informa se é um roque longo
        tabuleiro (DataFrame): Matriz com os ângulos dos motores referente a cada casa do tabuleiro
    """
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
        
        # Muda a variável para False para que ele na função movimentaPeca ele volte para a posição inicial no final
        roque = False
        
        movimentaPeca(theta1,phi1,z1,theta2,phi2,z2,roque)
        
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
        
        # Muda a variável para False para que ele na função movimentaPeca ele volte para a posição inicial no final
        roque = False
            
        movimentaPeca(theta1,phi1,z1,theta2,phi2,z2,roque)