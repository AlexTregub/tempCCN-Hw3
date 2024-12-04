##### Alex Tregub
##### 2024-12-04
##### gameServer.py
##### ===========
##### Demonstrates socket-wise connections using base code by Dr. Giovanni Villalobos-Herrera
#####     for Computer Communication networks course Fall 2024.
##### - NEEDS 'FreeSansBold.ttf' file in working dir for text to display.
##### VERSION=v1.0.4
##### ===========
import threading
import pygame
import socket
import sys
import random as r
from time import time as time
from time import sleep

r.seed(time())
name = "test"
posx = 300
posy = 200
USER_SPEED = 20
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 400
RESET_GAME = False
GAME_SHUTDOWN = False

PORT = 5000

def GameThread():
    while(True):
        global USER_SPEED
        global RESET_GAME
        global posx 
        global posy 

        posx= SCREEN_WIDTH/2
        posy = SCREEN_HEIGHT/2

        USER_SPEED = 20
        pygame.init()
        background = (204, 230, 255)
        shapeColor = (0, 51, 204)
        shapeColorOver = (255, 0, 204)

        fps = pygame.time.Clock()
        screen_size = screen_width, screen_height = SCREEN_WIDTH, SCREEN_HEIGHT
        rect2 = pygame.Rect(int(SCREEN_WIDTH/2), 0, 25, 25)
        rect1 = pygame.Rect(0, 0, 50, 50)
        screen = pygame.display.set_mode(screen_size)
        pygame.display.set_caption('CCN Hw3 Bucket-Catch game')

        font = pygame.font.Font("FreeSansBold.ttf",25)

        score = 0
        levelScore = score
        boxSpeed = 1
        scoreMult = 5
        levelCounter = 0
        catcherSize = 50

        colorRect = (shapeColor)
        colorRect2 = (shapeColorOver)
        
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if GAME_SHUTDOWN:
                pygame.quit()
                sys.exit()

            screen.fill(background)

            text = font.render("Score: "+str(score)+"   "+"Level: "+str(levelCounter),True,(0,0,0),background)
            textRect = text.get_rect()
            textRect.center = (SCREEN_WIDTH//2,15)

            screen.blit(text,textRect)

            # oldBoxSpeed = boxSpeed
            # boxSpeed = 1 + int(score/scoreMult)

            # if boxSpeed == oldBoxSpeed+1:
            #     scoreMult+=1

            #print("box speed",boxSpeed)

            #rect2.move_ip(0,1) # Moves collision-able rectangle down
            if not screen.get_rect().contains(rect2):
                #print("Collided with edge")

                print("Game over")

                text1 = font.render("Game over, (r) to restart.",True,(0,0,0),background)
                textRect1 = text1.get_rect()
                textRect1.center = (SCREEN_WIDTH//2,SCREEN_HEIGHT//2)

                screen.blit(text1,textRect1)
                pygame.display.update()

                while(not RESET_GAME):
                    sleep(0.1)
                    if (RESET_GAME):
                        RESET_GAME = False
                        break

                break
            else:
                rect2.move_ip(0,boxSpeed)

            

            rect1.center = (posx, posy)
            collision = rect1.colliderect(rect2)
            pygame.draw.rect(screen, colorRect, rect1)
            if collision:
                pygame.draw.rect(screen, colorRect2, rect2, 6, 1)
                rect2.update(r.randint(0,screen_width-75),0,25,25) # Updates to random position
            
                score += 1 # Increases score
                levelScore += 1
                print("Score:"+str(score))

                if not (levelScore % scoreMult):
                    print("Increasing speeds")
                    boxSpeed += 1
                    scoreMult += 1
                    levelScore = 0
                    levelCounter += 1

                    USER_SPEED += levelCounter*2
                    catcherSize = catcherSize + levelCounter
                    rect1.update(posx,posy,catcherSize,50)
            else:
                pygame.draw.rect(screen, colorRect, rect2, 6, 1)
            pygame.display.update()
            fps.tick(30)


    pygame.quit()


def ServerThread():
    global GAME_SHUTDOWN
    global RESET_GAME 
    global posy
    global posx
    # get the hostname
    host = socket.gethostbyname(socket.gethostname())
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    host = s.getsockname()[0]
    s.close()
    print(host)
    port = PORT  # initiate port no above 1024

    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together
    print("Server enabled...")
    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))    
    while True:        
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(1024).decode()
        if not data:
            # if data is not received break
            GAME_SHUTDOWN = True
            break
        
        print("from connected user: " + str(data))
        if(data == 'w'):
            RESET_GAME = False
            posy -= USER_SPEED
            if posy <= 0: posy=0
        if(data == 's'):
            RESET_GAME = False
            posy += USER_SPEED
            if posy >= SCREEN_HEIGHT: posy = SCREEN_HEIGHT
        if(data == 'a'):
            RESET_GAME = False
            posx -= USER_SPEED
            if posx <= 0: posx = 0
        if(data == 'd'):
            RESET_GAME = False
            posx += USER_SPEED
            if posx >= SCREEN_WIDTH: posx = SCREEN_WIDTH

        if(data == 'r'):
            RESET_GAME = True
            if not (RESET_GAME):
                print("Restarting...")

        # if (data == 'q'):
        #     conn.close()

        #     exit(0)

    conn.close()  # close the connection


t1 = threading.Thread(target=GameThread, args=[])
t2 = threading.Thread(target=ServerThread, args=[])
t1.start()
t2.start()