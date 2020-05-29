import pygame
import random
import math
import copy
import statistics


WIDTH = 1000
HEIGHT = 500

win = pygame.display.set_mode((WIDTH + 160, HEIGHT + 160))
pygame.font.init()
font = pygame.font.SysFont('comicsans', 20)


def spawn_food(gm, q):
    for _ in range(q):
        gm.foods.append(Food(random.randrange(-WIDTH * game.virtual - 6, WIDTH - 6),
                             random.randrange(-HEIGHT * game.virtual, HEIGHT)))


def draw(obj, screen):
    pygame.draw.circle(screen, obj.color, (int(obj.x), int(obj.y)), obj.size)
    pygame.draw.circle(screen, (0, 0, 0), (int(obj.x), int(obj.y)), obj.size, 1)


def speed_1x():
    game.speed = 1


def speed_2x():
    game.speed = 2


def speed_4x():
    game.speed = 4


def ultra_low_mut():
    game.mutation = 0.001


def low_mut():
    game.mutation = 0.004


def med_mut():
    game.mutation = 0.016


def high_mut():
    game.mutation = 0.064


def ultra_high_mut():
    game.mutation = 0.256


def ultra_low_en():
    game.energy = 80


def low_en():
    game.energy = 320


def med_en():
    game.energy = 640


def high_en():
    game.energy = 1280


def ultra_high_en():
    game.energy = 2560


def ultra_low_food():
    game.food = 9 * (game.virtual + 1) ** 2


def low_food():
    game.food = 18 * (game.virtual + 1) ** 2


def med_food():
    game.food = 36 * (game.virtual + 1) ** 2


def high_food():
    game.food = 72 * (game.virtual + 1) ** 2


def ultra_high_food():
    game.food = 144 * (game.virtual + 1) ** 2


def absolute_mode():
    game.relative = False


def relative_mode():
    game.relative = True


def one_screen():
    game.virtual = 0


def two_sreen():
    game.virtual = 1


def three_screen():
    game.virtual = 2


class Game:
    def __init__(self):
        self.foods = []
        self.species = []
        self.buttons = [Button(WIDTH + 30, 330, speed_1x, '1x', 20), Button(WIDTH + 75, 330, speed_2x, '2x', 20),
                        Button(WIDTH + 120, 330, speed_4x, '4x', 20), Button(WIDTH + 20, 190, ultra_low_mut, 'UL', 15),
                        Button(WIDTH + 50, 190, low_mut, ' L', 15), Button(WIDTH + 80, 190, med_mut, ' M', 15),
                        Button(WIDTH + 110, 190, high_mut, ' H', 15), Button(WIDTH + 140, 190, ultra_high_mut, 'UH', 15),
                        Button(WIDTH + 20, 240, ultra_low_en, 'UL', 15), Button(WIDTH + 50, 240, low_en, ' L', 15),
                        Button(WIDTH + 80, 240, med_en, ' M', 15), Button(WIDTH + 110, 240, high_en, ' H', 15),
                        Button(WIDTH + 140, 240, ultra_high_en, 'UH', 15), Button(WIDTH + 20, 290, ultra_low_food, 'UL', 15),
                        Button(WIDTH + 50, 290, low_food, ' L', 15), Button(WIDTH + 80, 290, med_food, ' M', 15),
                        Button(WIDTH + 110, 290, high_food, ' H', 15), Button(WIDTH + 140, 290, ultra_high_food, 'UH', 15),
                        Button(WIDTH + 50, HEIGHT + 50, absolute_mode, 'ABS', 40),
                        Button(WIDTH + 110, HEIGHT + 110, relative_mode, 'REL', 40),
                        Button(WIDTH + 30, 415, one_screen, '1s', 20), Button(WIDTH + 75, 415, two_sreen, '2s', 20),
                        Button(WIDTH + 120, 415, three_screen, '3s', 20)]
        self.buttons[0].selected = True
        self.buttons[5].selected = True
        self.buttons[10].selected = True
        self.buttons[15].selected = True
        self.buttons[19].selected = True
        self.buttons[20].selected = True
        self.gen = 1
        self.f = 0
        self.speed = 1
        self.mutation = 0.016
        self.paused = True
        self.energy = 640
        self.food = 36
        self.relative = False
        self.virtual = 0

    def round_is_over(self):
        if [sp for sp in self.species if sp.energy < 0 or sp.collected_food >= 2] == self.species:
            return True
        return False

    def new_round(self):
        game.f = 0
        self.gen += 1
        self.foods = []
        spawn_food(self, game.food)
        new = []
        for sp in self.species:
            if sp.collected_food == 0:
                self.species = [s for s in self.species if not s == sp]
            elif sp.collected_food > 1:
                new.append(copy.copy(sp))
        self.species.extend(new)
        for sp in self.species:
            sp.target = None
            sp.collected_food = 0
            gauss = random.gauss(1, game.mutation)
            if gauss < 0.2:
                gauss = 0.2
            elif gauss > 5:
                gauss = 5
            sp.speed *= gauss
            sp.energy = game.energy
            sp.y = random.randrange(-HEIGHT * game.virtual, HEIGHT)
            sp.x = random.randrange(-WIDTH * game.virtual, WIDTH)


