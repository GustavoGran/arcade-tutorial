"""
Platformer Game
"""

import arcade
import logging

# Constants
DISPLAY_SIZE = arcade.get_display_size()
# SCREEN_WIDTH = int(DISPLAY_SIZE[0] // 1.5)
# SCREEN_HEIGHT = int(DISPLAY_SIZE[1] // 1.2)
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Platformer"
CHARACTER_SCALING = 0.5
TILE_SCALING = 0.5

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 10
GRAVITY = 1
PLAYER_JUMP_SPEED = 20

err_logger = logging.Logger("Error Logger")

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
                         resizable=False, center_window=True)

        # Create a variable for the game scene
        self.scene = None

        # Create a variable for the game camera
        self.camera = None

        # Separate variable that holds the player sprite
        self.player_sprite = None

        # Physics engine variable
        self.physics_engine = None

        arcade.set_background_color(arcade.color.LIGHT_SLATE_GRAY)

    def setup(self):
        """Set up game here. Call this function to restart the game
        """
        
        # Intialize the scene
        self.scene = arcade.Scene()

        # Intializes the camera
        self.camera = arcade.Camera(self.width, self.height)

        # Creates Sprite Lists
        self.scene.add_sprite_list("Player")
        self.scene.add_sprite_list("Walls", use_spatial_hash=True)

        # Set up the player, specifically placing at these cordinates
        player_img = ":resources:images/alien/alienBlue_walk1.png"
        self.player_sprite = arcade.Sprite(player_img, CHARACTER_SCALING)
        
        # Defines where player is positioned at start
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 150

        self.scene.add_sprite("Player", self.player_sprite)

        # Create the ground
        # places multiple sprites horizontally
        wall_img = ":resources:/images/tiles/stone.png"
        for x in range (0, SCREEN_WIDTH, 30):
            wall = arcade.Sprite(wall_img, TILE_SCALING)
            wall.center_x = x
            wall.center_y = 32
            self.scene.add_sprite("Walls", wall)
        
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
            spikes = arcade.Sprite(spike_img, TILE_SCALING)
            spikes.position = coordinate
            self.scene.add_sprite("Walls", spikes)

        # Creates physics engine to handle player movement and gravity
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            player_sprite= self.player_sprite,
            gravity_constant= GRAVITY,
            walls=self.scene.get_sprite_list("Walls"),
        )

    def on_draw(self):
        """Render the game screen. Call this function to render a new frame"""
        # Removes old renders
        self.clear()

        # Draw our scene
        self.scene.draw()

        # Activates our Camera
        self.camera.use()

    def on_key_press(self, symbol, modifiers):
        """Called whenever a key is pressed
        Allows for basic movement with arrows (up (jump), down, left, right)
        """
        try: 
            handler = self.get_key_press_handler(symbol)
            handler()

        except KeyError:
            err_logger.warning(f"Unmapped key pressed:  {symbol}")

    def on_key_release(self, symbol, modifiers):
        """Called whenever a key is realeased
        Allows for basic movement with arrows (up, down, left, right)
        """
        try: 
            handler = self.get_key_release_handler(symbol)
            handler()

        except KeyError:
            # err_logger.warning(f"Unmapped key pressed:  {symbol}")
            pass

    def on_update(self, delta_time):
        """Updates movements and game logic"""

        # Move the player with the physics engine
        self.physics_engine.update()

        # Repositions the camera according to player movement
        self.center_camera_to_player()

    def center_camera_to_player(self):
        """Moves the camera so it can follow the player on screen"""
        # First we determine what are our player coordinates
        player_coord = self.player_sprite.center_x, self.player_sprite.center_y
        
        # arcade.Camera.move_to() receives the location of the left bottom 
        # corner of the camera, therefore we should not pass our player coordinates
        # directly, instead, we should subtract half of the camera viewport width 
        # from x coordinate and half the viewport height from y coordinate
        cam_coord = (player_coord[0] - (self.camera.viewport_width / 2),
                     player_coord[1] - (self.camera.viewport_height / 2))

        self.camera.move_to(cam_coord, 1.0)

    def get_key_press_handler(self, key):
        """Provides handler functions for each key mapping configured"""
        handler_dict = {
            arcade.key.UP: self.jump,
            arcade.key.RIGHT: self.move_right,
            arcade.key.LEFT: self.move_left,
        }
        return handler_dict[key]

    def get_key_release_handler(self, key):
        """Provides handler functions for each key mapping configured"""
        handler_dict = {
            arcade.key.UP: self.stop_vertical_movement,
            arcade.key.RIGHT: self.stop_horizontal_movement,
            arcade.key.LEFT: self.stop_horizontal_movement,
        }
        return handler_dict[key]

    def stop_vertical_movement(self):
        self.player_sprite.change_y = 0

    def stop_horizontal_movement(self):
        self.player_sprite.change_x = 0

    def jump(self):
        self.player_sprite.change_y = PLAYER_JUMP_SPEED

    def move_right(self):
        self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
    
    def move_left(self):
        self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED

if __name__ == '__main__':
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()