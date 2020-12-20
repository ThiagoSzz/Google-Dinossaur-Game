#coding = utf-8

""" Módulos """
import pygame
import pygame_menu

from random import randint
from datetime import datetime

""" Classes """

class Dinossauro:
    """
    Classe que contém a inicialização de dados e métodos utilizados durante o programa referentes ao dinossauro
    """

    def __init__(self):
        """
        Método responsável pela inicialização das variáveis uteis ao controle do dinossauro
        """

        self.ta_pulando = False # representa o estado de pulo do dinossauro
        self.ta_subindo = False # representa o estado de subida durante o pulo do dinossauro
        self.ta_descendo = False # representa o estado de descida durante o pulo do dinossauro
        self.quer_descer = False # representa o estado que indica a decisão do usuário de cessar o pulo

        self.nao_bateu = True # representa o estado de colisão entre o dinossauro e os cactos

        self.velocidade = 6 # velocidade do dinossauro

        self.img = pygame.image.load('data/dino.png') # imagem que representa o dinossauro
        self.rect = self.img.get_rect()
        self.rect.x = 160
        self.rect.y = 500

    def movimentacao(self):
        """
        Método responsável pela movimentação do dinossauro (pular e cessar pulo) durante o jogo
        """

        comandos = pygame.key.get_pressed()

        if(comandos[pygame.K_UP] and self.rect.y == 500): # se o usuário entrar com 'UP BUTTON' -> pular
            self.ta_pulando = True
            self.ta_subindo = True

        if(comandos[pygame.K_DOWN] and self.rect.y <= 500): # se o usuário entrar com 'DOWN BUTTON' -> cessar pulo
            self.quer_descer = True

        if(self.ta_pulando):
            if(self.ta_subindo and (not self.quer_descer)): # fase 1 do pulo -> subida
                if(self.rect.y <= 360):
                    self.ta_descendo = True
                    self.ta_subindo = False
                else:
                    self.rect.y -= self.velocidade**2/8
            elif(self.ta_descendo or self.quer_descer): # fase 2 do pulo -> descida
                if(self.rect.y >= 500):
                    self.ta_descendo = False
                    self.ta_pulando = False
                    self.quer_descer = False
                    self.rect.y = 500
                else:
                    if(self.quer_descer): # se o usuário cessar o pulo, irá descer mais rapidamente
                        divisor = 4
                    else:
                        divisor = 8

                    self.rect.y += self.velocidade**2/divisor
        
    def checa_colisao(self, cacto):
        """
        Método responsável pela checagem de colisão entre o dinossauro e os cactos

        :param x_cacto: posição 'x' do cacto no mapa
        :param y_cacto: posição 'y' do cacto no mapa
        """

        if(self.rect.colliderect(cacto.rect)):
            self.nao_bateu = False

class Cactos:
    """
    Classe que contém a inicialização de dados e métodos utilizados durante o programa referentes aos cactos
    """

    def __init__(self, x, img):
        """
        Método responsável pela inicialização das variáveis uteis ao controle do cacto

        :param x: posição 'x' do cacto
        :param img: imagem que representa o cacto
        """

        self.x_inicial = x # posição inicial 'x' do cacto
        
        self.img = pygame.image.load(img) # imagem que representa o cacto
        self.rect = self.img.get_rect()
        self.rect.x = x
        self.rect.y = 460

    def atualiza_posicao(self, atual, lista_cactos, x_dino, velocidade_cactos):
        """
        Método responsável por atualizar os cactos que irão aparecer no jogo

        :param atual: cacto sendo iterado no 'for loop'
        :param lista_cactos: lista contendo os objetos dos cactos utilizados
        :param x_dino: posição 'x' do dinossauro para checar se deve re-alocar o cacto
        :param velocidade_cactos: a velocidade atual dos cactos em relação ao dinossauro
        """

        aumento_dist_velocidade = 20 # incremento de distância utilizado em relação à velocidade do cacto

        if(self.rect.x+50 <= x_dino-150): # se o cacto estiver fora da janela do jogo, e
            if(atual != 0): # se não for o primeiro cacto da lista de objetos de cactos
                cacto_anterior = lista_cactos[atual-1].rect.x # a posição 'x' do cacto anterior será dada pela posição de 'cacto-1',
            else: # senão,
                cacto_anterior = lista_cactos[len(lista_cactos)-1].rect.x # a posição 'x' do cacto anterior será dada pela posição do último cacto da lista

            # gera a nova posição 'x' do cacto que sumiu da tela levando em consideração a posição do cacto anterior
            self.rect.x = cacto_anterior + randint(int(300 + aumento_dist_velocidade*velocidade_cactos), int(600 + aumento_dist_velocidade*velocidade_cactos))

