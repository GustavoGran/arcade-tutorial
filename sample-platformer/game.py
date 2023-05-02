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


        arcade.set_background_color(arcade.color.LIGHT_SLATE_GRAY)

    def setup(self):
        """Set up game here. Call this function to restart the game
        """
        
        # Intialize the scene
        self.scene = arcade.Scene()

        # Intializes the camera
        self.camera = arcade.Camera(self.width, self.height)
        self.gui_camera = arcade.Camera(self.width, self.height)

        # Creates Sprite Lists
        self.scene.add_sprite_list("Player")
        self.scene.add_sprite_list("Walls", use_spatial_hash=True)
        self.scene.add_sprite_list("Coins", use_spatial_hash=True)

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
        for x in range (0, SCREEN_WIDTH, 64):
            wall = arcade.Sprite(wall_img, TILE_SCALING)
            wall.center_x = x
            wall.center_y = 32
            self.scene.add_sprite("Walls", wall)

        # resources are 128x128 px images
        # We want to place a coin each 3 blocks starting on 4th block 
        # until the map ends
        coin_start_coord = {
            'x': int(128*TILE_SCALING*4),
            'y': int(128*(TILE_SCALING + 1.5*COIN_SCALING))
        }

        coin_gen_step = int(128*COIN_SCALING*3)

        coin_coord_lists =[[x, coin_start_coord['y']] 
                            for x in range(coin_start_coord['x'],
                                           SCREEN_WIDTH,
                                           coin_gen_step)]
        
        # Add coins with the predefined coordinates
        coin_img = ':resources:/images/items/coinGold.png'
        for coord in coin_coord_lists:
            coin = arcade.Sprite(coin_img, COIN_SCALING)
            coin.position = coord
            self.scene.add_sprite("Coins", coin)
            
        # Put some spikes on the ground
        # Uses coordinate list to place sprites
        spike_start_coord = {
            "x": int(128 * TILE_SCALING*3),
            "y": int(128 * TILE_SCALING * 1.5),
        }

        spike_gen_step = int(128*TILE_SCALING*5)
        spikes_coords = [[x, spike_start_coord['y']] 
                            for x in range(spike_start_coord['x'],
                                           SCREEN_WIDTH,
                                           spike_gen_step)]
        # Add spikes to the ground
        spike_img = ":resources:/images/tiles/spikes.png"
        for coord in spikes_coords:
            spikes = arcade.Sprite(spike_img, TILE_SCALING)
            spikes.position = coord
            self.scene.add_sprite("Walls", spikes)

        # Creates physics engine to handle player movement and gravity
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            player_sprite= self.player_sprite,
            gravity_constant= GRAVITY,
            walls=self.scene.get_sprite_list("Walls"),
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