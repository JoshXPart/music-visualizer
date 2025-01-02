from pydub import AudioSegment
import numpy as np
import pygame
from pygame.locals import *
import time

# Function to load and process the audio file
def load_audio(file_path):
    audio = AudioSegment.from_file(file_path)
    samples = np.array(audio.get_array_of_samples())
    samples = samples / (2**15)
    return samples, audio.frame_rate

# Function to initialize Pygame
def init_pygame():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Music Visualizer')
    return screen

# Function to draw the visualizer
def draw_visualizer(screen, samples, sample_rate, color):
    screen.fill((0, 0, 0))
    width, height = screen.get_size()
    bar_width = width // len(samples)
    max_height = height // 2

    for i, sample in enumerate(samples):
        bar_height = int(sample * max_height)
        pygame.draw.rect(screen, color, (i * bar_width, height // 2 - bar_height, bar_width, bar_height * 2))

# Function to change colors
def get_next_color(current_color):
    # List of colors to cycle through
    colors = [
        (255, 0, 0),  # Red
        (0, 255, 0),  # Green
        (0, 0, 255),  # Blue
        (255, 255, 0),  # Yellow
        (255, 0, 255),  # Magenta
        (0, 255, 255),  # Cyan
        (245, 132, 66)  # Orange
    ]
    next_index = (colors.index(current_color) + 1) % len(colors)
    return colors[next_index]

# Main function to run the visualizer
def main():
    screen = init_pygame()
    file_path = 'audio/DoYaLike.mp3'

    # Initialize pygame.mixer for audio playback
    pygame.mixer.init()
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

    # Load the audio for visualization
    samples, sample_rate = load_audio(file_path)

    clock = pygame.time.Clock()
    running = True
    sample_index = 0
    samples_per_frame = sample_rate // 60

    # Initial color and interval settings
    current_color = (0, 255, 0)  # Start with green
    last_color_change_time = time.time()
    color_change_interval = 1  # Change color every 1 second

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

        # Check if it's time to change the color
        if time.time() - last_color_change_time >= color_change_interval:
            current_color = get_next_color(current_color)
            last_color_change_time = time.time()

        # Play visuals while music is playing
        if pygame.mixer.music.get_busy():
            current_samples = samples[sample_index : sample_index + 800]
            draw_visualizer(screen, current_samples, sample_rate, current_color)
            pygame.display.flip()

            sample_index += samples_per_frame
            if sample_index >= len(samples):
                sample_index = 0

        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    main()