""" Funções """

def atualiza_cabecalho(pontos, velocidade, msg, cor):
    """
    Função responsável pela atualização do cabeçalho do jogo, que contém a pontuação do jogador atual,
    a velocidade dos cactos em relação ao dinossauro e uma mensagem qualquer a ser passada ao jogador

    :param pontos: pontuação do jogador
    :param velocidade: velocidade dos cactos em relação ao dinossauro
    :param msg: mensagem a ser passada para o jogador (pode não ter mensagem)
    :param cor: cor da mensagem (se for dia, cor será cinza; se for noite, cor será branco)
    """
    
    # imprime a pontuação
    jogo_janela.blit(txt_pontuacao.render(f'Pontuação: {int(pontos)}', False, cor), (10, 10))
    # imprime a velocidade dos cactos
    jogo_janela.blit(txt_pontuacao.render('Velocidade: {:.2f}'.format(velocidade), False, cor), (10, 35))
    #imprime a mensagem
    jogo_janela.blit(txt_pontuacao.render(f'{msg}', False, cor), (10, 60))
    #imprime o nome do jogo
    jogo_janela.blit(txt_pontuacao.render('Google Dinossaur Game', False, cor), (520, 10))

def atualiza_tela(qtd_cenarios, qtd_cactos, lista_cenarios, x_cenarios, lista_cactos, dino='menu'):
    """
    Função responsável pela atualização da tela (irá atualizar a posição do dinossauro, dos cactos e do
    cenário do jogo)

    :param qtd_cenarios: quantidade de cenários utilizada no jogo
    :param qtd_cactos: quantidade de cactos utilizada no jogo
    :param lista_cenarios: lista contendo as superfícies (imagens do pygame) dos cenários
    :param x_cenarios: lista com as posições 'x' atuais dos cenários
    :param lista_cactos: lista contendo os objetos dos cactos
    :param dino: objeto do dinossauro ou string 'menu' indicando que o cenário será utilizado como background do menu
    """

    for cenario in range(0, qtd_cenarios): # itera os cenários
        # e atualiza-os na tela
        jogo_janela.blit(lista_cenarios[cenario], (x_cenarios[cenario], 0))

    for cacto_atual in range(0, qtd_cactos): # itera os cactos
        # e atualiza-os na tela
        jogo_janela.blit(lista_cactos[cacto_atual].img, lista_cactos[cacto_atual].rect)

    if(dino != 'menu'): # se não for durante o menu,
        jogo_janela.blit(dino.img, dino) # atualiza a posição do dinossauro na tela

