#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from turtle import *
from percursos import Waze

# add as seguintes bibliotecas
from utils import vector
from random import choice

class Agente:

    # inclui cor e tartaruta pro agente
    def __init__(self, id, tam_agente, cor1=None, cor2=None):
        # add uma identificação única pro agente
        self._id = id
        self._tam_agente = tam_agente

        # add uma tartaruga específica pro agente
        self._turtle = Turtle()
        self._turtle.hideturtle()

        # define a cor do agente
        self._cor1 = cor1
        self._cor2= cor2

        # REQ
        # deve definir a cor do agente aleatoriamente (verde, vermelho, rosa, laranja e marrom)
        # se não for passado no construtor
        # é um gerador de percursos

        self._waze = None

        #add os seguintes comandos
        ## TODO: Conferir estas direções
        #vector(1, 0) => direita
        #vector(-1, 0) => esquerda
        #vector(0, 1) => cima
        #vectorector(0, -1) => baixo
        self.direcao = vector(1,0) # este vector significa direita


    # adiciona um labirinto
    def add_labirinto(self, lab):
        self._labirinto = lab
        self._posicao = lab.cel_aleatoria()
        # REQ
        # Deve funcionar para passos menores que lab._tam_celula
        self.tam_passo = lab._tam_celula

    # Note que o nome do método mudou um pouco

    def ambulancia(self, cor1, cor2):
        self._turtle.pensize(1)
        self._turtle.color(cor1, cor2)
        self._turtle.pendown()
        self._turtle.begin_fill()
        self._turtle.forward(7)
        self._turtle.right(90)
        self._turtle.forward(3)
        self._turtle.right(90)
        self._turtle.forward(7)
        self._turtle.left(90)
        self._turtle.forward(7)
        self._turtle.right(90)
        self._turtle.forward(3)
        self._turtle.right(90)
        self._turtle.forward(7)
        self._turtle.left(90)
        self._turtle.forward(7)
        self._turtle.right(90)
        self._turtle.forward(3)
        self._turtle.right(90)
        self._turtle.forward(7)
        self._turtle.left(90)
        self._turtle.forward(7)
        self._turtle.right(90)
        self._turtle.forward(3)
        self._turtle.right(90)
        self._turtle.forward(7)
        self._turtle.left(90)
        self._turtle.end_fill()
        self._turtle.up()

    def desenhar_se(self, posicao=None):
        """ Leva a tartaruga até a posição (x,y) e desenha por exemplo um círculo
            para representar o agente (i.e., pacman, fantasmas)
        """
        self._turtle.clear()
        if (not posicao):
            posicao = self._posicao

        x, y = posicao.coord_turt_centralizada()
        self._turtle.up()
        self._turtle.goto(x, y)
        self._turtle.down()
        self.ambulancia(self._cor1, self._cor2)

    """ Métodos de percurso """

    def add_percurso(self):
        # Só na primeira vez que o agente não terá um _waze definido
        if (not self._waze):
            self._waze = Waze(self._labirinto) # Cria o objeto _waze passando uma referência do labirinto

    def percorrer(self):
        """ Percorrer significa seguir passar por todas as celulas do labirinto """
        pos_agente = self._posicao # Para melhorar a legibilidade

        self.add_percurso()
        if (self._waze.fim_percurso()): # Questiona se é fim de percurso
            self._waze = None # Se o percurso terminou, reinicializa o _waze
            return True # Se terminou, retorna indicando o término

        if (self._waze.esta_sem_coord()): # Se _waze está criado, mas sem coordenadas
            self._waze.gerar_percurso(pos_agente) # Gere um percurso

        if (not self._waze.esta_sem_coord()): # Se houver coordenadas a serem seguidas
            self._posicao = self._waze.obter_prox_coord() # Obtenha a próx e defina como a posição do agente
        self.desenhar_se() # Desenha o agente na posição em que se encontra

        return False # Se chegou até aqui é o porque não terminou o percurso e retorna False

    def vaguear(self):
        """ Vaguear significa continuar andando na mesma direção até que se
            encontre um obstáculo, quando se muda a direção aleatoriamente
        """
        '''        lab = self._labirinto
         # REQ
         # Deve obter o passo (sem efetivamente dar o passo)
        passo = self.prox_passo()
        lin_p, col_p= passo
        alin, acol= self._posicao.coord_turtle()
        prox_pos_agente= lab.criar_celula(coord_turt=[alin+ lin_p,acol + col_p])
        lin, col= prox_pos_agente.coord_matriz()
        id= self._id

        if lab.eh_caminho(lin, col) and not (lab.eh_celula_ocupada((lin, col), self._id)):
            self.posicao= prox_pos_agente
        else:
            prox_pos_agente= self._posicao
            self.direcao= self.mudar_direcao_aleatoriamente()

        self.desenhar_se()
        return'''

        lab = self._labirinto
        # REQ
        # Deve obter o passo (sem efetivamente dar o passo)
        passo = self.prox_passo()
        dx, dy = passo
        x, y = self._posicao.coord_turtle()  # ou .coord_turtle()
        prox_passo = lab.criar_celula(coord_turt=(x + dx, y + dy))
        lin, col = prox_passo.coord_matriz()

        if lab.eh_caminho(lin, col) and not (
        lab.eh_celula_ocupada((lin, col), self._id)):  # colocar numa variavel e comparar
            # nova_posicao = lab.criar_celula(coord_matr=(lin, col))
            self._posicao = prox_passo
        else:  # Caso contrário
            prox_passo = self._posicao
            self.direcao = self.mudar_direcao_aleatoriamente()
        # self._posicao = nova_posicao
        self.desenhar_se()


    def prox_passo(self):
        """ Obtém o próximo passo do agente na direção em que se encontra """
        dir_x = self.direcao[0] * self.tam_passo
        dir_y = self.direcao[1] * self.tam_passo

        passo = vector(dir_x, dir_y)
        return passo

    def mudar_direcao_aleatoriamente(self):
        """ Escolhe alguma direção aleatoriamente que não seja a atual """
        # REQ implementar o método
        """ k1 = [
            vector(1, 0),  # este vector significa direita
            vector(-1, 0),  # esquerda
            vector(0, 1),  # cima
            vector(0, -1),  # baixo
        ]
        """

        passo= [vector(1,0), vector(-1,0), vector(0,1), vector(0,-1)]
        random= choice(passo)
        return random

    def add_rota(self, destino):
        if (not self._waze):
            self._waze = Waze(self._labirinto)
            self._waze.add_destino(destino)

    def ir_a(self, destino):
        lab = self._labirinto # Para facilitar a leitura
        pos_agente = self._posicao

        self.add_rota(destino)
        waze = self._waze
        if (waze.chegou_ao_destino(pos_agente)):
            waze = None # Para uma próxima iteração, um novo destino
            return True

        if (waze.esta_sem_coord()):
            waze.gerar_rota(pos_agente)

        if (not waze.esta_sem_coord()):
            self._posicao = waze.obter_prox_coord()
            self.desenhar_se()
        return False
