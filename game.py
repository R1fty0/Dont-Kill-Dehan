from world import Image, Window, Text, Color, Scene

""" Game Window """
FPS = 60
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_NAME = "Don't Kill Dean!"
window = Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_NAME, FPS)

""" Scenes """
menu = Scene("menu", window)
game = Scene("game", window)
game_over = Scene("game_over", window)


def initialize():
    main()


def main():
    window.set_current_scene(menu)
    window.run()



if __name__ == '__main__':
    initialize()