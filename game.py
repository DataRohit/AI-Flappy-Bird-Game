# Imports
import neat
import sys
import os
import pygame
import random


# Initialize the font
pygame.font.init()


# Set global constant variables
WIN_WIDTH = 500
WIN_HEIGHT = 800


# List to store bird images
BIRD_IMGS = [
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird1.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird2.png"))),
    pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bird3.png"))),
]


# Load the pipe image
PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "pipe.png")))


# Load the base
BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "base.png")))


# Load the background image
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))


# Set the font
STAT_FONT = pygame.font.SysFont("comicsans", 50)


# Class to represe the bird
class Bird(object):
    # Member constants
    IMGS = BIRD_IMGS
    MAX_ROTATION = 25
    ROTATION_VEL = 20
    ANIMATION_TIME = 5

    # Constructor
    def __init__(self, x: int, y: int):
        # Store the x and y coordinates
        self.x = x
        self.y = y

        # Store the tilt of the bird
        self.tilt = 0

        # Store the tick count
        self.tick_count = 0

        # Store the velocity of the bird
        self.vel = 0

        # Store the height of the bird
        self.height = self.y

        # Store the image count
        self.img_count = 0

        # Store the current image
        self.img = self.IMGS[0]

    # Method to jump
    def jump(self):
        # Set the velocity to a negative value
        self.vel = -10.5

        # Set the tick count to 0
        self.tick_count = 0

        # Set the height to the current y coordinate
        self.height = self.y

    # Method to move
    def move(self):
        # Update the tick count
        self.tick_count += 1

        # Calculate the displacement
        displacement = self.vel * self.tick_count + 1.5 * self.tick_count**2

        # Limit the displacement
        if displacement >= 16:
            displacement = 16
        elif displacement < 0:
            displacement -= 2

        # Update the y coordinate
        self.y += displacement

        # Check if the bird is moving upwards
        if displacement < 0 or self.y < self.height + 50:
            # Check if the bird is tilted upwards
            if self.tilt < self.MAX_ROTATION:
                # Tilt the bird
                self.tilt = self.MAX_ROTATION
        else:
            # Check if the bird is tilted downwards
            if self.tilt > -90:
                # Tilt the bird
                self.tilt -= self.ROTATION_VEL

    # Method to draw the bird
    def draw(self, win):
        # Update the image count
        self.img_count += 1

        # Check if the bird is moving upwards
        if self.img_count < self.ANIMATION_TIME:
            # Set the image to the first image
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME * 2:
            # Set the image to the second image
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME * 3:
            # Set the image to the third image
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME * 4:
            # Set the image to the second image
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME * 4 + 1:
            # Set the image to the first image
            self.img = self.IMGS[0]
            # Reset the image count
            self.img_count = 0

        # Check if the bird is tilted downwards
        if self.tilt <= -80:
            # Set the image to the second image
            self.img = self.IMGS[1]
            # Reset the image count
            self.img_count = self.ANIMATION_TIME * 2

        # Rotate the image
        rotated_img = pygame.transform.rotate(self.img, self.tilt)

        # Draw the image
        win.blit(
            rotated_img,
            (
                self.x - rotated_img.get_width() / 2,
                self.y - rotated_img.get_height() / 2,
            ),
        )

    # Method to get the mask
    def get_mask(self):
        # Return the mask
        return pygame.mask.from_surface(self.img)


# Class for the pipe
class Pipe(object):
    # Member constants
    GAP = 200
    VEL = 5

    # Constructor
    def __init__(self, x: int):
        # Store the x coordinate
        self.x = x

        # Store the height
        self.height = 0

        # Store the top and bottom
        self.top = 0
        self.bottom = 0

        # Store the top and bottom pipes
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMG, False, True)
        self.PIPE_BOTTOM = PIPE_IMG

        # Store the passed flag
        self.passed = False

        # Set the height
        self.set_height()

    # Method to set the height
    def set_height(self):
        # Set the height
        self.height = random.randrange(50, 450)

        # Set the top and bottom
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.GAP

    # Method to move
    def move(self):
        # Update the x coordinate
        self.x -= self.VEL

    # Method to draw the pipe
    def draw(self, win):
        # Draw the top pipe
        win.blit(self.PIPE_TOP, (self.x, self.top))

        # Draw the bottom pipe
        win.blit(self.PIPE_BOTTOM, (self.x, self.bottom))

    # Method to check for collisions
    def collide(self, bird):
        # Get the masks
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.PIPE_TOP)
        bottom_mask = pygame.mask.from_surface(self.PIPE_BOTTOM)

        # Calculate the offsets
        top_offset = (round(self.x - bird.x), round(self.top - bird.y))
        bottom_offset = (round(self.x - bird.x), round(self.bottom - bird.y))

        # Calculate the points of collision
        b_point = bird_mask.overlap(bottom_mask, bottom_offset)
        t_point = bird_mask.overlap(top_mask, top_offset)

        # Check if there was a collision
        if t_point or b_point:
            # Return true
            return True

        # Return false
        return False


