"""
Platformer Game
"""

import arcade

# Constants
DISPLAY_SIZE = arcade.get_display_size()
SCREEN_WIDTH = int(DISPLAY_SIZE[0] // 1.5)
SCREEN_HEIGHT = int(DISPLAY_SIZE[1] // 1.2)
SCREEN_TITLE = "Platformer"

# Classes

class MyGame(arcade.Window):
    """Defines the game front-end
    """
    def __init__(self, height, width, title):

        # Calls arcade.Window initialization method
        super().__init__(height, width, title, 
                         resizable=True, center_window=True)

        arcade.set_background_color(arcade.color.LAVENDER_BLUSH)

    def setup(self):
        """Set up game here. Call this function to restart the game
        """
        pass

    def on_draw(self):
        """Render the game screen. Call this function to render a new frame"""
        # Removes old renders
        self.clear()




if __name__ == '__main__':
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()