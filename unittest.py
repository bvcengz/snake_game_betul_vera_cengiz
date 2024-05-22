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

    def grow_snake(self):
        self.grow = True

class Game:
    def __init__(self):
        self.snake = Snake()
        self.food = FoodFactory.create_food("regular")
        self.score = 0
        self.game_over = False

    def check_food_collision(self):
        if self.snake.segments[0] == self.food.position:
            self.snake.grow_snake()
            self.food = FoodFactory.create_food("regular")
            self.score += 1
