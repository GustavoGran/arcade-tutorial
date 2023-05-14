"""
Platformer Game
"""

import arcade
import logging
from random import randint

# Constants
DISPLAY_SIZE = arcade.get_display_size()
# SCREEN_WIDTH = int(DISPLAY_SIZE[0] // 1.5)
# SCREEN_HEIGHT = int(DISPLAY_SIZE[1] // 1.2)
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Platformer"
CHARACTER_SCALING = 0.5
TILE_SCALING = 0.5
COIN_SCALING = 0.5

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
        self.gui_camera = None

        # Separate variable that holds the player sprite
        self.player_sprite = None

        # Physics engine variable
        self.physics_engine = None

        # Create sounds variables
        self.jump_sound = None
        self.collect_coins_sound = None

        # Game score and attributes
        self.score = 0
        # self.lifes = 3

        # Game TileMap Object
        self.tile_map = None


        arcade.set_background_color(arcade.color.LIGHT_SLATE_GRAY)

    def setup(self):
        """Set up game here. Call this function to restart the game
        """
        # Intializes the camera
        self.camera = arcade.Camera(self.width, self.height)
        self.gui_camera = arcade.Camera(self.width, self.height)

        # Name of map file to load
        map_name = ":resources:tiled_maps/map.json"

        # Layer specific options are defined based on layer names in a dictionary
        # Doing this will make the SpriteList for the platforms layers
        # use spatial hashing for etection
        layer_options = {
            "Platforms": {
                "use_spatial_hash": True,
            },
        }

        # Read in the tiled_map
        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)

        # Initialize Scene with our TileMap, this will automatically add all layers
        # from the map as SpriteLists in the scene in the proper order.
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        # Keep track of the score
        self.score = 0

        # Set up the player, specifically placing it at these coordinates
        image_source = ":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png"
        self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.player_sprite.center_x = 128
        self.player_sprite.center_y = 128
        self.scene.add_sprite("Player", self.player_sprite)

        # --- Other stuff
        # Set the background color
        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)

        # Create the physiscs engine
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, gravity_constant=GRAVITY, walls=self.scene["Platforms"],
        )

        # Load sounds
        self.jump_sound = arcade.load_sound(":resources:/sounds/jump5.wav")
        self.collect_coins_sound = arcade.load_sound(":resources:/sounds/coin5.wav") 

    def on_draw(self):
        """Render the game screen. Call this function to render a new frame"""
        # Removes old renders
        self.clear()

        # Draw our scene
        self.scene.draw()

        # Activates our Camera
        self.camera.use()

        # Activates the GUI Camera
        self.gui_camera.use()

        # Draws our score on the screen, scrolling it with the viewport
        score_text = f"Score: {self.score}"
        arcade.draw_text(
            score_text,
            10, 
            SCREEN_HEIGHT - 24,
            arcade.color.WHITE,
            18,
        )

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

        # Collect coins if player passes through it
        coins_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, 
            self.scene.get_sprite_list("Coins"),
        )

        for coin in coins_hit_list:
            # Removes the coin
            coin.remove_from_sprite_lists()
            # Updates the score
            self.score += 1
            # Play a sound
            arcade.play_sound(self.collect_coins_sound)

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
        if self.physics_engine.can_jump():
            self.player_sprite.change_y = PLAYER_JUMP_SPEED
            arcade.play_sound(self.jump_sound)

    def move_right(self):
        self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
    
    def move_left(self):
        self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED

if __name__ == '__main__':
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()