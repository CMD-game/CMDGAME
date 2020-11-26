# 게임 조건
# 1. 캐릭터 : 좌우로 움직일 수 있고 활을 쏨
# 2. 적은 양쪽에서 다가오고, 방향을 조절하여 맞춰야 함
# 3. 화살에 적이 맞으면 적이 죽음과 동시에 경험치가 오름
# 4. 경험치가 일정량 이상 모이면 레벨 업 - 레벨 업 시 HP, MP 완전 회복
# 5. 일정 레벨 이상이면 더 강력한 스킬 사용 가능
# 6. 적에게 닿으면 HP 감소, HP가 0이 되면 게임 오버
# 7. 적을 죽이면 일정 확률로 인벤토리에 HP, MP 물약이 들어옴

# 게임 이미지
# 배경 : 640 * 480 (가로 세로) - M_background.png
# 캐릭터 : 50 * 100 - M_character.png
# 적 : 50 * 50 - M_enemy.png

import pygame
import time
#################################################################################################
# 기본 초기화 (반드시 해야 하는 것들)
pygame.init()

# 화면 크기 설정
screen_width = 640 # 가로 크기
screen_height = 480 # 세로 크기
screen = pygame.display.set_mode((screen_width, screen_height))

# 화면 타이틀 설정
pygame.display.set_caption("Maple_shooter")

# FPS
clock = pygame.time.Clock()
#################################################################################################

# 1. 사용자 게임 초기화 (배경 화면, 게임 이미지, 좌표, 속도, 폰트 등)

background = pygame.image.load("C:/Users/user/Desktop/PythonWorkSpace/CMDGAME/M_background.png")

character_RIGHT = pygame.image.load("C:/Users/user/Desktop/PythonWorkSpace/CMDGAME/M_character_RIGHT.png")
character = pygame.image.load("C:/Users/user/Desktop/PythonWorkSpace/CMDGAME/M_character_LEFT.png")
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width - character_width)/ 2
character_y_pos = screen_height - character_height - 50

character_speed = 0.3
character_HP = 100
character_MP = 100
character_Exp = 0
MAX_Exp = 100
invincibility = 0

character_to_x_LEFT = 0
character_to_x_LEFT_press = 0
character_to_x_RIGHT = 0
character_to_x_RIGHT_press = 0

arrow = pygame.image.load("C:/Users/user/Desktop/PythonWorkSpace/CMDGAME/M_arrow_LEFT.png")
arrow_RIGHT = pygame.image.load("C:/Users/user/Desktop/PythonWorkSpace/CMDGAME/M_arrow_RIGHT.png")
arrow_size = character.get_rect().size
arrow_width = character_size[0]
arrow_height = character_size[1]
arrow_x_pos = character_x_pos
arrow_y_pos = character_y_pos + 50
arrow_LEFT = True
arrow_speed = 0.6

enemy_slime = pygame.image.load("C:/Users/user/Desktop/PythonWorkSpace/CMDGAME/M_enemy_slime.png")
enemy_slime_size = enemy_slime.get_rect().size
enemy_slime_width = enemy_slime_size[0]
enemy_slime_height = enemy_slime_size[1]
enemy_slime_x_pos = 0
enemy_slime_y_pos = screen_height - enemy_slime_height - 50
enemy_slime_regen = 0.5
enemy_slime_regen_time = 0

enemy_slime_attack = 5

game_font = pygame.font.Font(None, 40)
total_time = 0
start_ticks = pygame.time.get_ticks()

