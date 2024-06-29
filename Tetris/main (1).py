import pygame
import random
# класс - игровое поле
# класс - тетмино - фигуры
# игровой цикл


height_win = 900
width_win = 1400
speed_game = 1000

game_width = 600
game_height = 900
block_size = 50
RED = (220, 10, 10)
GREEN = (15, 240, 10)
YEllOW = (220, 200, 10)
PURPLE = (220, 10, 220)
GREY = (244, 244, 244)
BLACK = (0, 0, 0)
pygame.init()
pygame.mixer.music.load('mp3.ogg')
pygame.mixer.music.play()
pygame.mixer.music.set_volume(0.2)

sound2 = pygame.mixer.Sound('igrovaya-sreda-audio-energoobespechenie-audio-material-39368.ogg')
sound2.set_volume(0.4)
sound1 = pygame.mixer.Sound('metallicheskiy-zvon.ogg')
sound1.set_volume(0.4)
class Board:
    def __init__(self):
        self.grid = []
        self.count_w = game_width//block_size
        self.count_h = game_height//block_size
        for i in range(self.count_h):
            tm = []
            for j in range(self.count_w):
                tm.append(0)
            self.grid.append(tm)


    def remove_line(self, line):
        del self.grid[line]
        new_line = [0 for _ in range(self.count_w)]
        self.grid.insert(0, new_line)
        sound2.play()
        
        
    def move_lines_down(self, line):
        for i in range(line, 0, -1):
            self.grid[i] = self.grid[i - 1]
        self.grid[0] = [0 for _ in range(self.count_w)]
        
    def draw(self):
        for y in range(self.count_h):
           # print(self.grid[y])
            for x in range(self.count_w):
                if self.grid[y][x]:
                    pygame.draw.rect(window, RED, (block_size*x, block_size*y, block_size, block_size))
                    pygame.draw.rect(window, GREY, (block_size*x, block_size*y, block_size, block_size), 1)
                # else:
                #     pygame.draw.rect(window, GREY, (block_size * x, block_size * y, block_size, block_size), 1)
    def check_line(self):
        for i in range(len(self.grid)):
            if all(self.grid[i]):
                self.remove_line(i)
                self.move_lines_down(i)


class Figures:
    shapes = [
        [[1, 1, 1, 1]],

        [[1, 1],
         [1, 1]],

        [[1, 1, 1],
         [0, 1, 0]],

        [[1, 0],
         [1, 1],
         [0, 1]],

        [[1, 0],
         [1, 0],
         [1, 1]],
    ]
    
    def rotate(self):
        self.shape = list(zip(*self.shape[::-1]))
    
    def __init__(self):
        self.shape = random.choice(self.shapes)
        self.x = game_width // 2
        self.y = 0
        self.speed_y = 5
    def draw(self):
        for y in range(len(self.shape)):
            for x in range(len(self.shape[y])):
                if self.shape[y][x]:
                    pygame.draw.rect(window, GREEN, ((self.x) + x * block_size, (self.y) + y * block_size, block_size, block_size))

    def update(self, board):
        if self.can_move(0, self.speed_y, board):
            self.y += self.speed_y
        else:
            self.add_to_board(board)
            self.__init__()

    def can_move(self, dx, dy, board):
        for y in range(len(self.shape)):
            for x in range(len(self.shape[y])):
                if self.shape[y][x]:
                    new_x = self.x + dx + x * block_size
                    new_y = self.y + dy + y * block_size

                    board_y = self.y // block_size + y + 1
                    board_x = self.x // block_size + x

                    if new_x < 0 or new_x > game_width - block_size or new_y > game_height - block_size or board.grid[board_y][board_x]:
                            return False
        print("______")
        return True


    def move_player(self, dx, board):
        if self.can_move(dx, 0, board):
            self.x += dx

    def add_to_board(self, board):
        for y in range(len(self.shape)):
            for x in range(len(self.shape[y])):
                if self.shape[y][x]:
                    board_y = self.y // block_size + y
                    board_x = self.x // block_size + x
                    board.grid[board_y][board_x] = 1
                    sound1.play()

window = pygame.display.set_mode((width_win, height_win))
clock = pygame.time.Clock()

game_board = Board()
#print(len(game_board.grid), len(game_board.grid[0]))
shape = Figures()
while True:
    game_board.check_line()
    window.fill(BLACK)
    pygame.draw.rect(window, GREY, (0, 0, game_width, game_height), 2)
    shape.draw()
    game_board.draw()
    shape.update(game_board)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_r:
            shape.rotate()    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_d]:
        shape.move_player(5, game_board)
    if keys[pygame.K_a]:
        shape.move_player(-5, game_board)
    
       
  
       
    

    clock.tick(60)
    pygame.display.update()