def menu(x_cenarios, lista_cenarios, qtd_cenarios, lista_cactos, qtd_cactos):
    """
    Função responsável pela apresentação do menu inicial do jogo

    :param x_cenarios: lista com as posições 'x' atuais dos cenários
    :param lista_cenarios: lista contendo as superfícies (imagens do pygame) dos cenários
    :param lista_cactos: lista contendo os objetos dos cactos
    :param qtd_cactos: quantidade de cactos utilizada no jogo

    :return: estado da janela (caso o usuário decida fechar o jogo antes de começar)
    """

    menu_aberto = True # estado do menu
    janela_aberta = True # estado da janela
    img_menu = pygame.image.load('data/dino_grande.png') # imagem que representa o dinossauro grande apresentado no menu
    txt_menu = pygame.font.SysFont('PressStart2P', 91) # inicializa uma fonte que será utilizada e seu tamanho
    txt_menu_menor = pygame.font.SysFont('PressStart2P', 25) # inicializa uma fonte que será utilizada e seu tamanho

    pygame.mixer.music.load('data/menu.mp3') # música tocada durante a apresentação do menu
    pygame.mixer.music.play(loops=-1) # inicia a música

    timer = 0 # timer para a animação de 'blink' do texto 'Jogar'
    wait = False # variável auxiliar do timer acima

    while menu_aberto:

        pygame.time.delay(20)

        for event in pygame.event.get(): # se o usuário decidir fechar a janela
            if(event.type == pygame.QUIT):
                janela_aberta = False # a janela do jogo será fechada e
                menu_aberto = False # o menu será encerrado

        comandos = pygame.key.get_pressed()

        if(comandos[pygame.K_RETURN]): # se o usuário pressionar 'ENTER', inicia o jogo e
            menu_aberto = False # fecha o menu

        for cenario in range(0, qtd_cenarios): # faz passar os cenários na tela
            if(x_cenarios[cenario] <= -763):
                x_cenarios[cenario] = 763

            x_cenarios[cenario] -= 10

        for cacto_atual in range(0, qtd_cactos): # faz passar os cactos na tela
            if(cacto[cacto_atual].rect.x <= -50):
                cacto[cacto_atual].rect.x = randint(763, 1500)

            cacto[cacto_atual].rect.x -= 10.5

        # atualiza a tela com as informações modificadas acima
        atualiza_tela(qtd_cenarios, qtd_cactos, lista_cenarios, x_cenarios, lista_cactos)

        # imprime o nome do jogo
        jogo_janela.blit(txt_menu.render('Google Dinossaur Game', True, (80, 80, 80)), (16, 184))
        # imprime o texto para iniciar o jogo
        jogo_janela.blit(txt_menu_menor.render('Press ENTER to start', True, (80, 80, 80)), (280, 430))
        # imprime as configurações de teclas padrão
        jogo_janela.blit(txt_menu_menor.render('UP: Pula', False, (80, 80, 80)), (330, 455))
        jogo_janela.blit(txt_menu_menor.render('DOWN: Desce', False, (80, 80, 80)), (306, 480))

        timer += 1 # incrementa o timer em uma unidade
        if(timer != 25 and not wait): # após 24 ticks,
            jogo_janela.blit(txt_menu.render('Jogar', True, (80, 80, 80)), (280, 350)) # faz o efeito 'blink' no texto 'Jogar'
        else:
            timer = 0 # zera o timer
            wait = not wait # aumenta o tempo da animação de 'blink'

        jogo_janela.blit(img_menu, (382-64, 40)) # imprime o dinossauro grande ao topo do menu
        pygame.display.update() # atualiza a tela
    
    for cacto_atual in range(0, qtd_cactos): # ao encerrar o menu, reinicializa as posições 'x' dos cactos
        cacto[cacto_atual].rect.x = cacto[cacto_atual].x_inicial

    pygame.mixer.music.stop() # encerra a música tocada durante a apresentação do menu

    return janela_aberta # retorna o estado da janela

dino = Dinossauro() # criação do objeto que representará o dinossauro

cacto = list() # cria a lista dos objetos de cactos
cacto.append(Cactos(x=736, img='data/cacto1.png')) # inclui cacto
cacto.append(Cactos(x=1400, img='data/cacto2.png')) # inclui cacto

cactos_velocidade_inicial = 6
cactos_velocidade = cactos_velocidade_inicial
qtd_cactos = len(cacto)
incremento_velocidade = 0.0003 # incremento da velocidade conforme a progressão do jogo

musica_tocando = False

x_cenarios = [0, 763]
cenarios = [pygame.image.load('data/fundo1.png'), pygame.image.load('data/fundo2.png')] # imagens do cenário
qtd_cenarios = len(cenarios)

dia = 1 # contador de dias/noites
periodo_noite = False # representa o estado que indica se está de noite
tempo_anoitecer = 38 # tempo levado para anoitecer e para voltar ao dia
mudar_periodo = False

jogo_janela = pygame.display.set_mode((763, 640)) # janela de tamanho 763x640
pygame.display.set_icon(dino.img)
pygame.display.set_caption('Google Dinossaur Game')

pygame.init() 

# apresenta o menu do jogo
janela_aberta = menu(x_cenarios=x_cenarios, lista_cenarios=cenarios, qtd_cenarios=qtd_cenarios, lista_cactos=cacto, qtd_cactos=qtd_cactos)

# inicia o timer
tempo_inicial = datetime.now().strftime("%H %M %S").split()
tempo_inicial = int(tempo_inicial[0])*3600 + int(tempo_inicial[1])*60 + int(tempo_inicial[2])

pygame.font.init()
pontuacao = 0 # pontuação inicial do jogador
soma_pontuacao = True
txt_pontuacao = pygame.font.SysFont('PressStart2P', 30)
cor = (80, 80, 80) # cor cinza

mensagem = 'Iniciando... Boa sorte!' # mensagem inicial do jogo

