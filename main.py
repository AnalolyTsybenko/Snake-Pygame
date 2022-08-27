from random import randrange
import pygame_menu
import pygame
import time


class Settings:
    def __init__(self):
        pygame.init()
        self.image = pygame.image.load('python_image.jpeg')
        self.screen_w_h = 960
        self.screen_surface = pygame.display.set_mode((self.screen_w_h, self.screen_w_h), pygame.NOFRAME)
        pygame.display.set_caption('Snake', 'Snake')
        pygame.display.set_icon(self.image)
        self.fps_controller = pygame.time.Clock()
        self.speed = 10
        self.score = 0

    @staticmethod
    def game_menu(image, start_game, screen_surface):
        font = pygame_menu.font.FONT_DIGITAL
        main_theme = pygame_menu.Theme(widget_font=font,
                                       background_color=(0, 0, 0, 0),
                                       title_background_color=(0, 0, 0),
                                       title_font_shadow=True,
                                       widget_padding=(35, 0),
                                       widget_font_size=70,
                                       widget_margin=(0, 20)
                                       )
        main_theme.set_background_color_opacity(0)
        menu = pygame_menu.Menu('', 960, 960, theme=main_theme)
        menu.add.button('Play', start_game)

        menu.add.button('Quit', pygame_menu.events.EXIT)

        while True:
            screen_surface.blit(image, (0, 0))
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    exit()

            if menu.is_enabled():
                menu.update(events)
                menu.draw(screen_surface)

            pygame.display.update()

    @staticmethod
    def control(change_direction):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    change_direction = 'UP'
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    change_direction = 'DOWN'
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    change_direction = 'RIGHT'
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    change_direction = 'LEFT'
        return change_direction

    def screen_update(self):
        pygame.display.flip()
        self.fps_controller.tick(self.speed)

    def drawing_a_score_speed(self):
        font = pygame.font.SysFont('Arial', 25)
        render_score = font.render(f'Score: {self.score}', True, pygame.Color('white'))
        render_speed = font.render(f'Speed: {int(self.speed-10)}', True, pygame.Color('white'))
        self.screen_surface.blit(render_score, (10, 40))
        self.screen_surface.blit(render_speed, (10, 10))

    def game_over(self):
        font_end = pygame.font.SysFont('Arial', 70)
        render_end = font_end.render('Game over', True, pygame.Color('red'))
        self.screen_surface.blit(render_end, (self.screen_w_h // 3, 5))
        self.drawing_a_score_speed()
        pygame.display.flip()
        time.sleep(1)
        self.game_menu(self.image, start_the_game, self.screen_surface)


class Snake:
    def __init__(self, snake_color):
        self.snake_head_x_y = [120, 60]
        self.snake_b = [[120, 60]]
        self.size = 30
        self.snake_color = pygame.Color(f'{snake_color}')
        self.direction = 'DOWN'
        self.change_direction = self.direction

    def direction_change_control(self):
        if any((
            self.change_direction == 'UP' and not self.direction == 'DOWN',
            self.change_direction == 'DOWN' and not self.direction == 'UP',
            self.change_direction == 'RIGHT' and not self.direction == 'LEFT',
            self.change_direction == 'LEFT' and not self.direction == 'RIGHT'
        )):
            self.direction = self.change_direction

    def change_of_direction(self):
        if self.direction == 'UP':
            self.snake_head_x_y[1] -= self.size
        elif self.direction == 'DOWN':
            self.snake_head_x_y[1] += self.size
        elif self.direction == 'RIGHT':
            self.snake_head_x_y[0] += self.size
        elif self.direction == 'LEFT':
            self.snake_head_x_y[0] -= self.size

    def snake_body(self, speed, score, food_position, screen_w_h):
        self.snake_b.insert(0, list(self.snake_head_x_y))
        if self.snake_head_x_y[0] == food_position[0] and self.snake_head_x_y[1] == food_position[1]:
            food_position = [randrange(1, screen_w_h / self.size) * self.size,
                             randrange(1, screen_w_h / self.size) * self.size]
            score += 1
            speed += 0.5
        else:
            self.snake_b.pop()
        return speed, score, food_position

    def drawing_a_snake(self, surface_color, screen_surface):
        screen_surface.fill(pygame.Color(f'{surface_color}'))
        for pos in self.snake_b:
            pygame.draw.rect(screen_surface, self.snake_color, pygame.Rect(
                pos[0], pos[1], self.size - 0.5, self.size - 0.5))

    def collision_check(self, game_over, screen_w_h):
        if any((
                self.snake_head_x_y[0] > screen_w_h - self.size or self.snake_head_x_y[0] < 0,
                self.snake_head_x_y[1] > screen_w_h - self.size or self.snake_head_x_y[1] < 0
        )):
            game_over()
        for block in self.snake_b[1:]:
            if block[0] == self.snake_head_x_y[0] and block[1] == self.snake_head_x_y[1]:
                game_over()


class Food:
    def __init__(self, food_color, screen_w_h):
        self.food_color = pygame.Color(f'{food_color}')
        self.size = 30
        self.food_position = [randrange(1, screen_w_h / self.size) * self.size,
                              randrange(1, screen_w_h / self.size) * self.size]

    def draw_a_food(self, screen_surface):
        pygame.draw.rect(screen_surface, self.food_color, pygame.Rect(
            self.food_position[0], self.food_position[1], self.size, self.size))


def start_the_game():
    select_surface_color = 'black'
    select_snake_color = 'blue'
    select_food_color = 'yellow'

    run = Settings()
    snake = Snake(select_snake_color)
    food = Food(select_food_color, run.screen_w_h)

    while True:
        snake.change_direction = run.control(snake.change_direction)
        snake.direction_change_control()
        snake.change_of_direction()
        run.speed, run.score, food.food_position = snake.snake_body(
            run.speed, run.score, food.food_position, run.screen_w_h)
        snake.drawing_a_snake(select_surface_color, run.screen_surface)
        food.draw_a_food(run.screen_surface)
        snake.collision_check(run.game_over, run.screen_w_h)
        run.drawing_a_score_speed()
        run.screen_update()


if __name__ == '__main__':
    Settings().game_menu(Settings().image, start_the_game, Settings().screen_surface)
