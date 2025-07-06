import numpy as np
import pygame
def play_sound_with_pitch(path, pitch_factor=1.0):
    sound = pygame.mixer.Sound(path)
    arr = pygame.sndarray.array(sound)

    new_length = int(arr.shape[0] / pitch_factor)
    arr_resampled = np.interp(
        np.linspace(0, arr.shape[0], new_length, endpoint=False),
        np.arange(arr.shape[0]),
        arr[:, 0] if arr.ndim > 1 else arr
    )
    if arr.ndim > 1:
        arr_resampled = np.column_stack([arr_resampled, arr_resampled])
    sound_resampled = pygame.sndarray.make_sound(arr_resampled.astype(arr.dtype))
    sound_resampled.set_volume(0.1)
    sound_resampled.play()