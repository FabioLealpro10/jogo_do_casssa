
import pygame as pg
from pygame.locals import *
from random import randint as aleatorio
from sys import exit


resolu_x = 800
resolu_y = 600

tela = pg.display.set_mode((resolu_x,resolu_y))
nome = pg.display.set_caption('JOGO0001')


FUNDO = pg.transform.scale(pg.image.load('fundo.jpg'),(resolu_x,resolu_y))
cassa = pg.transform.scale(pg.image.load('cassa-removebg-preview.png'),(70,60))
missel = pg.transform.scale(pg.image.load('missil-removebg-preview.png'),(15,8))
alienigina = pg.transform.scale(pg.image.load('nave-removebg-preview.png'),(50,50))




# dados inciais dos jogador
jogo_em_andamento = True
local_cassa_X,local_cassa_Y = 70,200
mover_fundo = resolu_x
max_baixo = resolu_y - 60
max_frent = resolu_x - 70
missil_designado = False
cassa_destruido = False
qdt_cassa = 3
vidas_cassas = pg.transform.scale(pg.image.load('vidas_cassas-removebg-preview.png'),(15,30))

# dados iniciais do booot
local_y_do_aliem = aleatorio(0,600)
local_x_do_alin = 800
aliem_para_cima = True
alienigena_destruido = False
naves = 10
vidas_alie = pg.transform.scale(pg.image.load('nave-removebg-preview.png'),(15,15))
atake_alien_x = -1




velocidade_jogo = pg.time.Clock()
while jogo_em_andamento:
    velocidade_jogo.tick(30)
    resto = mover_fundo%resolu_x
    tela.blit(FUNDO,(resto-FUNDO.get_rect().width,0))
    if resto<resolu_x:
        tela.blit(FUNDO,(resto,0))
    mover_fundo-=1

    for x in range(qdt_cassa):
        tela.blit(vidas_cassas,(x*15+15,0))

    for x in range(naves):
        tela.blit(vidas_alie,(resolu_x-(x*15+15),0))


    for evet in pg.event.get():
        if evet.type == pg.QUIT:
            jogo_em_andamento = False

        if evet.type == KEYDOWN:
            if pg.key.get_pressed()[K_SPACE]:
                missil_designado = True


    if not(cassa_destruido):
        if pg.key.get_pressed()[K_UP]:
            local_cassa_Y -=4
            if local_cassa_Y<=0:
                local_cassa_Y = 0

        elif pg.key.get_pressed()[K_DOWN]:
            local_cassa_Y +=4
            if local_cassa_Y >= max_baixo:
                local_cassa_Y = max_baixo

        elif pg.key.get_pressed()[K_LEFT]:
            local_cassa_X -=4
            if local_cassa_X<=0:
                local_cassa_X = 0
        elif pg.key.get_pressed()[K_RIGHT]:
            local_cassa_X +=4
            if local_cassa_X>=max_frent:
                local_cassa_X = max_frent



    if not(missil_designado):
        missel_lX = local_cassa_X + 25
        missel_lY = local_cassa_Y + 30
    else:
        tela.blit(missel, (missel_lX, missel_lY))
        if missel_lX > resolu_x:
            missil_designado = False
        missel_lX +=15


    if not(cassa_destruido):
        tela.blit(cassa,(local_cassa_X,local_cassa_Y))

    # execução do aliem
    if not(alienigena_destruido):
        tela.blit(alienigina,(local_x_do_alin,local_y_do_aliem))
        if atake_alien_x<0:
            atake_alien_x,atake_alien_y = local_x_do_alin,local_y_do_aliem+20
        else:
            atake_alien = pg.draw.circle(tela, (250, 0, 0,), (atake_alien_x, atake_alien_y), 5)
            if local_cassa_Y< atake_alien_y <local_cassa_Y + 60 and local_cassa_X < atake_alien_x < local_cassa_X+70:
                cassa_destruido = True
                qdt_cassa -= 1
                if qdt_cassa == 0:
                    print('Perdeu')
                    jogo_em_andamento = False
                    exit()
                else:
                    cassa_destruido = False
                atake_alien_x = -1
            atake_alien_x -= 7
        tela.blit(alienigina, (local_x_do_alin, local_y_do_aliem))
        local_x_do_alin -=2
        if aliem_para_cima:
            local_y_do_aliem -= 1
        else:
            local_y_do_aliem +=1
        if local_x_do_alin<= -50:
            local_x_do_alin = resolu_x
            local_y_do_aliem = aleatorio(0,resolu_y)
        if local_y_do_aliem<=0:
            aliem_para_cima = False
        elif local_y_do_aliem>=(resolu_y-50):
            aliem_para_cima = True
    else:
        local_cassa_X += 4

    # colisão do fuguete com o aliem
    if (local_x_do_alin<(missel_lX-15)<(local_x_do_alin+50)) and (local_y_do_aliem <=missel_lY<=(local_y_do_aliem+50)):
        naves -=1
        missil_designado = False
        local_x_do_alin = resolu_x
        local_y_do_aliem = aleatorio(0, resolu_y)
        if naves == 0:
            alienigena_destruido = True


    if  (local_x_do_alin<(local_cassa_X+70)<(local_x_do_alin+50)) and (local_y_do_aliem <=local_cassa_Y<=(local_y_do_aliem+50)):
        local_cassa_X, local_cassa_Y = 70, 200
        qdt_cassa-=1
        naves -= 1
        missil_designado = False
        local_x_do_alin = resolu_x
        local_y_do_aliem = aleatorio(0, resolu_y)
        if naves == 0:
            alienigena_destruido = True
            #tela.blit(texto_j1,(70,100))
            #tela.blit(texto_j2,(70,250))
    pg.display.update()
    # original FLP