running = True
Slime = True 
Shoot = False
while running:
    dt = clock.tick(60)

    # 2. 이벤트 처리 (키보드, 마우스 등)
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            running = False 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                character_to_x_LEFT -= character_speed
                character_to_x_LEFT_press = 1
                character_to_x_RIGHT_press = 0
            elif event.key == pygame.K_RIGHT:
                character_to_x_RIGHT += character_speed
                character_to_x_LEFT_press = 0
                character_to_x_RIGHT_press = 1
            elif event.key == pygame.K_a:
                if Shoot == False:
                    arrow_x_pos = character_x_pos
                    arrow_y_pos = character_y_pos + 50
                    if character_to_x_LEFT_press == 1:
                        arrow_LEFT = True
                    else:
                        arrow_LEFT = False
                    Shoot = True
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                character_to_x_LEFT = 0
            elif event.key == pygame.K_RIGHT:
                character_to_x_RIGHT = 0
    
    if Shoot == True:
        if arrow_LEFT == True:
            arrow_x_pos -= arrow_speed * dt
        else:
            arrow_x_pos += arrow_speed * dt
        arrow_y_pos += 1
    else:
        arrow_y_pos = -1000

    character_x_pos += (character_to_x_LEFT + character_to_x_RIGHT) * dt
    if character_x_pos < 0:
        character_x_pos = 0
    if character_x_pos > screen_width - character_width:
        character_x_pos = screen_width - character_width

            

    # 3. 게임 캐릭터 위치 정의
   
    # 4. 충돌 처리 
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    enemy_slime_rect = enemy_slime.get_rect()
    enemy_slime_rect.left = enemy_slime_x_pos
    enemy_slime_rect.top = enemy_slime_y_pos
    
    arrow_rect = arrow.get_rect()
    arrow_rect.left = arrow_x_pos
    arrow_rect.top = arrow_y_pos

    if arrow_rect.colliderect(enemy_slime_rect):
        Slime = False
        Shoot = False
        character_Exp += 10
        enemy_slime_x_pos = -1000
        enemy_slime_regen_time = elapsed_time
    elif (arrow_x_pos < 0) or (arrow_x_pos > (screen_width - arrow_width)) or (arrow_y_pos > screen_height):
        Shoot = False

    if Slime == False:
        if (pygame.time.get_ticks() - start_ticks) / 1000 - enemy_slime_regen_time >= enemy_slime_regen:
            Slime = True

    if Slime == True:
        enemy_slime_x_pos = 0

    if invincibility == 0: 
        if character_rect.colliderect(enemy_slime_rect):
            character_HP -= enemy_slime_attack
            print("HP - " + str(int(enemy_slime_attack)) + ", 남은 HP : " + str(int(character_HP)))
            invincibility = 2
            if character_HP <= 0:
                print("game over")
                running = False

    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
    if invincibility == 2:
        invincibility_time = elapsed_time
        invincibility = 1
    if invincibility == 1:
        if (pygame.time.get_ticks() - start_ticks) / 1000 - invincibility_time >= 1:
            invincibility = 0

    timer = game_font.render("Time : {}".format(int(elapsed_time)), True, (255, 255, 255))
    HP = game_font.render("HP : {}".format(int(character_HP)), True, (255, 0, 0))
    MP = game_font.render("MP : {}".format(int(character_MP)), True, (0, 0, 255))
    Exp = game_font.render("Exp : {} / {}".format(int(character_Exp), int(MAX_Exp)), True, (255, 255, 0))

    # 5. 화면에 그리기
    screen.blit(background, (0, 0))
    if invincibility == True:
        if ((pygame.time.get_ticks() - start_ticks) / 1000 - invincibility_time) <= 0.25 or (((pygame.time.get_ticks() - start_ticks) / 1000 - invincibility_time) >= 0.5 and ((pygame.time.get_ticks() - start_ticks) / 1000 - invincibility_time) <= 0.75):
            pass
        else:
            if (character_to_x_LEFT + character_to_x_RIGHT) > 0:
                screen.blit(character_RIGHT, (character_x_pos, character_y_pos))
            elif (character_to_x_LEFT + character_to_x_RIGHT) < 0:
                screen.blit(character, (character_x_pos, character_y_pos))
            elif character_to_x_RIGHT_press == 0:
                screen.blit(character, (character_x_pos, character_y_pos))
            else:
                screen.blit(character_RIGHT, (character_x_pos, character_y_pos))
    else:
        if (character_to_x_LEFT + character_to_x_RIGHT) > 0:
            screen.blit(character_RIGHT, (character_x_pos, character_y_pos))
        elif (character_to_x_LEFT + character_to_x_RIGHT) < 0:
            screen.blit(character, (character_x_pos, character_y_pos))
        elif character_to_x_RIGHT_press == 0:
            screen.blit(character, (character_x_pos, character_y_pos))
        else:
            screen.blit(character_RIGHT, (character_x_pos, character_y_pos))
    if Slime == True:
        screen.blit(enemy_slime, (enemy_slime_x_pos, enemy_slime_y_pos))
    if Shoot == True:
        if arrow_LEFT == True:
            screen.blit(arrow, (arrow_x_pos, arrow_y_pos))
        else:
            screen.blit(arrow_RIGHT, (arrow_x_pos, arrow_y_pos))
    screen.blit(timer, (10, 10))
    screen.blit(HP, ((screen_width - 150), 10))
    screen.blit(MP, ((screen_width - 150), 40))
    screen.blit(Exp, ((screen_width - 500), 10))
    pygame.display.update() 

pygame.quit()