import random

import pygame

from Variables import *


class Application:
    def __init__(pac_god):
        pac_god.screen = pygame.Surface((1280, 720))
        pac_god.current_scene = "Login"
        pac_god.scene_game = GameScene()
        pac_god.scene_records = RecordsScene()
        pac_god.scene_login = LogInScene()
        pac_god.stay_here = True

        pac_god.username = None

        pygame.mixer.music.load('Static/Sounds/background.ogg')
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)

    def updating(pac_god, userinput, events):
        pac_god.logic(userinput)

        if not pac_god.stay_here:
            pac_god.reset()

        if pac_god.current_scene == "Game":
            pac_god.scene_game.update(userinput)
            pac_god.screen.blit(pac_god.scene_game.screen, (0, 0))
        if pac_god.current_scene == "Login":
            pac_god.scene_login.update()
            pac_god.screen.blit(pac_god.scene_login.screen, (0, 0))
        if pac_god.current_scene == "Records":
            pac_god.scene_records.update(userinput)
            pac_god.screen.blit(pac_god.scene_records.screen, (0, 0))

    def logic(pac_god, userinput):
        pass
        if pac_god.scene_login.done and pac_god.current_scene == "Login":
            pac_god.username = pac_god.scene_login.nickname
            pac_god.scene_game.username = pac_god.username
            pac_god.scene_game.start("generated")
            pygame.mixer.music.set_volume(0.1)
            pac_god.current_scene = "Game"
        if pac_god.scene_game.stay_here == False and pac_god.current_scene == "Game":
            pac_god.scene_game.stay_here = True
            pygame.mixer.music.set_volume(0.5)
            pac_god.current_scene = "Records"
        if pac_god.scene_records.stay_here == False and pac_god.current_scene == "Records":
            pac_god.scene_records.stay_here = True
            pygame.mixer.music.set_volume(0.1)
            pac_god.current_scene = "Game"


def stopchecking():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
    user_input = pygame.key.get_pressed()
    if user_input[pygame.K_ESCAPE]:
        return False
    return True


def main():
    pygame.init()
    screen = pygame.Surface((1280, 720))
    game_app = Application()

    while stopchecking():
        events = pygame.event.get()
        user_input = pygame.key.get_pressed()
        game_app.updating(user_input, events)
        screen.blit(game_app.screen, (0, 0))
        pygame.display.flip()

    pygame.quit()


