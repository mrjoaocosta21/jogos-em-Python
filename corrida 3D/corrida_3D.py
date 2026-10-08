from ursina import * 
import random 

app = Ursina()
sky = Sky()
camera.position = (0, 5, -14)
camera.rotation_x = 15

pista = []
for i in range(8):
    trecho = Entity(z=i*20)
    Entity(parent=trecho, model='plane', color=color.lime, scale=(60, 1, 20))
    Entity(parent=trecho, model='cube', y = 0.05, color=color.dark_gray, scale=(8, 0.1, 20))
    for x in (-1.3, 1.3):
        Entity(parent=trecho, model='cube', x=x, y=0.11, color=color.white, scale=(0.15, 0.02, 5))
    pista.append(trecho)

def novo_carro(cor, x, z):
    c = Entity(model='cube', color=cor, x=x, y=0.5, z=z, scale=(1.4, 0.6, 2.6), collider='box')
    Entity(parent=c, model='cube', color=color.black, y= 0.9, z= 0.1, scale=(0.8, 0.9, 0.5))
    return c

carro = novo_carro(color.red, 0, 0)
velocidade = 25
faixas = [-2.6, 0, 2.6]
outros_carros = [novo_carro(color.azure, random.choice(faixas), 40 + i * 25) for i in range(4)]
placar = [Text('0 m', scale=3, position=window.top_left + Vec2(.03, -.03))]

def update():    
    carro.z += velocidade * time.dt
    camera.z = carro.z - 14
    for trecho in pista:
        if trecho.z < carro.z - 20:
            trecho.z += 160
    lado = held_keys['d'] - held_keys['a']
    carro.x = clamp(carro.x + lado * 8 * time.dt, -3, 3)
    carro.rotation_y = lado * 12
    for outro_carro in outros_carros:
        outro_carro.z += 10 * time.dt
        if outro_carro.z < carro.z - 15:
            outro_carro.z += 100
            outro_carro.x = random.choice(faixas)        

app.run()    