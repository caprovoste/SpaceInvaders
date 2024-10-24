import pygame
import sys
import random
import time
import threading

class Jugador(object):
    def __init__(self):
        self.imagen_nave = pygame.image.load("assets/nave.png").convert()
        self.dimension_jugador = pygame.transform.scale(self.imagen_nave, (60, 60))
        self.dimension_jugador.set_colorkey((255,255,255))
        self.jugadorX = 370
        self.jugadorY = 550
        self.bala = None
        self.bala1 = None
        self.bala2 = None
        self.balas = []
        self.vidas = 3
        self.puntaje = 0
        self.posX_bala = 0
        self.posY_bala = 0
        self.objeto_especial = False
        self.bonoVelocidad = 0
    
    def movimientoJugador(self):
        tecla = pygame.key.get_pressed()
        if tecla[pygame.K_RIGHT]:
            if self.jugadorX + self.dimension_jugador.get_width() < 800:
                self.jugadorX += 7 + self.bonoVelocidad
        elif tecla[pygame.K_LEFT]:
            if self.jugadorX > 0:
                self.jugadorX -=7 + self.bonoVelocidad
        if(self.objeto_especial == False):
            if tecla[pygame.K_SPACE] and not self.bala:
                self.bala = pygame.Rect(self.jugadorX + self.dimension_jugador.get_width()/2 -2, self.jugadorY, 5, 10)
                self.posX_bala = self.jugadorX + self.dimension_jugador.get_width()/2 - 2
                self.posY_bala = self.jugadorY
        #si tiene el objeto especial, se accionan estas balas con el space
        else:
            if tecla[pygame.K_SPACE] and not self.bala1 and not self.bala2:
                    self.bala1 = pygame.Rect(self.jugadorX + self.dimension_jugador.get_width()/2 -3, self.jugadorY, 5, 10)
                    self.bala2 = pygame.Rect(self.jugadorX + self.dimension_jugador.get_width()/2 +3, self.jugadorY, 5, 10)

    def balaUpdate(self):
        if self.bala:
            self.bala.y -= 20
            if self.bala.y < 0:
                self.bala = None

        #aqui se incluyeron las balas nuevas del objeto especial
        if(self.objeto_especial == True and self.bala1):
            self.bala1.x -= 2
            self.bala1.y -= 20
            if self.bala1.y < 0 or self.bala1.x < 0:
                self.bala1 = None
        if(self.objeto_especial == True and self.bala2):
            self.bala2.x += 2
            self.bala2.y -= 20
            if self.bala2.y < 0 or self.bala2.x > 800:
                self.bala2 = None
    
            
                
class Enemigo(object):
    def __init__(self, dimX, dimY):
        self.imagen_enemigo = pygame.image.load("assets/enemigo.png").convert()
        self.dimension_enemigo = pygame.transform.scale(self.imagen_enemigo, (60,60))
        self.dimension_enemigo.set_colorkey((255,255,255))
        self.enemigoX = dimX
        self.enemigoY = dimY
        self.direccion = 1
        self.movimientos = 0
        self.velocidad = 1
        
    def movimiento(self, nivel):
        if(self.movimientos >= 130):
            self.direccion = self.direccion * -1
            self.movimientos = 0
            self.enemigoY = self.enemigoY + 30 
        elif(self.movimientos < 130):
            self.enemigoX = self.enemigoX + (self.direccion * self.velocidad * nivel / 2)
            self.movimientos += 1 * nivel / 2

class Boss(object):
    def __init__(self):
        self.imagen_boss = pygame.image.load("assets/boss.png").convert()
        self.dimension_boss = pygame.transform.scale(self.imagen_boss, (300,250))
        self.dimension_boss.set_colorkey((0,0,0))
        #self.pantalla.blit(self.dimension_boss, (50, 50))
        self.bossX = 50
        self.bossY = 50
        self.direccion = 1
        self.movimientos = 0
        self.velocidad = 1
        self.herida = 0
    def movimiento(self):
        if(self.movimientos >= 400):
            self.direccion = self.direccion * -1
            self.movimientos = 0
            self.bossY = self.bossY + 30
        elif(self.movimientos < 400):
            self.bossX = self.bossX + (self.direccion * self.velocidad)
            self.movimientos += 1 