# Class for the base
class Base(object):
    # Member constants
    VEL = 5
    WIDTH = BASE_IMG.get_width()
    IMG = BASE_IMG

    # Constructor
    def __init__(self, y: int):
        # Store the y coordinate
        self.y = y

        # Store the x coordinates
        self.x1 = 0
        self.x2 = self.WIDTH

    # Method to move
    def move(self):
        # Update the x coordinates
        self.x1 -= self.VEL
        self.x2 -= self.VEL

        # Check if the first image has moved off the screen
        if self.x1 + self.WIDTH < 0:
            # Move the image to the end
            self.x1 = self.x2 + self.WIDTH

        # Check if the second image has moved off the screen
        if self.x2 + self.WIDTH < 0:
            # Move the image to the end
            self.x2 = self.x1 + self.WIDTH

    # Method to draw the base
    def draw(self, win):
        # Draw the first image
        win.blit(self.IMG, (self.x1, self.y))

        # Draw the second image
        win.blit(self.IMG, (self.x2, self.y))


# Function to draw the window
def draw_window(win, birds: list[Bird], pipes: list[Pipe], base: Base, score: int):
    # Draw the background
    win.blit(BG_IMG, (0, 0))

    # Draw the pipes
    for pipe in pipes:
        pipe.draw(win)

    # Draw the score
    text = STAT_FONT.render("Score: " + str(score), 1, (255, 255, 255))

    # Draw the text
    win.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

    # Draw the base
    base.draw(win)

    # Traverse over the birds
    for bird in birds:
        # Draw the bird
        bird.draw(win)

    # Update the display
    pygame.display.update()


# Function to main
def main(genomes, config):
    # Create a window
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))

    # Lists to store nets, ge and ai birds
    nets = []
    ge = []
    birds = []

    # Traverse over the genomes
    for _, g in genomes:
        # Create a neural network
        net = neat.nn.FeedForwardNetwork.create(g, config)

        # Add the net to the list
        nets.append(net)

        # Create a bird
        birds.append(Bird(230, 350))

        # Set the fitness to 0
        g.fitness = 0

        # Add the genome to the list
        ge.append(g)

    # Create a base
    base = Base(730)

    # Create a list to store the pipes
    pipes = [Pipe(700)]

    # Create a clock
    clock = pygame.time.Clock()

    # Track the score
    score = 0

    # Create a flag
    run = True

    # Main loop
    while run:
        # Set the clock
        clock.tick(30)

        # Check for events
        for event in pygame.event.get():
            # Check if the user wants to quit
            if event.type == pygame.QUIT:
                # Set the flag to false
                run = False

                # Quit pygame
                pygame.quit()

                # Quit the program
                quit()

        # Set the index
        pipe_ind = 0

        # Check if there are pipes
        if len(birds) > 0:
            # Check if the bird is past the pipe
            if (
                len(pipes) > 1
                and birds[0].x > pipes[0].x + pipes[0].PIPE_TOP.get_width()
            ):
                # Set the index to 1
                pipe_ind = 1

        # Check if the bird has collided with the pipe
        else:
            # Set the flag to false
            run = False

            # Break out of the loop
            break

        # Traverse over the birds
        for idx, bird in enumerate(birds):
            # Increase the fitness
            ge[idx].fitness += 0.1

            # Move the bird
            bird.move()

            # Get the output from the neural network
            output = nets[idx].activate(
                (
                    bird.y,
                    abs(bird.y - pipes[pipe_ind].height),
                    abs(bird.y - pipes[pipe_ind].bottom),
                )
            )

            # Check if the output is greater than 0.5
            if output[0] > 0.5:
                # Make the bird jump
                bird.jump()

        # Initial state of add pipe
        add_pipe = False

        # List to store the pipes to remove
        rem = []

        # Track the pipes
        for pipe in pipes:
            # Traverse over the birds
            for idx, bird in enumerate(birds):
                # Check for collisions
                if pipe.collide(bird):
                    # Remove the bird
                    ge[idx].fitness -= 1

                    # Remove the bird, net and genome
                    birds.pop(idx)
                    nets.pop(idx)
                    ge.pop(idx)

                # Check if the bird has passed the pipe
                if not pipe.passed and pipe.x < bird.x:
                    # Set the passed flag
                    pipe.passed = True

                    # Add a pipe
                    add_pipe = True

            # Check if the pipe has passed the bird
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                # Remove the pipe
                rem.append(pipe)

            # Move the pipe
            pipe.move()

        # Check if the bird has passed the pipe
        if add_pipe:
            # Update the score
            score += 1

            # Traverse over the genomes
            for g in ge:
                # Increase the fitness
                g.fitness += 5

            # Add a pipe
            pipes.append(Pipe(600))

        # Remove the pipes
        for r in rem:
            pipes.remove(r)

        # Traverse over the birds
        for idx, bird in enumerate(birds):
            # Check if the bird has hit the ground
            if bird.y + bird.img.get_height() >= 730 or bird.y < 0:
                # Remove the bird, net and genome
                birds.pop(idx)
                nets.pop(idx)
                ge.pop(idx)

        # Move the base
        base.move()

        # Draw the window
        draw_window(win, birds, pipes, base, score)


# Function to run the game
def run(config_path: str):
    # Load the configuration file
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path,
    )

    # Create a population
    p = neat.Population(config)

    # Add a reporter
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()

    # Add the statistics reporter to write to the log file
    p.add_reporter(stats)

    # Add a checkpointer to save the population every N generations
    checkpointer = neat.Checkpointer(
        generation_interval=5,
        time_interval_seconds=None,
        filename_prefix="train-log.txt",
    )
    p.add_reporter(checkpointer)

    # Run the simulation
    winner = p.run(main, 50)

    # Run the simulation
    winner = p.run(main, 50)


# Check if the file is being run directly
if __name__ == "__main__":
    # Set the path to the configuration file
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")

    # Run the game
    run(config_path)
