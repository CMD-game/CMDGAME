
# 게임 조건
# 0. 더 좋은 조건이 있다면 추가나 수정 바람
# 1. 캐릭터 : 좌우로 움직일 수 있고 캐릭터에 따라 다른 무기를 사용 가능
# 2. 보스를 잡으면서 진행, 보스를 잡을 때마다 레벨이 오름
# 4. 
# 5. 일정 레벨 이상이면 더 강력한 스킬 사용 가능
# 6. 적에게 닿으면 HP 감소, HP가 0이 되면 게임 오버
# 7. 적을 죽이면 일정 확률로 인벤토리에 HP, MP 물약이 들어옴
# 8. 모든 평타와 스킬에는 공통적인 쿨타임(장전 시간)이 있고, 스킬에는 각자의 쿨타임이 따로 존재한다.

# 게임 이미지
# 배경 : 640 * 480 (가로 세로) - M_background.png
# 캐릭터 : 50 * 100 - M_character_Bowmaster.png
# 적 : 50 * 50 - M_enemy.png

import pygame
import time
import os #파일위치 반환을 위한 라이브러리
#################################################################################################
# 기본 초기화 (반드시 해야 하는 것들)
pygame.init()


# 화면 크기 설정
screen_width = 640 # 가로 크기
screen_height = 480 # 세로 크기
screen = pygame.display.set_mode((screen_width, screen_height))

# 화면 타이틀 설정
pygame.display.set_caption("boss_killer")

# FPS(초당 프레임)
clock = pygame.time.Clock()
#################################################################################################

# 1. 사용자 게임 초기화 (배경 화면, 게임 이미지, 좌표, 속도, 폰트 등)

current_path = os.path.dirname(__file__) #현재 파일의 위치 반환
image_path = os.path.join(current_path, "images") #images 폴더 위치 반환

background = pygame.image.load(os.path.join(image_path, "M_background.png"))
stage = pygame.image.load(os.path.join(image_path, "M_stage.png"))
stage_size = stage.get_rect().size
stage_height = stage_size[1]

platform = pygame.image.load(os.path.join(image_path, "M_platform.png"))
platform_x_pos = 300
platform_y_pos = screen_height - 150

Qskill_effect = pygame.image.load(os.path.join(image_path, "M_Qskill_effect.png"))
Qskill_arrow = pygame.image.load(os.path.join(image_path, "M_Qskill_arrow.png"))
Qskill_size = Qskill_effect.get_rect().size
Qskill_width = Qskill_size[0]
Qskill_effect_x_pos = 50
Qskill_arrow_x_pos = 50
Qskill_arrow_y_pos = 0


character_Bowmaster_RIGHT = pygame.image.load(os.path.join(image_path, "M_character_Bowmaster_RIGHT.png"))
character_Bowmaster = pygame.image.load(os.path.join(image_path, "M_character_Bowmaster_LEFT.png"))
character_Bowmaster_size = character_Bowmaster.get_rect().size
character_Bowmaster_width = character_Bowmaster_size[0]
character_Bowmaster_height = character_Bowmaster_size[1]
character_Bowmaster_x_pos = (screen_width - character_Bowmaster_width)/ 2
character_Bowmaster_y_pos = screen_height - character_Bowmaster_height - stage_height

character_Bowmaster_speed = 0.3
character_Bowmaster_HP = 100
character_Bowmaster_Exp = 0
character_Bowmaster_Level = 1
MAX_Exp = 100
MAX_HP = 100
invincibility = 0
attack_delay = False
attack_delay_time = 1000 #ms

character_Bowmaster_to_x_LEFT = 0
character_Bowmaster_to_x_LEFT_press = 1 # 왼쪽을 보고 있는지 확인하기 위한 변수
character_Bowmaster_to_x_RIGHT = 0
character_Bowmaster_to_x_RIGHT_press = 0
bullet_1 = pygame.image.load(os.path.join(image_path, "bullet_1.png"))
bullet_2 = pygame.image.load(os.path.join(image_path, "bullet_2.png"))
bullet_3 = pygame.image.load(os.path.join(image_path, "bullet_3.png"))
bullet_4 = pygame.image.load(os.path.join(image_path, "bullet_4.png"))
arrow_size = character_Bowmaster.get_rect().size
arrow_width = character_Bowmaster_size[0]
arrow_height = character_Bowmaster_size[1]
arrow_LEFT = 1

arrow_speed_y = -15

arrows = []

arrow_speed = 10
arrow_to_remove = -1

