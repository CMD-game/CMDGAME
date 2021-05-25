## 게임 조건
####### 이 버전엔 버그 있음
# 0. 더 좋은 조건이 있다면 추가나 수정 바람
# 1. 캐릭터 : 좌우로 움직일 수 있고 캐릭터에 따라 다른 무기를 사용 가능
# 2. 보스를 잡으면서 진행, 보스를 잡을 때마다 레벨이 오름 (최대 체력 추가)
# 3. 보스를 잡을 때마다 저장 가능
# 4. boshy: : 총알 발사(최대 4발), 자동 장전

## 해야할 일
# 0. 버그 수정(중요)
# 1. 저장, 불러오기 기능 추가
# 2. 체력 시스템 정비
# 3. 튜토리얼 만들기
# 4. 보스 추가

## 중요하지 않은 일
# 1. 캐릭터 추가
# 2. 낮점 추가
# 3. 스킬 추가
# 4. 스토리 추가
# 5. 하드코어 모드 추가
# 6. 이스터에그 추가
# 7. 3단점프 기믹 추가

# 게임 이미지
# 배경 : 640 * 480 (가로 세로) - M_background.png
# 캐릭터 : 50 * 100 - M_character_boshy.png
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

# 플랫폼은 하나가 제일 적당할 듯
platform = pygame.image.load(os.path.join(image_path, "M_platform.png"))
platform_x_pos = 300
platform_y_pos = screen_height - 150

# 가져온 캐릭터 이름이 boshy
character_boshy = pygame.image.load(os.path.join(image_path, "character_boshy.png"))
character_boshy_LEFT = pygame.image.load(os.path.join(image_path, "character_boshy_LEFT.png"))
character_boshy_size = character_boshy.get_rect().size
character_boshy_width = character_boshy_size[0]
character_boshy_height = character_boshy_size[1]
character_boshy_x_pos = (screen_width - character_boshy_width)/ 2
character_boshy_y_pos = screen_height - character_boshy_height - stage_height

character_boshy_speed = 0.3
character_boshy_HP = 100
character_boshy_Exp = 0
character_boshy_Level = 1
MAX_Exp = 100
MAX_HP = 100
invincibility = 0

character_boshy_to_x_LEFT = 0
character_boshy_to_x_LEFT_press = 1 # 왼쪽을 보고 있는지 확인하기 위한 변수
character_boshy_to_x_RIGHT = 0
character_boshy_to_x_RIGHT_press = 0

# 총알 이미지
bullet_images = [
    pygame.image.load(os.path.join(image_path, "bullet_1.png")),
    pygame.image.load(os.path.join(image_path, "bullet_2.png")),
    pygame.image.load(os.path.join(image_path, "bullet_3.png")),
    pygame.image.load(os.path.join(image_path, "bullet_4.png"))]

# 총알 사용 여부 확인 변수
bullet_1_using = False
bullet_2_using = False
bullet_3_using = False
bullet_4_using = False

# 총알 정보
bullet_size = bullet_images[1].get_rect().size
bullet_width = bullet_size[0]
bullet_height = bullet_size[1]
bullet_speed = 10
bullet_LEFT = 1
bullet_number = 1

bullets = []

