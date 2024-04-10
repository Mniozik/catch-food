import pygame
from random import randint
from CatchFood_Game import window, window_width, window_height
import os
import json


class UserScore:
    def __init__(self):
        cwd = os.getcwd()
        scores_folder_name = "Highscores"
        scores_file_name = "scores.json"
        self.dir_folder = os.path.join(cwd, scores_folder_name)
        self.dir_scores = os.path.join(self.dir_folder, scores_file_name)

        if not os.path.exists(self.dir_folder):  # utworz jesli folder nie istnieje
            os.mkdir(self.dir_folder)

    def load_scores(self):
        try:
            with open(self.dir_scores, 'r') as file:
                scores = json.load(file)
        except FileNotFoundError:
            scores = []
        return scores

    def update_score(self, player_name, player_score):
        scores = self.load_scores()
        for stats in scores:
            if stats['name'] == player_name:
                if stats['score'] < player_score:
                    stats['score'] = player_score
                break
        else:
            scores.append({'name': player_name, 'score': player_score})
        self.save_score(scores)

    def save_score(self, scores):
        with open(self.dir_scores, 'w') as file:
            json.dump(scores, file)

    def show_scores(self):
        y = 150
        scores = self.load_scores()
        s = 1
        score_font = pygame.font.SysFont("Calibri", 42)
        score_font_best = pygame.font.SysFont("Calibri", 48, bold=True)

        # Sortowanie wyniku
        sorted_scores = sorted(scores, key=lambda x: x['score'], reverse=True)

        for stats in sorted_scores:
            text = f"[{s}] Score: {stats['score']} - {stats['name']}"
            if s == 1:
                text_surface = pygame.font.Font.render(score_font_best, text, True, (255, 215, 0))
            elif s == 2:
                text_surface = pygame.font.Font.render(score_font_best, text, True, (192, 192, 192))
            elif s == 3:
                text_surface = pygame.font.Font.render(score_font_best, text, True, (205, 127, 50))
            else:
                text_surface = pygame.font.Font.render(score_font, text, True, (255, 255, 255))

            window.blit(text_surface, (100, y))
            s += 1
            y += 50


class MenuText:
    def __init__(self, x_cord, y_cord, width, height, background_text):
        self.x_cord = x_cord
        self.y_cord = y_cord
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont("Calibri", 32)
        self.background_text = background_text
        self.font_background_text = pygame.font.Font.render(self.font, self.background_text, True, (100, 100, 100))
        self.text = ""
        self.active = False

    def tick(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # enter
                    # TableScore(self.text)
                    return self.text
                if self.active:
                    if event.key == pygame.K_BACKSPACE:
                        self.text = self.text[:-1]
                    else:
                        self.text += event.unicode  # wcisniety jakis klawisz
                    # return self.text # zapisze pod zmienna user_name

        if pygame.mouse.get_pressed()[0]:
            if pygame.rect.Rect(self.x_cord, self.y_cord, self.width, self.height).collidepoint(pygame.mouse.get_pos()):
                self.active = True
            else:
                self.active = False

    def draw(self, error, approved):
        if error:
            pygame.draw.rect(window, (255, 0, 0), (self.x_cord - 16, self.y_cord - 16, self.width + 32, self.height + 32))
        elif approved:
            pygame.draw.rect(window, (0, 120, 0), (self.x_cord - 16, self.y_cord - 16, self.width + 32, self.height + 32))

        pygame.draw.rect(window, (0, 0, 120), (self.x_cord - 8, self.y_cord - 8, self.width + 16, self.height + 16))
        # pygame.draw.rect(window, (200, 200, 255), (self.x_cord, self.y_cord, self.width, self.height))

        if self.active:
            pygame.draw.rect(window, (180, 180, 255), (self.x_cord, self.y_cord, self.width, self.height)) ##
        else:
            pygame.draw.rect(window, (200, 200, 255), (self.x_cord, self.y_cord, self.width, self.height))

        if self.text:  # jesli cos w zmiennej jest
            name_text = pygame.font.Font.render(self.font, self.text, True, (0, 0, 0))
            window.blit(name_text, (self.x_cord + 7, self.y_cord + 7))
        else:
            window.blit(self.font_background_text, (self.x_cord + 7, self.y_cord + 7))


class Lives:
    def __init__(self):
        self.image = pygame.image.load("Images/heart.png")
        self.x_cord = 0
        self.y_cord = 40

    def draw(self, amount):
        if amount >= 1:
            window.blit(self.image, (self.x_cord, self.y_cord))
        if amount >= 2:
            window.blit(self.image, (self.x_cord + 30, self.y_cord))
        if amount == 3:
            window.blit(self.image, (self.x_cord + 60, self.y_cord))


class MenuIcon:
    def __init__(self, x_cord, y_cord):
        self.image = pygame.image.load("Images/Menu_1.png")
        self.x_cord = x_cord  # 100
        self.y_cord = y_cord  # 30
        self.up_direction = False

    def tick(self, speed): # dzieki self przekazujemy do kazdej funkcji w ramach tego samego obiektu te zmienne
        self.speed = speed
        if self.y_cord <= 20 or self.y_cord >= 440:
            self.up_direction = not self.up_direction
        if self.up_direction:
            self.y_cord -= self.speed
        else:
            self.y_cord += self.speed
        window.blit(self.image, (self.x_cord, self.y_cord))

    def draw(self):
        window.blit(self.image, (self.x_cord, self.y_cord))


class Button:
    def __init__(self, x_cord, y_cord, type):
        self.x_cord = x_cord
        self.y_cord = y_cord

        if type == 1:
            self.image_0 = pygame.image.load("Images/singleplayer_0.png")
            self.image_1 = pygame.image.load("Images/singleplayer_1.png")
        elif type == 2:
            self.image_0 = pygame.image.load("Images/multiplayer_0.png")
            self.image_1 = pygame.image.load("Images/multiplayer_1.png")
        elif type == 3:
            self.image_0 = pygame.image.load("Images/arrow1.png")
            self.image_1 = pygame.image.load("Images/arrow2.png")
        elif type == 4:
            self.image_0 = pygame.image.load("Images/scoreboard_butt_1.png")
            self.image_1 = pygame.image.load("Images/scoreboard_butt_2.png")
        elif type == 5:
            self.image_0 = pygame.image.load("Images/button_menu_0.png")
            self.image_1 = pygame.image.load("Images/button_menu_1.png")
        elif type == 6:
            self.image_0 = pygame.image.load("Images/restart_0.png")
            self.image_1 = pygame.image.load("Images/restart_1.png")

        self.width = self.image_0.get_width()
        self.height = self.image_0.get_height()
        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.width, self.height)

    def tick_draw(self):
        if self.hitbox.collidepoint(pygame.mouse.get_pos()):
            window.blit(self.image_1, (self.x_cord, self.y_cord))
            if pygame.mouse.get_pressed()[0]:
                return True
        else:
            window.blit(self.image_0, (self.x_cord, self.y_cord))


