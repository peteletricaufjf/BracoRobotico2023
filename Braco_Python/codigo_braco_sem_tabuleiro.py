# pip install chess

# pip install pyserial

import chess
import chess.engine
import serial
import Funcoes_Braco as funcB #importariamos o novo módulo chamado Funcoes_Braco

import math
import pandas as pd

#aqui temos que baixar o stockfish no pc que formos usar (aquele lenovo ta horrivel, vamos usar msm assim?)

# Monta a matriz vazia referente as casas do tabuleiro

col = ["a","b","c","d","e","f","g","h"]
index = [1,2,3,4,5,6,7,8]
tabuleiro = pd.DataFrame(index = index, columns = col)

# Preenche a matriz com as coordenadas de cada casa

tabuleiro["a"] = [[64,63],[55,83],[50,98],[42,112],[36,124],[33,136],[23,145],[17,154]]
tabuleiro["b"] = [[69,65],[58,88],[52,102],[46,118],[45,129],[36,142],[35,154],[29,165]]
tabuleiro["c"] = [[69,72],[62,92],[56,107],[52,121],[48,135],[45,147],[42,159],[46,173]]
tabuleiro["d"] = [[73,75],[68,94],[62,110],[58,124],[55,137],[55,150],[54,163],[60,178]]
tabuleiro["e"] = [[78,77],[72,95],[68,110],[65,125],[64,138],[63,150],[66,164],[76,180]]
tabuleiro["f"] = [[84,75],[80,93],[75,109],[73,123],[73,137],[76,151],[77,161],[86,176]]
tabuleiro["g"] = [[90,74],[86,90],[83,106],[81,120],[81,133],[83,146],[88,157],[100,169]]
tabuleiro["h"] = [[97,67],[92,87],[90,102],[88,116],[89,128],[92,140],[96,151],[105,162]]



# Abre uma conexão serial com o Arduino
# serTabuleiro = serial.Serial('COM8',115200,timeout= None)

# Recebe uma string do Arduino referente a jogada
# jogada_usuario = serTabuleiro.readline()

# Fatiou passou
# jogada_usuario[2:6]

# Vamos dar a jogada do usuario ao invés do tabuleiro dar 
jogada_usuario = input("Qual foi o movimento feito pelo usuário? ")

# Fecha a conexão serial
# serTabuleiro.close()

#seleciona a engine desejada e especifica o pathing de onde ela foi baixada, devemos especificar o path no pc escolhido
#IMPORTANTE: TEM QUE TER O r ANTES DA STRING DO CAMINHO DO ARQUIVO DE ONDE ESTÁ O STOCKFISH OK?????

engine = chess.engine.SimpleEngine.popen_uci(r"C:\Users\PC PET Eletrica\Desktop\RepositorioBraco\BracoRobotico2023\stockfish\stockfish-windows-x86-64-modern.exe") 

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

print(movimentoBraco.move)
board.push(movimentoBraco.move) #joga pro tabuleiro a jogada do braço
print(board.is_checkmate())
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

theta1 = tabuleiro.loc[l1, c1][0]
phi1 = tabuleiro.loc[l1, c1][1]

theta2 = tabuleiro.loc[l2, c2][0]
phi2 = tabuleiro.loc[l2, c2][1]


import time

funcB.seComeu(pacman,theta2,phi2)
funcB.movimentaPeca(theta1,phi1,theta2,phi2)
