import pygame
import copy

# pygame init
pygame.init()
screen=pygame.display.set_mode((1000,600))
screen.fill((255,255,255))
pygame.display.set_caption("Test Game")
font=pygame.font.SysFont('microsoftjhenghei',50)

# variables
FPS=60
MAX_COMMAND=50
border=[[0,1000],[0,600]]
spawnPosition=[[300,300],[700,300]]

players=[
    Tank.Player(spawnPosition[0][0],spawnPosition[0][1],picture='Tank1.png',id=0),
    Tank.Player(spawnPosition[1][0],spawnPosition[1][1],picture='Tank2.png',id=1)
]
mainTower=[
    Tank.Player(spawnPosition[0][0],spawnPosition[0][1],picture='MainTower1.png',id=0),
    Tank.Player(spawnPosition[1][0],spawnPosition[1][1],picture='MainTower2.png',id=1)
]

for i in range(2):
    mainTower[i].hp=20000
    mainTower[i].maxHp=20000

bullets=[
    Tank.Bullet(0, 100, 10, Tank.vec2D(1, 1), Tank.vec2D(100, 100),'Bullet1.png')
]
clock=pygame.time.Clock()
userFunction=[
    Player1.robot_movement,
    Player2.robot_movement
]

# Get a Tuple shows that user's input
def get_movement():
    x=0; y=0
    keys=pygame.key.get_pressed()
    if keys[pygame.K_w]:
        y=max(-1,y-1)
    if keys[pygame.K_s]:
        y=min(1,y+1)
    if keys[pygame.K_a]:
        x=max(-1,x-1)
    if keys[pygame.K_d]:
        x=min(1,x+1)
    return (x,y)

# move
def move_by_vector(userID,x,y):
    # print(players[userID].position.x,players[userID].position.y)
    players[userID].move((x,y),FPS)
    
def move_by_angle(userID,a):
    v=Tank.vec2D()
    v.set_angle(a,players[userID].moveSpeed/FPS)
    players[userID].position+=v

# shoot
def shoot_by_vector(userID,x,y):
    if players[userID].timeToFire>0:
        return
    v=Tank.vec2D()
    v.set(x,y,players[userID].bulletSpeed/FPS)
    b=players[userID].shoot(get_movement())
    bullets.append(Tank.Bullet(
        b[0],b[1],b[2],v,b[4],players[userID].bulletPicture
    ))
    players[userID].set_shoot_time()
def shoot_by_angle(userID,a):
    if players[userID].timeToFire>0:
        return
    v=Tank.vec2D()
    v.set(a,players[userID].bulletSpeed/FPS)
    b=players[userID].shoot(get_movement())
    bullets.append(Tank.Bullet(
        b[0],b[1],b[2],v,b[4],players[userID].bulletPicture
    ))
    players[userID].set_shoot_time()


def run_command(userID,command):
    if command[0]==1:
        x,y = command[1],command[2]
        move_by_vector(userID,x,y)
    elif command[0]==2:
        a=command[1]
        move_by_angle(userID,a)
    elif command[0]==3:
        x,y = command[1],command[2]
        shoot_by_vector(userID,x,y)
    elif command[0]==4:
        a=command[1]
        shoot_by_angle(userID,a)
    elif command[0]==5:
        t=command[1]
        players[userID].use_skillpoint(t)

def deal_damage(p,b,op):
    if op==0:
        if Tank.dis(players[p].position,bullets[b].position)<=35 and players[p].id!=bullets[b].master:
            distance=Tank.dis(players[p].position,bullets[b].position)
            force=Tank.vec2D(players[p].position.x,players[p].position.y); force-=bullets[b].position
            for i in range(2):
                players[p].move((force.x,force.y),FPS)
            force.set(force.x,force.y,(25+10-distance)/2/FPS*(((80-bullets[b].maxHp)**1)/(80**1)))
            bullets[b].velocity-=force
            
            players[p].hp-=bullets[b].damage*(300-players[p].hardness)/300*60/FPS
            bullets[b].hp-=(players[p].hardness+1)/5*60/FPS
            if players[p].hp<=0:
                return True
    elif op==1:
        if Tank.dis(mainTower[p].position,bullets[b].position)<=60 and mainTower[p].id!=bullets[b].master:
            distance=Tank.dis(mainTower[p].position,bullets[b].position)
            force=Tank.vec2D(mainTower[p].position.x,mainTower[p].position.y); force-=bullets[b].position
            force.set(force.x,force.y,(50+10-distance)/4/FPS*(((80-bullets[b].maxHp)**2)/(80**2)))
            bullets[b].velocity-=force
            
            mainTower[p].hp-=bullets[b].damage*(300-players[p].hardness)/300*60/FPS
            bullets[b].hp-=(players[p].hardness+1)/10*60/FPS
            if mainTower[p].hp<=0:
                mainTower[p].hp=0
                return True
    return False

def bullet_collision(b1,b2):
    if Tank.dis(bullets[b1].position,bullets[b2].position)<=20:
        distance=Tank.dis(bullets[b1].position,bullets[b2].position)
        bullets[b1].hp-=0.05*60/FPS
        bullets[b2].hp-=0.05*60/FPS
        force=Tank.vec2D(bullets[b1].position.x,bullets[b1].position.y); force-=bullets[b2].position
        # print(bullets[b1].position.get_tuple())
        force.set(force.x,force.y,(2*10-distance)/2/FPS*(((80-bullets[b1].maxHp)**2)/(80**2)))
        bullets[b1].velocity+=force
        force.set(force.x,force.y,(2*10-distance)/2/FPS*(((80-bullets[b2].maxHp)**2)/(80**2)))
        bullets[b2].velocity-=force

