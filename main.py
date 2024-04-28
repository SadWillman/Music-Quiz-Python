"Author: SadWillman"
"Made: 23-04-2024"

import pygame
import random
import os
import time
import pickle

# Initialize Pygame
pygame.init()

# Screen Setup
screen_width = 800
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Öresus: Song Quiz") # Screen Title

def load_random_song():
    '''Function to load a random song from the songs folder and return the path to the song file.
    
    Parameters:
    None
    
    Returns:
    str: The path to the song file.
    '''
    songPath = os.listdir('songs')
    songList = []
    
    for song in songPath:
        songList.append('songs/' + song)
    return random.choice(songList)

def play_song(song_path, duration):
    '''Function to play the song for a specified duration.
    
    Parameters:
    song_path (str): The path to the song file.
    duration (int): The duration to play the song in seconds.
    
    Returns:
    None
    '''
    pygame.mixer.music.load(song_path)
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play()
    time.sleep(duration)
    pygame.mixer.music.stop()

def display_text(text, font, size, color, x, y, align="center"):
    '''Function to display text on the screen at the specified position and with the specified font, size, and color.
    
    Parameters:
    text (str): The text to display.
    font (str): The font to use for the text (default is None for system font).
    size (int): The font size.
    color (tuple): The color of the text in RGB format.
    x (int): The x-coordinate of the text position.
    y (int): The y-coordinate of the text position.
    align (str): The alignment of the text (default is "center").

    Returns:
    None
    '''
    font = pygame.font.Font(font, size)
    text_surface = font.render(text, True, color)

    if align == "center":
        text_rect = text_surface.get_rect(center=(x, y))

    elif align == "topright":
        text_rect = text_surface.get_rect(topright=(x, y))

    screen.blit(text_surface, text_rect)

def display_buttons(buttons):
    '''Function to display buttons on the screen with the specified text and return the button rectangles.
    
    Parameters:
    buttons (list): A list of button texts.

    Returns:
    dict: A dictionary with button texts as keys and button rectangles as values.
    '''
    button_font = pygame.font.SysFont(None, 30)
    button_width = 200
    button_height = 50
    button_gap_x = 20
    button_gap_y = 20
    button_x = (screen_width - (2 * button_width + button_gap_x)) // 2
    button_rects = {}  # Dictionary to store button texts as keys and button rectangles as values

    for i, option in enumerate(buttons):
        button_row = i // 2
        button_col = i % 2
        button_y = 200 + button_row * (button_height + button_gap_y)
        button_rect = pygame.Rect(button_x + button_col * (button_width + button_gap_x), button_y, button_width, button_height)
        pygame.draw.rect(screen, (0, 0, 0), button_rect, 2)
        text_surface = button_font.render(option, True, (0, 0, 0))
        
        if text_surface.get_width() > button_width - 20:
            text_surface = pygame.transform.scale(text_surface, (button_width - 20, text_surface.get_height()))
        text_rect = text_surface.get_rect(center=button_rect.center)
        screen.blit(text_surface, text_rect)
        # Store button_rect in the dictionary with button text as key
        button_rects[option] = button_rect
    return button_rects

def save_highscore(highscore):
    '''Function to save the highscore to a text file.
    
    Parameters:
    highscore (int): The highscore to save.
    
    Returns:
    None
    '''
    # with open("highscore.txt", "w") as file:
    #     file.write(str(highscore))
    
    
    with open("highscore.dat", "wb") as file:
        pickle.dump(highscore, file)

def load_highscore():
    '''Function to load the highscore from a text file.
    
    Parameters:
    None
    
    Returns:
    int: The highscore loaded from the text file.
    '''
    # try:
    #     with open("highscore.txt", "r") as file:
    #         highscore_str = file.read().strip()
    #         if highscore_str:
    #             highscore = int(highscore_str)
    #         else:
    #             highscore = 0
    # except FileNotFoundError:
    #     highscore = 0
    # return highscore
    try:
        with open("highscore.dat", "rb") as file:
            highscore = pickle.load(file)
    except FileNotFoundError:
        highscore = 0
    return highscore

# Main function to run the quiz
def music_quiz():
    '''Main function to run the music quiz game.

    Parameters:
    None
    
    Returns:
    None
    '''
    running = True
    lives = 3
    score = 0
    highscore = load_highscore()

    while lives > 0 and running:
        # Load a random song
        song_path = load_random_song()

        # Get the name of the song (without extension) for comparison
        song_name = os.path.splitext(os.path.basename(song_path))[0]

        # Shuffle the song list and choose three random songs (including the correct one)
        songPath = os.listdir('songs')
        songList = ['songs/' + song for song in songPath]
        random.shuffle(songList)
        options = random.sample(songList, 3)
        options.append(song_path)
        random.shuffle(options)

        # Play the song for 5 seconds
        play_song(song_path, 5)

        correct_guess = False
        guessed = False
        start_time = time.time()

        while not correct_guess and time.time() - start_time < 5 and not guessed:  # User has 5 seconds to guess
            screen.fill((255, 255, 255))
            display_text("Guess the Song!", None, 50, (0, 0, 0), screen_width // 2, 50)
            display_text(f"Lives: {max(lives, 0)}", None, 30, (255, 0, 0), screen_width // 2, 100)
            display_text(f"Score: {score}", None, 30, (0, 0, 0), screen_width // 2, 150)
            display_text(f"Highscore: {highscore}", None, 30, (0, 0, 0), screen_width // 2, 180)
            display_text(f"Time Left: {int(5 - (time.time() - start_time))}s", None, 30, (0, 0, 0), screen_width - 10, 10, align="topright")

            # Display buttons with song options and get button_rects dictionary
            button_rects = display_buttons([os.path.splitext(os.path.basename(option))[0] for option in options])

            # Check for user input
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    #running = False
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Check if any button is clicked
                    for option, button_rect in button_rects.items():
                        if button_rect.collidepoint(event.pos):
                            guessed = True  # User has guessed
                            if option == song_name:  # Correct guess
                                print("Correct!")
                                correct_guess = True
                                score += 1
                                if score > highscore:
                                    highscore = score
                                    save_highscore(highscore)
                                pygame.draw.rect(screen, (0, 255, 0), button_rect, 0)  # Green color for correct button
                            else:  # Incorrect guess
                                print("Incorrect!")
                                lives -= 1
                                pygame.draw.rect(screen, (255, 0, 0), button_rect, 0)  # Red color for incorrect button
                                pygame.draw.rect(screen, (0, 255, 0), button_rects[song_name], 0)  # Green color for correct button
                                if lives <= 0:
                                    running = False
                                break  # Exit the loop after one guess
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        running = False

            pygame.display.update()

    # Game Over screen
    screen.fill((255, 255, 255))
    display_text("Game Over", None, 50, (255, 0, 0), screen_width // 2, screen_height // 2 - 50)
    display_text("Restart (R)", None, 30, (0, 0, 0), screen_width // 2, screen_height // 2 + 20)
    display_text("Quit (Q)", None, 30, (0, 0, 0), screen_width // 2, screen_height // 2 + 60)
    display_text(f"Your Score: {score}", None, 30, (0, 0, 0), screen_width // 2, screen_height // 2 + 100)

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                elif event.key == pygame.K_q:
                    return False

    pygame.quit()

#Run the quiz
while music_quiz():
   pass


    
