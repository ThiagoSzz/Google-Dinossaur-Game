#coding = utf-8

# to-do list:
#
# criar classes
# melhorar a pixel art
#    colocar montanhas
#    dia e noite
# pontuação
#    coletar "ossos" durante o mapa
# animação de movimento do dinossauro
# pássaros?
#    colisão pássaros
# menu para o jogo
# arrumar a coloração do dinossauro
# difícil: multi-player?

import time
import pygame

from random import randint
from datetime import datetime

janela_aberta = True

ta_pulando = False
ta_subindo = False
ta_descendo = False
quer_descer = False

musica_tocando = False

nao_bateu = True

x_dino = 160
y_dino = 640
velocidade = 6

x_cactos = [736, 1400]
y_cacto = 460
cacto_sumiu = True
cactos = [pygame.image.load('cacto1.png'), pygame.image.load('cacto2.png')]
qtd_cactos = 2
velocidade_cactos_inicial = 6
velocidade_cactos = velocidade_cactos_inicial

x_cenarios = [0, 763]
cenarios = [pygame.image.load('fundo1.png'), pygame.image.load('fundo2.png')]
qtd_cenarios = 2

dinossauro = pygame.image.load('dino.png')

jogo_janela = pygame.display.set_mode((763, 640))
pygame.display.set_icon(dinossauro)
pygame.display.set_caption('Google Dinossaur Game')

pygame.init()

tempo_inicial = datetime.now().strftime("%H %M %S").split()
tempo_inicial = int(tempo_inicial[0])*3600 + int(tempo_inicial[1])*60 + int(tempo_inicial[2])

pygame.font.init()
pontuacao = 0
soma_pontuacao = True
txt_pontuacao = pygame.font.SysFont('PressStart2P', 30)

mensagem = 'Iniciando... Boa sorte!'

while janela_aberta:

    pygame.time.delay(1)
    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            janela_aberta = False

    comandos = pygame.key.get_pressed()

    if(comandos[pygame.K_UP] and y_dino == 640):
        ta_pulando = True
        ta_subindo = True

    if(comandos[pygame.K_DOWN] and y_dino <= 640):
        quer_descer = True

    if(ta_pulando):
        if(ta_subindo and (not quer_descer)):
            if(y_dino <= 500):
                ta_descendo = True
                ta_subindo = False
            else:
                y_dino -= velocidade**2/8
        elif(ta_descendo or quer_descer):
            if(y_dino >= 640):
                ta_descendo = False
                ta_pulando = False
                quer_descer = False
                y_dino = 640
            else:
                if(quer_descer):
                    divisor = 4
                else:
                    divisor = 8

                y_dino += velocidade**2/divisor

    for cenario in range(0, qtd_cenarios):
        if(x_cenarios[cenario] <= -763):
            x_cenarios[cenario] = 763

    for cenario in range(0, qtd_cenarios):
        x_cenarios[cenario] -= velocidade

    for cacto in range(0, qtd_cactos):
        if(x_cactos[cacto]+50 <= x_dino-150):
            if(cacto != 0):
                cacto_anterior = x_cactos[cacto-1]
            else:
                cacto_anterior = x_cactos[cacto+1]

            x_cactos[cacto] = cacto_anterior + randint(400, 600)

    for cacto in range(0, qtd_cactos):
        x_cactos[cacto] -= velocidade_cactos

        if(y_dino-60 >= y_cacto+35 and (x_dino+42 >= x_cactos[cacto] and x_dino <= x_cactos[cacto]+45)):
            nao_bateu = False

    for cenario in range(0, qtd_cenarios):
        jogo_janela.blit(cenarios[cenario], (x_cenarios[cenario], 0))

    for cacto in range(0, qtd_cactos):
        jogo_janela.blit(cactos[cacto], (x_cactos[cacto], y_cacto))

    jogo_janela.blit(dinossauro, (x_dino, y_dino-140))
    
    jogo_janela.blit(txt_pontuacao.render(f'Pontuação: {int(pontuacao)}', False, (80, 80, 80)), (10, 10))
    jogo_janela.blit(txt_pontuacao.render('Velocidade: {:.1f}'.format(velocidade_cactos), False, (80, 80, 80)), (10, 35))
    jogo_janela.blit(txt_pontuacao.render(f'{mensagem}', False, (80, 80, 80)), (10, 60))
    
    if(nao_bateu):
        pygame.display.update()
    else:
        mensagem = 'Você perdeu! Recomeçando...'
        nao_bateu = True
        musica_tocando = False

        pygame.mixer.music.load('colidiu.mp3')
        pygame.mixer.music.play(start=4.7)

        tempo_inicial = datetime.now().strftime("%H %M %S").split()
        tempo_inicial = int(tempo_inicial[0])*3600 + int(tempo_inicial[1])*60 + int(tempo_inicial[2])

        nivel_atual = 0
        velocidade_cactos = velocidade_cactos_inicial
        pontuacao = 0

        x_cactos = [736, 1400]

        ta_pulando = False
        ta_subindo = False
        ta_descendo = False
        y_dino = 640

    tempo_final = datetime.now().strftime("%H %M %S").split()
    tempo_final = int(tempo_final[0])*3600 + int(tempo_final[1])*60 + int(tempo_final[2])

    velocidade_cactos += 0.0003
    pontuacao += 0.1

    if(tempo_final - tempo_inicial >= 3 and (not musica_tocando)):
        mensagem = ''
        musica_tocando = True
        pygame.mixer.music.load('soundtrack.mp3')
        pygame.mixer.music.play(loops=-1)
        
pygame.quit()