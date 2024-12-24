import tkinter as tk
from tkinter import filedialog, ttk
import librosa
import soundfile as sf
import numpy as np
from scipy.signal import butter, lfilter
import customtkinter as ctk
import noisereduce as nr
import pygame

class AudioFilterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎧 Audio Filter Studio")
        self.root.geometry("600x800")  # زودت المساحة شوية
        self.root.configure(bg="#2C3E50")  # Deep blue-gray background

        # Initialize pygame mixer
        pygame.mixer.init()

        # متغير لتخزين مسار الملف الصوتي الحالي
        self.current_audio_file = None

        # Create main frame
        self.main_frame = ctk.CTkFrame(root, corner_radius=20, fg_color="#34495E")
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Title
        self.title_label = ctk.CTkLabel(
            self.main_frame, 
            text="Audio Filter Studio", 
            font=("Helvetica", 24, "bold"),
            text_color="#ECF0F1"
        )
        self.title_label.pack(pady=(20, 10))

        # Create main content
        self.create_buttons()
        self.create_playback_controls()

        # Status Label
        self.status_label = ctk.CTkLabel(
            self.main_frame, 
            text="", 
            text_color="#2ECC71",
            font=("Helvetica", 12)
        )
        self.status_label.pack(pady=20)

    def create_playback_controls(self):
        # إطار للتحكم في التشغيل
        self.playback_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.playback_frame.pack(pady=10)

        # أزرار التحكم
        playback_style = {
            "width": 100,
            "height": 40,
            "font": ("Helvetica", 14),
            "corner_radius": 8,
            "hover_color": "#3498DB",
            "fg_color": "#2980B9",
            "text_color": "white"
        }

        # زر التشغيل
        self.play_button = ctk.CTkButton(
            self.playback_frame, 
            text="▶️ Play", 
            command=self.play_current_audio,
            **playback_style
        )
        self.play_button.pack(side="left", padx=5)

        # زر الإيقاف
        self.stop_button = ctk.CTkButton(
            self.playback_frame, 
            text="⏹️ Stop", 
            command=self.stop_audio,
            **playback_style
        )
        self.stop_button.pack(side="left", padx=5)

        # زر الإيقاف المؤقت
        self.pause_button = ctk.CTkButton(
            self.playback_frame, 
            text="⏸️ Pause", 
            command=self.pause_audio,
            **playback_style
        )
        self.pause_button.pack(side="left", padx=5)

    def play_current_audio(self):
        """Play the current audio file"""
        if self.current_audio_file and pygame.mixer.music.get_busy() == False:
            try:
                pygame.mixer.music.load(self.current_audio_file)
                pygame.mixer.music.play()
                self.status_label.configure(text=f"Playing audio from {self.current_audio_file}")
            except Exception as e:
                self.status_label.configure(text=f"Error playing audio: {str(e)}")

    def pause_audio(self):
        """Pause the current audio"""
        pygame.mixer.music.pause()
        self.status_label.configure(text="Audio paused")

    def stop_audio(self):
        """Stop the current audio"""
        pygame.mixer.music.stop()
        self.status_label.configure(text="Audio stopped")

    def create_buttons(self):
        # Button style
        button_style = {
            "width": 250,
            "height": 50,
            "font": ("Helvetica", 16),
            "corner_radius": 10,
            "hover_color": "#3498DB",
            "fg_color": "#2980B9",
            "text_color": "white"
        }

        # Pitch Change Button
        self.button_pitch = ctk.CTkButton(
            self.main_frame, 
            text="🎵 Change Pitch", 
            command=self.change_pitch,
            **button_style
        )
        self.button_pitch.pack(pady=10)

        # Speed Change Button
        self.button_speed = ctk.CTkButton(
            self.main_frame, 
            text="⏩ Change Speed", 
            command=self.change_speed,
            **button_style
        )
        self.button_speed.pack(pady=10)

        # Noise Reduction Button
        self.button_noise = ctk.CTkButton(
            self.main_frame, 
            text="🔇 Reduce Noise", 
            command=self.reduce_noise,
            **button_style
        )
        self.button_noise.pack(pady=10)

        # Audio Equalization Button
        self.button_equalize = ctk.CTkButton(
            self.main_frame, 
            text="📊 Equalize Audio", 
            command=self.equalize_audio,
            **button_style
        )
        self.button_equalize.pack(pady=10)

    def play_audio(self, file_path):
        """Play the audio file using pygame and store the file path"""
        try:
            # تخزين مسار الملف الصوتي
            self.current_audio_file = file_path
            
            # تشغيل الصوت
            pygame.mixer.music.load(file_path)
            pygame.mixer.music.play()
            
            self.status_label.configure(text=f"Playing audio from {file_path}")
        except Exception as e:
            self.status_label.configure(text=f"Error playing audio: {str(e)}")

    def change_pitch(self):
        input_file = filedialog.askopenfilename(title="Select Input Audio File", filetypes=[("Audio Files", "*.wav *.mp3")])
        if not input_file:
            return
        output_file = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[("WAV Files", "*.wav")])
        if not output_file:
            return
        
        audio, sr = librosa.load(input_file, sr=None)
        pitched_audio = librosa.effects.pitch_shift(audio, sr=sr, n_steps=4)
        sf.write(output_file, pitched_audio, sr)
        self.status_label.configure(text=f"Pitch changed and saved to {output_file}")
        
        # Play the modified audio
        self.play_audio(output_file)

    def change_speed(self):
        input_file = filedialog.askopenfilename(title="Select Input Audio File", filetypes=[("Audio Files", "*.wav *.mp3")])
        if not input_file:
            return
        output_file = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[("WAV Files", "*.wav")])
        if not output_file:
            return
        
        audio, sr = librosa.load(input_file, sr=None)
        stretched_audio = librosa.effects.time_stretch(audio, rate = 1.7)
        sf.write(output_file, stretched_audio, sr)
        self.status_label.configure(text=f"Speed changed and saved to {output_file}")

    def reduce_noise(self):
        input_file = filedialog.askopenfilename(title="Select Input Audio File", filetypes=[("Audio Files", "*.wav *.mp3")])
        if not input_file:
            return
        output_file = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[("WAV Files", "*.wav")])
        if not output_file:
            return
        
        audio, sr = librosa.load(input_file, sr=None)
        reduced_noise_audio = nr.reduce_noise(y=audio, sr=sr)
        sf.write(output_file, reduced_noise_audio, sr)
        self.status_label.configure(text=f"Noise reduced and saved to {output_file}")

    def equalize_audio(self):
        input_file = filedialog.askopenfilename(title="Select Input Audio File", filetypes=[("Audio Files", "*.wav *.mp3")])
        if not input_file:
            return
        output_file = filedialog.asksaveasfilename(defaultextension=".wav", filetypes=[("WAV Files", "*.wav")])
        if not output_file:
            return
        
        def butter_bandpass(lowcut, highcut, fs, order=5):
            nyquist = 0.5 * fs
            low = lowcut / nyquist
            high = highcut / nyquist
            b, a = butter(order, [low, high], btype='band')
            return b, a
        
        def bandpass_filter(data, lowcut, highcut, fs, order=5):
            b, a = butter_bandpass(lowcut, highcut, fs, order=order)
            y = lfilter(b, a, data)
            return y
        
        audio, sr = librosa.load(input_file, sr=None)
        filtered_audio = bandpass_filter(audio, 300, 3000, sr)
        sf.write(output_file, filtered_audio, sr)
        self.status_label.configure(text=f"Audio equalized and saved to {output_file}")

    
def main():
    pygame.init() 
    root = ctk.CTk()
    app = AudioFilterApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
