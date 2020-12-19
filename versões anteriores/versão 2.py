#coding = utf-8

# to-do list:
#
# otimizações

import pygame
import pygame_menu

from random import randint
from datetime import datetime

class Dinossauro:
    def __init__(self):
        self.ta_pulando = False
        self.ta_subindo = False
        self.ta_descendo = False
        self.quer_descer = False

        self.nao_bateu = True

        self.x = 160
        self.y = 640
        self.velocidade = 6

        self.img = pygame.image.load('data/dino.png')

    def movimentacao(self):
        comandos = pygame.key.get_pressed()

        if(comandos[pygame.K_UP] and self.y == 640):
            self.ta_pulando = True
            self.ta_subindo = True

        if(comandos[pygame.K_DOWN] and self.y <= 640):
            self.quer_descer = True

        if(self.ta_pulando):
            if(self.ta_subindo and (not self.quer_descer)):
                if(self.y <= 500):
                    self.ta_descendo = True
                    self.ta_subindo = False
                else:
                    self.y -= self.velocidade**2/8
            elif(self.ta_descendo or self.quer_descer):
                if(self.y >= 640):
                    self.ta_descendo = False
                    self.ta_pulando = False
                    self.quer_descer = False
                    self.y = 640
                else:
                    if(self.quer_descer):
                        divisor = 4
                    else:
                        divisor = 8

                    self.y += self.velocidade**2/8
        
    def checa_colisao(self, x_cacto, y_cacto):
        if(self.y-60 >= y_cacto+35 and (self.x+42 >= x_cacto and self.x <= x_cacto+45)):
            self.nao_bateu = False
        

class Cactos:
    def __init__(self, x, img):
        self.x = x
        self.y = 460

        self.x_inicial = x
        
        self.img = pygame.image.load(img)

    def atualiza_posicao(self, atual, lista_cactos, x_dino, velocidade_cactos):

        aumento_dist_velocidade = 20

        if(self.x+50 <= x_dino-150):
            if(atual != 0):
                cacto_anterior = lista_cactos[atual-1].x
            else:
                cacto_anterior = lista_cactos[atual+1].x

            self.x = cacto_anterior + randint(int(300 + aumento_dist_velocidade*velocidade_cactos), int(600 + aumento_dist_velocidade*velocidade_cactos))

def atualiza_cabecalho(pontos, velocidade, msg, cor):
    jogo_janela.blit(txt_pontuacao.render(f'Pontuação: {int(pontos)}', False, cor), (10, 10))
    jogo_janela.blit(txt_pontuacao.render('Velocidade: {:.2f}'.format(velocidade), False, cor), (10, 35))
    jogo_janela.blit(txt_pontuacao.render(f'{msg}', False, cor), (10, 60))
    jogo_janela.blit(txt_pontuacao.render('Google Dinossaur Game', False, cor), (520, 10))

def atualiza_tela(qtd_cenarios, qtd_cactos, lista_cenarios, x_cenarios, lista_cactos, dino='menu'):

    for cenario in range(0, qtd_cenarios):
        jogo_janela.blit(lista_cenarios[cenario], (x_cenarios[cenario], 0))

    for cacto_atual in range(0, qtd_cactos):
        jogo_janela.blit(lista_cactos[cacto_atual].img, (lista_cactos[cacto_atual].x, lista_cactos[cacto_atual].y))

    if(dino != 'menu'):
        jogo_janela.blit(dino.img, (dino.x, dino.y-140))

def menu(x_cenarios, lista_cenarios, qtd_cenarios, lista_cactos, qtd_cactos):

    menu_aberto = True
    janela_aberta = True
    img_menu = pygame.image.load('data/dino_grande.png')
    txt_menu = pygame.font.SysFont('PressStart2P', 91)
    txt_menu_menor = pygame.font.SysFont('PressStart2P', 25)

    pygame.mixer.music.load('data/menu.mp3')
    pygame.mixer.music.play(loops=-1)

    timer = 0
    wait = False

    while menu_aberto:

        pygame.time.delay(20)

        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                janela_aberta = False
                menu_aberto = False

        comandos = pygame.key.get_pressed()

        if(comandos[pygame.K_RETURN]):
            menu_aberto = False
            sair_menu = True

        for cenario in range(0, qtd_cenarios):
            if(x_cenarios[cenario] <= -763):
                x_cenarios[cenario] = 763

            x_cenarios[cenario] -= 10

        for cacto_atual in range(0, qtd_cactos):
            if(cacto[cacto_atual].x <= -50):
                cacto[cacto_atual].x = randint(763, 1500)

            cacto[cacto_atual].x -= 10.5

        atualiza_tela(qtd_cenarios, qtd_cactos, lista_cenarios, x_cenarios, lista_cactos)

        jogo_janela.blit(txt_menu.render('Google Dinossaur Game', True, (80, 80, 80)), (16, 184))
        jogo_janela.blit(txt_menu_menor.render('[ENTER] para selecionar', True, (80, 80, 80)), (266, 430))
        jogo_janela.blit(txt_menu_menor.render('UP: Pula', False, (80, 80, 80)), (330, 455))
        jogo_janela.blit(txt_menu_menor.render('DOWN: Desce', False, (80, 80, 80)), (306, 480))

        timer += 1
        if(timer != 25 and not wait):
            jogo_janela.blit(txt_menu.render('Jogar', True, (80, 80, 80)), (280, 350))
        else:
            timer = 0
            wait = not wait

        jogo_janela.blit(img_menu, (382-64, 40))
        pygame.display.update()
    
    for cacto_atual in range(0, qtd_cactos):
        cacto[cacto_atual].x = cacto[cacto_atual].x_inicial

    pygame.mixer.music.stop()

    return janela_aberta

