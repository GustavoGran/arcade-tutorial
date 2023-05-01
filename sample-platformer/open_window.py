"""
Platformer Game
"""

import arcade

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Platformer"

# Classes

class MyGame(arcade.Window):
    """Defines the game front-end
    """
    def __init__(self, height, width, title):

        # Calls arcade.Window initialization method
        super().__init__(height, width, title)

        arcade.set_background_color(arcade.color.PINK)

    def setup(self):
        """Set up game here. Call this function to restart the game
        """
        pass

    def on_draw(self):
        """Render the game screen. Call this function to render a new frame"""
        pass


if __name__ == '__main__':
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()