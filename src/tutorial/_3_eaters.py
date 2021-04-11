from lib.pysoarlib import *
from time import sleep
from random import choice, randint
# Visualization
from PIL import Image, ImageDraw, ImageFont
from IPython import display
import sys
sys.path.append('../../src/')

font_sm = ImageFont.truetype(
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", 14, encoding="unic")


class Food:
    def __init__(self, bonus=False):
        self.points = 10 if bonus else 5
        self.color = 'gold' if bonus else 'green'
        self.bonus = bonus

    def __repr__(self):
        return 'bonusfood' if self.bonus else 'normalfood'


class Blank:
    def __init__(self):
        pass

    def __repr__(self):
        return 'blank'


class Grave:
    "A result of two eaters colliding. "

    def __init__(self, eater_1, eater_2):
        self.here_lies = (eater_1, eater_2)
        pass

    def __repr__(self):
        # Graves can be treated as blank.
        # Eaters are disrespectful.
        return 'blank'


class Wall:
    def __init__(self):
        pass

    def __repr__(self):
        return 'wall'


class GridBuilder:
    def __init__(self, world_type, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [[Blank() for x in range(cols)] for y in range(rows)]

        if world_type == 'all food':
            self._add_random_food()
        elif world_type == 'random':
            # Initialize grid with walls/blank squares
            self._add_random_walls()
            # Fill the rest with food
            self._add_random_food(blank_only=True)
        else:
            raise Exception("Unknown world type")

    def get_iter(self):
        def flatten(t): return [item for sublist in t for item in sublist]
        return flatten([[(row, col) for col in range(self.cols)] for row in range(self.rows)])

    def _add_random_walls(self):
        choices = [Wall(), Blank(), Blank(), Blank(), Blank()]
        for row, col in self.get_iter():
            self.grid[row][col] = choice(choices)

    def _add_random_food(self, blank_only=False):
        for row, col in self.get_iter():
            if (blank_only and isinstance(self.grid[row][col], Blank)) or not blank_only:
                self.grid[row][col] = choice(
                    [Food(bonus=True), Food(bonus=False)])


class Death(Exception):
    def __init__(self, message):
        super().__init__(message)


# action_space = ['north', 'east', 'south', 'west']
class World:
    def __init__(self, display, world_type, width=300, height=300, rows=16, cols=16):
        self.n_rows = rows
        self.n_cols = cols
        self.width = width
        self.height = height

        builder = GridBuilder(world_type, rows, cols)
        self.grid = builder.grid

        self.image = Image.new(
            "RGBA", (self.width, self.height), (255, 255, 255, 0))
        self.canvas = ImageDraw.Draw(self.image)
        self.display = display
        self.cell_w = self.width / cols
        self.cell_h = self.width / rows

    def place_eaters(self, eaters):
        # Place the eaters randomly
        for eater in eaters:
            while True:
                row, col = randint(
                    0, self.n_rows - 1), randint(0, self.n_cols - 1)
                if not isinstance(self.grid[row][col], Wall):
                    self.grid[row][col] = eater
                    break

    def step(self, ID: str, action=None):
        """ Returns (observations, reward) or throws Death if a collision occurs """
        (row_n, col_n), cell = self.find(ID)

        new_row = row_n
        new_col = col_n
        if action == 'north':
            new_row -= 1
        if action == 'south':
            new_row += 1
        if action == 'west':
            new_col -= 1
        if action == 'east':
            new_col += 1

        no_move = new_row == row_n and new_col == col_n
        if not self.is_valid_move(new_row, new_col) or no_move:
            # Don't move and return current observations
            return self.observations(row_n, col_n), 0

        if self.is_collision((row_n, col_n), (new_row, new_col)):
            other_eater = self.grid[new_row][new_col]
            cell.is_dead = True
            other_eater.is_dead = True
            # Average points between eaters
            avg = (other_eater.points + cell.points) / 2
            cell.points = avg
            other_eater.points = avg
            self.grid[new_row][new_col] = Blank()
            self.grid[row_n][col_n] = Grave(cell, other_eater)
            raise Death(cell.ID + '  ' + other_eater.ID)

        # aka reward
        points = 0
        if hasattr(self.grid[new_row][new_col], 'points'):
            points = self.grid[new_row][new_col].points
        self.grid[new_row][new_col] = self.grid[row_n][col_n]
        self.grid[row_n][col_n] = Blank()

        return self.observations(new_row, new_col), points

    def is_valid_move(self, row, col):
        # Out of bounds
        if row < 0 or col < 0 or row >= self.n_rows or col >= self.n_cols:
            return False
        is_wall = isinstance(self.grid[row][col], Wall)
        return not is_wall

    def is_collision(self, pos1, pos2):
        eater_1 = self.grid[pos1[0]][pos1[1]]
        eater_2 = self.grid[pos2[0]][pos2[1]]
        return isinstance(eater_1, Eater) and isinstance(eater_2, Eater) and eater_1.ID != eater_2.ID

    def observations(self, row, col):
        default = 'blank'
        north = default if row == 0 else self.grid[row - 1][col]
        south = default if row >= self.n_rows-1 else self.grid[row + 1][col]
        east = default if col >= self.n_cols-1 else self.grid[row][col + 1]
        west = default if col == 0 else self.grid[row][col - 1]
        return {
            'north': str(north),
            'south': str(south),
            'east': str(east),
            'west': str(west),
        }

    def find(self, ID: str):
        for row_n, row in enumerate(self.grid):
            for col_n, cell in enumerate(row):
                if hasattr(cell, 'ID') and cell.ID == ID:
                    return ((row_n, col_n), cell)
        raise Exception(f"Couldn't find {ID}")

    def draw(self):
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                rect = (x * self.cell_w, y * self.cell_h,
                        self.cell_w, self.cell_h)
                if isinstance(cell, Blank):
                    self._draw_rect(rect, fill='white')
                if isinstance(cell, Wall):
                    self._draw_rect(rect, fill='black')
                if isinstance(cell, Eater):
                    self._draw_rect(rect, fill=cell.color)
                    self._center_text(rect, font_sm, str(cell.points))
                if isinstance(cell, Food):
                    padding = .30 * self.cell_w if cell.bonus else .35 * self.cell_w
                    x_pos, y_pos = x * self.cell_w + padding, y * self.cell_h + padding
                    w = self.cell_w - (padding * 2)
                    h = self.cell_h - (padding * 2)
                    self._draw_circle((x_pos, y_pos, w, h), fill=cell.color)
                if isinstance(cell, Grave):
                    e1, e2 = cell.here_lies
                    # Eater 1 grave stone
                    e1_rect = (rect[0], rect[1], rect[2], rect[3] / 2)
                    self._draw_rect(e1_rect, fill=e1.color)
                    # Eater 2 grave stone
                    e2_rect = (rect[0], rect[1] + rect[3] /
                               2, rect[2], rect[3] / 2)
                    self._draw_rect(e2_rect, fill=e2.color)
                    # Add an alpha overlay to fade the color a bit (nvm need to revisit this, doesn't work)
                    # self._draw_rect(rect, fill=(255, 255, 255, 127))
                    # Scores
                    self._center_text(e1_rect, font_sm, str(e1.points))
                    self._center_text(e2_rect, font_sm, str(e2.points))

        self.display.update(self.image)

    # Private
    def _draw_circle(self, bg, fill: str, outline: str = 'black'):
        x, y, width, height = bg
        self.canvas.ellipse((x, y, x + width, y + height),
                            fill=fill, outline=outline)

    def _draw_rect(self, bg, fill: str):
        x, y, width, height = bg
        self.canvas.rectangle((x, y, x + width, y + height), fill=fill)

    def _center_text(self, bg, font, text, color=(0, 0, 0)):
        x, y, width, height = bg
        text_width, text_height = self.canvas.textsize(text, font)
        position = ((width - text_width)/2 + x, (height - text_height)/2 + y)
        self.canvas.text(position, text, color, font=font)


class Eater():
    def __init__(self, ID: str, agent_raw: str, world: World, watch_level=1):
        """ Initialize eater. ID works as the color too. """
        self.ID = ID
        self.color = ID
        self.points = 0
        self.is_dead = False
        self.agent = SoarAgent(
            agent_name=f"agent_{ID}",
            write_to_stdout=True,
            agent_raw=agent_raw,
            watch_level=watch_level,
        )
        self.connector = MoveConnector(self.agent)
        self.agent.add_connector("eater", self.connector)
        self.agent.connect()

    def step(self):
        self.agent.execute_command("step")

    def get_move(self):
        move = self.connector.last_move_output
        self.connector.last_move_output = None
        return move

    def update_wm_from_observations(self, coords, observations):
        (x, y) = coords
        self.connector.x.set_value(x)
        self.connector.y.set_value(y)
        for (direction, contents) in observations.items():
            # Example: connector.contents['north'].set_value('bonusfood')
            self.connector.contents[direction].set_value(contents)


class MoveConnector(AgentConnector):
    def __init__(self, agent):
        AgentConnector.__init__(self, agent)
        self.move_command = "move"
        self.add_output_command(self.move_command)
        self.last_move_output = None
        self.location_id = None
        self.eater_id = None
        self.x = SoarWME('x', -1)
        self.y = SoarWME('y', -1)
        self.directions = {'north': None,
                           'south': None, 'east': None, 'west': None}
        # content is "bonusfood" | "normalfood" | "wall" | "blank"
        self.contents = {}
        for direction in self.directions.keys():
            self.contents[direction] = SoarWME('content', '')

    def on_input_phase(self, input_link):
        # Intialize WM elements on the input-link
        if self.eater_id is None or self.location_id is None:
            if self.eater_id is None:
                self.eater_id = input_link.CreateIdWME('eater')
                self.x.add_to_wm(self.eater_id)
                self.y.add_to_wm(self.eater_id)

            if self.location_id is None:
                self.location_id = input_link.CreateIdWME('location')
                for direction in self.directions.keys():
                    # Add a <direction> identifier on the location identifier
                    self.directions[direction] = self.location_id.CreateIdWME(
                        direction)
                    # Add the ^contents attribute to the direction
                    # Accessing this in full would look like location.north.content
                    self.contents[direction].add_to_wm(
                        self.directions[direction])
            return

        self.x.update_wm()
        self.y.update_wm()

        # If the value has changed, will update soar's working memory with the new value
        for direction, contents in self.contents.items():
            """ TODO i should be removing this, right? i can't tell if the tutorial visual-soar is programmed
            to do this (meaning i should too)
            p.65
            "Unlike the move-north operator, these proposal rules do not have to test the coordinates of the 
            eater because the contents of the neighboring cells will change when the eater moves. The contents 
            will change (the working memory elements for contents of all of the sensed cells are removed and 
            re-added to working memory) even if the sensed object is the same type."

            removing and adding back does not seem to work, though.
            The move_to_food agent will move correctly for awhile, but then, if it gets stuck,
            it will move to a blank space. This shouldn't happen.
            """
#             contents.remove_from_wm()
#             contents.add_to_wm(self.directions[direction])
            contents.update_wm()

    def on_output_event(self, command_name, root_id):
        if command_name == self.move_command:
            self.process_move_command(root_id)

    def process_move_command(self, root_id):
        direction = root_id.GetChildString("direction")
        self.last_move_output = direction
        root_id.AddStatusComplete()


def runner(
    eaters,
    world_type='random',
    debug=False,
    total_ticks=100,
    tick_speed=1,
    soar_watch_level=0,
    display_world=True,
    debug_output_link=False,
):
    """
    param eaters:
        list of tuples (color, Soar script)
    """
    d = display.display("z", display_id=True)

    world = World(d, world_type, width=600, height=600, rows=16, cols=16)
    eaters = [Eater(color, script, world, watch_level=soar_watch_level)
              for (color, script) in eaters]
    world.place_eaters(eaters)

    # Set intial eater WM
    for e in eaters:
        pos, cell = world.find(e.ID)
        observations = world.observations(pos[0], pos[1])
        e.update_wm_from_observations(pos, observations)
        e.step()

    debug_on = debug
    def debug(x): return print(x) if debug_on else 0

    if display_world:
        world.draw()

    for i in range(total_ticks):
        debug(
            '==============================================================================')
        debug(
            '==============================================================================')
        debug(
            f'============================== WORLD TICK {i} ==================================')
        debug(
            '==============================================================================')
        debug(
            '==============================================================================')

        for eater in eaters:
            if eater.is_dead == True:
                continue

            # Get observations
            pos, cell = world.find(eater.ID)
            observations = world.observations(pos[0], pos[1])
            debug(
                f'\t>>>>>>>>> Eater "{eater.ID}"\'s observations: {observations}')

            # Update eater
            eater.update_wm_from_observations(pos, observations)
            # Propose new move operator
            eater.step()
            # Apply new move operator, triggering an output link
            eater.step()

            # Take action
            action = eater.get_move()
            debug(f'\t>>>>>>>>> Eater "{eater.ID}" chose action {action}')

            # TODO: Not sure why adding this makes it work
            # Have to set these to null so that there isn't a 'state no change'
            eater.update_wm_from_observations((-1, -1), {
                'north': 'null',
                'south': 'null',
                'east': 'null',
                'west': 'null',
            })

            if debug_output_link:
                print(f'\t>>>>>>>>> Eater "{eater.ID}" output-link')
                eater.agent.execute_command(
                    "print --depth 2 i3", print_res=True)

            try:
                _, reward = world.step(eater.ID, action)
            except Death as e:
                print(e)
                continue

            eater.points += reward

        if display_world:
            world.draw()

        sleep(tick_speed)
