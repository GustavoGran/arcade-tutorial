"""
Platformer Game
"""

import arcade

# Constants
DISPLAY_SIZE = arcade.get_display_size()
SCREEN_WIDTH = int(DISPLAY_SIZE[0] // 1.5)
SCREEN_HEIGHT = int(DISPLAY_SIZE[1] // 1.2)
SCREEN_TITLE = "Platformer"
CHARACTER_SCALING = 1.0
TILE_SCALING = 0.5

# Classes

class MyGame(arcade.Window):
    """Defines the game front-end
    """
    def __init__(self, height, width, title):
        """Initialization class will only define variables ans set them to None. 
        Setup class can be called multiple times to start / restart the game
        """
        # Calls parent class and setup the window
        super().__init__(height, width, title, 
                         resizable=True, center_window=True)

        # Lists that keep track of sprites. Each sprite should go into a list
        self.player_list = None
        self.wall_list = None

        # Separate variable that holds the player sprite
        self.player_sprite = None

        arcade.set_background_color(arcade.color.LIGHT_SLATE_GRAY)

    def setup(self):
        """Set up game here. Call this function to restart the game
        """   
        # using spatial hash for fixed sprites can enhance collision check speed
        # not a good idea to use on moving sprites as it will increase the speed 
        # to find collisions
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList(use_spatial_hash=True)

        # Setup the player sprite
        player_img = ":resources:images/alien/alienBlue_walk1.png"
        self.player_sprite = arcade.Sprite(player_img, CHARACTER_SCALING)

        # Defines where player is positioned at start
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 150

        # We should add playet to the player list
        self.player_list.append(self.player_sprite)

        # Create the ground
        # places multiple sprites horizontally
        wall_img = ":resources:/images/tiles/stone.png"
        for x in range (0, SCREEN_WIDTH, 30):
            wall = arcade.Sprite(wall_img, TILE_SCALING)
            wall.center_x = x
            wall.center_y = 32
            self.wall_list.append(wall)
        
        # Put some spikes on the ground
        # Uses coordinate list to place sprites
        coordinate_lists = [
            [256,96],
            [512, 96],
            [768, 96],
            [1024, 96]
        ]
        spike_img = ":resources:/images/tiles/spikes.png"
        for coordinate in coordinate_lists:
            # Add a spike on the ground
            spike = arcade.Sprite(spike_img, TILE_SCALING)
            spike.position = coordinate
            self.wall_list.append(spike)


    def on_draw(self):
        """Render the game screen. Call this function to render a new frame"""
        # Removes old renders
        self.clear()

        # Draw our sprites
        self.wall_list.draw()
        self.player_list.draw()

if __name__ == '__main__':
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()