class Food:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.color = (255, 20, 147)
        self.size = 3


class Specie:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
        self.size = 6
        self.energy = game.energy
        self.color = (255, 255, 0)
        self.target = None
        self.collected_food = 0

    def find_food(self, f):
        distances = [math.hypot(self.x - z.x, self.y - z.y) for z in f]
        try:
            self.target = f[distances.index(min(distances))]
        except ValueError:
            game.new_round()

    def move(self, target):
        dx = target.x - self.x
        dy = target.y - self.y
        if self.energy >= 0 and self.collected_food < 2 and (dx, dy) != (0, 0):
            self.x += dx / math.hypot(dx, dy) * self.speed
            self.y += dy / math.hypot(dx, dy) * self.speed
            self.energy -= self.speed ** 2
        
        if math.hypot(dx, dy) <= target.size + self.size:
            game.foods = [food for food in game.foods if not food == target]
            self.collected_food += 1
            game.f += 1
            for sp in game.species:
                if sp.target == target:
                    sp.target = None


class Button:
    def __init__(self, x, y, command, text, size):
        self.x = x
        self.y = y
        self.command = command
        self.color = (20, 20, 200)
        self.size = size
        self.selected_color = (200, 40, 200)
        self.selected = False
        self.text = text

    def blit(self, screen):
        screen.blit(font.render(self.text, False, (0, 0, 0)), (self.x - 10, self.y - 6))


class Graph:
    def __init__(self):
        self.categories = []
        for n in range(1, 33):
            self.categories.insert(0, (0.5 * (33 - n) ** 0.6))
            self.categories.append(32 / (33 - n) ** 0.6)
        self.categories[31] = 4
        self.categories.pop(32)
        self.categories.insert(0, -math.inf)
        self.categories.append(math.inf)
        self.y_axis = [0 for _ in range(64)]
        for sp in game.species:
            for n in range(64):
                if self.categories[n + 1] > sp.speed > self.categories[n]:
                    self.y_axis[n] += 1
                    adjust_color(sp, n)

    def draw(self, screen):
        if max(self.y_axis) > 0 and game.relative:
            mod = len(game.species) / max(self.y_axis)
        else:
            mod = 1
        for n, bar in enumerate(self.y_axis):
            pygame.draw.rect(screen, (n, n * 4, n * 4), (n * 15 + 20, HEIGHT + 155, 15, -150 * bar * mod / len(game.species)))
            pygame.draw.rect(screen, (0, 0, 0), (n * 15 + 20, HEIGHT + 155, 15, -150 * bar * mod / len(game.species)), 2)


def adjust_color(o, p):
    o.color = (255 - 4 * p, 4 * p, 0)
    while o.color[0] < 255 and o.color[1] < 255:
        o.color = (o.color[0] + 1, o.color[1] + 1, 0)