class LogInScene:
    def __init__(pac_god):
        pac_god.screen = pygame.Surface((1280, 720))
        pac_god.nickname = ""
        pac_god.done = False
        pac_god.font_header = pygame.font.Font('Static/Fonts/PAC-FONT.ttf', 120)
        pac_god.font_sub_header = pygame.font.Font('Static/Fonts/mini_pixel-7.ttf', 60)
        pac_god.font_regular = pygame.font.Font('Static/Fonts/mini_pixel-7.ttf', 50)
        pac_god.font_small = pygame.font.Font('Static/Fonts/mini_pixel-7.ttf', 30)
        pac_god.rendering()

    def update(pac_god):
        events = pygame.event.get()
        while not pac_god.done and len(events) > 0:
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        pac_god.done = True
                    elif event.key == pygame.K_BACKSPACE:
                        pac_god.nickname = pac_god.nickname[:-1]
                    elif len(pac_god.nickname) < 15:
                        pac_god.nickname += event.unicode
            events = pygame.event.get()
        pac_god.rendering()

    def rendering(pac_god):
        pac_god.screen.fill(color_black)
        header_text = pac_god.font_header.render("Pac----Man", True, whiteColor)
        sub_header_text = pac_god.font_sub_header.render("Enter Your UserName And Press Enter", True, whiteColor)
        nickname_text = pac_god.font_regular.render(pac_god.nickname, True, whiteColor)
        middle = pac_god.screen.get_width() // 2
        pac_god.screen.blit(header_text, (middle - header_text.get_width() // 2, 30))
        pac_god.screen.blit(sub_header_text, (middle - sub_header_text.get_width() // 2, 250))
        pac_god.screen.blit(nickname_text, (middle - nickname_text.get_width() // 2, 350))
        pygame.draw.rect(pac_god.screen, whiteColor, (
            middle - nickname_text.get_width() // 2 - 10, 360 - 10, nickname_text.get_width() + 15,
            nickname_text.get_height()), 3)


class RecordsScene:
    def __init__(pac_god):
        pac_god.screen = pygame.Surface((1280, 720))
        pac_god.stay_here = True

    def update(pac_god, userinput):
        pac_god.manage_user_input(userinput)

        font_regular = pygame.font.Font('Static/Fonts/mini_pixel-7.ttf', 50)
        font_large = pygame.font.Font('Static/Fonts/mini_pixel-7.ttf', 70)
        font_small = pygame.font.Font('Static/Fonts/mini_pixel-7.ttf', 30)
        lines = get_all()
        lines.reverse()

        surfaces = []
        for line in lines:
            new_surface = font_regular.render(line, True, whiteColor)
            surfaces.append(new_surface)

        header = font_large.render("RECORDS", True, whiteColor)
        go_back_text = font_small.render("Press 'B' to go back", True, whiteColor)
        middle = pac_god.screen.get_width() // 2
        pac_god.screen.fill(color_black)
        pac_god.screen.blit(header, (middle - header.get_width() // 2, 20))
        pac_god.screen.blit(go_back_text, (middle - header.get_width() // 2, pac_god.screen.get_height() - 50))

        for i in range(len(surfaces)):
            pac_god.screen.blit(surfaces[i], (100, 100 + 40 * i))

    def manage_user_input(pac_god, userinput):
        if userinput[pygame.K_b]:
            pac_god.stay_here = False


class PacMan:
    def __init__(pac_god, screenWidth, map, position, cellWidth):
        pac_god.screen = pygame.Surface((screenWidth, screenWidth), pygame.SRCALPHA)
        pac_god.map = map
        pac_god.direction_movement = 'R'
        pac_god.direction_desired = 'R'
        pac_god.speed = 2
        pac_god.pos_x = position[1]  # j - index
        pac_god.pos_y = position[0]  # i - index
        pac_god.cell_width = cellWidth
        pac_god.screen_pos_x = cellWidth * pac_god.pos_x - cellWidth // 4
        pac_god.screen_pos_y = cellWidth * pac_god.pos_y - cellWidth // 4
        pac_god.sprite_faze = 0

    def update(pac_god, userinput):
        pac_god.manage_portals()
        pac_god.manage_user_input(userinput)
        pac_god.manage_speed()
        pac_god.manage_position()
        pac_god.screen.fill(color_transparent)
        sprite_path = f"Static/Sprites/Pacman/Pacman-{pac_god.get_sprite()}"
        sprite = pygame.image.load(sprite_path)
        pac_god.screen.blit(sprite, (0, 0))
        # pygame.draw.circle(self.screen, color_yellow, (self.screen.get_width() // 2, self.screen.get_height() // 2), self.screen.get_width() // 2)

    def get_sprite(pac_god):
        pac_god.sprite_faze += 0.35
        if pac_god.sprite_faze > 3:
            pac_god.sprite_faze = 0
        fazes = ["Closed", "Ajar", "Open", "Ajar"]

        if fazes[int(pac_god.sprite_faze)] != "Closed":
            return f"{fazes[int(pac_god.sprite_faze)]}-{pac_god.direction_movement}.png"
        else:
            return f"{fazes[int(pac_god.sprite_faze)]}.png"

    def manage_portals(pac_god):
        pac_god.update_pos()
        portal_pos = find_portals(pac_god.map)
        p1_pos = [portal_pos[0], portal_pos[1]]
        p2_pos = [portal_pos[2], portal_pos[3]]
        if pac_god.map[pac_god.pos_y][pac_god.pos_x] == 'p1':
            pac_god.pos_x = p2_pos[1] - 1
            pac_god.pos_y = p2_pos[0]
            pac_god.screen_pos_x = pac_god.cell_width * pac_god.pos_x - pac_god.cell_width // 4
            pac_god.screen_pos_y = pac_god.cell_width * pac_god.pos_y - pac_god.cell_width // 4
        if pac_god.map[pac_god.pos_y][pac_god.pos_x] == 'p2':
            pac_god.pos_x = p1_pos[1] + 1
            pac_god.pos_y = p1_pos[0]
            pac_god.screen_pos_x = pac_god.cell_width * pac_god.pos_x - pac_god.cell_width // 4
            pac_god.screen_pos_y = pac_god.cell_width * pac_god.pos_y - pac_god.cell_width // 4

    def manage_position(pac_god):
        if pac_god.direction_movement == 'D':
            pac_god.screen_pos_y += pac_god.speed
        elif pac_god.direction_movement == 'L':
            pac_god.screen_pos_x -= pac_god.speed
        elif pac_god.direction_movement == 'R':
            pac_god.screen_pos_x += pac_god.speed
        elif pac_god.direction_movement == 'U':
            pac_god.screen_pos_y -= pac_god.speed
        pac_god.align()

    def manage_speed(pac_god):
        i = pac_god.pos_y
        j = pac_god.pos_x
        if pac_god.direction_movement == 'D':
            if pac_god.map[i + 1][j] != '#':
                pac_god.speed = 2
            elif pac_god.screen_pos_y > pac_god.pos_y * pac_god.cell_width - pac_god.cell_width // 4:
                pac_god.screen_pos_y = pac_god.pos_y * pac_god.cell_width - pac_god.cell_width // 4
                pac_god.speed = 0
        elif pac_god.direction_movement == 'L':
            if pac_god.map[i][j - 1] != '#':
                pac_god.speed = 2
            elif pac_god.screen_pos_x < pac_god.pos_x * pac_god.cell_width - pac_god.cell_width // 4:
                pac_god.screen_pos_x = pac_god.pos_x * pac_god.cell_width - pac_god.cell_width // 4
                pac_god.speed = 0

        elif pac_god.direction_movement == 'R':
            if pac_god.map[i][j + 1] != '#':
                pac_god.speed = 2
            elif pac_god.screen_pos_x > pac_god.pos_x * pac_god.cell_width - pac_god.cell_width // 4:
                pac_god.screen_pos_x = pac_god.pos_x * pac_god.cell_width - pac_god.cell_width // 4
                pac_god.speed = 0
        elif pac_god.direction_movement == 'U':
            if pac_god.map[i - 1][j] != '#':
                pac_god.speed = 2
            elif pac_god.screen_pos_y < pac_god.pos_y * pac_god.cell_width - pac_god.cell_width // 4:
                pac_god.screen_pos_y = pac_god.pos_y * pac_god.cell_width - pac_god.cell_width // 4
                pac_god.speed = 0

    def manage_user_input(self, user_input):
        self.update_pos()
        i = self.pos_y
        j = self.pos_x

        if user_input[pygame.K_w]:
            self.direction_desired = 'U'
        if user_input[pygame.K_d]:
            self.direction_desired = 'R'
        if user_input[pygame.K_s]:
            self.direction_desired = 'D'
        if user_input[pygame.K_a]:
            self.direction_desired = 'L'

        if self.direction_desired == 'U' and self.map[i - 1][j] != '#':
            self.direction_movement = self.direction_desired
        if self.direction_desired == 'R' and self.map[i][j + 1] != '#':
            self.direction_movement = self.direction_desired
        if self.direction_desired == 'D' and self.map[i + 1][j] != '#':
            self.direction_movement = self.direction_desired
        if self.direction_desired == 'L' and self.map[i][j - 1] != '#':
            self.direction_movement = self.direction_desired

    def align(self):
        if self.direction_movement in ['U', 'D']:
            self.align_horizontal()
        if self.direction_movement in ['R', 'L']:
            self.align_vertical()

    def align_vertical(self):
        self.screen_pos_y = self.cell_width * self.pos_y - self.cell_width // 4

    def align_horizontal(self):
        self.screen_pos_x = self.cell_width * self.pos_x - self.cell_width // 4

    def update_pos(self):
        self.pos_x = int((self.screen_pos_x + (
                    self.screen.get_width() - self.cell_width // 2) // 2 + self.cell_width // 4) // self.cell_width)
        self.pos_y = int((self.screen_pos_y + (
                    self.screen.get_height() - self.cell_width // 2) // 2 + self.cell_width // 4) // self.cell_width)


def find_portals(map):
    result = [None] * 4
    for i in range(len(map)):
        for j in range(len(map[0])):
            if map[i][j] == 'p1':
                result[0] = i
                result[1] = j
            if map[i][j] == 'p2':
                result[2] = i
                result[3] = j
    return result


class GameScene:
    def __init__(self):
        self.screen = pygame.Surface((1280, 720))
        self.screen_map = pygame.Surface((644, 713))
        self.stay_here = True
        self.username = ""
        self.paused = False
        self.music = True
        self.ivent_timer = 0
        self.pacman = None
        self.ghosts = []
        self.map = None
        self.food = []
        self.score = 0
        self.score_high = 0
        self.lives = 3
        self.start_sound = pygame.mixer.Sound('Static/Sounds/game_start.ogg')

    def start(self, map_type):
        if map_type == "default":
            self.map = default_map
        elif map_type == "generated":
            self.map = map_generator.generate_map()

        width = self.screen_map.get_height() // len(self.map)
        qw = width // 4  # quater width
        pacman_spawn = get_pacman_spawn(self.map)
        self.pacman = PacMan(width + 2 * qw, self.map, pacman_spawn, width)
        self.ghosts = self.init_ghosts()
        self.food = self.init_food()

        self.score = 0
        self.lives = 3

        self.start_sound.stop()
        self.start_sound.play()

    def update(self, user_input):
        self.ivent_timer += 1
        self.manage_user_input(user_input)
        if not self.paused:
            self.pacman.updating(user_input, )
            self.update_gosts()
            self.game_logic()
        self.screen_map.fill(color_black)
        self.screen.fill(color_black)
        self.render_map()
        self.render_food()
        self.render_ghosts()
        self.render_pacman()
        self.render_ui()
        self.screen.blit(self.screen_map, (0, 0))

    def game_logic(self):
        if self.pacman_bumped_into_ghost():
            if self.ghosts[0].mode == "Normal":
                self.death()
            else:
                eat_ghost_sound = pygame.mixer.Sound('Static/Sounds/eat_ghost.ogg')
                eat_ghost_sound.play()
                self.send_ghost_to_prison()

        if len(self.food) == 0:
            win_sound = pygame.mixer.Sound('Static/Sounds/win.ogg')
            win_sound.play()
            make_a_record(self.username, self.score)
            self.start("generated")

        self.update_food()
        self.check_gates()
        self.score_high = get_high(self.username)
        self.score_high = max(self.score_high, self.score)

    def send_ghost_to_prison(self):
        for ghost in self.ghosts:
            if self.pacman.pos_x == ghost.pos_x and self.pacman.pos_y == ghost.pos_y:
                spawn = get_ghost_spawn(self.map)
                sp_i = spawn[0]
                sp_j = spawn[1]
                ghost.pos_x = sp_j + 2
                ghost.pos_y = sp_i
                width = self.screen_map.get_height() // len(self.map)
                ghost.screen_pos_x = width * ghost.pos_x - width // 4
                ghost.screen_pos_y = width * ghost.pos_y - width // 4
        num_of_ghost = self.how_many_prisoned_ghosts()
        self.score += (200 * num_of_ghost)

    def manage_user_input(self, user_input):
        if self.ivent_timer < 10:
            return
        if user_input[pygame.K_p]:
            self.paused = not self.paused
            self.ivent_timer = 0
        if user_input[pygame.K_r] and user_input[pygame.K_c]:
            self.replay_on_current_map()
            self.ivent_timer = 0
        if user_input[pygame.K_r] and user_input[pygame.K_g]:
            self.start("generated")
            self.ivent_timer = 0
        if user_input[pygame.K_r] and user_input[pygame.K_d]:
            self.start("default")
            self.ivent_timer = 0
        if user_input[pygame.K_v]:
            self.stay_here = False
        if user_input[pygame.K_m]:
            self.music = not self.music
            if self.music:
                pygame.mixer.music.play()
            else:
                pygame.mixer.music.pause()
            self.ivent_timer = 0

    def replay_on_current_map(self):
        width = self.screen_map.get_height() // len(self.map)
        qw = width // 4  # quater width
        pacman_spawn = get_pacman_spawn(self.map)
        self.pacman = PacMan(width + 2 * qw, self.map, pacman_spawn, width)
        self.ghosts = self.init_ghosts()
        self.food = self.init_food()
        self.score = 0
        self.lives = 3

    def death(self):
        death_sound = pygame.mixer.Sound('Static/Sounds/death.ogg')
        death_sound.play()

        self.lives -= 1

        if self.lives > 0:
            width = self.screen_map.get_height() // len(self.map)
            qw = width // 4  # quater width
            pacman_spawn = get_pacman_spawn(self.map)
            self.pacman = PacMan(width + 2 * qw, self.map, pacman_spawn, width)
            self.ghosts = self.init_ghosts()
        else:
            make_a_record(self.username, self.score)
            self.start("generated")

    def render_ui(self):
        small_font = pygame.font.Font('Static/Fonts/mini_pixel-7.ttf', 23)
        regular_font = pygame.font.Font('Static/Fonts/mini_pixel-7.ttf', 30)
        regular_font_large = pygame.font.Font('Static/Fonts/mini_pixel-7.ttf', 40)
        header_font = pygame.font.Font('Static/Fonts/PAC-FONT.ttf', 98)
        header = header_font.render("Pac---Man", True, whiteColor)
        score_text = regular_font_large.render(
            f"Score: {str(self.score)}", True, whiteColor
        )

        lives_text = regular_font_large.render(
            f"Lives: {str(self.lives)}", True, whiteColor
        )

        replay_default_text = regular_font.render("R + D -> replay on default map", True, whiteColor)
        replay_generated_text = regular_font.render("R + G -> replay on generated map", True, whiteColor)
        replay_text = regular_font.render("R + C -> replay on current map", True, whiteColor)
        see_records_text = regular_font.render("V     -> see records", True, whiteColor)
        pause_text = regular_font.render("P     -> play/pause", True, whiteColor)
        escape_text = regular_font.render("Esc   -> quit game", True, whiteColor)
        paused_text = regular_font_large.render("PAUSED", True, whiteColor)
        username_text = regular_font_large.render(
            f"Player: {self.username}", True, whiteColor
        )

        high_score_text = regular_font_large.render(
            f"High: {str(self.score_high)}", True, whiteColor
        )

        mute_music_text = None
        if self.music:
            mute_music_text = regular_font.render("M     -> mute music", True, whiteColor)
        else:
            mute_music_text = regular_font.render("M     -> unmute music", True, whiteColor)
        credit_text = small_font.render("G.Koganovskiy 2020", True, whiteColor)
        self.screen.blit(header, (self.screen_map.get_width() + 20, 10))
        self.screen.blit(score_text, (self.screen_map.get_width() + 20, 120))
        self.screen.blit(high_score_text, (self.screen_map.get_width() + 20, 150))
        self.screen.blit(lives_text, (self.screen_map.get_width() + 20, 180))
        self.screen.blit(username_text, (self.screen_map.get_width() + 20, 220))
        self.screen.blit(pause_text, (self.screen_map.get_width() + 20, 310))
        self.screen.blit(replay_text, (self.screen_map.get_width() + 20, 340))
        self.screen.blit(replay_generated_text, (self.screen_map.get_width() + 20, 370))
        self.screen.blit(replay_default_text, (self.screen_map.get_width() + 20, 400))
        self.screen.blit(see_records_text, (self.screen_map.get_width() + 20, 430))
        self.screen.blit(mute_music_text, (self.screen_map.get_width() + 20, 460))
        self.screen.blit(escape_text, (self.screen_map.get_width() + 20, 490))
        self.screen.blit(credit_text,
                         (self.screen.get_width() - credit_text.get_width() - 10, self.screen.get_height() - 20))
        middle = (self.screen.get_width() - self.screen_map.get_width()) // 2 + self.screen_map.get_width()
        if self.paused:
            self.screen.blit(paused_text, (middle - paused_text.get_width() // 2, 550))

    def check_gates(self):
        gates_pos = get_gates_pos(self.map)
        i = gates_pos[0]
        j = gates_pos[1]
        if self.prisoned_ghosts():
            self.map[i][j] = 'U'
            self.map[i][j + 1] = 'U'
        else:
            self.map[i][j] = '#'
            self.map[i][j + 1] = '#'

    def prisoned_ghosts(self):
        for ghost in self.ghosts:
            i = ghost.pos_y
            j = ghost.pos_x
            if self.map[i][j] == 'U' and ghost.mode == "Normal":
                return True
        return False

    def how_many_prisoned_ghosts(self):
        result = 0
        for ghost in self.ghosts:
            i = ghost.pos_y
            j = ghost.pos_x
            if self.map[i][j] in ['U', 'g']:
                result += 1
        return result

    def scare_ghosts(self):
        for ghost in self.ghosts:
            ghost.go_to_scare_mode()

    def update_food(self):
        ind = 0
        while ind < len(self.food):
            food_piece = self.food[ind]
            i = food_piece.i
            j = food_piece.j
            if self.pacman.pos_y == i and self.pacman.pos_x == j:
                if food_piece.type == "Energizer":
                    energizer_sound = pygame.mixer.Sound('Static/Sounds/energizer.ogg')
                    energizer_sound.play()
                    self.scare_ghosts()
                if len(self.food) % 4 == 0:
                    eat_sound = pygame.mixer.Sound('Static/Sounds/eating.ogg')
                    eat_sound.play()
                self.food.pop(ind)
                self.score += 10
            ind += 1

    def render_food(self):
        width = self.screen_map.get_height() // len(self.map)
        for food_piece in self.food:
            i = food_piece.i
            j = food_piece.j
            if food_piece.type == "Energizer":
                if self.ivent_timer % 30 > 15:
                    pygame.draw.circle(self.screen_map, color_food, (j * width + width // 2, i * width + width // 2),
                                       12)
            else:
                pygame.draw.circle(self.screen_map, color_food, (j * width + width // 2, i * width + width // 2), 3)

    def init_food(self):
        food_array = []
        for i in range(len(self.map)):
            for j in range(len(self.map[0])):
                if self.map[i][j] == 'O':
                    new_food_piece = None
                    if (i == 1 and j == 1) or (i == 29 and j == 1) or (i == 1 and j == 26) or (i == 29 and j == 26):
                        new_food_piece = FoodPiece(i, j, "Energizer")
                    else:
                        new_food_piece = FoodPiece(i, j)
                    food_array.append(new_food_piece)
        return food_array

    def pacman_bumped_into_ghost(self):
        return any(
            self.pacman.pos_x == ghost.pos_x and self.pacman.pos_y == ghost.pos_y
            for ghost in self.ghosts
        )

    def update_gosts(self):
        blinky = self.ghosts[0]
        for ghost in self.ghosts:
            ghost.updating(self.pacman, blinky)

    def render_map(self):
        width = self.screen_map.get_height() // len(self.map)
        qw = width // 4  # quater width
        for i in range(len(self.map)):
            for j in range(len(self.map[0])):
                if self.map[i][j] == '#':
                    pygame.draw.rect(self.screen_map, color_dark_blue, (j * width, i * width, width, width))
                lines = get_render_lines(self.map, i, j)
                if lines[0]:
                    pygame.draw.line(self.screen_map, color_bright_blue, (j * width, i * width + qw),
                                     ((j + 1) * width, i * width + qw), 10)
                if lines[1]:
                    pygame.draw.line(self.screen_map, color_bright_blue, ((j + 1) * width - qw, i * width),
                                     ((j + 1) * width - qw, (i + 1) * width), 10)
                if lines[2]:
                    pygame.draw.line(self.screen_map, color_bright_blue, ((j + 1) * width, (i + 1) * width - qw),
                                     (j * width, (i + 1) * width - qw), 10)
                if lines[3]:
                    pygame.draw.line(self.screen_map, color_bright_blue, (j * width + qw, i * width),
                                     (j * width + qw, (i + 1) * width), 10)
                if lines[0]:
                    pygame.draw.line(self.screen_map, color_blue, (j * width, i * width + qw),
                                     ((j + 1) * width, i * width + qw), 5)
                if lines[1]:
                    pygame.draw.line(self.screen_map, color_blue, ((j + 1) * width - qw, i * width),
                                     ((j + 1) * width - qw, (i + 1) * width), 5)
                if lines[2]:
                    pygame.draw.line(self.screen_map, color_blue, ((j + 1) * width, (i + 1) * width - qw),
                                     (j * width, (i + 1) * width - qw), 5)
                if lines[3]:
                    pygame.draw.line(self.screen_map, color_blue, (j * width + qw, i * width),
                                     (j * width + qw, (i + 1) * width), 5)
        for i in range(len(self.map)):
            for j in range(len(self.map[0])):
                if self.map[i][j] != '#':
                    pygame.draw.rect(self.screen_map, color_black,
                                     (j * width - qw, i * width - qw, width + 2 * qw, width + 2 * qw))
        pygame.draw.rect(self.screen_map, color_black, (0, 0, 644, 713), width // 2)
        # pygame.draw.rect(self.screen_map, color_yellow, (self.ghost.pos_x * width, self.ghost.pos_y * width, width, width))

    def render_pacman(self):
        self.screen_map.blit(self.pacman.screen, (self.pacman.screen_pos_x, self.pacman.screen_pos_y))

    def render_ghosts(self):
        for ghost in self.ghosts:
            self.screen_map.blit(ghost.screen, (ghost.screen_pos_x, ghost.screen_pos_y))

    def init_ghosts(self):
        width = self.screen_map.get_height() // len(self.map)
        qw = width // 4  # quater width
        spawn = get_ghost_spawn(self.map)
        sp_i = spawn[0]
        sp_j = spawn[1]
        blinky = Ghost("Blinky", width + 2 * qw, self.map, [sp_i, sp_j + 2], width)
        pinky = Ghost("Pinky", width + 2 * qw, self.map, [sp_i, sp_j + 3], width)
        inky = Ghost("Inky", width + 2 * qw, self.map, [sp_i + 1, sp_j + 2], width)
        clyde = Ghost("Clyde", width + 2 * qw, self.map, [sp_i + 1, sp_j + 3], width)
        return [blinky, pinky, inky, clyde]


def get_render_lines(map, i, j):
    result = [False, False, False, False]  # up - right - down - left
    if map[i][j] == '#':
        if i == 0 or map[i - 1][j] != '#':
            result[0] = True
        if j == len(map[0]) - 1 or map[i][j + 1] != '#':
            result[1] = True
        if i == len(map) - 1 or map[i + 1][j] != '#':
            result[2] = True
        if j == 0 or map[i][j - 1] != '#':
            result[3] = True
    return result


def get_pacman_spawn(map):
    result = [None, None]
    for i in range(len(map)):
        for j in range(len(map[0])):
            if map[i][j] == 'p':
                result[0] = i
                result[1] = j
                return result


def get_ghost_spawn(map):
    result = [None, None]
    for i in range(len(map)):
        for j in range(len(map[0])):
            if map[i][j] == 'g':
                result[0] = i
                result[1] = j
                return result


def get_gates_pos(map):
    result = [None, None]
    for i in range(len(map)):
        for j in range(len(map[0])):
            if map[i][j] == 'g':
                result[0] = i - 2
                result[1] = j + 2
                return result


def get_high(name):
    result = 0
    DataBase = open("DataBase.txt", "r")
    lines = DataBase.readlines()
    for line in lines:
        line = line.split()
        if line[0] == name and int(line[1]) > result:
            result = int(line[1])
    return result


def make_a_record(name, score):
    line = f"{name} {str(score)} \n"
    DataBase = open("DataBase.txt", "a+")
    DataBase.write(line)


def get_all():
    DataBase = open("DataBase.txt", "r")
    return DataBase.readlines()


if __name__ == '__main__':
    DataBase = open("DataBase.txt", "r")
    lines = DataBase.readlines()
    make_a_record("Hira", 3770)
    print(get_high("Hira"))
    for line in lines:
        print(line)


class Ghost:
    def __init__(self, name, screen_width, map, position, cell_width):
        self.screen = pygame.Surface((screen_width, screen_width), pygame.SRCALPHA)
        self.map = map
        self.direction_movement = 'U'
        self.speed = 1.88
        self.pos_x = position[1]  # j - index
        self.pos_y = position[0]  # i - index
        self.cell_width = cell_width
        self.screen_pos_x = cell_width * self.pos_x - cell_width // 4
        self.screen_pos_y = cell_width * self.pos_y - cell_width // 4
        self.name = name
        self.mode = "Normal"
        self.target = None
        self.timer = 0
        self.last_cell = [self.pos_y, self.pos_x]
        if self.name == "Blinky":
            self.color = color_red
        elif self.name == "Inky":
            self.color = color_inky
        elif self.name == "Pinky":
            self.color = color_pink
        elif self.name == "Clyde":
            self.color = color_clyde
        else:
            self.color = whiteColor

    def update(self, pacman, blinky=None):
        self.timer += 1

        if self.mode == "Scared" and self.timer > 850:
            self.mode = "Normal"

        target = self.get_target(pacman, blinky)
        self.target = target
        self.follow_target(target)
        self.manage_speed([pacman.pos_x, pacman.pos_y])
        self.manage_position()

        self.screen.fill(color_transparent)
        sprite_path = None
        if self.mode == "Normal":
            sprite_path = f"Static/Sprites/{str(self.name)}/{str(self.name)}-{self.direction_movement}.png"

        else:
            sprite_faze = str((self.timer % 30 > 15) + 1)
            sprite_path = f"Static/Sprites/Scared/Fear-{sprite_faze}.png"
        sprite = pygame.image.load(sprite_path)
        self.screen.blit(sprite, (0, 0))

    def get_target(self, pacman, blinky=None):
        if self.mode == "Scared":
            if self.timer % 20 == 1:
                return [random.randint(0, 30), random.randint(0, 27)]
            else:
                return self.target

        if self.map[self.pos_y][self.pos_x] == 'U':
            return [13, 0]

        if self.name == "Blinky":
            return [pacman.pos_x, pacman.pos_y]
        if self.name == "Pinky":
            pacman_direction = pacman.direction_movement
            target_x = None
            target_y = None
            if pacman_direction == 'D':
                target_x = pacman.pos_x
                target_y = pacman.pos_y + 4
            elif pacman_direction == 'L':
                target_x = pacman.pos_x - 4
                target_y = pacman.pos_y
            elif pacman_direction == 'R':
                target_x = pacman.pos_x + 4
                target_y = pacman.pos_y
            elif pacman_direction == 'U':
                target_x = pacman.pos_x
                target_y = pacman.pos_y - 4
            return [target_x, target_y]
        if self.name == "Inky":
            vector_x = blinky.pos_x - pacman.pos_x
            target_x = pacman.pos_x - vector_x
            vector_y = blinky.pos_y - pacman.pos_y
            target_y = pacman.pos_y - vector_y
            return [target_x, target_y]
        if self.name == "Clyde":
            dist_to_pacman = dist(pacman.pos_x, pacman.pos_y, self.pos_x, self.pos_y)
            return [14, 15] if dist_to_pacman <= 8 else [pacman.pos_x, pacman.pos_y]

    def follow_target(self, target):
        self.update_pos()
        i = self.pos_y
        j = self.pos_x

        potential_directions = []
        if self.direction_movement == 'D':
            potential_directions.extend(('D', 'L', 'R'))
        elif self.direction_movement == 'L':
            potential_directions.extend(('D', 'L', 'U'))
        elif self.direction_movement == 'R':
            potential_directions.extend(('D', 'U', 'R'))
        elif self.direction_movement == 'U':
            potential_directions.extend(('L', 'U', 'R'))
        else:
            potential_directions.extend(('D', 'L', 'U', 'R'))
        final_directions = []
        last_i = self.last_cell[0]
        last_j = self.last_cell[1]
        for direction in potential_directions:
            if (
                    direction == 'U'
                    and self.map[i - 1][j] == 'O'
                    and (last_i != i - 1 or last_j != j)
            ):
                final_directions.append('U')
            if (
                    direction == 'R'
                    and self.map[i][j + 1] == 'O'
                    and (last_i != i or last_j != j + 1)
            ):
                final_directions.append('R')
            if (
                    direction == 'D'
                    and self.map[i + 1][j] == 'O'
                    and (last_i != i + 1 or last_j != j)
            ):
                final_directions.append('D')
            if (
                    direction == 'L'
                    and self.map[i][j - 1] == 'O'
                    and (last_i != i or last_j != j - 1)
            ):
                final_directions.append('L')

        if not final_directions:
            for direction in potential_directions:
                if (
                        direction == 'U'
                        and self.map[i - 1][j] != '#'
                        and (last_i != i - 1 or last_j != j)
                ):
                    final_directions.append('U')
                if (
                        direction == 'R'
                        and self.map[i][j + 1] != '#'
                        and (last_i != i or last_j != j + 1)
                ):
                    final_directions.append('R')
                if (
                        direction == 'D'
                        and self.map[i + 1][j] != '#'
                        and (last_i != i + 1 or last_j != j)
                ):
                    final_directions.append('D')
                if (
                        direction == 'L'
                        and self.map[i][j - 1] != '#'
                        and (last_i != i or last_j != j - 1)
                ):
                    final_directions.append('L')

        direction_desired = None
        shortest_dist = 1000
        for direction in final_directions:
            if direction == 'D':
                if dist(target[0], target[1], j, i + 1) < shortest_dist:
                    shortest_dist = dist(target[0], target[1], j, i + 1)
                    direction_desired = 'D'
            elif direction == 'L':
                if dist(target[0], target[1], j - 1, i) < shortest_dist:
                    shortest_dist = dist(target[0], target[1], j - 1, i)
                    direction_desired = 'L'

            elif direction == 'R':
                if dist(target[0], target[1], j + 1, i) < shortest_dist:
                    shortest_dist = dist(target[0], target[1], j + 1, i)
                    direction_desired = 'R'
            elif direction == 'U':
                if dist(target[0], target[1], j, i - 1) < shortest_dist:
                    shortest_dist = dist(target[0], target[1], j, i - 1)
                    direction_desired = 'U'
        if direction_desired:
            self.direction_movement = direction_desired

    def manage_speed(self, target):
        if self.pos_x == target[0] and self.pos_y == target[1]:
            self.speed = 0
        else:
            self.speed = 1.88 if self.mode == "Normal" else 1.5

    def manage_position(self):
        if self.direction_movement == 'D':
            self.screen_pos_y += self.speed
        elif self.direction_movement == 'L':
            self.screen_pos_x -= self.speed
        elif self.direction_movement == 'R':
            self.screen_pos_x += self.speed
        elif self.direction_movement == 'U':
            self.screen_pos_y -= self.speed
        self.align()

    def align(self):
        if self.direction_movement in ['U', 'D']:
            self.align_horizontal()
        if self.direction_movement in ['R', 'L']:
            self.align_vertical()

    def align_vertical(self):
        self.screen_pos_y = self.cell_width * self.pos_y - self.cell_width // 4

    def align_horizontal(self):
        self.screen_pos_x = self.cell_width * self.pos_x - self.cell_width // 4

    def update_pos(self):
        new_pos_x = int((self.screen_pos_x + (
                    self.screen.get_width() - self.cell_width // 2) // 2 + self.cell_width // 4) // self.cell_width)
        new_pos_y = int((self.screen_pos_y + (
                    self.screen.get_height() - self.cell_width // 2) // 2 + self.cell_width // 4) // self.cell_width)
        if new_pos_x != self.pos_x or new_pos_y != self.pos_y:
            self.last_cell = [self.pos_y, self.pos_x]
        self.pos_x = new_pos_x
        self.pos_y = new_pos_y

    def go_to_scare_mode(self):
        self.mode = "Scared"
        self.timer = 0


def dist(x1, y1, x2, y2):
    return (abs(x1 - x2) ** 2 + abs(y1 - y2) ** 2) ** 0.5


class MapGenerator:
    def __init__(self):
        self.width = 8
        self.height = 9

    def generate_map(self):
        map = None

        while not quality_check(map):
            map = self.make_skeleton()
            map = self.add_ghots_house(map)
            map = self.add_portals(map)
            map = self.thin_passages(map)
            map = self.fill_pockets(map)
            map = self.add_ghots_house(map)
            map = self.add_portals(map)
            map = self.move_dead_ends_to_edges(map)
            map = self.eleminate_dead_ends_on_edges(map)
            map = self.eleminate_extra_passages(map)
        map = self.convert_to_normal_type(map)
        return map

    def make_skeleton(self):
        map = None
        while count_passages_to_walls_ratio(map) <= 0.8:
            maze = self.generate_thin_maze()
            maze = self.no_dead_ends(maze)
            map = self.convert_to_thick_walls(maze)
            map = self.clear_extra_walls(map)
            map = self.cut_out_14X16_piece(map)
            map = self.add_edges(map)
            map = self.check_connection(map)
            map = self.qudruple_map(map)
            map = self.fill_pockets(map)
        return map

    def convert_to_normal_type(self, map):
        map = self.add_converted_ghots_house(map)
        map = self.add_converted_portals(map)
        for i in range(len(map)):
            for j in range(len(map[i])):
                if map[i][j] == 1:
                    map[i][j] = '#'
                if map[i][j] == 0:
                    map[i][j] = 'O'
        map[15][0] = 'p1'
        map[15][1] = 'U'
        map[15][2] = 'U'
        map[15][3] = 'U'
        map[15][4] = 'U'
        map[15][5] = 'U'
        map[15][27] = 'p2'
        map[15][26] = 'U'
        map[15][25] = 'U'
        map[15][24] = 'U'
        map[15][23] = 'U'
        map[15][22] = 'U'
        map[15][11] = 'g'
        map[18][13] = 'p'
        return map

    def eleminate_extra_passages(self, map):
        if quality_check(map):
            for i in range(1, len(map) // 2):
                for j in range(1, len(map[i]) // 2):
                    map_copy = copy_2d_array(map)
                    if map_copy[i][j] == 0:
                        mirror_change(map_copy, i, j, 1)
                        map_copy = self.fill_pockets(map_copy)
                        map_copy = self.add_ghots_house(map_copy)
                        map_copy = self.add_portals(map_copy)
                        if quality_check(map_copy):
                            map = map_copy
        return map

    def eleminate_dead_ends_on_edges(self, map):
        for j in range(1, len(map[0]) - 1):
            map = mirror_change(map, 1, j, 0)
            map = mirror_change(map, 2, j, 1)
        for i in range(2, 10):
            map = mirror_change(map, i, 1, 0)
            map = mirror_change(map, i, 2, 1)

        for j in range(2, len(map[0]) - 2):
            if map[3][j] == 0 and map[2][j - 1] == 1 and map[2][j + 1] == 1:
                map = mirror_change(map, 2, j, 0)
        for i in range(2, 10):
            if map[i][3] == 0 and map[i - 1][2] == 1 and map[i + 1][2] == 1:
                map = mirror_change(map, i, 2, 0)
        map = self.thin_passages(map)
        map = self.fill_pockets(map)
        map = self.add_ghots_house(map)
        map = self.add_portals(map)
        map = self.thin_passages(map)
        map = self.add_ghots_house(map)
        map = self.add_portals(map)
        return map

    def move_dead_ends_to_edges(self, map):
        for i in range(1, len(map) - 1):
            for j in range(1, len(map[i]) - 1):
                neighbors = count_neighbors(map, i, j)
                if neighbors == 3 and map[i][j] == 0:
                    next_cell_i = None
                    next_cell_j = None
                    if map[i + 1][j] == 0:
                        next_cell_i = i - 1
                        next_cell_j = j
                    elif map[i - 1][j] == 0:
                        next_cell_i = i + 1
                        next_cell_j = j
                    elif map[i][j + 1] == 0:
                        next_cell_i = i
                        next_cell_j = j - 1
                    elif map[i][j - 1] == 0:
                        next_cell_i = i
                        next_cell_j = j + 1
                    if next_cell_i > 0 and next_cell_i < len(map) - 1 and next_cell_j > 0 and next_cell_j < len(
                            map[0]) - 1:
                        map = mirror_change(map, next_cell_i, next_cell_j, 0)
        return map

    def thin_passages(self, map):
        for i in range(1, len(map) - 2):
            for j in range(1, len(map[i]) - 2):
                if map[i][j] == 0 and map[i + 1][j] == 0 and map[i][j + 1] == 0 and map[i + 1][j + 1] == 0:
                    fill_x = None
                    fill_y = None
                    fill_y = 0 if i < 15 else 1
                    fill_x = 0 if j < 14 else 1
                    final_y = i + fill_y
                    final_x = j + fill_x
                    map = mirror_change(map, final_y, final_x, 1)
        return map

    def add_portals(self, map):
        start_x = 0
        start_y = int(len(map) // 2 - len(portal_entrance_left) // 2)  # 31 // 2 - 7 // 2
        for i in range(len(portal_entrance_left)):
            for j in range(len(portal_entrance_left[0])):
                map[start_y + i][start_x + j] = portal_entrance_left[i][j]
        start_x = len(map[0]) - len(portal_entrance_right[0])
        for i in range(len(portal_entrance_right)):
            for j in range(len(portal_entrance_right[0])):
                map[start_y + i][start_x + j] = portal_entrance_right[i][j]
        return map

    def add_converted_portals(self, map):
        start_x = 0
        start_y = int(len(map) // 2 - len(portal_entrance_left_converted) // 2)  # 31 // 2 - 7 // 2
        for i in range(len(portal_entrance_left_converted)):
            for j in range(len(portal_entrance_left_converted[0])):
                map[start_y + i][start_x + j] = portal_entrance_left_converted[i][j]
        start_x = len(map[0]) - len(portal_entrance_right_converted[0])
        for i in range(len(portal_entrance_right_converted)):
            for j in range(len(portal_entrance_right_converted[0])):
                map[start_y + i][start_x + j] = portal_entrance_right_converted[i][j]
        return map

    def fill_pockets(self, map):
        result = [[0 for _ in range(len(map[0]))] for _ in range(len(map))]
        start = [15, 0]
        stack = [start]
        while stack:
            current_cell = stack.pop(0)
            i = current_cell[0]
            j = current_cell[1]
            result[i][j] = 1
            if i < len(map) - 1 and result[i + 1][j] == 0 and map[i + 1][j] == 0:
                stack.append([i + 1, j])
            if i > 0 and result[i - 1][j] == 0 and map[i - 1][j] == 0:
                stack.append([i - 1, j])
            if j < len(map[0]) - 1 and result[i][j + 1] == 0 and map[i][j + 1] == 0:
                stack.append([i, j + 1])
            if j > 0 and result[i][j - 1] == 0 and map[i][j - 1] == 0:
                stack.append([i, j - 1])
        result = inverse(result)
        return result

    def check_connection(self, map):
        for i in range(1, len(map[len(map) - 1]) - 1):
            if map[len(map) - 1][i - 1] == 0 and map[len(map) - 1][i + 1] == 0:
                map[len(map) - 1][i] = 1
        return map

    def add_ghots_house(self, map):
        start_x = int(len(map[0]) / 2 - len(ghosts_house[0]) / 2)  # 28 / 2 - 10 / 2
        start_y = int(len(map) // 2 - len(ghosts_house) // 2)  # 31 // 2 - 7 // 2

        for i in range(len(ghosts_house)):
            for j in range(len(ghosts_house[0])):
                map[start_y + i][start_x + j] = ghosts_house[i][j]
        return map

    def add_converted_ghots_house(self, map):
        start_x = int(len(map[0]) / 2 - len(ghosts_house_converted[0]) / 2)  # 28 / 2 - 10 / 2
        start_y = int(len(map) // 2 - len(ghosts_house_converted) // 2)  # 31 // 2 - 7 // 2

        for i in range(len(ghosts_house_converted)):
            for j in range(len(ghosts_house_converted[0])):
                map[start_y + i][start_x + j] = ghosts_house_converted[i][j]
        return map

    def add_edges(self, map):
        for i in range(len(map[0])):
            map[0][i] = 1

        for i in range(len(map)):
            map[i][0] = 1

        return map

    def qudruple_map(self, map):
        original = map
        mirrored_x = copy_2d_array(original)
        for i in range(len(mirrored_x)):
            mirrored_x[i].reverse()
        first_half = []
        for i in range(len(original)):
            line = [original[i][j] for j in range(len(original[0]))]
            line.extend(mirrored_x[i][j] for j in range(len(original[0])))
            first_half.append(line)
        second_half = copy_2d_array(first_half)
        second_half.reverse()
        result = list(first_half)
        result.append(middle_separation_line)
        result.extend(second_half[i] for i in range(len(second_half)))
        return result

    def cut_out_14X16_piece(self, map):
        result = []
        for i in range(1, 16):
            line = [map[i][j] for j in range(1, 15)]
            result.append(line)
        return result

    def clear_extra_walls(self, map):
        original_ratio = 1
        current_ratio = count_passages_to_walls_ratio(map)
        while current_ratio < original_ratio:
            random_x = random.randint(1, len(map[0]) - 2)
            random_y = random.randint(1, len(map) - 2)
            if map[random_y][random_x] == 1:
                map[random_y][random_x] = 0

            current_ratio = count_passages_to_walls_ratio(map)

        return map

    def convert_to_thick_walls(self, maze):
        maze_2d = to_2d(maze, self.width, self.height)

        first_line = [1 for _ in range(self.width * 2 + 1)]
        result = [first_line]
        for i in range(self.height):
            line_up = [1]
            line_side = [1]
            for j in range(self.width):
                line_side.append(0)
                if maze_2d[i][j].wall_right:
                    line_side.append(1)
                else:
                    line_side.append(0)
            for j in range(self.width - 1):
                if i > 0:
                    if maze_2d[i][j].wall_up:
                        line_up.append(1)
                    else:
                        line_up.append(0)
                    if maze_2d[i][j + 1].wall_up or maze_2d[i][j].wall_right or maze_2d[i - 1][j].wall_right or \
                            maze_2d[i][j].wall_up:
                        line_up.append(1)
                    else:
                        line_up.append(0)
            if maze_2d[i][self.width - 1].wall_up:
                line_up.append(1)
            else:
                line_up.append(0)
            line_up.append(1)
            if i > 0:
                result.append(line_up)
            result.append(line_side)

        last_line = [1 for _ in range(self.width * 2 + 1)]
        result.append(last_line)
        return result

    def no_dead_ends(self, maze):
        for c in maze:
            if (c.wall_up + c.wall_right + c.wall_down + c.wall_left > 2):
                remove_random_wall(c, maze, self.width, self.height)
        return maze

    def generate_thin_maze(self):
        grid = []
        for i in range(self.height):
            for j in range(self.width):
                new_cell = Cell(i, j, self.width)
                grid.append(new_cell)

        current_cell = grid[0]
        stack = []

        while not is_maze_completed(grid):
            current_cell.visited = True
            if next_cell := current_cell.get_next(grid, self.width, self.height):
                stack.append(current_cell)
                remove_wall(current_cell, next_cell)
                current_cell = next_cell
            else:
                current_cell = stack.pop()

        return grid


class Cell:
    def __init__(self, i, j, line_len):
        self.i = i
        self.j = j
        self.wall_up = True
        self.wall_down = True
        self.wall_left = True
        self.wall_right = True
        self.visited = False
        self.line_len = line_len

    def get_next(self, grid, width, height):
        neighbors = []

        neighbor_up_index = get_index(self.i - 1, self.j, width, height)
        neighbor_right_index = get_index(self.i, self.j + 1, width, height)
        neighbor_down_index = get_index(self.i + 1, self.j, width, height)
        neighbor_left_index = get_index(self.i, self.j - 1, width, height)

        if neighbor_up_index >= 0 and not grid[neighbor_up_index].visited:
            neighbors.append(grid[neighbor_up_index])
        if neighbor_right_index >= 0 and not grid[neighbor_right_index].visited:
            neighbors.append(grid[neighbor_right_index])
        if neighbor_down_index >= 0 and not grid[neighbor_down_index].visited:
            neighbors.append(grid[neighbor_down_index])
        if neighbor_left_index >= 0 and not grid[neighbor_left_index].visited:
            neighbors.append(grid[neighbor_left_index])

        if neighbors:
            rand_index = random.randint(0, len(neighbors) - 1)
            return neighbors[rand_index]
        else:
            return None


def is_maze_completed(grid):
    return all(c.visited for c in grid)


def get_index(i, j, width, height):
    return -1 if i < 0 or i >= height or j < 0 or j >= width else j + i * width


def remove_wall(cell_a, cell_b):
    shift_x = cell_a.j - cell_b.j
    shift_y = cell_a.i - cell_b.i

    if shift_x == -1:
        cell_a.wall_right = False
        cell_b.wall_left = False
    elif shift_x == 1:
        cell_a.wall_left = False
        cell_b.wall_right = False
    if shift_y == -1:
        cell_a.wall_down = False
        cell_b.wall_up = False
    elif shift_y == 1:
        cell_a.wall_up = False
        cell_b.wall_down = False


def remove_random_wall(current_cell, grid, width, height):
    walls = []

    neighbor_up_index = get_index(current_cell.i - 1, current_cell.j, width, height)
    neighbor_right_index = get_index(current_cell.i, current_cell.j + 1, width, height)
    neighbor_down_index = get_index(current_cell.i + 1, current_cell.j, width, height)
    neighbor_left_index = get_index(current_cell.i, current_cell.j - 1, width, height)

    if (current_cell.wall_up and neighbor_up_index >= 0):
        walls.append('U')
    if (current_cell.wall_right and neighbor_right_index >= 0):
        walls.append('R')
    if (current_cell.wall_down and neighbor_down_index >= 0):
        walls.append('D')
    if (current_cell.wall_left and neighbor_left_index >= 0):
        walls.append('L')

    random_ind = random.randint(0, len(walls) - 1)
    removeable_wall = walls[random_ind]

    if removeable_wall == 'D':
        current_cell.wall_down = False
        grid[neighbor_down_index].wall_up = False
    elif removeable_wall == 'L':
        current_cell.wall_left = False
        grid[neighbor_left_index].wall_right = False

    elif removeable_wall == 'R':
        current_cell.wall_right = False
        grid[neighbor_right_index].wall_left = False
    elif removeable_wall == 'U':
        current_cell.wall_up = False
        grid[neighbor_up_index].wall_down = False
    return grid


def to_2d(linear_array, width, height):
    result = []
    array_copy = copy_array(linear_array)
    for _ in range(height):
        line = [array_copy.pop(0) for _ in range(width)]
        result.append(line)
    return result


def copy_array(array):
    return list(array)


def copy_2d_array(array_2d):
    return [copy_array(array) for array in array_2d]


def count_passages_to_walls_ratio(map):
    if map is None:
        return 0

    walls = 0
    passages = 0
    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j] == 1:
                walls += 1
            if map[i][j] == 0:
                passages += 1
    return passages / walls


def count_neighbors(map, y, x):
    return map[y - 1][x] + map[y + 1][x] + map[y][x - 1] + map[y][x + 1]


def inverse(map):
    for i in range(len(map)):
        for j in range(len(map[i])):
            if map[i][j] == 1:
                map[i][j] = 0
            elif map[i][j] == 0:
                map[i][j] = 1
    return map


def mirror_change(map, y, x, value):
    map[y][x] = value
    map[y][abs(len(map[0]) - x - 1)] = value
    map[abs(len(map) - y - 1)][x] = value
    map[abs(len(map) - y - 1)][abs(len(map[0]) - x - 1)] = value
    return map


def count_thick_passages(map):
    result = 0
    for i in range(1, len(map) - 2):
        for j in range(1, len(map[i]) - 2):
            if map[i][j] == 0 and map[i + 1][j] == 0 and map[i][j + 1] == 0 and map[i + 1][j + 1] == 0:
                condition_1 = (i >= 11 and i <= 13 and j >= 0 and j <= 4)
                condition_2 = (i >= 17 and i <= 19 and j >= 0 and j <= 4)
                condition_3 = (i >= 11 and i <= 13 and j >= 23 and j <= 27)
                condition_4 = (i >= 17 and i <= 19 and j >= 23 and j <= 27)
                condition_5 = (i >= 14 and i <= 16 and j >= 11 and j <= 16)
                if condition_1 and condition_2 and condition_3 and condition_4 and condition_5:
                    result += 1
    return result


def count_dead_ends(map):
    result = 0
    for i in range(1, len(map) - 1):
        for j in range(1, len(map[i]) - 1):
            neighbors = count_neighbors(map, i, j)
            if neighbors == 3 and map[i][j] == 0:
                result += 1
    return result


def quality_check(map):
    result = map is not None
    if result and count_dead_ends(map) > 0:
        result = False
    if result and count_thick_passages(map) > 0:
        result = False
    if result and count_passages_to_walls_ratio(map) < 0.8:
        result = False
    return result


map_generator = MapGenerator()


class FoodPiece:
    def __init__(self, i, j, type=None):
        self.type = None
        self.type = "Energizer" if type else "Normal"
        self.i = i
        self.j = j


class RecordsScene:
    def __init__(self):
        self.screen = pygame.Surface((1280, 720))
        self.stay_here = True

    def update(self, user_input):
        self.manage_user_input(user_input)

        font_regular = pygame.font.Font('Static/Fonts/mini_pixel-7.ttf', 50)
        font_large = pygame.font.Font('Static/Fonts/mini_pixel-7.ttf', 70)
        font_small = pygame.font.Font('Static/Fonts/mini_pixel-7.ttf', 30)
        lines = get_all()
        lines.reverse()

        surfaces = []
        for line in lines:
            new_surface = font_regular.render(line, True, whiteColor)
            surfaces.append(new_surface)

        header = font_large.render("RECORDS", True, whiteColor)
        go_back_text = font_small.render("Press 'B' to go back", True, whiteColor)
        middle = self.screen.get_width() // 2
        self.screen.fill(color_black)
        self.screen.blit(header, (middle - header.get_width() // 2, 20))
        self.screen.blit(go_back_text, (middle - header.get_width() // 2, self.screen.get_height() - 50))

        for i in range(len(surfaces)):
            self.screen.blit(surfaces[i], (100, 100 + 40 * i))

    def manage_user_input(self, user_input):
        if user_input[pygame.K_b]:
            self.stay_here = False
