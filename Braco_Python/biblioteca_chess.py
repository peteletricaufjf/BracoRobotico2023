import chess
import chess.engine
from stockfish import Stockfish

# Seleciona a engine desejada e especifica o pathing de onde ela foi baixada
engine = chess.engine.SimpleEngine.popen_uci(r"D:\Arquivos\BracoRobotico2023\Braco_Python\stockfish-windows-x86-64-avx2\stockfish\stockfish-windows-x86-64-avx2.exe") 

# Inicializa o tabuleiro
board = chess.Board()


# ALGUNS CONCEITOS BÁSICOS PARA EU EXPLICAR PRA PRINCESA DA LAIS
"""
# Pega a jogada     
jogada_usuario = input("Qual foi o movimento feito pelo usuário? ")
    
# Inicializa um objeto move1 com o comando de movimento a partir da string de jogada "e2e4"(simulando jogada de humano que foi e2e4)
move1 = chess.Move.from_uci(jogada_usuario) 

# Atualiza o movimento no tabuleiro
board.push(move1) 
"""


# DIFICULDADE
"""
engine.configure({"Skill Level": 20})
"""


# COMO VERIFICAR SE O MOVIMENTO FOI LEGAL OU NÃO (TRUE OU FALSE)
"""
jogada_usuario = input("Qual foi o movimento feito pelo usuário?")
mov = chess.Move.from_uci(jogada_usuario)

while board.is_legal(mov) == False:
        jogada_usuario = input("Movimento inválido, digite novamente: ")
        mov = chess.Move.from_uci(jogada_usuario)
"""


"""
stockfish=Stockfish(r"D:\Arquivos\BracoRobotico2023\Braco_Python\stockfish-windows-x86-64-avx2\stockfish\stockfish-windows-x86-64-avx2.exe")
stockfish.set_depth(20)#How deep the AI looks
stockfish.set_skill_level(20)#Highest rank stockfish
stockfish.get_parameters()
"""


# PARTIDA
"""
while True:
        movb = engine.play(board, chess.engine.Limit(time=1))
        print(movb.move)
        
        if board.is_castling(movb.move) == True:
                input("Vai rolar o roque")
                
        if board.is_kingside_castling(movb.move) == True:
                input("Vai rolar o roque na ala do Rei")
                
        if board.is_queenside_castling(movb.move) == True:
                input("Vai rolar o roque na ala da Rainha")
                
        board.push(movb.move)
        # input("Pressione Enter para prosseguir")
        print(board)
        
        
        movp = engine.play(board, chess.engine.Limit(time=1))
        
        print(movp.move)
        if board.is_castling(movp.move) == True:
                input("Vai rolar o roque")
                
        if board.is_kingside_castling(movp.move) == True:
                input("Vai rolar o roque na ala do Rei")
                
        if board.is_queenside_castling(movp.move) == True:
                input("Vai rolar o roque na ala da Rainha")
                
        board.push(movp.move)
        # input("Pressione Enter para prosseguir")
        print(board)
"""