class Power_Up(object):
    def __init__(self):
        self.imagen_power_up = pygame.image.load("assets/bala.png").convert()
        self.dimension_power_up = pygame.transform.scale(self.imagen_power_up, (30, 30))
        self.dimension_power_up.set_colorkey((0,0,0))
        self.power_upX = 500
        self.power_upY = 570
    def set_upX(self, upX_random):
        self.power_upX=upX_random
        
class Bomba(object):
    def __init__(self):
        self.imagen_bomba = pygame.image.load("assets/bomba.png").convert()
        self.dimension_bomba = pygame.transform.scale(self.imagen_bomba, (30, 30))
        self.dimension_bomba.set_colorkey((255,255,255))
        self.bombaX = 500
        self.bombaY = 570
    def set_bombaX(self,nueva_bombaX):
        self.bombaX = nueva_bombaX
        
class Corazon(object):
    def __init__(self):
        self.imagen_corazon = pygame.image.load("assets/corazon.png").convert()
        self.dimenson_corazon = pygame.transform.scale(self.imagen_corazon, (30,30))
        self.dimenson_corazon.set_colorkey((255,255,255))
        self.corazonX = 385
        self.corazonY = 570
            
class SpaceInvaders(object):
    def __init__(self):
        pygame.font.init()
        self.fuente = pygame.font.Font("assets/s.otf", 20)
        self.pantalla = pygame.display.set_mode((800, 600))
        self.fondoNegro = pygame.image.load("assets/ReiniciarLevel.png").convert_alpha()
        self.fondo = pygame.image.load("assets/n.png").convert_alpha()
        self.gameOver = pygame.image.load("assets/GameOver.png").convert_alpha()
        self.reiniciar = False
        self.jugador = Jugador()
        self.power_up = Power_Up()
        self.bomba = Bomba()
        self.corazon = Corazon()
        self.objeto_especial = False
        self.objeto_bomba = False
        self.objeto_corazon = False
        self.objeto_tiempo_obtencion = 0
        self.objeto_tiempo_obtencion_bomba = 0
        self.objeto_tiempo_obtencion_corazon = 0
        self.aparece_bomba=0
        self.enemigo = []
        self.boss = None    
        self.nivel = 1
        posY = 70
        posX = 30
        self.contadorDeBalasEnemigas = 0
        self.balasEnemigos = []
        self.posBalaEnemigosX = []
        self.posBalaEnemigosY = []
        self.contadorDeBalasBoss = 0
        self.balasBoss = []
        self.posBalaBossX = []
        self.posBalaBossY = []
        self.bossvivo = False
        self.threadDisparosBoss = None
        self.vivo=True
        for i in range(3):
            posY = 70
            posX = 30
            posY = posY * (i+1)
            for j in range(8):
               enemigoAux = Enemigo(posX, posY)
               self.enemigo.append(enemigoAux)
               posX += 80

    def disparoEnemigos(self):
        while self.vivo:
            time.sleep(3)
            cantidad = 5
            if(len(self.enemigo) < 5):
                cantidad = len(self.enemigo)
            enemigos = set()
            for i in range(cantidad):
                a = random.randrange(len(self.enemigo)) - 1     
                enemigos.add(a)
            for i in enemigos:
                self.contadorDeBalasEnemigas += 1
                self.balasEnemigos.append(i)
                self.balasEnemigos[self.contadorDeBalasEnemigas - 1] =  pygame.Rect(self.enemigo[i].enemigoX, self.enemigo[i].enemigoY, 5, 10)
                self.posBalaEnemigosX.append(self.enemigo[i].enemigoX)
                self.posBalaEnemigosY.append(self.enemigo[i].enemigoY)
                

    def balaEnemigoUpdate(self):
        for i in self.balasEnemigos:
            i.y += 7
            if i.y > 600:
                self.balasEnemigos.remove(i)
                self.contadorDeBalasEnemigas -= 1
    
    def disparoBoss(self):
        while self.vivo:
            time.sleep(3)
            for i in range(4):
                self.contadorDeBalasBoss += 1
                self.balasBoss.append(pygame.Rect(self.boss.bossX+50*(i+1), self.boss.bossY+200, 5, 10))
                self.posBalaBossX.append(self.boss.bossX+50*(i+1))
                self.posBalaBossY.append(self.boss.bossY+200)  
    
    def balaBossUpdate(self):
        for i in self.balasBoss:
            i.y += 7
            if i.y > 600:
                self.balasBoss.remove(i)
                self.contadorDeBalasBoss -= 1    
        
               
    def eliminar(self):
        if(self.jugador.bala):
            if self.boss_activo == False:
                for enemigo in self.enemigo:
                    if((self.jugador.posX_bala > enemigo.enemigoX  and self.jugador.posX_bala < enemigo.enemigoX + 60) and (self.jugador.bala.y > enemigo.enemigoY -40 and self.jugador.bala.y < enemigo.enemigoY +40)):
                        self.enemigo.remove(enemigo)
                        self.jugador.bala = None
                        self.jugador.puntaje += 100
                        break
            if(self.jugador.bala!=None and self.boss_activo == True):
                if((self.jugador.posX_bala > self.boss.bossX and self.jugador.posX_bala < self.boss.bossX + 300) and (self.jugador.bala.y > self.boss.bossY -250 and self.jugador.bala.y < self.boss.bossY +250)):
                    self.boss.herida +=1 
                    self.jugador.bala = None
                    self.jugador.puntaje += 10
        if(self.jugador.objeto_especial == True):
            if(self.jugador.bala1):
                if self.boss_activo == False:
                    for enemigo in self.enemigo:
                        if((self.jugador.bala1.x > enemigo.enemigoX  and self.jugador.bala1.x < enemigo.enemigoX + 60) and (self.jugador.bala1.y > enemigo.enemigoY -40 and self.jugador.bala1.y < enemigo.enemigoY +40)):
                            self.enemigo.remove(enemigo)
                            self.jugador.bala1 = None
                            self.jugador.puntaje += 100
                            break
                if(self.jugador.bala1!=None and self.boss_activo == True):
                    if((self.jugador.bala1.x > self.boss.bossX and self.jugador.bala1.x < self.boss.bossX + 300) and (self.jugador.bala1.y > self.boss.bossY -250 and self.jugador.bala1.y < self.boss.bossY +250)):
                        self.boss.herida +=1 
                        self.jugador.bala1 = None
                        self.jugador.puntaje += 10
            if(self.jugador.bala2):
                if self.boss_activo == False:
                    for enemigo in self.enemigo:
                        if((self.jugador.bala2.x > enemigo.enemigoX  and self.jugador.bala2.x < enemigo.enemigoX + 60) and (self.jugador.bala2.y > enemigo.enemigoY -40 and self.jugador.bala2.y < enemigo.enemigoY +40)):
                            self.enemigo.remove(enemigo)
                            self.jugador.bala2 = None
                            self.jugador.puntaje += 100
                            break
                if(self.jugador.bala2!=None and self.boss_activo == True):
                        if((self.jugador.bala2.x > self.boss.bossX and self.jugador.bala2.x < self.boss.bossX + 300) and (self.jugador.bala2.y > self.boss.bossY -250 and self.jugador.bala2.y < self.boss.bossY +250)):
                            self.boss.herida +=1 
                            self.jugador.bala2 = None
                            self.jugador.puntaje += 10
    
    #Esta la uso para reiniciar el nivel en caso de que un enemigo llegue a la "tierra", lo que hace es borrar los enemigos que
    # Quedan y reinicia el arreglo con las posiciones originales de cada enemigo.
    def reiniciarLevel(self):
        pygame.mixer.music.load('assets/fallo.mp3')
        pygame.mixer.music.play(0)
        self.reiniciar = True
        if self.boss_activo == True:
            self.boss.bossX = 50
            self.boss.bossY = 50
            self.boss.herida = 0
            self.boss.movimientos = 0
            self.boss.direccion = 1
        elif self.boss_activo == False:
            self.contadorDeBalasEnemigas = 0
            self.balasEnemigos = []
            self.enemigo = []
            posY = 70
            posX = 30
            for i in range(3):
                posY = 70
                posX = 30
                posY = posY * (i + 1)
                for j in range(8):
                    enemigoAux = Enemigo(posX, posY)
                    self.enemigo.append(enemigoAux)
                    posX += 80
        return 
                
    def enemigoMataJugador(self):
        for i in self.balasEnemigos:
            if(i.y > self.jugador.jugadorY-10 and i.y < self.jugador.jugadorY and i.x > self.jugador.jugadorX and i.x < self.jugador.jugadorX + 50):
                i.y = 600                
                self.reiniciarLevel()
                self.jugador.vidas -= 1
                break
    
    def bossMataJugador(self):
        for i in self.balasBoss:
            if(i.y > self.jugador.jugadorY-10 and i.y < self.jugador.jugadorY and i.x > self.jugador.jugadorX and i.x < self.jugador.jugadorX + 50):
                i.y = 600                
                self.reiniciarLevel()
                self.jugador.vidas -= 1
                break
    
    def levelUp(self):
        self.pantalla.fill((255,255,255))
        self.pantalla.blit(self.fondoNegro, [0,0])
        self.pantalla.blit(self.fuente.render("Vidas Restantes: {}".format(self.jugador.vidas), -1, (255,255,255)), (300, 300))
        self.pantalla.blit(self.fuente.render("Nivel: {}".format(self.nivel + 1), -1, (255,255,255)), (350, 250))
        pygame.display.flip()
        time.sleep(3)
        self.nivel += 1
        posY = 70
        posX = 30
        for i in range(3):
            posY = 70
            posX = 30
            posY = posY * (i + 1)
            for j in range(8):
                enemigoAux = Enemigo(posX, posY)
                self.enemigo.append(enemigoAux)
                posX += 80
    def get_nivel(self):
        return self.nivel
    
    def get_puntaje(self):
        return self.jugador.puntaje
    
    def run(self):
        pygame.init()
        clock = pygame.time.Clock()
        self.vivo=True
        self.jugar=True
        self.upx_random=0
        self.bombax_random=0
        self.boss_activo=False
        while self.jugar:
            
            clock.tick(60)
            self.pantalla.fill((255,255,255))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            
            self.pantalla.blit(self.fondo,[0,0])
            self.pantalla.blit(self.jugador.dimension_jugador, (self.jugador.jugadorX, self.jugador.jugadorY))
            #si el boss esta activo se muestra en pantalla
            if self.boss_activo == True:
                self.pantalla.blit(self.boss.dimension_boss, (self.boss.bossX, self.boss.bossY))
                self.boss.movimiento()
                if(self.boss.bossY > 490):
                    self.reiniciarLevel()
            #se activa el objeto
            if (pygame.time.get_ticks()/1000)%15 == 0 and self.jugador.objeto_especial==False:
                self.objeto_especial = True
                self.upx_random=self.upx_random+1
                if self.upx_random==1:
                    self.power_up.set_upX(random.randint(30, 740))
            #si se activa el objeto, aparece en pantalla
            if self.objeto_especial == True:
                self.pantalla.blit(self.power_up.dimension_power_up, (self.power_up.power_upX, self.power_up.power_upY))
            #se activa la bomba
            if (pygame.time.get_ticks() / 1000) % 20 == 0:
                self.objeto_bomba = True
                self.aparece_bomba = pygame.time.get_ticks()/1000
                self.bombax_random=self.bombax_random+1
                if self.bombax_random==1:
                    self.bomba.set_bombaX(random.randint(30, 740))
            #aparece la bomba en pantalla
            if self.objeto_bomba == True:
                self.pantalla.blit(self.bomba.dimension_bomba, (self.bomba.bombaX, self.bomba.bombaY))
            if (pygame.time.get_ticks() / 100) %300 == 0:
                self.objeto_corazon = True
            if self.objeto_corazon == True:
                self.pantalla.blit(self.corazon.dimenson_corazon, (self.corazon.corazonX, self.corazon.corazonY))
            if self.boss_activo == False:
                for i in self.enemigo:
                    self.pantalla.blit(i.dimension_enemigo, (i.enemigoX, i.enemigoY))
            self.pantalla.blit(self.fuente.render("Vidas: {}".format(self.jugador.vidas), -1, (255,255,255)), (20, 10))
            self.pantalla.blit(self.fuente.render("Puntaje: {}".format(self.jugador.puntaje), -1, (255,255,255)), (350, 10))
            if self.boss_activo == False:
                self.pantalla.blit(self.fuente.render("Nivel: {}".format(self.nivel), -1, (255,255,255)), (700,10))
            elif self.boss_activo == True:
                self.pantalla.blit(self.fuente.render("Nivel:Especial", -1, (255,255,255)), (650,10))
            if self.jugador.bala:
                pygame.draw.rect(self.pantalla, (255, 48, 48), self.jugador.bala)
            if self.jugador.bala1:
               pygame.draw.rect(self.pantalla, (255,255,255), self.jugador.bala1)
            if self.jugador.bala2:
               pygame.draw.rect(self.pantalla, (255,255,255), self.jugador.bala2)
            #si la nave toca el objeto, este lo remueve de la pantalla
            if (self.jugador.jugadorX+60 >= self.power_up.power_upX and self.jugador.jugadorX <= self.power_up.power_upX+30) and self.objeto_especial == True:
                self.jugador.objeto_especial = True
                self.objeto_especial = False
                self.objeto_tiempo_obtencion = pygame.time.get_ticks()/1000
                self.jugador.bonoVelocidad = 4
                self.upx_random=0
            #luego de los 5 segundos despues de obtener el objeto ya no tendra la habilidad especial y volvera a tener las balas iniciales
            if (pygame.time.get_ticks()/1000-self.objeto_tiempo_obtencion) >= 5 and self.objeto_tiempo_obtencion != 0:
                if self.jugador.bala1==None and self.jugador.bala2==None:
                    self.jugador.bonoVelocidad = 0
                    self.jugador.objeto_especial = False
            #si el jugador toca la bomba, le resta una vida y reinicia la pantalla
            if (self.jugador.jugadorX+60 >= self.bomba.bombaX and self.jugador.jugadorX <= self.bomba.bombaX+30) and self.objeto_bomba == True:
                self.objeto_bomba = False
                self.reiniciar = True
                self.reiniciarLevel()
                self.jugador.vidas -=1
                self.bombax_random=0
            #si pasan 2 segundos y la boomba sigue  activa, se desactiva y desaparece de la pantalla
            if (pygame.time.get_ticks()/1000-self.aparece_bomba) >= 2 and self.aparece_bomba != 0:
                self.objeto_bomba = False
                self.bombax_random = 0
            # CORAZON
            if (self.jugador.jugadorX+60 >= self.corazon.corazonX and self.jugador.jugadorX <= self.corazon.corazonX+30) and self.objeto_corazon == True:
                self.objeto_corazon = False
                self.jugador.vidas = self.jugador.vidas + 1
            #Para verificar si se ha reiniciado el nivel
            if self.reiniciar == True and self.jugador.vidas > 0 and self.boss_activo == False:
                self.pantalla.fill((255,255,255))
                self.pantalla.blit(self.fondoNegro, [0,0])
                self.pantalla.blit(self.fuente.render("Vidas Restantes: {}".format(self.jugador.vidas), -1, (255,255,255)), (300, 300))
                self.pantalla.blit(self.fuente.render("Nivel: {}".format(self.nivel), -1, (255,255,255)), (350, 250))
                pygame.display.flip()
                time.sleep(3)
                self.contadorDeBalasEnemigas = 0
                self.balasEnemigos = []
                self.reiniciar = False 
            if self.reiniciar == True and self.jugador.vidas > 0 and self.boss_activo == True:
                self.pantalla.fill((255,255,255))
                self.pantalla.blit(self.fondoNegro, [0,0])
                self.pantalla.blit(self.fuente.render("Vidas Restantes: {}".format(self.jugador.vidas), -1, (255,255,255)), (300, 300))
                self.pantalla.blit(self.fuente.render("Nivel: Especial", -1, (255,255,255)), (300, 250))
                pygame.display.flip()
                time.sleep(3)
                self.contadorDeBalasBoss = 0
                self.reiniciar = False     
            if self.jugador.vidas > 0 and self.boss_activo == False:
                self.jugador.movimientoJugador()
                self.jugador.balaUpdate()
                self.eliminar()
                for i in self.balasEnemigos:
                    try:
                        pygame.draw.rect(self.pantalla, (255, 48, 48), i)
                    except:
                        print("Unexpected error:", sys.exc_info()[0])
                        print(type(i))
                self.balaEnemigoUpdate()
                self.enemigoMataJugador()
            elif self.jugador.vidas > 0 and self.boss_activo == True:
                self.jugador.movimientoJugador()
                self.jugador.balaUpdate()
                self.eliminar()
                for i in self.balasBoss:
                    try:
                        pygame.draw.rect(self.pantalla, (255, 48, 48), i)
                    except:
                        print("Unexpected error:", sys.exc_info()[0])
                        print(type(i))
                self.balaBossUpdate()
                self.bossMataJugador()
            elif self.jugador.vidas <= 0:
                self.pantalla.blit(self.gameOver,[0,0])
                pygame.display.flip()
                time.sleep(2)
                self.jugar=False
            if self.boss_activo == False:
                for enemigo in self.enemigo:
                    enemigo.movimiento(self.nivel)
                    if(enemigo.enemigoY > 490):
                        self.reiniciarLevel()
                        self.jugador.vidas -= 1
                        break
                        for i in self.enemigo:
                            self.pantalla.blit(i.dimension_enemigo, (i.enemigoX, i.enemigoY))
                            #Si se eliminan a todos los enemigos, se avanza 1 nivel y se vuelven a dibujar los enemigos.
                if(len(self.enemigo) == 0):
                    self.levelUp()
                    if(self.nivel%2 == 0 and self.boss_activo == False):
                        self.nivel -=1
                        self.pantalla.fill((255,255,255))
                        self.pantalla.blit(self.fondoNegro, [0,0])
                        self.pantalla.blit(self.fuente.render("Vidas Restantes: {}".format(self.jugador.vidas), -1, (255,255,255)), (300, 300))
                        self.pantalla.blit(self.fuente.render("Nivel: Especial", -1, (255,255,255)), (300, 250))
                        pygame.display.flip()
                        time.sleep(3)
                        self.boss_activo = True
                        self.boss = Boss()
                        self.threadDisparosBoss = threading.Thread(target = self.disparoBoss)
                        self.threadDisparosBoss.start()
                    if(self.boss_activo == False):
                        for i in self.enemigo:
                            self.pantalla.blit(i.dimension_enemigo, (i.enemigoX, i.enemigoY))
            if self.boss_activo == True:
                if(self.boss.bossY > 300):
                        self.reiniciar = True
                        self.reiniciarLevel()
                        self.jugador.vidas -=1
                if self.boss.herida >= 100:
                    self.boss_activo = False
                    self.levelUp()
                    for i in self.enemigo:
                            self.pantalla.blit(i.dimension_enemigo, (i.enemigoX, i.enemigoY))
            pygame.display.flip()
        self.vivo=False
        self.threadDisparosEnemigos.join()
        if self.threadDisparosBoss != None:
            self.threadDisparosBoss.join()


