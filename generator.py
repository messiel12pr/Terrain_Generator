import pygame
import sys
import random
import noise
import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox

random.seed()

GREY = (128, 128, 128)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

L_BLUE = (173,216,230)
S_BLUE = (0,138,216)
D_GREEN = (0,100,0)
L_GREEN = (34,139,34)

window_width = 600
window_height = 600
scale = window_width * window_height

pygame.init()
window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Terrain Generator')


font = pygame.font.Font('freesansbold.ttf', 18)

text_1 = font.render('Number of Octaves', True, WHITE)
text_2 = font.render('Persistence', True, WHITE)
text_3 = font.render('Lacunarity', True, WHITE)

rect_1 = text_1.get_rect()
rect_2 = text_2.get_rect()
rect_3 = text_3.get_rect()

rect_1.left = 150
rect_1.top = 10

rect_2.left = 150
rect_2.top = 40

rect_3.left = 150
rect_3.top = 70


output_1 = TextBox(window, 110, 8, 30, 25, fontSize=15)
octaves_slider = Slider(window, 10, 10, 80, 20, min=1, max=8, step=1)

output_2 = TextBox(window, 110, 38, 30, 25, fontSize=15)
persistence_slider = Slider(window, 10, 40, 80, 20, min=0.1, max=1.0, step=0.1)

output_3 = TextBox(window, 110, 68, 30, 25, fontSize=15)
lacunarity_slider = Slider(window, 10, 70, 80, 20, min=0.1, max=10.0, step=0.1)


columns = 300
rows = 300

box_width = window_width // columns
box_height = window_height // rows

def main():
    scale = 100.0
    octaves = 6
    persistence = 0.5
    lacunarity = 2.0
    seed = 0

    grid = []

    for r in range(rows):
        grid.append([0 for c in range(columns)])

    while True:
        events = pygame.event.get()
        for event in events:
            # Quit
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                # Generate Seed
                if event.key == pygame.K_SPACE:
                    seed = random.randint(0, 100)

            window.fill(S_BLUE)

        grid.clear()
        for r in range(rows):
            grid.append([0 for c in range(columns)])

        # Generating shape
        for c in range(columns):
            r2 = noise.pnoise2(rows/scale, 
                            c/scale, 
                            octaves=octaves, 
                            persistence=persistence, 
                            lacunarity=lacunarity, 
                            repeatx=window_width, 
                            repeaty=window_height, 
                            base=seed)
            
            for r in range(int(r2 * 100) + 150, rows):
                grid[r][c] = -1
        
        # Generating color
        for r in range(rows):
            color_num = 0
            mult = 0

            if r < 130:
                color_num = 1
                mult = 10

            elif r in range(130, 140):
                color_num = 2
                mult = 35

            elif r in range(140, 220):
                color_num = 3
                mult = 50

            else:
                color_num = 4
                mult = 80
    
            for c in range(columns):
                if grid[r][c] != -1:
                    continue

                y = noise.pnoise2(rows/scale, 
                        c/scale, 
                        octaves=octaves, 
                        persistence=persistence, 
                        lacunarity=lacunarity, 
                        repeatx=window_width, 
                        repeaty=window_height, 
                        base=seed)
                
                y = abs(int(abs(y) * mult) + r)

                if y < rows:
                    for r2 in range(r, y):
                        grid[r2][c] = color_num

                else:
                    for r2 in range(r, rows):
                        grid[r2][c] = color_num


        for r in range(rows):
            for c in range(columns):
                if grid[r][c] == 0:
                    continue
                
                if grid[r][c] == 1:
                    color = WHITE

                if grid[r][c] == 2:
                    color = L_BLUE

                if grid[r][c] == 3:
                    color = D_GREEN

                if grid[r][c] == 4:
                    color = L_GREEN

                pygame.draw.rect(window, color, 
                                (c * box_width, 
                                r * box_height, 
                                box_width, 
                                box_height)) 
        


        octaves = octaves_slider.getValue()
        output_1.setText(octaves)

        persistence = persistence_slider.getValue()
        output_2.setText(round(persistence, 2))

        lacunarity = lacunarity_slider.getValue()
        output_3.setText(round(lacunarity, 2))

        window.blit(text_1, rect_1)
        window.blit(text_2, rect_2)
        window.blit(text_3, rect_3)

        pygame_widgets.update(event)
        pygame.display.update()


main()