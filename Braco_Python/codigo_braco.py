# pip install chess

# pip install pyserial

import chess
import chess.engine
import serial

import math

def inverseKinematics(x, y):
    L1 = 228
    L2 = 136.5
    PI = math.pi
    
    theta2 = math.acos((x**2 + y**2 - L1**2 - L2**2) / (2 * L1 * L2))
    if x < 0 and y < 0:
        theta2 = -theta2
    
    theta1 = math.atan(x / y) - math.atan((L2 * math.sin(theta2)) / (L1 + L2 * math.cos(theta2)))
    
    theta2 = -theta2 * 180 / PI
    theta1 = theta1 * 180 / PI

    # Angles adjustment depending in which quadrant the final tool coordinate x,y is
    if x >= 0 and y >= 0: # 1st quadrant
        theta1 = 90 - theta1
    if x < 0 and y > 0: # 2nd quadrant
        theta1 = 90 - theta1
    if x < 0 and y < 0: # 3d quadrant
        theta1 = 270 - theta1
        # phi = 270 - theta1 - theta2
        # phi = -phi
    if x > 0 and y < 0: # 4th quadrant
        theta1 = -90 - theta1
    if x < 0 and y == 0:
        theta1 = 270 + theta1

    # Calculate "phi" angle so gripper is parallel to the X axis
    # phi = 90 + theta1 + theta2
    # phi = -phi

    # Angle adjustment depending in which quadrant the final tool coordinate x,y is
    # if x < 0 and y < 0: # 3d quadrant
    #    phi = 270 - theta1 - theta2
    # if abs(phi) > 165:
    #    phi = 180 + phi

    theta1 = round(theta1)
    theta2 = round(theta2)
    return [theta1, theta2]
    # phi = round(phi)

#aqui temos que baixar o stockfish no pc que formos usar (aquele lenovo ta horrivel, vamos usar msm assim?)

import pandas as pd

# Monta a matriz vazia referente as casas do tabuleiro

col = ["a","b","c","d","e","f","g","h"]
index = [1,2,3,4,5,6,7,8]
tabuleiro = pd.DataFrame(index = index, columns = col)

# Preenche a matriz com as coordenadas de cada casa

tabuleiro["a"] = [[30,50],[20,30],[0,0],[0,0],[0,0],[0,0],[0,0],[50,0]]
tabuleiro["b"] = [[0,0],[0,1],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]
tabuleiro["c"] = [[0,0],[0,1],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]
tabuleiro["d"] = [[0,0],[0,1],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]
tabuleiro["e"] = [[0,0],[0,1],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]
tabuleiro["f"] = [[0,0],[0,1],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]
tabuleiro["g"] = [[0,0],[0,1],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]
tabuleiro["h"] = [[0,0],[0,1],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]]


# Abre uma conexão serial com o Arduino
ser = serial.Serial('COM8',115200,timeout= None)

# Recebe uma string do Arduino referente a jogada
jogada_usuario = ser.readline().decode('utf-8').rstrip()
""" 
ser.readline(): Lê uma linha de texto da porta serial e retorna uma string 
de bytes terminada em uma quebra de linha ("\n").

.decode('utf-8'): Decodifica a string de bytes em um objeto Unicode usando o 
codec UTF-8. UTF-8 é um conjunto de caracteres que pode representar qualquer 
caractere em qualquer idioma, tornando-o uma escolha comum para a codificação
de texto em programas de computador.

.rstrip(): Remove os caracteres de quebra de linha do final da string. Isso 
é importante para garantir que a string lida da porta serial não contenha caracteres indesejados ou vazios.
"""

# Fecha a conexão serial
ser.close()

#seleciona a engine desejada e especifica o pathing de onde ela foi baixada, devemos especificar o path no pc escolhido
engine = chess.engine.SimpleEngine.popen_uci("/content/stockfish_14_linux_x64_popcnt/stockfish_14_x64_popcnt") 

board = chess.Board() #inicializa o objeto tabuleiro de xadrez na posição inicial

# aqui entraria comunicação com arduino e interpretação movimento humano e gera string que seria o movimento
# !!SEMPRE PRIMEIRO MOVIMENTO ENVIADO SERÁ DAS PEÇAS BRANCAS
move1 = chess.Move.from_uci(jogada_usuario) #inicializa um objeto move1 com o comando de movimento a partir da string de jogada "e2e4"(simulando jogada de humano que foi e2e4)
board.push(move1) #comando que envia o objeto move1 com o comando de movimento para o tabuleiro de jogo atual

movimentoBraco = engine.play(board, chess.engine.Limit(time=1.0)) #obtém um objeto de jogada a partir do pensamento da IA Stockfish
                                                                  #o objeto contem as seguintes informações
                                                                  #move -> string de jogada
                                                                  #ponder -> string de jogada que foi considerada durante pensamento IA
                                                                  #info{}-> um dicionario de informação extra mandada pela engine
                                                                  #draw_offered -> retorna booleano de acordo se a engine quis oferecer empate ou nao
                                                                  #resigned->

board.push(movimentoBraco.move) #joga pro tabuleiro a jogada do braço
jogadabraco = str(movimentoBraco.move) # transforma jogada que ta em string para coordenadas que o braço ira efetuar movimentos
# move1 = chess.Move.from_uci(jogadabraco) # ex: move1 = chess.Move.from_uci('d2d4')
# board.push(move1)

