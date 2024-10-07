import sys
import os
import random
import math
import pygame
import pymunk

from constants import *

pygame.display.init()
pygame.font.init()

pygame.display.set_caption(TITLE)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock  = pygame.time.Clock()
space  = pymunk.Space()
space.gravity = GRAVITY

def load_image(filename, size):
    if hasattr(sys, '_MEIPASS'):
        path = os.path.join(sys._MEIPASS, 'assets', filename)
    else:
        path = os.path.join(os.path.dirname(__file__), 'assets', filename)
    return pygame.transform.scale(pygame.image.load(path).convert_alpha(), size)


skull_image   = load_image(SKULL_IMAGE_NAME, (50, 50))
bag_image     = load_image(BAG_IMAGE_NAME, (160, 100))
bag_sel_image = load_image(BAG_SEL_IMAGE_NAME, (160, 100))
bg_image      = load_image(BG_IMAGE_NAME, (SCREEN_WIDTH, SCREEN_HEIGHT))

boxes = []

def drop_shadow_text(text, pos, font_size=FONT_SIZE_SMALL, color=WHITE, shadow_color=BLACK):
    drop_shadow_offset = 1 + (font_size // 15)
    font = pygame.font.SysFont(None, font_size)
    text_surface = font.render(text, True, shadow_color)
    text_rect = text_surface.get_rect(center=pos)
    screen.blit(text_surface, (text_rect.x + drop_shadow_offset, text_rect.y + drop_shadow_offset))
    # make the overlay text
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, text_rect)

def create_boxes(box_count=BOX_COUNT, box_width=BOX_WIDTH, box_height=BOX_HEIGHT, box_spacing=BOX_SPACING):
    boxes.clear()  # Clear existing boxes if any
    total_box_width = (box_width + box_spacing) * box_count - box_spacing
    start_x = SCREEN_WIDTH - total_box_width - BOX_X_OFFSET  # Move boxes further left
    y = SCREEN_HEIGHT - box_height
    for i in range(box_count):
        x = start_x + i * (box_width + box_spacing)
        rect = pygame.Rect(x, y, box_width, box_height)
        boxes.append(rect)
 
def draw_selected_box(selected_index):
    if selected_index is not None and 0 <= selected_index < len(boxes):
        rect = boxes[selected_index]
        screen.blit(bag_sel_image, bag_sel_image.get_rect(center=rect.center))
        drop_shadow_text(str(selected_index + 1), rect.center, color=BLACK, shadow_color=WHITE)
        
def draw_boxes():
    for i, rect in enumerate(boxes):
        screen.blit(bag_image, bag_image.get_rect(center=rect.center))
        drop_shadow_text(str(i + 1), rect.center)

def create_ball(ball_mass=BALL_MASS, ball_radius=BALL_RADIUS):
    moment      = pymunk.moment_for_circle(ball_mass, 0, ball_radius)
    ball_body   = pymunk.Body(ball_mass, moment)
    ball_body.position = BALL_START_POS
    shape = pymunk.Circle(ball_body, ball_radius)
    shape.friction   = FRICTION
    shape.elasticity = ELASTICITY
    shape.sensor     = True  # Make the shape a sensor so it's not drawn
    space.add(ball_body, shape)
    return ball_body, shape

def apply_random_impulse(body, min_power=MIN_POWER, max_power=MAX_POWER, min_angle=MIN_ANGLE, max_angle=MAX_ANGLE):
    angle = random.uniform(math.radians(min_angle), math.radians(max_angle))
    power = random.uniform(min_power, max_power)
    impulse_x = power * math.cos(angle)
    impulse_y = power * math.sin(angle)
    body.apply_impulse_at_local_point((impulse_x, -impulse_y), TOP_LEFT)

def pause_game():
    drop_shadow_text("Click a bag to guess!", (SCREEN_MIDDLE_X, SCREEN_MIDDLE_Y - 100), color=RED)

def display_win():
    drop_shadow_text("CAPTCHA Unlocked!", (SCREEN_MIDDLE_X, SCREEN_MIDDLE_Y - 50), color=GREEN, font_size=FONT_SIZE_LARGE)
    drop_shadow_text("Press any key to exit.", (SCREEN_MIDDLE_X, SCREEN_MIDDLE_Y+ 20), font_size=FONT_SIZE_MEDIUM)

def main():
    create_boxes()
    ball_body, ball_shape = create_ball()
    apply_random_impulse(ball_body)

    paused     = False
    game_over  = False
    player_won = False
    user_guess = None
    catches_remaining = TOTAL_CATCHES
    halfway_reached   = False

    while True:
        screen.blit(bg_image, TOP_LEFT)
        draw_boxes()

        if game_over:
            if player_won:
                display_win()
                for event in pygame.event.get():
                    if event.type in (pygame.QUIT, pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN):
                        pygame.quit()
                        return
            else:
                # Remove the old ball from the space
                space.remove(ball_body, ball_shape)
                # Reset game variables
                paused = False
                halfway_reached = False
                user_guess = None
                game_over  = False
                player_won = False
                user_guess = None
                # Create a new ball and apply impulse
                ball_body, ball_shape = create_ball()
                apply_random_impulse(ball_body)
                continue
        else: # Game is not over
            drop_shadow_text(f"Catches Remaining: {catches_remaining}", (SCREEN_MIDDLE_X, 50), color=YELLOW)
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
                            paused = False
                            break
            if not paused:
                space.step(1 / FPS)

                # Pause the game halfway through the arc
                if not halfway_reached and ball_body.position.x >= SCREEN_MIDDLE_X:
                    paused = True
                    halfway_reached = True

            else:
                pause_game()
            # Check if the ball has landed
            if ball_body.position.y >= SCREEN_HEIGHT:
                game_over = True
            elif not player_won and ball_body.position.y >= SCREEN_HEIGHT - BOX_HEIGHT and not game_over:
                # Determine whether the ball landed in the user's guessed box
                ball_x = ball_body.position.x
                for index, rect in enumerate(boxes):
                    if rect.left <= ball_x <= rect.right:
                        if index == user_guess:
                            catches_remaining -= 1
                            game_over = True
                            if catches_remaining <= 0:
                                player_won = True
                        break
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
