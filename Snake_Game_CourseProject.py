import pygame
import random
from abc import ABC, abstractmethod

pygame.init()

WIDTH, HEIGHT = 640, 480
CELL_SIZE = 20
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_BLUE = (0, 0, 139)
PINK = (255, 192, 203)


class Food(ABC):
    
    def __init__(self):
        self.position = (random.randint(0, (WIDTH - CELL_SIZE) // CELL_SIZE) * CELL_SIZE,
                         random.randint(0, (HEIGHT - CELL_SIZE) // CELL_SIZE) * CELL_SIZE)

    @abstractmethod
    def draw(self):
        pass

class RegularFood(Food):
    
    def draw(self):
        pygame.draw.rect(SCREEN, DARK_BLUE, pygame.Rect(self.position[0], self.position[1], CELL_SIZE, CELL_SIZE))


class FoodFactory:
    
    @staticmethod
    def create_food(food_type):
        if food_type == "regular":
            return RegularFood()
        else:
            raise ValueError("Unknown food type")


class Snake:

    
    def __init__(self):
        self.segments = [(100, 100), (80, 100), (60, 100)]
        self.direction = 'RIGHT'
        self.grow = False

    def move(self):
        head_x, head_y = self.segments[0]
        if self.direction == 'UP':
            head_y -= CELL_SIZE
        elif self.direction == 'DOWN':
            head_y += CELL_SIZE
        elif self.direction == 'LEFT':
            head_x -= CELL_SIZE
        elif self.direction == 'RIGHT':
            head_x += CELL_SIZE
        new_head = (head_x, head_y)

        if self.grow:
            self.segments.insert(0, new_head)
            self.grow = False
        else:
            self.segments = [new_head] + self.segments[:-1]

    def change_direction(self, new_direction):
        opposite_directions = {'UP': 'DOWN', 'DOWN': 'UP', 'LEFT': 'RIGHT', 'RIGHT': 'LEFT'}
        if new_direction != opposite_directions[self.direction]:
            self.direction = new_direction

    def check_collision(self):
        head = self.segments[0]
        return (head in self.segments[1:] or 
                head[0] < 0 or head[0] >= WIDTH or 
                head[1] < 0 or head[1] >= HEIGHT)

    def grow_snake(self):
        self.grow = True

    def draw(self):
        for segment in self.segments:
            pygame.draw.rect(SCREEN, WHITE, pygame.Rect(segment[0], segment[1], CELL_SIZE, CELL_SIZE))


class Game:

    
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        self.snake = Snake()
        self.food = FoodFactory.create_food("regular")
        self.score = 0
        self.game_over = False

    def reset(self):
        self.snake = Snake()
        self.food = FoodFactory.create_food("regular")
        self.score = 0
        self.game_over = False

    def check_food_collision(self):
        if self.snake.segments[0] == self.food.position:
            self.snake.grow_snake()
            self.food = FoodFactory.create_food("regular")
            self.score += 1

    def show_message(self, message, font_size, color, y_offset=0):
        font = pygame.font.SysFont(None, font_size)
        text = font.render(message, True, color)
        text_rect = text.get_rect(center=(WIDTH / 2, HEIGHT / 2 + y_offset))
        SCREEN.blit(text, text_rect)

    def run(self):
        running = True
        start_screen = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if start_screen:
                        if event.key == pygame.K_RETURN:
                            start_screen = False
                    elif self.game_over:
                        if event.key == pygame.K_RETURN:
                            self.reset()
                    else:
                        if event.key == pygame.K_UP:
                            self.snake.change_direction('UP')
                        elif event.key == pygame.K_DOWN:
                            self.snake.change_direction('DOWN')
                        elif event.key == pygame.K_LEFT:
                            self.snake.change_direction('LEFT')
                        elif event.key == pygame.K_RIGHT:
                            self.snake.change_direction('RIGHT')

            if start_screen:
                SCREEN.fill(PINK)
                self.show_message("Press ENTER to Start", 50, BLACK)
            elif self.game_over:
                SCREEN.fill(PINK)
                self.show_message("GAME OVER", 50, BLACK, -50)
                self.show_message("Press ENTER to Start Again", 30, BLACK, 50)
            else:
                self.snake.move()
                if self.snake.check_collision():
                    self.game_over = True

                self.check_food_collision()

                SCREEN.fill(PINK)
                self.snake.draw()
                self.food.draw()
                self.show_message(f"Score: {self.score}", 30, BLACK, -200)
            
            pygame.display.flip()
            CLOCK.tick(10)

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