class Bonus:
    def __init__(self):
        self.x_cord = randint(90, window_width - 90)
        self.y_cord = randint(int(window_height/2), window_height - 90)
        self.image = pygame.image.load("Images/fast.png")

        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.width, self.height)

    def draw(self):
        window.blit(self.image, (self.x_cord, self.y_cord))


class Food:
    def __init__(self):
        self.x_cord = randint(90, window_width - 90)
        self.y_cord = -60
        # self.speed = 2
        self.rand = randint(1, 5)

        if self.rand == 1:
            self.image = pygame.image.load("Images/donut.png")
        elif self.rand == 2:
            self.image = pygame.image.load("Images/fries.png")
        elif self.rand == 3:
            self.image = pygame.image.load("Images/hamburger.png")
        elif self.rand == 4:
            self.image = pygame.image.load("Images/popcorn.png")
        elif self.rand == 5:
            self.image = pygame.image.load("Images/sandwich.png")

        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def tick(self, speed):  # dzieki self przekazujemy do kazdej funkcji w ramach tego samego obiektu te zmienne
        self.speed = speed

        self.y_cord += self.speed
        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.width, self.height)

    def draw(self):
        window.blit(self.image, (self.x_cord, self.y_cord))


class BadFood:
    def __init__(self):
        self.x_cord = randint(90, window_width - 90)
        self.y_cord = -60
        self.rand = randint(1, 4)

        if self.rand == 1:
            self.image = pygame.image.load("Images/doll.png")
        elif self.rand == 2:
            self.image = pygame.image.load("Images/scissors.png")
        elif self.rand == 3:
            self.image = pygame.image.load("Images/wrench.png")
        elif self.rand == 4:
            self.image = pygame.image.load("Images/teddybear.png")

        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def tick(self, speed):  # dzieki self przekazujemy do kazdej funkcji w ramach tego samego obiektu te zmienne
        self.speed = speed

        self.y_cord += self.speed
        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.width, self.height)

    def draw(self):
        window.blit(self.image, (self.x_cord, self.y_cord))


class Player:
    def __init__(self):
        self.x_cord = int(window.get_width()/2 - 100)
        self.y_cord = int(window.get_height()/2 + 100)
        self.image = pygame.image.load("Images/basket.png")
        self.image_fast = pygame.image.load("Images/basket_fast.png")
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        # self.speed = 5

    def tick(self, keys, speed):
        if keys[pygame.K_UP] and self.y_cord > 0:
            self.y_cord -= speed
        if keys[pygame.K_DOWN] and self.y_cord < (window_height - self.height):
            self.y_cord += speed
        if keys[pygame.K_RIGHT] and self.x_cord < (window_width - self.width):
            self.x_cord += speed
        if keys[pygame.K_LEFT] and self.x_cord > 0:
            self.x_cord -= speed
        self.hitbox = pygame.Rect(self.x_cord, self.y_cord, self.width, self.height)

    def draw(self, bonus):
        if bonus:
            window.blit(self.image_fast, (self.x_cord, self.y_cord))
        else:
            window.blit(self.image, (self.x_cord, self.y_cord))