# movimentoBraco = engine.play(board,chess.engine.Limit(time=1.0))
pacman = board.is_capture(movimentoBraco.move)  #cria a variavel pacman que será um booleano. A partir do objeto "board" usamos o metodo "is_capture"
                                                #passando para esse metodo a variavel do tipo chess.move "movimentoBraco.move"

# Divide os valores da string para ter separado os valores das linhas e colunas
# ex: coluna do primeiro movimento: c1
#     linha do primeiro movimento: l1

c1 = jogadabraco[0]
l1 = float(jogadabraco[1])
c2 = jogadabraco[2]
l2 = float(jogadabraco[3])

x1 = tabuleiro.loc[l1, c1][0]
y1 = tabuleiro.loc[l1, c1][1]

x2 = tabuleiro.loc[l2, c2][0]
y2 = tabuleiro.loc[l2, c2][1]


theta1, theta2 = inverseKinematics(311, 75)
print("Ângulos do motor: theta1 = {}, theta2 = {}".format(theta1, theta2))

# theta1_j1 -> angulo 1 da primeira jogada(j1)
[theta1_j1,theta2_j1] = inverseKinematics(x1, y1)

[theta1_j2,theta2_j2] = inverseKinematics(x2, y2)


# timeout é o tempo que o python irá esperar para receber o dado do arduino, nesse caso coloquei o tempo como indefinido
serBraco = serial.Serial('COM8', 115200,timeout= None) # ajuste a porta serial e a taxa de transmissão de acordo com as configurações do seu Arduino

import time

# Função resposável pra ver se o arduino terminou de execultar o movimento 

def confere():
    opa = 'hugostoso'
    while True:
        opa = str(serBraco.readline())
        print(opa[2])
        if opa[2] == '1':
            ser.flush()
            break

    '''
    ser.readline(): Lê uma linha de texto da porta serial e retorna 
    uma string de bytes terminada em uma quebra de linha ("\n").
    '''

if pacman is True:
    
    # Manda o braço subir somente o eixo z para evitar de esbarrar nas peças
    coord = f"0, 0 , '200', 500, 500, 0"  # (angulo j1, angulo j2, posição z, vel, acel, eletroimã)
    ser.write(coord.encode())
    confere()
    
    # Manda o braço ir até a peça que será removida do jogo
    coord = f"{theta1_j2}, {theta2_j2}, {'200'}, 500, 500, 0"
    ser.write(coord.encode())
    confere()

    # Manda o braço descer somente o eixo z para encostar na peça
    coord = f"{theta1_j2}, {theta2_j2}, '50', 500, 500, 0"
    ser.write(coord.encode())
    confere()

    # Mandar ativar o eletroimã
    coord = f"{theta1_j2}, {theta2_j2}, '50', 500, 500, 1"
    ser.write(coord.encode())
    confere()

    # Manda o braço subir somente o eixo z antes de mover a peça
    coord = f"{theta1_j2}, {theta2_j2}, '200', 500, 500, 1"
    ser.write(coord.encode())
    confere()

    # Manda o braço levar a peça para fora do jogo
    coord = f"'x', 'y' , '200', 500, 500, 1"
    ser.write(coord.encode())
    confere()

    # Manda soltar a peça
    coord = f"'x', 'y' , '200', 500, 500, 0"
    ser.write(coord.encode())
    confere()


#podemos fazer uma função chamada movimento, que recebe uma string coord e manda via serial

# Manda o braço subir somente o eixo z para evitar de esbarrar nas peças
coord = f"0, 0 , '200', 500, 500, 0"
serBraco.write(coord.encode())
confere()

# Manda o braço ir até a peça que será mexida 
coord = f"{theta1_j1}, {theta2_j1}, '200', 500, 500, 0"
serBraco.write(coord.encode())
confere()
      
# Manda o braço descer somente o eixo z para encostar na peça
coord = f"{theta1_j1}, {theta2_j1}, '50', 500, 500, 0"
serBraco.write(coord.encode())
confere()

# Mandar ativar o eletroimã
coord = f"{theta1_j1}, {theta2_j1}, '50', 500, 500, 1"
serBraco.write(coord.encode())
confere()

# Manda o braço subir somente o eixo z antes de mover a peça
coord = f"{theta1_j1}, {theta2_j1}, '200', 500, 500, 1"
serBraco.write(coord.encode())
confere()

# Manda o braço levar a peça pra casa desejada 
coord = f"{theta1_j2}, {theta2_j2}, '200', 500, 500, 1"
serBraco.write(coord.encode())
confere()

# Manda o braço descer somente o eixo z para colocar a peça no lugar
coord = f"{theta1_j2}, {theta2_j2}, '200', 500, 500, 1"
serBraco.write(coord.encode())
confere()

# Manda soltar a peça
coord = f"{theta1_j2}, {theta2_j2}, '200', 500, 500, 0"
serBraco.write(coord.encode())
confere()

# Manda o braço para uma posição inicial
coord = f"0, 0, '200', 500, 500, 0"
serBraco.write(coord.encode())
confere()