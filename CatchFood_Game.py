from CatchFood_Classes import *

pygame.init()

basic_time = pygame.time.Clock()
window_width = 1280
window_height = 720
window = pygame.display.set_mode((window_width, window_height))

pygame.display.set_caption("Catch Food")
icon = pygame.image.load("Images/fries.png")
pygame.display.set_icon(icon)

user_name = "User"
score = 0


def endmenu():
    background_menu = pygame.image.load("Images/endmenu.png")
    button_restart = Button(500, 340, 6)
    button_menu = Button(500, 440, 5)

    loop = True
    while loop:
        basic_time.tick(60)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                loop = False  # gdyby nie to, to nie mozemy zamknac pygame "iksem"

        window.blit(background_menu, (280, 120))
        game_score_text = pygame.font.Font.render(pygame.font.SysFont("Calibri", 48), f"{user_name}, your score is: " + str(score), True, (0, 0, 0))
        window.blit(game_score_text, (350, 250))

        if button_menu.tick_draw():
            main()
            break
        if button_restart.tick_draw():
            single()
            break
        pygame.display.update()


def scoreboard():
    background_menu = pygame.image.load("Images/Scoreboard1.png")
    button_reset = Button(50, 20, 3)
    icon_menu = MenuIcon(950, 30)
    UserScoreClass = UserScore()

    loop = True
    while loop:
        basic_time.tick(60)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                loop = False  # gdyby nie to, to nie mozemy zamknac pygame "iksem"

        window.blit(background_menu, (0, 0))
        pygame.draw.rect(window, (255, 215, 0), (40, 120, 820, 520))
        pygame.draw.rect(window, (0, 0, 120), (50, 130, 800, 500))
        icon_menu.tick(2)
        icon_menu.draw()
        UserScoreClass.show_scores()

        if button_reset.tick_draw():
            main()
            break

        pygame.display.update()