enemy_slime = pygame.image.load(os.path.join(image_path, "M_enemy_slime.png"))
enemy_slime_size = enemy_slime.get_rect().size
enemy_slime_width = enemy_slime_size[0]
enemy_slime_height = enemy_slime_size[1]
enemy_slime_x_pos = 0
enemy_slime_y_pos = screen_height - enemy_slime_height - stage_height
enemy_slime_Exp = 10
enemy_slime_regen = 1000 # 실제 리젠 시간
enemy_slime_regen_time = 0 # 리젠 시간을 재기 위한 변수(0으로 고정)

enemy_slime_attack = 5

# 필수
game_font = pygame.font.Font(None, 40) 
total_time = 0
start_ticks = pygame.time.get_ticks()

running = True
Slime = True 
Shoot = False
Qskill_ready = False
Qskill_input = False
Qskill_damage = False
Qskill_delay = False
Qskill_delay_time = 50
airborne = False
double_jump = True
jump_height = -10
jump_speed = 0.5
airborne_distance = jump_height
invincibility = 0
while running:
    dt = clock.tick(60) # 프레임 수

    # 2. 이벤트 처리 (키보드, 마우스 등)
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: # 창을 닫았을 때
            running = False 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                character_Bowmaster_to_x_LEFT -= character_Bowmaster_speed
                character_Bowmaster_to_x_LEFT_press = 1
                character_Bowmaster_to_x_RIGHT_press = 0
            elif event.key == pygame.K_RIGHT:
                character_Bowmaster_to_x_RIGHT += character_Bowmaster_speed
                character_Bowmaster_to_x_LEFT_press = 0
                character_Bowmaster_to_x_RIGHT_press = 1
            elif event.key == pygame.K_UP:
                if airborne == False:
                    airborne = True
                elif double_jump == True:
                    double_jump = False
                    airborne_distance = jump_height
            elif event.key == pygame.K_DOWN:
                character_Bowmaster_y_pos += 20
                airborne = True
                airborne_distance = 5
            elif event.key == pygame.K_a: # a키를 누름 : 공격
                if attack_delay == False:
                    arrow_x_pos = character_Bowmaster_x_pos + (character_Bowmaster_width - arrow_width) / 2
                    arrow_y_pos = character_Bowmaster_y_pos + 50
                    if character_Bowmaster_to_x_LEFT_press == 1:
                        arrow_LEFT = 1
                    else:
                        arrow_LEFT = 0
                    arrows.append([arrow_x_pos, arrow_y_pos, arrow_LEFT])
                    attack_delay = True
                    A_elapsed_time = pygame.time.get_ticks() - start_ticks
            elif event.key == pygame.K_q: # q키를 누름 : 스킬1
                if attack_delay == False and Qskill_delay == False and Qskill_ready == False and Qskill_input == False and Qskill_damage == False:
                    Qskill_input = True
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                character_Bowmaster_to_x_LEFT = 0
            elif event.key == pygame.K_RIGHT:
                character_Bowmaster_to_x_RIGHT = 0

    if airborne == True: # 점프
        character_Bowmaster_y_pos += airborne_distance
        airborne_distance += jump_speed
        if airborne_distance > 10:
            airborne_distance = 10
        if character_Bowmaster_y_pos >= screen_height - stage_height - character_Bowmaster_height:
            airborne = False
            character_Bowmaster_y_pos = screen_height - stage_height - character_Bowmaster_height
            airborne_distance = jump_height
            double_jump = True

    if Qskill_input == True:
        if character_Bowmaster_to_x_LEFT_press == 1:
            Qskill_effect_x_pos = character_Bowmaster_x_pos - 200 - character_Bowmaster_width
        else:
            Qskill_effect_x_pos = character_Bowmaster_x_pos + 200
        if Qskill_effect_x_pos < 0:
            Qskill_effect_x_pos = 0
        if Qskill_effect_x_pos > screen_width - Qskill_width:
            Qskill_effect_x_pos = screen_width - Qskill_width
        attack_delay = True
        A_elapsed_time = pygame.time.get_ticks() - start_ticks
        Q_damage_elapsed_time = pygame.time.get_ticks() - start_ticks
        Qskill_ready = True
        Qskill_input = False

    if Qskill_ready == True:
        Qskill_arrow_x_pos = Qskill_effect_x_pos
        Qskill_arrow_y_pos = 0
        Q_elapsed_time = pygame.time.get_ticks() - start_ticks
        Qskill_delay = True
        if pygame.time.get_ticks() - start_ticks - Q_damage_elapsed_time >= 1000:
            Qskill_damage = True
            Qskill_ready = False

    if Qskill_damage == True:
        Qskill_arrow_y_pos += 15
        
    if attack_delay == True:
        if pygame.time.get_ticks() - start_ticks - A_elapsed_time >= attack_delay_time:
            attack_delay = False

    if Qskill_delay == True:
        if pygame.time.get_ticks() - start_ticks - Q_elapsed_time >= Qskill_delay_time:
            Qskill_delay = False

    character_Bowmaster_x_pos += (character_Bowmaster_to_x_LEFT + character_Bowmaster_to_x_RIGHT) * dt # 캐릭터 이동
    if character_Bowmaster_x_pos < 0:
        character_Bowmaster_x_pos = 0
    if character_Bowmaster_x_pos > screen_width - character_Bowmaster_width:
        character_Bowmaster_x_pos = screen_width - character_Bowmaster_width
    
    # 화살 위치 조정
    for w in arrows:
        if w[2] == 1:
            arrows = [ [w[0] - arrow_speed, w[1], w[2]]]
        else:
            arrows = [ [w[0] + arrow_speed, w[1], w[2]]]
    

    # 바닥 또는 벽에 닿은 화살 없애기
    arrows = [ [w[0], w[1], w[2]] for w in arrows if (w[0] < 0) or (w[0] > screen_width - arrow_width) or (w[1] < screen_height - stage_height)]
   
    # 4. 충돌 처리 
    # 필수 (캐릭터 크기를 재는 함수들)
    character_Bowmaster_rect = character_Bowmaster.get_rect()
    character_Bowmaster_rect.left = character_Bowmaster_x_pos
    character_Bowmaster_rect.top = character_Bowmaster_y_pos

    enemy_slime_rect = enemy_slime.get_rect()
    enemy_slime_rect.left = enemy_slime_x_pos
    enemy_slime_rect.top = enemy_slime_y_pos

    Qskill_arrow_rect = Qskill_arrow.get_rect()
    Qskill_arrow_rect.left = Qskill_arrow_x_pos
    Qskill_arrow_rect.top = Qskill_arrow_y_pos

    platform_rect = platform.get_rect()
    platform_rect.left = platform_x_pos
    platform_rect.top = platform_y_pos
    
    for arrow_idx, arrow_val in enumerate(arrows):
        arrow_pos_x = arrow_val[0]
        arrow_pos_y = arrow_val[1]

        arrow_rect = arrow.get_rect()
        arrow_rect.left = arrow_pos_x
        arrow_rect.right = arrow_pos_y

        if arrow_rect.colliderect(enemy_slime_rect): # 화살과 슬라임이 충돌
            arrow_to_remove = arrow_idx
            character_Bowmaster_Exp += enemy_slime_Exp
            enemy_slime_regen_time = pygame.time.get_ticks() - start_ticks
            Slime = False
            break
        elif (arrow_x_pos < 0) or (arrow_x_pos > (screen_width - arrow_width)) or (arrow_y_pos > screen_height):
            arrow_to_remove = arrow_idx
            break

    if arrow_to_remove > -1:
        del arrows[arrow_to_remove]
        arrow_to_remove = -1
    
    if character_Bowmaster_rect.colliderect(platform_rect): # 플랫폼 착지
        if (character_Bowmaster_y_pos + character_Bowmaster_height - 10) <= platform_y_pos and airborne_distance >= 0:
            airborne = False
            airborne_distance = jump_height
            character_Bowmaster_y_pos = platform_y_pos - character_Bowmaster_height + 1
            double_jump = True
    else:
        if character_Bowmaster_y_pos + character_Bowmaster_height < screen_height - stage_height:
            if airborne == False:
                airborne_distance = 0
                airborne = True

    if Qskill_arrow_rect.colliderect(enemy_slime_rect):
        Slime = False
        enemy_slime_regen_time = pygame.time.get_ticks() - start_ticks
        character_Bowmaster_Exp += enemy_slime_Exp

    if Qskill_arrow_y_pos >= screen_height:
        Qskill_damage = False

    if character_Bowmaster_Exp >= MAX_Exp:
        character_Bowmaster_Exp -= MAX_Exp
        character_Bowmaster_Level += 1
        MAX_Exp += MAX_Exp * 0.1 # MAX Exp, Hp 는 모두 1.1배 
        MAX_HP += MAX_HP * 0.1
        character_Bowmaster_HP = MAX_HP # 레벨업시 즉시 회복

    if Slime == False:
        enemy_slime_x_pos = -1000
        if (pygame.time.get_ticks() - start_ticks) - enemy_slime_regen_time >= enemy_slime_regen:
            Slime = True

    if Slime == True:
        enemy_slime_x_pos = 0

    if invincibility == 0: # 무적이 아닐 때
        if character_Bowmaster_rect.colliderect(enemy_slime_rect): # 캐릭터와 슬라임이 충돌
            character_Bowmaster_HP -= enemy_slime_attack
            print("HP - " + str(int(enemy_slime_attack)) + ", 남은 HP : " + str(int(character_Bowmaster_HP)))
            invincibility = 2
            if character_Bowmaster_HP <= 0:
                print("game over")
                running = False

    if invincibility == 2:
        invincibility_time = pygame.time.get_ticks() - start_ticks
        invincibility = 1
    if invincibility == 1:
        if (pygame.time.get_ticks() - start_ticks) - invincibility_time >= 1000: # 1: 무적 시간(초)
            invincibility = 0

    # 게임 화면 표시
    HP = game_font.render("HP : {} / {}".format(int(character_Bowmaster_HP), int(MAX_HP)), True, (255, 0, 0))
    Exp = game_font.render("Exp : {} / {}".format(int(character_Bowmaster_Exp), int(MAX_Exp)), True, (255, 255, 0))
    Level = game_font.render("Lv.{}".format(int(character_Bowmaster_Level)), True, (0, 255, 0))

    # 5. 화면에 그리기
    screen.blit(background, (0, 0))
    screen.blit(stage, (0, (screen_height - stage_height))) 
    screen.blit(platform, (platform_x_pos, platform_y_pos))
    if invincibility == True: # 무적 시간에 깜빡임 구현 (더 나은 방안이 있으면 수정 바람)
        if int((pygame.time.get_ticks() - start_ticks - invincibility_time) / 250) % 2 == 0:
            pass
        else:
            if (character_Bowmaster_to_x_LEFT + character_Bowmaster_to_x_RIGHT) > 0:
                screen.blit(character_Bowmaster_RIGHT, (character_Bowmaster_x_pos, character_Bowmaster_y_pos))
            elif (character_Bowmaster_to_x_LEFT + character_Bowmaster_to_x_RIGHT) < 0:
                screen.blit(character_Bowmaster, (character_Bowmaster_x_pos, character_Bowmaster_y_pos))
            elif character_Bowmaster_to_x_RIGHT_press == 0:
                screen.blit(character_Bowmaster, (character_Bowmaster_x_pos, character_Bowmaster_y_pos))
            else:
                screen.blit(character_Bowmaster_RIGHT, (character_Bowmaster_x_pos, character_Bowmaster_y_pos))
    else:
        if (character_Bowmaster_to_x_LEFT + character_Bowmaster_to_x_RIGHT) > 0:
            screen.blit(character_Bowmaster_RIGHT, (character_Bowmaster_x_pos, character_Bowmaster_y_pos))
        elif (character_Bowmaster_to_x_LEFT + character_Bowmaster_to_x_RIGHT) < 0:
            screen.blit(character_Bowmaster, (character_Bowmaster_x_pos, character_Bowmaster_y_pos))
        elif character_Bowmaster_to_x_RIGHT_press == 0:
            screen.blit(character_Bowmaster, (character_Bowmaster_x_pos, character_Bowmaster_y_pos))
        else:
            screen.blit(character_Bowmaster_RIGHT, (character_Bowmaster_x_pos, character_Bowmaster_y_pos))
    if Slime == True:
        screen.blit(enemy_slime, (enemy_slime_x_pos, enemy_slime_y_pos))
    for arrow_x_pos, arrow_y_pos, arrow_LEFT in arrows:
        if arrow_LEFT == 1:
            screen.blit(arrow, (arrow_x_pos, arrow_y_pos))
        else:
            screen.blit(arrow_RIGHT, (arrow_x_pos, arrow_y_pos))
    if Qskill_ready == True:
        screen.blit(Qskill_effect, (Qskill_effect_x_pos, screen_height - stage_height))
    if Qskill_damage == True:
        screen.blit(Qskill_arrow, (Qskill_arrow_x_pos, Qskill_arrow_y_pos))
    screen.blit(HP, ((screen_width - 200), 10))
    screen.blit(Exp, ((screen_width - 500), 10))
    screen.blit(Level, (10, 10))
    pygame.display.update() 

pygame.quit()