def draw_window(screen, f, s, b, g):
    t_alive = font.render('Alive: ' + str(len(game.species)), False, (0, 0, 0))
    t_aspd = font.render('Avg Spd: ' +
                        str(round(statistics.mean([sp.speed for sp in game.species]), 3)), False, (0, 0, 0))
    t_gen = font.render('Gen: ' + str(game.gen), False, (0, 0, 0))
    t_max = font.render('Max Spd: ' + str(round(max([sp.speed for sp in game.species]), 3)), False, (0, 0, 0))
    t_min = font.render('Min Spd: ' + str(round(min([sp.speed for sp in game.species]), 3)), False, (0, 0, 0))
    if len(game.species) > 1:
        t_std = font.render('Std Dvt: ' +
                            str(round(statistics.stdev([sp.speed for sp in game.species]), 3)), False, (0, 0, 0))
    else:
        t_std = font.render('Std Dvt: ' + '-', False, (0, 0, 0))
    t_mutrt = font.render('Mutation rate: ' + str(game.mutation), False, (0, 0, 0))
    t_en = font.render('Energy: ' + str(game.energy), False, (0, 0, 0))
    t_food = font.render('Food: ' + str(game.food), False, (0, 0, 0))
    t_moving = font.render('Moving: ' + str(len([x for x in game.species if x.energy > 0 and x.collected_food < 2])),
                           False, (0, 0, 0))
    t_virtual = font.render('Screens: ' + str((game.virtual + 1) ** 2), False, (0, 0, 0))

    win.fill((255, 170, 132))
    for sp in s:
        draw(sp, screen)

    for food in f:
        draw(food, screen)

    for button in b:
        to_draw = copy.copy(button)
        if button.selected:
            to_draw.color = to_draw.selected_color
        draw(to_draw, screen)
        button.blit(screen)
    g.draw(screen)

    pygame.draw.line(win, (0, 0, 0), (WIDTH, 0), (WIDTH, HEIGHT + 160), 3)
    pygame.draw.line(win, (0, 0, 0), (0, HEIGHT), (WIDTH + 160, HEIGHT), 3)

    win.blit(t_alive, (WIDTH + 5, 5))
    win.blit(t_min, (WIDTH + 5, 30))
    win.blit(t_aspd, (WIDTH + 5, 55))
    win.blit(t_max, (WIDTH + 5, 80))
    win.blit(t_gen, (WIDTH + 5, 105))
    win.blit(t_std, (WIDTH + 5, 130))
    win.blit(t_mutrt, (WIDTH + 5, 155))
    win.blit(t_en, (WIDTH + 5, 210))
    win.blit(t_food, (WIDTH + 5, 260))
    win.blit(t_moving, (WIDTH + 5, 360))
    win.blit(t_virtual, (WIDTH + 5, 380))

    pygame.display.update()


game = Game()
game.species.append(Specie(random.randrange(0, WIDTH), random.randint(0, HEIGHT), 4))
spawn_food(game, game.food)
run = True
clock = pygame.time.Clock()
counter = 0
while run:
    graph = Graph()
    counter += 1
    if counter % game.speed == 0:
        clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mx = pygame.mouse.get_pos()[0]
            my = pygame.mouse.get_pos()[1]
            for button in game.buttons:
                if math.hypot((mx - button.x), (my - button.y)) < button.size:
                    button.command()
                    for b in game.buttons:
                        if b.y == button.y or b.y == button.y + 60 or b.y == button.y - 60:
                            b.selected = False
                    button.selected = True
            if mx < WIDTH and my < HEIGHT:
                if game.paused:
                    game.paused = False
                else:
                    game.paused = True

    for specie in game.species:
        if not specie.target:
            specie.find_food(game.foods)
        else:
            if not game.paused:
                specie.move(specie.target)
    if game.round_is_over():
        game.new_round()

    draw_window(win, game.foods, game.species, game.buttons, graph)
pygame.quit()


