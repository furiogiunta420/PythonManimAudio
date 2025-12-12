from manim import *
from pydub import AudioSegment
import numpy as np
import os 

class AspidaAudio(Scene):
    def construct(self):
        
        AUDIO_FILE = "song.wav"          # <--- PUT YOUR AUDIO FILE HERE
        BAR_COUNT = 70                        # Number of bars
        SMOOTHING = 0.5                       # 0-1, higher = smoother
        SENSITIVITY = 1.4                     # How strong the reaction is
        BAR_WIDTH = 0.15
        MAX_HEIGHT = 3.7
        COLOR_SHIFT_SPEED = 2.5                 # How fast colors change
        

        # Load and process audio
        audio = AudioSegment.from_file(AUDIO_FILE)
        
        # Convert to mono and get raw data
        audio = audio.set_channels(1)
        raw_data = np.array(audio.get_array_of_samples(), dtype=np.float32)
        
        # Normalize to -1 to 1
        raw_data = raw_data / (2**15) if audio.sample_width == 2 else raw_data / (2**31)
        
        # Resample to reduce data points (match frame rate (~30-60 fps)
        duration = audio.duration_seconds
        frame_rate = self.camera.frame_rate  # Usually 60 or 30
        total_frames = int(duration * frame_rate)
        
        # Downsample audio to match number of frames
        chunk_size = len(raw_data) // total_frames
        amplitudes = []
        
        for i in range(total_frames):
            start = i * chunk_size
            end = (i + 1) * chunk_size
            chunk = raw_data[start:end]
            if len(chunk) == 0:
                amplitudes.append(0)
            else:
                # RMS amplitude for smoother response
                amplitudes.append(np.sqrt(np.mean(chunk**2)))
        
        # Normalize amplitudes
        if max(amplitudes) > 0:
            amplitudes = np.array(amplitudes) / max(amplitudes)
        
        # Create bars
        bars = VGroup(*[
            Rectangle(width=BAR_WIDTH, height=0.1, color=BLUE)
            for _ in range(BAR_COUNT)
        ])
        bars.arrange(RIGHT, buff=0.05)
        bars.shift(DOWN * 3)
        self.add(bars)

        # Add a cool title or background
        self.camera.background_color = "#0a0a0a"

        # Animation loop over time
        prev_heights = [0.1] * BAR_COUNT
        
        for frame_idx in range(total_frames):
            amp = amplitudes[frame_idx] * SENSITIVITY
            bass_boost = min(amp * 2, 1.0)  # More bass reaction

            # Update each bar with frequency-like illusion
            new_heights = []
            for i, bar in enumerate(bars):
                # Simulate frequency bands using sine + bass
                freq_factor = np.sin(i * 0.3 + frame_idx * 0.05) * 0.3 + 0.7
                target_height = (amp ** 0.8) * freq_factor * MAX_HEIGHT * (1 + bass_boost)
                # Smooth interpolation
                smooth_height = prev_heights[i] * SMOOTHING + target_height * (1 - SMOOTHING)
                new_heights.append(smooth_height)
                
                bar.become(
                    Rectangle(
                        width=BAR_WIDTH,
                        height=smooth_height,
                        color=interpolate_color(BLUE, RED, (i / BAR_COUNT + frame_idx * 0.01) % 1),
                        fill_opacity=0.9
                    ).move_to(bars[i].get_center())
                    .align_to(bars[i], DOWN)
                )
            
            prev_heights = new_heights

            # Color shift over time
            hue = (frame_idx * COLOR_SHIFT_SPEED / total_frames) % 1
            for i, bar in enumerate(bars):
                bar.set_color(color=[PURPLE, PURPLE_B, PURPLE_C, PURPLE_D][i % 4])

            # Control playback speed to match audio
            self.wait(1 / frame_rate)

        
        
        


        self.play(Unwrite(bars))

        self.wait()