def single():
    player = Player()
    UserScoreClass = UserScore()
    global score
    score = 0
    lives = 3
    food = []
    bad_food = []
    bonuses = []
    background = pygame.image.load("Images/wall.png")

    # Difficulty
    food_fall_speed = 3.0
    badfood_fall_speed = 3.0
    food_append_queue = 1.5  # im mmniejsza wartosc tym szybciej tworzone sa nowe items
    badfood_append_queue = 2.25


    pause = False
    pause_text = pygame.font.Font.render(pygame.font.SysFont("Calibri", 68), "Pause", True, (0, 0, 0))
    gameover_text = pygame.font.Font.render(pygame.font.SysFont("Calibri", 68), "Game Over", True, (0, 0, 0))

    # --- TIME
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    bonus_time = 0
    food_time = 0
    bad_food_time = 0
    bonus_element_wait = False
    bonus_switch = False
    bonus_switch_time = 0
    # speed_switch_time = 0
    # badfood_append_time = 0
    difficult_switch_time = 0

    # --------- LOOP ---------
    loop = True
    while loop:

        # FPS
        # basic_time.tick(74.973)
        basic_time.tick(60)


        # EVENT
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False  # gdyby nie to, to nie mozemy zamknac pygame "iksem"
                # break
            if event.type == pygame.USEREVENT:
                bonus_time += 1
                food_time += 1
                bad_food_time += 1
                bonus_switch_time += 1
                # speed_switch_time += 1
                # badfood_append_time += 1
                difficult_switch_time += 1

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
               pause = not pause

        if pause:
            window.blit(pause_text, (550, 300))
            pygame.display.update()
            # bonus_time, food_time, bad_food_time, bonus_switch_time, speed_switch_time = 0, 0, 0, 0, 0
            bonus_time, food_time, bad_food_time, difficult_switch_time = 0, 0, 0, 0
            continue

        if lives < 1:
            # window.blit(gameover_text, (470, 300))
            endmenu()
            break
            # pygame.display.update()
            # continue
        #
        # MOVING (by ticking)
        keys = pygame.key.get_pressed()

        if bonus_switch:
            player.tick(keys, 10)
        else:
            player.tick(keys, 5)

        # FOOD
        if food_time >= food_append_queue:
            food.append(Food())
            food_time = 0


        if difficult_switch_time >= 20:
            food_fall_speed += 0.5
            badfood_fall_speed += 1
            if badfood_append_queue > 0.5:
                badfood_append_queue -= 0.5
            difficult_switch_time = 0

        # # Co 20s, zwiekszamy predkosc spadania items
        # if speed_switch_time >= 20:
        #     food_fall_speed += 0.5
        #     badfood_fall_speed += 1
        #     speed_switch_time = 0
        # # Co 30s, szybciej produkowane sa bad_food
        # if badfood_append_time >= 20 and badfood_append_queue > 0.5:
        #     badfood_append_queue -= 0.5
        #     badfood_append_time = 0

        # FOOD (moving)
        for item in food:  # jesli bedzie kilka itemow, to zeby wszystkie sie poruszaly
            item.tick(food_fall_speed)

            # BAD FOOD
        if bad_food_time >= badfood_append_queue:
            bad_food.append(BadFood())
            bad_food_time = 0

            # BAD FOOD (moving)
        for item in bad_food:  # jesli bedzie kilka itemow, to zeby wszystkie sie poruszaly
            item.tick(badfood_fall_speed)

        # BONUS
        if bonus_time >= 10:
            if bonus_element_wait is not True:
                bonuses.append(Bonus())
                bonus_element_wait = True
            if bonus_time >= 15:
                for item in bonuses:
                    bonuses.remove(item)
                bonus_element_wait = False
                bonus_time = 0


        score_text = pygame.font.Font.render(pygame.font.SysFont("Calibri", 36), f"Score: {score}", True, (0, 0, 0))
        # CHECK COLLISION
        for item in food:
            if player.hitbox.colliderect(item.hitbox):
                food.remove(item)
                score += 1

        for item in bad_food:
            if player.hitbox.colliderect(item.hitbox):
                bad_food.remove(item)
                lives -= 1

        for bonus in bonuses:
            if player.hitbox.colliderect(bonus.hitbox):
                bonuses.remove(bonus)
                bonus_switch = True
                bonus_switch_time = 0
        if bonus_switch_time >= 3:
            bonus_switch = False

        # DRAWING
        window.blit(background, (0, 0))
        window.blit(score_text, (10, 10))
        Lives().draw(lives)
        player.draw(bonus_switch)

        for item in food:  # item, to obiekt z klasy Food,  mamy ich kilka zapisanych w tablicy food.
            item.draw()

        for item in bad_food:
            item.draw()

        for bonus in bonuses:
            bonus.draw()

        pygame.display.update()  # te wszyskie blity i drawy wrzuca na ekran

    UserScoreClass.update_score(user_name, score)


def main():
    background_menu = pygame.image.load("Images/Menu.png")
    button_single = Button(880, 250, 1)
    button_multi = Button(880, 350, 2)
    button_scoreboard = Button(892, 500, 4)

    icon_menu = MenuIcon(100, 30)
    text_menu = MenuText(580, 250, 250, 45, background_text="Enter your name")
    error = False  # user_name
    approved = False  # user_name

    loop = True
    while loop:
        basic_time.tick(60)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                loop = False  # gdyby nie to, to nie mozemy zamknac pygame "iksem"
                return 0

        name = text_menu.tick(events)
        icon_menu.tick(2)
        if name:  # is not None: #... #wyswietla jesli cos sie zmieni w tej zmiennej, jesli jest cos zwracane (np po kliknieciu enter zwraca 'True?')
            global user_name
            user_name = name
            approved = True
            error = False

        window.blit(background_menu, (0, 0))
        text_menu.draw(error, approved)
        icon_menu.draw()

        if button_single.tick_draw():  # wywoluje funkcje (nawet po ifie to ta funkcja sie wlacza)
            if approved:
                single()  # if ... jesli True to wchodzi dalej we wnetrze tego ifa i wykonuje co ma
                break  # by zakonczyl to pracujace okno
            else:
                error = True
        if button_multi.tick_draw():
            endmenu()
            break
        if button_scoreboard.tick_draw():
            scoreboard()
            break

        pygame.display.update()


if __name__ == '__main__':
    main()