# 사라질 총알 저장 변수
bullet_to_remove = -1
bullet_not_using = 0

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
airborne = False # 공중에 떠 있는지 확인하기 위한 변수
double_jump = True # 더블점프가 가능한지 확인하기 위한 변수
jump_height = -10 # 점프 시작시 속도
jump_speed = 0.5 # 점프할동안 증가할 속도
airborne_distance = jump_height # 점프 중 속도
invincibility = 0 # 피격 시 무적 확인 변수
while running:
    dt = clock.tick(60) # 프레임 수

    # 2. 이벤트 처리 (키보드, 마우스 등)
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: # 창을 닫았을 때
            # 저장 후 종료하시겠습니까? 창 띄우기
            running = False 
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                character_boshy_to_x_LEFT -= character_boshy_speed
                character_boshy_to_x_LEFT_press = 1
                character_boshy_to_x_RIGHT_press = 0
            elif event.key == pygame.K_RIGHT:
                character_boshy_to_x_RIGHT += character_boshy_speed
                character_boshy_to_x_LEFT_press = 0
                character_boshy_to_x_RIGHT_press = 1
            elif event.key == pygame.K_UP:
                if airborne == False:
                    airborne = True
                elif double_jump == True:
                    double_jump = False
                    airborne_distance = jump_height
            elif event.key == pygame.K_DOWN: # 하향점프
                character_boshy_y_pos += 20 # y좌표를 20만큼 내려서 발판에서 떨어지게 만듦
                airborne = True
                airborne_distance = 5 # 하향점프의 처음 속도는 5
            elif event.key == pygame.K_a: # a키를 누름 : 공격
                try: # try/except/else 구문 : try에서 error가 발생하면 except, 아니면 else 실행
                    if bullet_1_using == False: # 총알 사용 여부 확인
                        bullet_1_using = True
                        bullet_number = 0
                    elif bullet_2_using == False:
                        bullet_2_using = True
                        bullet_number = 1
                    elif bullet_3_using == False:
                        bullet_3_using = True
                        bullet_number = 2
                    elif bullet_4_using == False:
                        bullet_4_using = True
                        bullet_number = 3
                    else: # 모든 총알이 사용중일 때 a를 누르면 고의로 에러 발생
                        print(5/0)
                except ZeroDivisionError: # 에러가 나면 break
                    break
                else: # 아니면 총알의 정보를 수집해 저장
                    bullet_x_pos = character_boshy_x_pos + (character_boshy_width - bullet_width) / 2
                    bullet_y_pos = character_boshy_y_pos + 10
                    if character_boshy_to_x_LEFT_press == 1: # 왼쪽을 보고 있다면 to_x의 부호 반대
                        bullet_LEFT = -1
                    else:
                        bullet_LEFT = 1
                    bullets.append({
                        "pos_x" : bullet_x_pos, 
                        "pos_y" : bullet_y_pos,
                        "img_idx" : bullet_number,
                        "to_x" : bullet_speed * bullet_LEFT }) # 딕셔너리를 이용함, 중괄호 안의 수치는 변경 가능
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                character_boshy_to_x_LEFT = 0
            elif event.key == pygame.K_RIGHT:
                character_boshy_to_x_RIGHT = 0

    if airborne == True: # 점프
        character_boshy_y_pos += airborne_distance # 캐릭터가 점프 속도만큼 이동
        airborne_distance += jump_speed # 점프 속도 증가
        if airborne_distance > 10: # 종단 속도
            airborne_distance = 10
        if character_boshy_y_pos >= screen_height - stage_height - character_boshy_height:
            airborne = False
            character_boshy_y_pos = screen_height - stage_height - character_boshy_height
            airborne_distance = jump_height
            double_jump = True

    character_boshy_x_pos += (character_boshy_to_x_LEFT + character_boshy_to_x_RIGHT) * dt # 캐릭터 이동
    if character_boshy_x_pos < 0:
        character_boshy_x_pos = 0
    if character_boshy_x_pos > screen_width - character_boshy_width:
        character_boshy_x_pos = screen_width - character_boshy_width
        
    # 4. 충돌 처리 
    # 필수 (캐릭터 크기를 재는 함수들)
    character_boshy_rect = character_boshy.get_rect()
    character_boshy_rect.left = character_boshy_x_pos
    character_boshy_rect.top = character_boshy_y_pos

    enemy_slime_rect = enemy_slime.get_rect()
    enemy_slime_rect.left = enemy_slime_x_pos
    enemy_slime_rect.top = enemy_slime_y_pos

    platform_rect = platform.get_rect()
    platform_rect.left = platform_x_pos
    platform_rect.top = platform_y_pos

    # 총알 위치 정의
    for bullet_idx, bullet_val in enumerate(bullets):
        bullet_pos_x = bullet_val["pos_x"]
        bullet_pos_y = bullet_val["pos_y"]
        bullet_img_idx = bullet_val["img_idx"] # 위에서 정의한 총알의 정보를 딕셔너리를 이용해 값 추출

        bullet_rect = bullet_images[bullet_img_idx].get_rect()
        bullet_rect.left = bullet_pos_x
        bullet_rect.top = bullet_pos_y

        bullet_val["pos_x"] += bullet_val["to_x"] # 총알 이동

        if bullet_rect.colliderect(enemy_slime_rect): # 총알과 슬라임이 충돌
            Slime = False
            character_boshy_Exp += 10
            slime_start_ticks = pygame.time.get_ticks()
            bullet_to_remove = bullet_img_idx
            break
        elif bullet_pos_x < 0 or bullet_pos_x > screen_width - bullet_width: # 가로벽에 닿았을 때
            bullet_to_remove = bullet_img_idx
        #버그 밑의 break가 총알 정의 for문에서 빠져나오면서 버그가 생김
        if bullet_to_remove > -1: # bullet_to_remove의 최초값은 -1
            if bullet_to_remove == 0: # 1번 총알을 제거해야할 때
                bullet_1_using = False               
            elif bullet_to_remove == 1: # 2번 총알을 제거해야 할 때
                if bullet_1_using == True:
                    break
                else: # 1번이 사용되고있지 않다면
                    bullet_not_using += 1 # bullet_not_using + 1
                bullet_2_using = False
            elif bullet_to_remove == 2:
                if bullet_1_using == True:
                    break
                else:
                    bullet_not_using += 1
                if bullet_2_using == True:
                    break
                else:
                    bullet_not_using += 1
                bullet_3_using = False
            else:
                if bullet_1_using == True:
                    break
                else:
                    bullet_not_using += 1
                if bullet_2_using == True:
                    break
                else:
                    bullet_not_using += 1
                if bullet_3_using == True:
                    break
                else:
                    bullet_not_using += 1
                bullet_4_using = False # 총알을 다시 사용가능하게 함
            del bullets[bullet_to_remove - bullet_not_using] # 사용된 총알 제거 / break를 pass로 바꾸어 실행하였을때 index 오류 발생
            bullet_to_remove = -1 # 변수값 초기화
            bullet_not_using = 0

    if character_boshy_rect.colliderect(platform_rect): # 플랫폼 착지
        if (character_boshy_y_pos + character_boshy_height - 10) <= platform_y_pos and airborne_distance >= 0:
            airborne = False
            airborne_distance = jump_height
            character_boshy_y_pos = platform_y_pos - character_boshy_height + 1
            double_jump = True
    else:
        if character_boshy_y_pos + character_boshy_height < screen_height - stage_height:
            if airborne == False:
                airborne_distance = 0
                airborne = True

    if character_boshy_Exp >= MAX_Exp:
        character_boshy_Exp -= MAX_Exp
        character_boshy_Level += 1
        MAX_Exp += MAX_Exp * 0.1 # MAX Exp, Hp 는 모두 1.1배 
        MAX_HP += MAX_HP * 0.1
        character_boshy_HP = MAX_HP # 레벨업시 즉시 회복

    if Slime == False:
        enemy_slime_x_pos = -1000
        if (pygame.time.get_ticks() - slime_start_ticks) - enemy_slime_regen_time >= enemy_slime_regen:
            Slime = True

    if Slime == True:
        enemy_slime_x_pos = 0

    if invincibility == 0: # 무적이 아닐 때
        if character_boshy_rect.colliderect(enemy_slime_rect): # 캐릭터와 슬라임이 충돌
            character_boshy_HP -= enemy_slime_attack
            invincibility = 2
            if character_boshy_HP <= 0:
                print("game over")
                running = False

    if invincibility == 2:
        invincibility_time = pygame.time.get_ticks() - start_ticks
        invincibility = 1
    if invincibility == 1:
        if (pygame.time.get_ticks() - start_ticks) - invincibility_time >= 1000: # 1000: 무적 시간(ms)
            invincibility = 0

    # 게임 화면 표시
    HP = game_font.render("HP : {} / {}".format(int(character_boshy_HP), int(MAX_HP)), True, (255, 0, 0))
    Exp = game_font.render("Exp : {} / {}".format(int(character_boshy_Exp), int(MAX_Exp)), True, (255, 255, 0))
    Level = game_font.render("Lv.{}".format(int(character_boshy_Level)), True, (0, 255, 0))

    # 5. 화면에 그리기
    screen.blit(background, (0, 0))
    screen.blit(stage, (0, (screen_height - stage_height))) 
    screen.blit(platform, (platform_x_pos, platform_y_pos))
    if invincibility == True: # 무적 시간에 깜빡임 구현 (더 나은 방안이 있으면 수정 바람)
        if int((pygame.time.get_ticks() - start_ticks - invincibility_time) / 250) % 2 == 0:
            pass
        else:
            if (character_boshy_to_x_LEFT + character_boshy_to_x_RIGHT) > 0:
                screen.blit(character_boshy, (character_boshy_x_pos, character_boshy_y_pos))
            elif (character_boshy_to_x_LEFT + character_boshy_to_x_RIGHT) < 0:
                screen.blit(character_boshy_LEFT, (character_boshy_x_pos, character_boshy_y_pos))
            elif character_boshy_to_x_RIGHT_press == 0:
                screen.blit(character_boshy_LEFT, (character_boshy_x_pos, character_boshy_y_pos))
            else:
                screen.blit(character_boshy, (character_boshy_x_pos, character_boshy_y_pos))
    else:
        if (character_boshy_to_x_LEFT + character_boshy_to_x_RIGHT) > 0:
            screen.blit(character_boshy, (character_boshy_x_pos, character_boshy_y_pos))
        elif (character_boshy_to_x_LEFT + character_boshy_to_x_RIGHT) < 0:
            screen.blit(character_boshy_LEFT, (character_boshy_x_pos, character_boshy_y_pos))
        elif character_boshy_to_x_RIGHT_press == 0:
            screen.blit(character_boshy_LEFT, (character_boshy_x_pos, character_boshy_y_pos))
        else:
            screen.blit(character_boshy, (character_boshy_x_pos, character_boshy_y_pos))
    
    if Slime == True:
        screen.blit(enemy_slime, (enemy_slime_x_pos, enemy_slime_y_pos))

    for idx, val in enumerate(bullets): # 모든 총알에 대해 정보를 불러와 그리기
        bullet_pos_x = val["pos_x"]
        bullet_pos_y = val["pos_y"]
        bullet_img_idx = val["img_idx"]
        screen.blit(bullet_images[bullet_img_idx], (bullet_pos_x, bullet_pos_y))

    screen.blit(HP, ((screen_width - 200), 10))
    screen.blit(Exp, ((screen_width - 500), 10))
    screen.blit(Level, (10, 10))
    pygame.display.update() 

pygame.quit()