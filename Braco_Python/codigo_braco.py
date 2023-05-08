# pip install chess

# pip install pyserial

import chess
import chess.engine
import serial
import Funcoes_Braco as funcB #importariamos o novo módulo chamado Funcoes_Braco

import math

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
serTabuleiro = serial.Serial('COM8',115200,timeout= None)

# Recebe uma string do Arduino referente a jogada
jogada_usuario = serTabuleiro.readline().decode('utf-8').rstrip()

# Fecha a conexão serial
serTabuleiro.close()

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

# theta1_j1 -> angulo 1 da primeira jogada(j1)
jogada1 = funcB.inverseKinematics(x1,y1) #acessamos theta1_j1 por jogada1[0], etc
jogada2 = funcB.inverseKinematics(x2,y2) #acessamos theta1_j2 por jogada2[0], etc


# timeout é o tempo que o python irá esperar para receber o dado do arduino, nesse caso coloquei o tempo como indefinido
serBraco = serial.Serial('COM8', 115200,timeout= None) # ajuste a porta serial e a taxa de transmissão de acordo com as configurações do seu Arduino

import time

funcB.seComeu(serBraco,pacman,jogada2)
funcB.movimentaPeca(serBraco,jogada1,jogada2)