while janela_aberta: # loop principal do jogo

    # contabiliza o tempo passado até o momento
    tempo_final = datetime.now().strftime("%H %M %S").split()
    tempo_final = int(tempo_final[0])*3600 + int(tempo_final[1])*60 + int(tempo_final[2])
    
    # verifica se o usuário quer fechar a janela
    for event in pygame.event.get():
        if(event.type == pygame.QUIT):
            janela_aberta = False

    # método de movimentação do dinossauro
    dino.movimentacao()

    # atualiza a posição do cenário
    # no jogo, os cactos e o cenário se movem em direção à esquerda ('x' diminui)
    # e o dinossauro apenas é movimentado para cima e para baixo ('y' aumenta/diminui)
    for cenario in range(0, qtd_cenarios):
        if(x_cenarios[cenario] <= -763):
            x_cenarios[cenario] = 763

        x_cenarios[cenario] -= cactos_velocidade

    # atualiza a posicao dos cactos
    # se o cacto sumir da tela, será 're-spawnado'
    for cacto_atual in range(0, qtd_cactos):
        cacto[cacto_atual].atualiza_posicao(atual=cacto_atual, lista_cactos=cacto, x_dino=dino.rect.x, velocidade_cactos=cactos_velocidade)
        cacto[cacto_atual].rect.x -= cactos_velocidade

        # checa se o dinossauro e o cacto mais próximo colidiram
        dino.checa_colisao(cacto=cacto[cacto_atual])

    # atualiza os itens da tela (dinossauro, cactos e cenário)
    atualiza_tela(qtd_cenarios=qtd_cenarios, qtd_cactos=qtd_cactos, lista_cenarios=cenarios, x_cenarios=x_cenarios, lista_cactos=cacto, dino=dino)
    # atualiza o cabeçalho do jogo (pontuação, velocidade dos cactos e mensagem)
    atualiza_cabecalho(pontos=pontuacao, velocidade=cactos_velocidade, msg=mensagem, cor=cor)

    if(dino.nao_bateu): # se não houver colisão dinossauro-cacto,
        pygame.time.delay(1) # atualiza a tela a cada 1ms
        pygame.display.update() # atualiza a tela;
    else: # senão, reinicializa as variáveis
        mensagem = 'Você perdeu! Recomeçando...'
        musica_tocando = False

        pygame.mixer.music.load('data/colidiu.mp3') # som de 'batida' do dinossauro no cacto
        pygame.mixer.music.play(start=4.7)

        # reinicializa o timer
        tempo_inicial = datetime.now().strftime("%H %M %S").split()
        tempo_inicial = int(tempo_inicial[0])*3600 + int(tempo_inicial[1])*60 + int(tempo_inicial[2])

        nivel_atual = 0
        cactos_velocidade = cactos_velocidade_inicial
        pontuacao = 0

        for cacto_atual in range(0, qtd_cactos):
            cacto[cacto_atual].rect.x = cacto[cacto_atual].x_inicial

        dino.ta_pulando = False
        dino.ta_subindo = False
        dino.ta_descendo = False
        dino.rect.y = 500

        periodo_noite = False
        mudar_periodo = True
        dia = 1
        dino.nao_bateu = True

    cactos_velocidade += incremento_velocidade # incrementa a velocidade dos cactos por 'incremento_velocidade'
    pontuacao += 0.1 # aumenta a pontuação do jogador

    if(tempo_final - tempo_inicial >= 3 and (not musica_tocando)): # inicializar a música principal do jogo
        mensagem = ''
        musica_tocando = True
        pygame.mixer.music.load('data/soundtrack.mp3')
        pygame.mixer.music.play(loops=-1)

    if(tempo_final - tempo_inicial >= dia*tempo_anoitecer): # verifica se está na hora de mudar o cenário
        dia += 1 
        periodo_noite = not periodo_noite
        mudar_periodo = True

    # mudança de cenário dia->noite e vice-versa
    if(not periodo_noite and mudar_periodo): # cenário de dia, contendo as imagens adaptadas
        dino.img = pygame.image.load('data/dino.png')

        for cacto_atual in range(0, qtd_cactos):
            cacto[cacto_atual].img = pygame.image.load('data/cacto' + str(cacto_atual+1) + '.png')

        for cenario in range(0, qtd_cenarios):
            cenarios[cenario] = pygame.image.load('data/fundo' + str(cenario+1) + '.png')

        cor = (80, 80, 80)
        mudar_periodo = False
        incremento_velocidade = 0.0003 # o incremento da velocidade dos cactos ao dia é de 0.0003
    elif(periodo_noite and mudar_periodo): # cenário de noite, contendo as imagens adaptadas
        dino.img = pygame.image.load('data/n_dino.png')
        
        for cacto_atual in range(0, qtd_cactos):
            cacto[cacto_atual].img = pygame.image.load('data/n_cacto' + str(cacto_atual+1) + '.png')

        for cenario in range(0, qtd_cenarios):
            cenarios[cenario] = pygame.image.load('data/n_fundo' + str(cenario+1) + '.png')

        cor = (255, 255, 255)
        mudar_periodo = False
        incremento_velocidade = -0.00005 # à noite, a velocidade dos cactos diminui 0.00005
        
pygame.quit() # encerra a janela
