from random import choice, randrange as rand
import pygame

class Actors:
    def __init__(self,surface, pos=None, name="", reward=0.0, scale=(0,0)):
        self.surface = pygame.transform.scale(surface, scale)

        self.pos = (0,0)
        self.x = self.y = 0.0
        self.name = name
        self.reward = reward
        self.start = pos
        self.end = None
        self.direction = "DOWN"
        self.angle = 0.0

    def update_coords(self, x=0, y=0):
        self.x += x
        self.y += y

    def get_coords(self):
        return self.x, self.y

    def update_pos(self, col=0, row=0):
        self.pos = (self.pos[0] + col, self.pos[1] + row)

    def update_rotation(self, angle, delta=0):
        self.surface = pygame.transform.rotate(self.surface, delta)
        self.angle = angle






class MouseMaze:

    def __init__(self, actions, values,  window=(480,480), rows=6, cols=6, epoch=100, train=False):
        self.rows = rows
        self.cols = cols
        self.window_width = window[0]
        self.window_height = window[1]
        self.sq_sz = window[0] // rows
        self.game_over = False
        self.epoch = epoch
        self.values = values
        self.train = train
        self.running = False
        self.actions = actions

        self.chars = {}
        self.walls = {(2,1):[(2,2)]}

        pygame.init()
        self.board_colors = [[255, 255, 255], [0, 150, 255]]

        self.game_window = pygame.display.set_mode((self.window_width, self.window_height))

        self.locations = {}
        self.init_chars()
        self.init_controls()
        self.init_text_values()
        self.draw_board(self.game_window, self.board_colors)
        pygame.display.update()


    def exit_game(self):
        pygame.quit()


    def check_impact(self):
        return self.mouse.pos == self.chars['cat'].pos or self.mouse.pos == self.chars['trap'].pos


    def get_state(self):
        return ("%s-%s-%s-%s" % (str(self.mouse.pos),
                                 str(self.chars['cat'].pos),
                                 str(self.chars['trap'].pos),
                                 str(self.chars['cheese'].pos)))


    def got_cheese(self):
        return self.mouse.pos == self.chars['cheese'].pos


    def updateScreen(self):
        self.draw_board(self.game_window, self.board_colors)
        pygame.display.update()


    def get_reward(self, cheese=False, impact=False, canMove=True):
        reward = 0.0

        if cheese:
            print("GOT CHEESE")
            reward = 1
        if impact:
            print("DEAD")
            reward = -1
        if canMove == False:
            reward = -0.2

        return reward, True if cheese or impact else False


    def init_text_values(self):
        self.font = pygame.font.SysFont("comicsansms", 12)
        val = "00.00"
        w, h = self.font.size(val)
        text = self.font.render(val, True, (0, 0, 0))
        if not self.values:
            for row in range(self.rows):
                for col in range(self.cols):

                    if (col, row) == self.chars['cheese'].pos:
                        _val = 1
                    elif (col, row) == self.chars['trap'].pos or (col, row) == self.chars['cat'].pos:
                        _val = -1
                    else:
                        _val = 0.0

                    textpos = text.get_rect(centerx=col * self.sq_sz,
                                            centery=row * self.sq_sz)

                    l = (textpos[0]+self.sq_sz//4,textpos[1]+self.sq_sz//2)
                    r = (textpos[0]+self.sq_sz - (w//2),textpos[1]+self.sq_sz//2)
                    u = (textpos[0]+self.sq_sz//2 + (w//4) ,textpos[1]+self.sq_sz//4)
                    d = (textpos[0]+self.sq_sz//2 + (w//4), textpos[1]+self.sq_sz - h)


                    if _val == 0.0:
                        key = "(%s, %s)LEFT" % (str(col), str(row))
                        self.values[key] = (_val, l)
                        key = "(%s, %s)RIGHT" % (str(col), str(row))
                        self.values[key] = (_val, r)
                        key = "(%s, %s)UP" % (str(col), str(row))
                        self.values[key] = (_val, u)
                        key = "(%s, %s)DOWN" % (str(col), str(row))
                        self.values[key] = (_val, d)
                    else:
                        c = (textpos[0] + self.sq_sz//2 + (w // 4), textpos[1] + self.sq_sz//2)
                        key = "(%s, %s)" % (str(col), str(row))
                        self.values[key] = (_val, c)



    def updateText(self, q_val, last_state, cur_state, cameFrom):
        pos = str(last_state[:6])+cameFrom
        value = self.values.get(pos, None)
        if value:
            value = (q_val, value[1])
            self.values[pos] = value


    def hit_wall(self, x, y):
        new_pos = self.mouse.pos[0] + x, self.mouse.pos[1]+y
        _key = None
        for key, val in self.walls.items():
            if (key[1], key[0]) == self.mouse.pos:
                _key = key

        if _key:
            for pos in self.walls[_key]:
                if y < 0:
                    if pos[1] > _key[1]:
                        return True

                if x < 0:
                    if pos[0] > _key[0]:
                        return True
        return False


    def draw_wall(self):
        for key, val in self.walls.items():
            for pos in val:
                start_y = key[0] * self.sq_sz
                start_x = key[1] * self.sq_sz

                end_y = pos[0] * self.sq_sz
                end_x = pos[1] * self.sq_sz

                pygame.draw.line(self.game_window, (255,0,0), (start_x, start_y), (end_x, end_y), 5)


                '''
                if key[0] == pos[0]:
                    if key[1] < pos[1]: #drawing on the bottom from left to right
                        pygame.draw.line(self.game_window, (255, 0, 0),
                                         (self.sq_sz * (key[0]), self.sq_sz * (key[1]+1)),
                                         (self.sq_sz * (key[0]+1), self.sq_sz * (key[1]+1)), 5)
                    else: #drawing on the top from left o right
                        pygame.draw.line(self.game_window, (255, 0, 0),
                                         (self.sq_sz * (key[0]), self.sq_sz * (key[1])),
                                         (self.sq_sz * (key[0] + 1), self.sq_sz * (key[1])), 5)
                elif key[1] == pos[1]:
                    pass
                '''
        return


    def move(self, x=0, y=0):
        if self.hit_wall(x, y):
            return False

        cur_x = self.mouse.x
        cur_y = self.mouse.y

        new_x = cur_x + (x * self.sq_sz)
        new_y = cur_y + (y * self.sq_sz)

        if new_x >= 0 and new_x < self.window_width:
            self.mouse.x = new_x
            if x > 0:
                self.mouse.update_pos(col=1)
            elif x < 0:
                self.mouse.update_pos(col=-1)

        if new_y >= 0 and new_y < self.window_height:
            self.mouse.y = new_y
            if y > 0:
                self.mouse.update_pos(row=1)
            elif y < 0:
                self.mouse.update_pos(row=-1)

        angle = self.mouse.angle // 90
        delta = 0

        if y > 0:
            if self.mouse.angle != 0:
                if angle == 2:
                    delta = 180
                elif angle == 1:
                    delta = 90
                elif angle == 3:
                    delta = -90

                self.mouse.update_rotation(0, delta=delta)

        elif y < 0:
            if self.mouse.angle != 180:
                if angle == 0:
                    delta = 180
                elif angle == 1:
                    delta  = -90
                elif angle == 3:
                    delta = 90

                self.mouse.update_rotation(180, delta=delta)

        if x > 0:
            if self.mouse.angle != 270:
                if angle == 0:
                    delta = 90
                elif angle == 1:
                    delta  = 180
                elif angle == 2:
                    delta = -90

                self.mouse.update_rotation(270, delta=delta)

        elif x < 0:
            if self.mouse.angle != 90:
                if angle == 2:
                    delta = 90
                elif angle == 0:
                    delta = -90
                elif angle == 3:
                    delta = 180

                self.mouse.update_rotation(90, delta=delta)
        return True


    def reset(self):
        row, col = self.place_characters("mouse")
        self.mouse.pos = (0, 0)
        self.mouse.update_pos(col=col, row=row)
        self.mouse.x, self.mouse.y = col * self.sq_sz, row * self.sq_sz
        return self.get_state()


    def init_chars(self):
        cheese = Actors(pygame.image.load("resources/images/cheese.png"), scale=(self.sq_sz//2, self.sq_sz//2))
        c_row, c_col = 0,0#self.place_characters("cheese")
        cheese.x, cheese.y = (c_col*self.sq_sz + (self.sq_sz//4)), (c_row*self.sq_sz + (self.sq_sz//4))
        cheese.update_pos(col=c_col, row=c_row)
        self.chars['cheese'] = cheese
        self.locations['cheese'] = cheese.pos #Comment out if using stochastic positioning

        cat = Actors(pygame.image.load("resources/images/cat.png"), scale=(self.sq_sz, self.sq_sz))
        row, col = 0,2#self.place_characters("cat")
        cat.update_pos(col=col, row=row)
        cat.x, cat.y = col*self.sq_sz, row*self.sq_sz
        self.chars['cat'] = cat
        self.locations['cat'] = cat.pos #Comment out if using stochastic positioning

        trap = Actors(pygame.image.load("resources/images/mouse_trap.png"), scale=(self.sq_sz, self.sq_sz))
        _row, _col = 1,0#self.place_characters("trap")
        trap.update_pos(col=_col, row=_row)
        trap.x, trap.y = _col*self.sq_sz, _row*self.sq_sz
        self.chars['trap'] = trap
        self.locations['trap'] = trap.pos #Comment out if using stochastic positioning

        self.mouse = Actors(pygame.image.load("resources/images/mouse.png"), scale=(self.sq_sz, self.sq_sz))
        m_row, m_col = self.place_characters("mouse")
        self.mouse.x, self.mouse.y = m_col * self.sq_sz, m_row * self.sq_sz
        self.mouse.update_pos(col=m_col, row=m_row)


    def place_characters(self, name):
        col = rand(0, self.cols)
        row = rand(0, self.rows)

        locs = self.locations.values()

        while (col, row) in locs:
            col = rand(0, self.cols)
            row = rand(0, self.rows)

        self.locations[name] = (col, row)

        return row, col


    def test(self):
        self.train = False
        self.start_game()

    def training(self):
        self.train = True
        self.start_game()

    def start_game(self):
        self.running = True

    def varify_action(self, action):
        canMove = self.controls[action]()
        if not canMove:
            while not canMove:
                action = choice(self.actions)
                canMove = self.controls[action]()
        return action

    def init_controls(self):
        self.controls = {
            'LEFT': lambda: self.move(x=-1),
            'RIGHT': lambda: self.move(x=1),
            'DOWN': lambda: self.move(y=1),
            'UP': lambda : self.move(y=-1),
            't':lambda : self.test(),
            's':lambda :self.training(),
        }

    def get_frame_step(self, ai, prevState, action=0):

        canMove = self.controls[action]()
        state = self.get_state()
        reward, status = self.get_reward(self.got_cheese(), self.check_impact(), canMove)

        return state, reward , status


    def draw_values(self, window):
        for k, v in self.values.items():
            val = round(v[0],2)
            if k == str(self.chars['cheese'].pos):
                val = 1
            elif k == str(self.chars['cat'].pos):
                val = -1
            elif k == str(self.chars['trap'].pos):
                val = -1

            if val < 0.0:
                text = self.font.render(str(val), False, (255, 0, 0))
            elif val > 0.0:
                text = self.font.render(str(val), False, (0, 255, 0))
            else:
                text = self.font.render(str(val), False, (100, 100, 100))

            window.blit(text, v[1])


    def draw_board(self, window, board_colors):
        window.fill((255,255,255))

        for row in range(self.rows):
            c_index = row % 2
            for col in range(self.cols):
                square = (col*self.sq_sz,row*self.sq_sz, self.sq_sz, self.sq_sz)
                window.fill(board_colors[c_index], square)
                c_index = (c_index+1) % 2

        window.blit(self.mouse.surface, (self.mouse.x, self.mouse.y))
        for name, actor in self.chars.items():
            window.blit(actor.surface, (actor.x, actor.y))

        self.draw_values(window)
        self.draw_wall()


    def run(self):

        event = pygame.event.poll()
        if event.type == pygame.QUIT:  # Window close button clicked?
            pass
        elif event.type == pygame.KEYDOWN:
            return event.key
        return None




if __name__ == "__main__":
    pass
    #game = MouseMaze(window=(640, 640), rows=8, cols=8)
    #game.run()