class menuSpaceInvaders():
    def __init__(self):
        pygame.init();
        self.fuente_boton = pygame.font.Font("assets/s.otf", 30)
    def principal(self):
        self.pantalla = pygame.display.set_mode((800,600));
        self.fuente = pygame.font.Font("assets/s.otf", 100)
        self.fondo = pygame.image.load("assets/n2.png").convert_alpha()
        self.pantalla.blit(self.fondo,[0,0])
        self.imagen_titulo2 = pygame.image.load("assets/titulo2.jpg").convert()
        self.dimension_titulo2 = pygame.transform.scale(self.imagen_titulo2, (300,250))
        self.dimension_titulo2.set_colorkey((255,255,255))
        self.pantalla.blit(self.dimension_titulo2, (250, 275))
        self.imagen_titulo = pygame.image.load("assets/titulo4.png").convert()
        self.dimension_titulo = pygame.transform.scale(self.imagen_titulo, (500,150))
        self.dimension_titulo.set_colorkey((255,255,255))
        self.pantalla.blit(self.dimension_titulo, (150, 100))
        self.pantalla.blit(self.fuente.render("Space", -1, (255,255,255)), (270, 100))
        self.pantalla.blit(self.fuente.render("Invaders", -1, (255,255,255)), (213, 170))
        self.imagen_boton1 = pygame.image.load("assets/boton5.jpg").convert()
        self.dimension_boton1 = pygame.transform.scale(self.imagen_boton1, (200,50))
        self.dimension_boton1.set_colorkey((0,0,0))
        self.pantalla.blit(self.dimension_boton1, (300, 300))
        self.pantalla.blit(self.fuente_boton.render("Jugar", -1, (255,255,255)), (360, 309))
        self.imagen_boton2 = pygame.image.load("assets/boton5.jpg").convert()
        self.dimension_boton2 = pygame.transform.scale(self.imagen_boton2, (200,50))
        self.dimension_boton2.set_colorkey((0,0,0))
        self.pantalla.blit(self.dimension_boton2, (300, 370))
        self.pantalla.blit(self.fuente_boton.render("Ayuda", -1, (255,255,255)), (362, 379))
        self.imagen_boton3 = pygame.image.load("assets/boton5.jpg").convert()
        self.dimension_boton3 = pygame.transform.scale(self.imagen_boton3, (200,50))
        self.dimension_boton3.set_colorkey((0,0,0))
        self.pantalla.blit(self.dimension_boton3, (300, 440))
        self.pantalla.blit(self.fuente_boton.render("Salir", -1, (255,255,255)), (370, 449))
        pygame.display.set_caption("menu");
        self.menuActivo = True;
        pygame.display.flip();
        
    def secundario(self):
        self.fondo_help = pygame.image.load("assets/n2.png").convert_alpha()
        self.pantalla_help=pygame.display.set_mode((800,600));
        self.pantalla_help.blit(self.fondo_help,[0,0])
        self.imagen_titulo2 = pygame.image.load("assets/titulo2.jpg").convert()
        self.dimension_titulo2 = pygame.transform.scale(self.imagen_titulo2, (640,300))
        self.dimension_titulo2.set_colorkey((255,255,255))
        self.pantalla_help.blit(self.dimension_titulo2, (80, 80))#se cambio a pantalla_help
        self.imagen_boton_salir = pygame.image.load("assets/boton5.jpg").convert()
        self.dimension_boton_salir = pygame.transform.scale(self.imagen_boton_salir, (150,50))
        self.dimension_boton_salir.set_colorkey((0,0,0))
        self.pantalla_help.blit(self.dimension_boton_salir, (100, 440))
        self.pantalla_help.blit(self.fuente_boton.render("Volver", -1, (255,255,255)), (120, 450))
        self.pantalla_help.blit(self.fuente_boton.render("Controles:", -1, (255,255,255)), (100, 100))
        self.pantalla_help.blit(self.fuente_boton.render("Movimiento nave: LEFT-RIGHT", -1, (255,255,255)), (150, 150))
        self.pantalla_help.blit(self.fuente_boton.render("Disparar: SPACE", -1, (255,255,255)), (150, 170))
        self.pantalla_help.blit(self.fuente_boton.render("Objetos:", -1, (255,255,255)), (100, 220))
        self.pantalla_help.blit(self.fuente_boton.render("Poder especial: ", -1, (255,255,255)), (150, 270))
        self.imagen_power = pygame.image.load("assets/bala.png").convert()
        self.dimension_power = pygame.transform.scale(self.imagen_power, (20, 20))
        self.dimension_power.set_colorkey((0,0,0))
        self.pantalla_help.blit(self.dimension_power, (400,270))
        self.pantalla_help.blit(self.fuente_boton.render("Vida extra: ", -1, (255,255,255)), (150, 300))
        self.imagen_corazon = pygame.image.load("assets/corazon.png").convert()
        self.dimension_corazon = pygame.transform.scale(self.imagen_corazon, (20, 20))
        self.dimension_corazon.set_colorkey((255,255,255))
        self.pantalla_help.blit(self.dimension_corazon, (400,300))
        self.pantalla_help.blit(self.fuente_boton.render("Quita vida: ", -1, (255,255,255)), (150, 330))
        self.imagen_bomba = pygame.image.load("assets/bomba.png").convert()
        self.dimension_bomba = pygame.transform.scale(self.imagen_bomba, (20, 20))
        self.dimension_bomba.set_colorkey((255,255,255))
        self.pantalla_help.blit(self.dimension_bomba, (400,330))
        self.menuActivo_help=True
        pygame.display.flip();
    def menu_final(self,nuevo):
        pygame.mixer.music.load('assets/intromenu.mp3')
        pygame.mixer.music.play(-1)
        self.fondo_final = pygame.image.load("assets/n2.png").convert_alpha()
        self.pantalla_final=pygame.display.set_mode((800,600));
        self.pantalla_final.blit(self.fondo_final,[0,0])
        self.imagen_titulo3 = pygame.image.load("assets/titulo2.jpg").convert()
        self.dimension_titulo3 = pygame.transform.scale(self.imagen_titulo3, (400,200))
        self.dimension_titulo3.set_colorkey((255,255,255))
        self.pantalla_final.blit(self.dimension_titulo3, (200, 80))
        self.imagen_boton_salir_final = pygame.image.load("assets/boton5.jpg").convert()
        self.dimension_boton_salir_final = pygame.transform.scale(self.imagen_boton_salir_final, (250,50))
        self.dimension_boton_salir_final.set_colorkey((0,0,0))
        self.pantalla_final.blit(self.dimension_boton_salir_final, (275, 420))
        self.imagen_boton_intentar_final = pygame.image.load("assets/boton5.jpg").convert()
        self.dimension_boton_intentar_final = pygame.transform.scale(self.imagen_boton_intentar_final, (250,50))
        self.dimension_boton_intentar_final.set_colorkey((0,0,0))
        self.pantalla_final.blit(self.dimension_boton_intentar_final, (275, 350))
        self.pantalla_final.blit(self.fuente_boton.render("Salir", -1, (255,255,255)), (370, 430))
        self.pantalla_final.blit(self.fuente_boton.render("Intentar de nuevo", -1, (255,255,255)), (280, 360))
        self.pantalla_final.blit(self.fuente_boton.render("Nivel", -1, (255,255,255)), (370, 100))
        self.pantalla_final.blit(self.fuente_boton.render("{}".format(nuevo.get_nivel()), -1, (255,255,255)), (390, 135))
        self.pantalla_final.blit(self.fuente_boton.render("Puntaje", -1, (255,255,255)), (350, 190))
        self.pantalla_final.blit(self.fuente_boton.render("{}".format(nuevo.get_puntaje()), -1, (255,255,255)), (370, 225))
        self.menuActivo_final=True
        pygame.display.flip();
    def run_help(self):
        self.secundario()
        while (self.menuActivo_help):
            for evento_help in pygame.event.get():
                if evento_help.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pos()[0] >= 100 and pygame.mouse.get_pos()[1] >= 440:
                        if pygame.mouse.get_pos()[0] <= 250 and pygame.mouse.get_pos()[1] <= 490:
                            self.menuActivo_help=False
                            self.menuActivo=True
    def run_final(self,nuevo):
        self.menu_final(nuevo)
        while (self.menuActivo_final):
            for evento_final in pygame.event.get():
                if evento_final.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pos()[0] >= 275 and pygame.mouse.get_pos()[1] >= 350:
                        if pygame.mouse.get_pos()[0] <= 525 and pygame.mouse.get_pos()[1] <= 400:
                            self.menuActivo_final=False
                            pygame.mixer.music.stop()
                            self.nuevo2=SpaceInvaders()
                            self.nuevo2.run()
                            self.menuActivo_final=True
                            self.menu_final(self.nuevo2)
                    if pygame.mouse.get_pos()[0] >= 275 and pygame.mouse.get_pos()[1] >= 420:
                        if pygame.mouse.get_pos()[0] <= 525 and pygame.mouse.get_pos()[1] <= 470:
                            self.menuActivo_final=False
                            self.menuActivo=True
        
    def run(self):
        self.principal()
        while (self.menuActivo):
            for evento in pygame.event.get():
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pos()[0] >= 300 and pygame.mouse.get_pos()[1] >= 300:
                        if pygame.mouse.get_pos()[0] <= 500 and pygame.mouse.get_pos()[1] <= 350:
                            self.menuActivo=False
                            pygame.mixer.music.stop()
                            self.nuevo=SpaceInvaders();
                            self.nuevo.run()
                            self.run_final(self.nuevo)
                    if pygame.mouse.get_pos()[0] >= 300 and pygame.mouse.get_pos()[1] >= 370:
                        if pygame.mouse.get_pos()[0] <= 500 and pygame.mouse.get_pos()[1] <= 420:
                            self.menuActivo=False
                            self.run_help()
                            self.principal()
                    if pygame.mouse.get_pos()[0] >= 300 and pygame.mouse.get_pos()[1] >= 440:
                        if pygame.mouse.get_pos()[0] <= 500 and pygame.mouse.get_pos()[1] <= 490:
                            self.menuActivo=False
        pygame.quit()
   
    

if __name__ == "__main__":
    menuSpaceInvaders().run()
    #SpaceInvaders().run()