dino = Dinossauro()

cacto = list()
cacto.append(Cactos(x=736, img='data/cacto1.png'))
cacto.append(Cactos(x=1400, img='data/cacto2.png'))

cactos_velocidade_inicial = 6
cactos_velocidade = cactos_velocidade_inicial
qtd_cactos = len(cacto)
incremento_velocidade = 0.0003

musica_tocando = False

x_cenarios = [0, 763]
cenarios = [pygame.image.load('data/fundo1.png'), pygame.image.load('data/fundo2.png')]
qtd_cenarios = len(cenarios)

dia = 1
periodo_noite = False
tempo_anoitecer = 38
mudar_periodo = False

jogo_janela = pygame.display.set_mode((763, 640))
pygame.display.set_icon(dino.img)
pygame.display.set_caption('Google Dinossaur Game')

pygame.init()

janela_aberta = menu(x_cenarios=x_cenarios, lista_cenarios=cenarios, qtd_cenarios=qtd_cenarios, lista_cactos=cacto, qtd_cactos=qtd_cactos)

tempo_inicial = datetime.now().strftime("%H %M %S").split()
tempo_inicial = int(tempo_inicial[0])*3600 + int(tempo_inicial[1])*60 + int(tempo_inicial[2])

pygame.font.init()
pontuacao = 0
soma_pontuacao = True
txt_pontuacao = pygame.font.SysFont('PressStart2P', 30)
cor = (80, 80, 80)

fps = pygame.time.Clock()

mensagem = 'Iniciando... Boa sorte!'

while janela_aberta:

    tempo_final = datetime.now().strftime("%H %M %S").split()
    tempo_final = int(tempo_final[0])*3600 + int(tempo_final[1])*60 + int(tempo_final[2])
    
    pygame.time.delay(1)
    
    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            janela_aberta = False

    dino.movimentacao()

    for cenario in range(0, qtd_cenarios):
        if(x_cenarios[cenario] <= -763):
            x_cenarios[cenario] = 763

        x_cenarios[cenario] -= cactos_velocidade

    for cacto_atual in range(0, qtd_cactos):
        cacto[cacto_atual].atualiza_posicao(atual=cacto_atual, lista_cactos=cacto, x_dino=dino.x, velocidade_cactos=cactos_velocidade)
        cacto[cacto_atual].x -= cactos_velocidade

        dino.checa_colisao(x_cacto=cacto[cacto_atual].x, y_cacto=cacto[cacto_atual].y)

    atualiza_tela(qtd_cenarios=qtd_cenarios, qtd_cactos=qtd_cactos, lista_cenarios=cenarios, x_cenarios=x_cenarios, lista_cactos=cacto, dino=dino)
    atualiza_cabecalho(pontos=pontuacao, velocidade=cactos_velocidade, msg=mensagem, cor=cor)
    
    if(dino.nao_bateu):
        pygame.display.update()
    else:
        mensagem = 'Você perdeu! Recomeçando...'
        musica_tocando = False

        pygame.mixer.music.load('data/colidiu.mp3')
        pygame.mixer.music.play(start=4.7)

        tempo_inicial = datetime.now().strftime("%H %M %S").split()
        tempo_inicial = int(tempo_inicial[0])*3600 + int(tempo_inicial[1])*60 + int(tempo_inicial[2])

        nivel_atual = 0
        cactos_velocidade = cactos_velocidade_inicial
        pontuacao = 0

        for cacto_atual in range(0, qtd_cactos):
            cacto[cacto_atual].x = cacto[cacto_atual].x_inicial

        dino.ta_pulando = False
        dino.ta_subindo = False
        dino.ta_descendo = False
        dino.y = 640

        periodo_noite = False
        mudar_periodo = True
        dia = 1
        dino.nao_bateu = True

    cactos_velocidade += incremento_velocidade
    pontuacao += 0.1

    if(tempo_final - tempo_inicial >= 3 and (not musica_tocando)):
        mensagem = ''
        musica_tocando = True
        pygame.mixer.music.load('data/soundtrack.mp3')
        pygame.mixer.music.play(loops=-1)

    if(tempo_final - tempo_inicial >= dia*tempo_anoitecer):
        dia += 1 
        periodo_noite = not periodo_noite
        mudar_periodo = True

    if(not periodo_noite and mudar_periodo):
        dino.img = pygame.image.load('data/dino.png')

        for cacto_atual in range(0, qtd_cactos):
            cacto[cacto_atual].img = pygame.image.load('data/cacto' + str(cacto_atual+1) + '.png')

        for cenario in range(0, qtd_cenarios):
            cenarios[cenario] = pygame.image.load('data/fundo' + str(cenario+1) + '.png')

        cor = (80, 80, 80)
        mudar_periodo = False
        incremento_velocidade = 0.0003
    elif(periodo_noite and mudar_periodo):
        dino.img = pygame.image.load('data/n_dino.png')
        
        for cacto_atual in range(0, qtd_cactos):
            cacto[cacto_atual].img = pygame.image.load('data/n_cacto' + str(cacto_atual+1) + '.png')

        for cenario in range(0, qtd_cenarios):
            cenarios[cenario] = pygame.image.load('data/n_fundo' + str(cenario+1) + '.png')

        cor = (255, 255, 255)
        mudar_periodo = False
        incremento_velocidade = -0.00005
        
pygame.quit()