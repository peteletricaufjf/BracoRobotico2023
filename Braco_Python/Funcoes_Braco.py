import serial

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

def confere(serBraco):
    opa = 'hugostoso'
    while True:
        opa = str(serBraco.readline())
        # print(opa[2])
        if opa[2] == '1':
            serBraco.flush()
            break

def seComeu(serBraco,pacman,jogada2):
    if pacman is True:
        # Manda o braço subir somente o eixo z para evitar de esbarrar nas peças
        coord = f"0, 0 , '200', 500, 500, 0"  # (angulo j1, angulo j2, posição z, vel, acel, eletroimã)
        serBraco.write(coord.encode())
        confere(serBraco)
    
        # Manda o braço ir até a peça que será removida do jogo
        coord = f"{jogada2[0]}, {jogada2[1]}, {'200'}, 500, 500, 0"
        serBraco.write(coord.encode())
        confere(serBraco)

        # Manda o braço descer somente o eixo z para encostar na peça
        coord = f"{jogada2[0]}, {jogada2[1]}, '50', 500, 500, 0"
        serBraco.write(coord.encode())
        confere(serBraco)

        # Mandar ativar o eletroimã
        coord = f"{jogada2[0]}, {jogada2[1]}, '50', 500, 500, 1"
        serBraco.write(coord.encode())
        confere(serBraco)

        # Manda o braço subir somente o eixo z antes de mover a peça
        coord = f"{jogada2[0]}, {jogada2[1]}, '200', 500, 500, 1"
        serBraco.write(coord.encode())
        confere(serBraco)

        # Manda o braço levar a peça para fora do jogo
        coord = f"'x', 'y' , '200', 500, 500, 1"
        serBraco.write(coord.encode())
        confere(serBraco)

        # Manda soltar a peça
        coord = f"'x', 'y' , '200', 500, 500, 0"
        serBraco.write(coord.encode())
        confere(serBraco)
    else
        continue

def movimentaPeca(jogada1,jogada2):
    # Manda o braço subir somente o eixo z para evitar de esbarrar nas peças
    coord = f"0, 0 , '200', 500, 500, 0"
    serBraco.write(coord.encode())
    confere(serBraco)

    # Manda o braço ir até a peça que será mexida 
    coord = f"{jogada1[0]}, {jogada1[1]}, '200', 500, 500, 0"
    serBraco.write(coord.encode())
    confere(serBraco)
      
    # Manda o braço descer somente o eixo z para encostar na peça
    coord = f"{jogada1[0]}, {jogada1[1]}, '50', 500, 500, 0"
    serBraco.write(coord.encode())
    confere(serBraco)

    # Mandar ativar o eletroimã
    coord = f"{jogada1[0]}, {jogada1[1]}, '50', 500, 500, 1"
    serBraco.write(coord.encode())
    confere(serBraco)

    # Manda o braço subir somente o eixo z antes de mover a peça
    coord = f"{jogada1[0]}, {jogada1[1]}, '200', 500, 500, 1"
    serBraco.write(coord.encode())
    confere(serBraco)

    # Manda o braço levar a peça pra casa desejada 
    coord = f"{jogada2[0]}, {jogada2[1]}, '200', 500, 500, 1"
    serBraco.write(coord.encode())
    confere(serBraco)

    # Manda o braço descer somente o eixo z para colocar a peça no lugar
    coord = f"{jogada2[0]}, {jogada2[1]}, '200', 500, 500, 1"
    serBraco.write(coord.encode())
    confere(serBraco)

    # Manda soltar a peça
    coord = f"{jogada2[0]}, {jogada2[1]}, '200', 500, 500, 0"
    serBraco.write(coord.encode())
    confere(serBraco)

    # Manda o braço para uma posição inicial
    coord = f"0, 0, '200', 500, 500, 0"
    serBraco.write(coord.encode())
    confere(serBraco)

def movimentaPecaTeste(serBraco):
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