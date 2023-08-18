# pip install chess

# pip install pyserial

import chess
import chess.engine
import serial
import Funcoes_Braco as funcB #importariamos o novo módulo chamado Funcoes_Braco

import math
import pandas as pd

# Monta o dataframe referente as casas do tabuleiro

col = ["a","b","c","d","e","f","g","h"]
index = [1,2,3,4,5,6,7,8]
tabuleiro = pd.DataFrame(index = index, columns = col)

# Preenche o dataframe com as coordenadas de cada casa

tabuleiro["a"] = [[64,63,150],[55,82,154],[48,99,156],[42,113,157],[36,125,159],[31,137,159],[26,147,160],[19,156,160]]
tabuleiro["b"] = [[69,65,150],[58,89,155],[52,105,157],[47,118,158],[42,131,159],[38,143,160],[34,154,161],[31,166,160]]
tabuleiro["c"] = [[69,72,150],[62,93,155],[58,109,157],[54,122,160],[50,135,160],[47,148,161],[45,161,160],[45,174,161]]
tabuleiro["d"] = [[73,75,150],[68,95,156],[63,111,158],[61,125,160],[58,138,160],[57,151,161],[57,164,161],[64,179,161]]
tabuleiro["e"] = [[78,77,150],[74,95,156],[71,111,158],[67,126,161],[66,139,161],[67,152,161],[69,164,162],[80,180,161]]
tabuleiro["f"] = [[84,75,150],[80,94,156],[77,110,158],[75,124,161],[75,137,160],[77,149,161],[81,162,161],[90,175,161]]
tabuleiro["g"] = [[90,74,150],[87,91,155],[84,107,157],[82,121,160],[83,133,159],[85,145,160],[90,159,161],[99,169,161]]
tabuleiro["h"] = [[97,67,150],[94,86,156],[91,102,157],[91,116,159],[91,128,159],[94,139,159],[99,152,160],[106,160,160]]



# Abre uma conexão serial com o Arduino
# serTabuleiro = serial.Serial('COM8',115200,timeout= None)

# Recebe uma string do Arduino referente a jogada
# jogada_usuario = serTabuleiro.readline()

# Fatiou passou
# jogada_usuario[2:6]


# Fecha a conexão serial
# serTabuleiro.close()

#seleciona a engine desejada e especifica o pathing de onde ela foi baixada, devemos especificar o path no pc escolhido
#IMPORTANTE: TEM QUE TER O r ANTES DA STRING DO CAMINHO DO ARQUIVO DE ONDE ESTÁ O STOCKFISH OK?????

engine = chess.engine.SimpleEngine.popen_uci(r"D:\Arquivos\BracoRobotico2023\Braco_Python\stockfish-windows-x86-64-avx2\stockfish\stockfish-windows-x86-64-avx2.exe") 

#inicializa o objeto tabuleiro de xadrez na posição inicial
board = chess.Board() 

while True:
    
    # Vamos dar a jogada do usuario ao invés do tabuleiro dar 
    jogada_usuario = input("Qual foi o movimento feito pelo usuário? ")
    
    # aqui entraria comunicação com arduino e interpretação movimento humano e gera string que seria o movimento
    # !!SEMPRE PRIMEIRO MOVIMENTO ENVIADO SERÁ DAS PEÇAS BRANCAS
    move1 = chess.Move.from_uci(jogada_usuario) #inicializa um objeto move1 com o comando de movimento a partir da string de jogada "e2e4"(simulando jogada de humano que foi e2e4)

    board.push(move1) #comando que envia o objeto move1 com o comando de movimento para o tabuleiro de jogo atual

    #se nao for cheque mate, ve o movimento que engine quer fazer e executa ele.    
    if not board.is_checkmate():

        movimentoBraco = engine.play(board, chess.engine.Limit(time=1.0)) #obtém um objeto de jogada a partir do pensamento da IA Stockfish
                                                                        #o objeto contem as seguintes informações
                                                                        #move -> string de jogada
                                                                        #ponder -> string de jogada que foi considerada durante pensamento IA
                                                                        #info{}-> um dicionario de informação extra mandada pela engine
                                                                        #draw_offered -> retorna booleano de acordo se a engine quis oferecer empate ou nao
                                                                        #resigned->

        print(movimentoBraco.move)
        
        pacman = board.is_capture(movimentoBraco.move)  #cria a variavel pacman que será um booleano. A partir do objeto "board" usamos o metodo "is_capture"
                                                        #passando para esse metodo a variavel do tipo chess.move "movimentoBraco.move"
        print(pacman)
        
        board.push(movimentoBraco.move) #joga pro tabuleiro a jogada do braço
        jogadabraco = str(movimentoBraco.move) # transforma jogada que ta em string para coordenadas que o braço ira efetuar movimentos
        # move1 = chess.Move.from_uci(jogadabraco) # ex: move1 = chess.Move.from_uci('d2d4')
        # board.push(move1)

        # movimentoBraco = engine.play(board,chess.engine.Limit(time=1.0))
        
        # Divide os valores da string para ter separado os valores das linhas e colunas
        # ex: coluna do primeiro movimento: c1
        #     linha do primeiro movimento: l1
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


        import time
        
        funcB.seComeu(pacman,theta2,phi2,z2)
        funcB.movimentaPeca(theta1,phi1,z1,theta2,phi2,z2)
        
        if board.is_check():
            print("VOCÊ ESTÁ EM CHEQUE! ")

        if board.is_checkmate():
            print("CHECKMATE DO BRAÇO!! O JOGO ACABOU. ")
            break
    else:
        print("CHECKMATE DO PLAYER!! O JOGO ACABOU. ")
        break
