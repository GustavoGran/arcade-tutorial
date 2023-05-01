"""
Platformer Game
"""

import arcade

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
PLAYER_MOVEMENT_SPEED = 5
GRAVITY = 1
PLAYER_JUMP_SPEED = 20

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

        self.scene = None

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

        # Create the physics engine handle player movement and prevent collisions
        # self.physics_engine = arcade.PhysicsEngineSimple(
        #     self.player_sprite, self.scene.get_sprite_list("Walls")
        # )

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

    def on_key_press(self, symbol, modifiers):
        """Called whenever a key is pressed
        Allows for basic movement with arrows (up (jump), down, left, right)
        """
        if symbol == arcade.key.UP:
            self.player_sprite.change_y = PLAYER_JUMP_SPEED
        elif symbol == arcade.key.DOWN:
            self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED
        elif symbol == arcade.key.RIGHT:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
        elif symbol == arcade.key.LEFT:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED

    def on_key_release(self, symbol, modifiers):
        """Called whenever a key is realeased
        Allows for basic movement with arrows (up, down, left, right)
        """
        if symbol == arcade.key.UP:
            self.player_sprite.change_y = 0
        elif symbol == arcade.key.DOWN:
            self.player_sprite.change_y = 0
        elif symbol == arcade.key.RIGHT:
            self.player_sprite.change_x = 0
        elif symbol == arcade.key.LEFT:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):
        """Updates movements and game logic"""

        # Move the player with the physics engine
        self.physics_engine.update()

if __name__ == '__main__':
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    window.setup()
    arcade.run()