def spawn_player(userID):
    players[userID].position=Tank.vec2D(spawnPosition[i][0],spawnPosition[i][1])
    players[userID].hp=players[userID].maxHp

def kill_reward(userID):
    if players[userID].level<33:
        players[userID].level_up()

def show_text(text='',x=0,y=0,color=(0,0,0)):
    text=font.render(text,True,color)
    textRect=text.get_rect()
    textRect.center=(x,y)
    screen.blit(text,textRect)

def end_game():
    score=[0,0]
    if mainTower[0].hp<=0:
        # player2 win
        score[0]=100*(1.0-mainTower[1].hp/mainTower[1].maxHp)
        score[1]=100+400*(mainTower[1].hp/mainTower[1].maxHp)
        show_text('Player2 Win, Score : '+f'{score[1]:9.2f}',500,200)
        show_text('Player1      Score : '+f'{score[0]:9.2f}',500,400)
    elif mainTower[1].hp<=0:
        # player1 win
        score[0]=100+400*(mainTower[0].hp/mainTower[0].maxHp)
        score[1]=100*(1.0-mainTower[0].hp/mainTower[0].maxHp)
        show_text('Player1 Win, Score : '+f'{score[0]:9.2f}',500,200)
        show_text('Player2      Score : '+f'{score[1]:9.2f}',500,400)
    return

# # Used to debug
# for j in range(2):
#     for i in range(33):
#         players[j].level_up()


# main loop

InGame=True
while InGame:
    screen.fill((255,255,255))
    
    # event in pygame
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
    # print(players[1].position.x,players[1].position.y)
    # user's function
    userInput=[]
    for i in range(2):
        player=players[i]
        userInput.append(userFunction[i](copy.copy(player),copy.copy(players),copy.copy(mainTower),copy.copy(bullets)))

    # user's command
    for i in range(2):
        commands=userInput[i]
        commandNumber=1
        commandType=set()
        for command in commands:
            if commandNumber>MAX_COMMAND:
                break
            else:
                commandNumber+=1
            # player can only do at most one move and one shoot
            if (command[0]==1 or command[0]==2) and (1 in commandType or 2 in commandType):
                continue
            if (command[0]==3 or command[0]==4) and (3 in commandType or 4 in commandType):
                continue
            commandType.add(command[0])
            run_command(i,command)

    # border detect
    for i in range(2):
        players[i].border_detect(border)
    

    # Used to debug
    # mouse input
    if pygame.mouse.get_pressed()[0]:
        b=players[0].shoot(get_movement())
        v=b[3]
        v.x/=FPS; v.y/=FPS
        bullets.append(Tank.Bullet(b[0],b[1],b[2],b[3],b[4],'Bullet1.png'))
    # key input
    players[0].move(get_movement(),FPS)

    # bullets movement
    for i in bullets:
        i.move()
        i.time_left-=1000/FPS
        if i.time_left<=0 or i.hp<=0:
            bullets.remove(i)
        
    # display
    for i in range(2):
        screen.blit(mainTower[i].spirit.image,mainTower[i].get_position())
        pos=players[i].get_position()
        screen.blit(players[i].spirit.image,pos)
        # blood display
        if players[i].hp<players[i].maxHp:
            length=46*(players[i].hp/players[i].maxHp)
            players[i].bloodRemain.image=pygame.transform.scale(players[i].bloodRemain.image,(length,6))
            screen.blit(players[i].bloodDisplay.image,(pos[0],pos[1]+55))
            screen.blit(players[i].bloodRemain.image,(pos[0]+2,pos[1]+57))
        if mainTower[i].hp<mainTower[i].maxHp:
            length=46*(mainTower[i].hp/mainTower[i].maxHp)
            mainTower[i].bloodRemain.image=pygame.transform.scale(mainTower[i].bloodRemain.image,(length,6))
            screen.blit(mainTower[i].bloodDisplay.image,(spawnPosition[i][0]-23,spawnPosition[i][1]+55))
            screen.blit(mainTower[i].bloodRemain.image,(spawnPosition[i][0]-21,spawnPosition[i][1]+57))

    for i in bullets:
        screen.blit(i.spirit.image,i.get_position())
    
    # hp regen
    for i in range(2):
        players[i].hp=min(players[i].maxHp,players[i].hp+players[i].hpRegen/FPS)

    # deal damage
    for i in range(2):
        for j in range(len(bullets)):
            if deal_damage(i,j,0):
                spawn_player(i)
                kill_reward(bullets[j].master)
            if deal_damage(i,j,1):
                end_game()
                InGame=False
    # bullet collision
    for i in range(len(bullets)):
        for j in range(len(bullets)):
            if bullets[i].master==bullets[j].master:
                continue
            bullet_collision(i,j)
            
    # update time to fire
    for i in range(2):
        players[i].update_timeToFire()
    
    # print(players[1].moveSpeed)
    pygame.display.flip()
    clock.tick(30*FPS)
    # clock.tick(FPS)

InGame=True
while InGame:
    # event in pygame
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            InGame=False            
pygame.quit()