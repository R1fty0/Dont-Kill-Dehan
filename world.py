import pygame
import os
import sys


class Color:
    def __init__(self, red, green, blue):
        """ Creates a new color. """
        self.values = (red, green, blue)

    def get_values(self):
        """ Returns the values of the color. """
        return self.values

class Image:
    def __init__(self, image_name, folder_name=None):
        """ Loads in a new image and provides other useful image related functions. """
        self.image = self.load_image(folder_name, image_name)

    def load_image(self, folder_name, image_name):
        """ Loads a new image into the game. """
        if folder_name is None:
            image = pygame.image.load(image_name)
        else:
            image = pygame.image.load(os.path.join(folder_name, image_name))
        return image

    def scale_image(self, width, height):
        """ Scales the class's image. """
        self.image = pygame.transform.scale(self.image, (width, height))



class TextEffects:
    def __init__(self):
        self.effects = {"is_italic": False, "is_bold": False, "is_antialiasing": False}

    def set(self, name, disable=False):
        match disable:
            case False:  # Enable an effect
                match name:
                    case key if key in self.effects and not self.effects[key]:
                        self.effects[key] = True
                        print(f"Enabled text effect: {key}.")
                    case key if key in self.effects and self.effects[key]:
                        print("Text effect already enabled.")
                    case _:
                        print(f"Invalid text effect: {name}.")
            case True:  # Disable an effect
                match name:
                    case key if key in self.effects and self.effects[key]:
                        self.effects[key] = False
                        print(f"Disabled text effect: {key}.")
                    case key if key in self.effects and not self.effects[key]:
                        print("Text effect already disabled.")
                    case _:
                        print(f"Invalid text effect: {name}.")

    def check_effect_state(self, effect_name) -> bool:
        """ Checks the state of a given text effect. """
        if self.effects.get(effect_name) is not None:
            if not self.effects[effect_name]:  # if the effect is set to false
                return False
            else:
                return True   # if the effect is set to true


class Text(TextEffects):
    def __init__(self, font_name, font_size, text, color, background_color):
        """ Creates a new text object. """
        TextEffects.__init__(self)
        self.font = self.load_font(font_name, font_size)
        self.text = self.create_label(self.font, color, text, background_color)

    def load_font(self, font_name, font_size) -> pygame.font:
        """ Creates a new font."""
        is_bold = self.check_effect_state("is_bold")
        is_italic = self.check_effect_state("is_italic")
        font = pygame.font.SysFont(font_name, font_size, is_bold, is_italic)
        return font

    def create_label(self, font, color, text, background_color):
        """ Creates a new label given a font. """
        is_aa = self.check_effect_state("is_antialiasing")
        label = font.render(text, is_aa, color.values, background_color.values)
        return label

class Window:
        def __init__(self, width, height, name, fps):
            self.window = self.create_window(width, height, name)
            self.clock = pygame.time.Clock()
            self.is_running = False
            self.scenes = []
            self.current_scene = None
            self.fps = fps

        def set_current_scene(self, scene):
            """ Set the current scene to the scene with the specified name. """
            for scenes in self.scenes:
                if scenes.name == scene.name:
                    self.current_scene = scene
                    break
            else:
                print(f"Scene '{scene.name}' not found.")

        def run(self):
            """ Runs the window and the current scene. """
            if self.current_scene is None:
                print("Scene not found!")
                return

            self.is_running = True
            while self.is_running:
                self.clock.tick(self.fps)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                self.current_scene.call_functions()
                pygame.display.update()

        def create_window(self, width, height, name) -> pygame.Surface:
            """ Creates a new game window. """
            window = pygame.display.set_mode((width, height))
            pygame.display.set_caption(name)
            return window

class Scene:
        def __init__(self, name, window: Window):
            """ Creates a new scene that can be run in the game window. """
            self.window = window
            self.name = name
            self.function_calls = []
            self.window.scenes.append(self)

        def add_function(self, function_name, var_1, var_2=None, var_3=None):
            """ Add a function call that will be called when the scene is running.  """
            match function_name:
                case "add_image":
                    self.function_calls.append(lambda: self.add_image(var_1, var_2, var_3))
                case "add_text":
                    self.function_calls.append(lambda: self.add_text(var_1, var_2, var_3))
                case "add_color":
                    self.function_calls.append(lambda: self.add_color(var_1))
                case "trigger_scene_on_key_pressed":
                    self.function_calls.append(lambda: self.trigger_scene_on_key_pressed(var_1, var_2))
                case "trigger_scene_on_condition_met":
                    self.function_calls.append(lambda: self.trigger_scene_on_condition_met(var_1, var_2))
                case _:
                    print("Method calls and/or their arguments are invalid")

        def call_functions(self):
            """ Update the scene. """
            for function in self.function_calls:
                function()

        def add_image(self, image_object, x, y):
            """ Draws an image to the game window at the given x and y coordinates. """
            self.window.window.blit(image_object.image, (x, y))

        def add_text(self, text_object, x, y):
            """ Draws text to the game window. """
            self.window.window.blit(text_object.text, (x, y))

        def add_color(self, color):
            """ Fills the game window with a solid color. """
            self.window.window.fill(color.values)

        def trigger_scene_on_key_pressed(self, key, next_scene):
            """ Loads the given scene if the given key is pressed. """
            key_pressed = pygame.key.get_pressed()
            if key_pressed[key]:
                self.window.set_current_scene(next_scene)


        def trigger_scene_on_condition_met(self, condition, next_scene):
            """Loads another scene if a given condition if-statement returns true. """
            if_statement = condition.strip()  # Remove whitespace
            if if_statement.endswith(":"):
                if_body = if_statement[:-1]  # Remove the colon at the end
                try:
                    # Execute the if statement
                    if eval(if_body):  # got this from AI
                        # load the next scene
                        self.window.set_current_scene(next_scene)
                except Exception as e:  # got this from AI
                    print("Error occurred while executing the if statement:")
                    print(e)
            else:
                print("Invalid trigger condition. ")



