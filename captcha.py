# Author: Nathaniel Byrd (cognitivegears)
# Copyright (C) 2024 Nathaniel Byrd
# This is free software, see LICENSE.md for more details

import pygame
import pymunk
import random
import math

pygame.display.init()
pygame.font.init()

pygame.display.set_caption("Spooky Captcha")
screen_width, screen_height = 1200, 600
screen = pygame.display.set_mode((screen_width, screen_height))
clock  = pygame.time.Clock()
fps    = 60
space  = pymunk.Space()
space.gravity = (0, 981)  # Gravity in pixels/sec^2

text_color = (255, 255, 255)
shadow_color = (0, 0, 0)
font_size = 36

# Load the images
skull_image   = pygame.transform.scale(pygame.image.load("skull.png").convert_alpha(), (50, 50))
bag_image     = pygame.transform.scale(pygame.image.load("bag.png").convert_alpha(), (160, 100))
bag_sel_image = pygame.transform.scale(pygame.image.load("bag_selected.png").convert_alpha(), (160, 100))
bg_image      = pygame.transform.scale(pygame.image.load("background.png"), (screen_width, screen_height))

# Define boxes
box_count = 5
box_width = 80
box_height = 50
box_spacing = 10
boxes = []


def drop_shadow_text(text, pos, font_size=font_size, color=text_color, shadow_color=shadow_color):
    drop_shadow_offset = 1 + (font_size // 15)
    font = pygame.font.SysFont(None, font_size)
    text_surface = font.render(text, True, shadow_color)
    text_rect = text_surface.get_rect(center=pos)
    screen.blit(text_surface, (text_rect.x + drop_shadow_offset, text_rect.y + drop_shadow_offset))
    # make the overlay text
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, text_rect)
    

def create_boxes():
    boxes.clear()  # Clear existing boxes if any
    total_box_width = (box_width + box_spacing) * box_count - box_spacing
    start_x = screen_width - total_box_width - 100  # Move boxes further left
    y = screen_height - box_height
    for i in range(box_count):
        x = start_x + i * (box_width + box_spacing)
        rect = pygame.Rect(x, y, box_width, box_height)
        boxes.append(rect)
 
def draw_selected_box(selected_index):
    if selected_index is not None and 0 <= selected_index < len(boxes):
        rect = boxes[selected_index]
        screen.blit(bag_sel_image, bag_sel_image.get_rect(center=rect.center))
        drop_shadow_text(str(selected_index + 1), rect.center, color=(0, 0, 0), shadow_color=(255, 255, 255))
        
def draw_boxes():
    for i, rect in enumerate(boxes):
        screen.blit(bag_image, bag_image.get_rect(center=rect.center))
        drop_shadow_text(str(i + 1), rect.center)

# Create the ball
def create_ball():
    ball_mass   = 1
    ball_radius = 15
    moment      = pymunk.moment_for_circle(ball_mass, 0, ball_radius)
    ball_body   = pymunk.Body(ball_mass, moment)
    ball_body.position = (50, screen_height - 100)  # Adjust x-coordinate if needed
    
    shape = pymunk.Circle(ball_body, ball_radius)
    shape.friction   = 0.5
    shape.elasticity = 0.8
    shape.sensor     = True  # Make the shape a sensor so it's not drawn
    space.add(ball_body, shape)
    
    return ball_body, shape

def apply_random_impulse(body):
    min_power = 800
    max_power = 1000
    min_angle = math.radians(45)
    max_angle = math.radians(60)
    
    angle = random.uniform(min_angle, max_angle)
    power = random.uniform(min_power, max_power)
    impulse_x = power * math.cos(angle)
    impulse_y = power * math.sin(angle)
    
    body.apply_impulse_at_local_point((impulse_x, -impulse_y), (0, 0))

def pause_game():
    drop_shadow_text("Click a box to guess!", (screen_width // 2, 50), color=(255, 0, 0))
    
def display_win():
    result_font = pygame.font.SysFont(None, 72)
    # Display "You Win!"
    drop_shadow_text("You Win!", (screen_width // 2, screen_height // 2 - 50), color=(0, 180, 0), font_size=72)

    # Display "Press any key to exit."
    drop_shadow_text("Press any key to exit.", (screen_width // 2, screen_height // 2 + 20), font_size=48)

    pygame.display.flip()
    # Do not wait here
    
def display_lose():
    drop_shadow_text("You Lose!", (screen_width // 2, screen_height // 2 - 50), color=(255, 0, 0), font_size=72)
    drop_shadow_text("Press any key to try again.", (screen_width // 2, screen_height // 2 + 20), font_size=48)
    pygame.display.flip()
    # Do not wait here

def main():
    create_boxes()
    ball_body, ball_shape = create_ball()
    apply_random_impulse(ball_body)

    paused = False
    halfway_reached = False
    user_guess = None
    game_over = False
    player_won = False  # Initialize the player_won variable

    while True:
        # If the game is over and the player won
        if game_over and player_won:
            # Wait for any key press to exit
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.quit()
                    return
            continue  # Wait without updating the display or physics

        # If the game is over and the player lost
        if game_over and not player_won:
            # Wait for any key press to restart
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    # Remove the old ball from the space
                    space.remove(ball_body, ball_shape)
                    # Reset game variables
                    paused = False
                    halfway_reached = False
                    user_guess = None
                    game_over  = False
                    player_won = False
                    # Create a new ball and apply impulse
                    ball_body, ball_shape = create_ball()
                    apply_random_impulse(ball_body)
                    break  # Exit the event loop to restart the game
            continue  # Wait without updating the display or physics

        # Proceed with normal game loop
        screen.blit(bg_image, (0, 0))
        draw_boxes()

        # Draw the skull image at the ball's position
        ball_position = ball_body.position
        ball_x = int(ball_position.x)
        ball_y = int(ball_position.y)
        skull_rect = skull_image.get_rect(center=(ball_x, ball_y))
        screen.blit(skull_image, skull_rect)
        
        draw_selected_box(user_guess)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if paused and event.type == pygame.MOUSEBUTTONDOWN and not user_guess:
                mouse_pos = pygame.mouse.get_pos()
                for index, rect in enumerate(boxes):
                    if rect.collidepoint(mouse_pos):
                        user_guess = index
                        paused = False  # Resume the game
                        break

        if not paused and not game_over:
            space.step(1 / fps)

        # Pause the game halfway through the arc
        if not halfway_reached and ball_body.position.x >= screen_width / 2:
            paused = True
            halfway_reached = True

        # Keep the pause message visible
        if paused:
            pause_game()

        # Check if the ball has landed
        if ball_body.position.y >= screen_height - ball_shape.radius and not game_over:
            # Determine which box the ball landed in
            ball_x = ball_body.position.x
            landed_in_box = None
            slop = 5
            for index, rect in enumerate(boxes):
                if rect.left - slop <= ball_x <= rect.right + slop:
                    landed_in_box = index
                    break
            # Determine win or lose
            if landed_in_box is not None and landed_in_box == user_guess:
                player_won = True
                display_win()
            else:
                player_won = False
                display_lose()
            game_over = True

        pygame.display.flip()
        clock.tick(fps)

if __name__ == "__main__":
    main()
