from moviepy.editor import AudioFileClip, VideoFileClip
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from tkinter import ttk
import os

class MediaConverter:
    def __init__(self, root):
        self.root = root
        self.root.title("Media Converter")
        self.root.geometry("600x400")  # Set the window size

        self.input_media_paths = []
        self.target_format = ""
        self.supported_audio_formats = [".mp3", ".wav"]
        self.supported_video_formats = [".mp4", ".avi", ".mkv"]

        self.select_frame = tk.Frame(root)
        self.select_frame.pack(pady=20)

        self.select_option_label = tk.Label(self.select_frame, text="Select Conversion Type:", font=("Helvetica", 12))
        self.select_option_label.pack()

        self.selected_option = tk.StringVar()
        self.audio_radio_button = tk.Radiobutton(self.select_frame, text="Audio", variable=self.selected_option, value="audio", font=("Helvetica", 10))
        self.audio_radio_button.pack(anchor="w")
        self.video_radio_button = tk.Radiobutton(self.select_frame, text="Video", variable=self.selected_option, value="video", font=("Helvetica", 10))
        self.video_radio_button.pack(anchor="w")

        self.upload_button = tk.Button(root, text="Upload Media Files", command=self.upload_media_files, font=("Helvetica", 12))
        self.upload_button.pack(pady=10)

        self.convert_button = tk.Button(root, text="Convert", command=self.convert, font=("Helvetica", 12))
        self.convert_button.pack(pady=10)

        self.progress_bar = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
        self.progress_bar.pack(pady=20)

        self.input_media_label = tk.Label(root, text="Uploaded Media Files:", font=("Helvetica", 12))
        self.input_media_label.pack()

    def upload_media_files(self):
        filetypes = [("Supported Files", "*.mp3;*.wav;*.mp4;*.avi;*.mkv")]
        self.input_media_paths = filedialog.askopenfilenames(title="Upload media files", filetypes=filetypes, multiple=True)
        self.display_uploaded_files()

    def convert(self):
        if not self.input_media_paths:
            messagebox.showinfo("Error", "No media files selected.")
            return

        if not self.selected_option.get():
            messagebox.showinfo("Error", "Please select a conversion type.")
            return

        if self.selected_option.get() == "audio":
            self.target_format = self.select_audio_format()
            if not self.target_format:
                return

        # Create a new folder named "converted_files" in the current directory
        output_folder = os.path.join(os.getcwd(), "converted_files")
        os.makedirs(output_folder, exist_ok=True)

        total_files = len(self.input_media_paths)
        converted_files = 0

        for input_media_path in self.input_media_paths:
            if self.selected_option.get() == "audio":
                self.convert_audio(input_media_path, output_folder)
            else:
                self.convert_video(input_media_path, output_folder)

            converted_files += 1
            progress = converted_files / total_files * 100
            self.update_progress(progress)

        messagebox.showinfo("Conversion Complete", f"All {total_files} files converted successfully.")
        self.input_media_paths = []  # Clear the input media paths
        self.display_uploaded_files()

    def select_audio_format(self):
        options = [".mp3", ".wav"]
        return simpledialog.askstring("Select Target Audio Format", "Choose the target audio format:", initialvalue=".mp3", parent=self.root)

    def convert_audio(self, input_path, output_folder):
        audio_clip = AudioFileClip(input_path)
        output_path = os.path.join(output_folder, os.path.basename(input_path).rsplit('.', 1)[0] + self.target_format)
        audio_clip.write_audiofile(output_path, logger=None)
        audio_clip.close()

    def convert_video(self, input_path, output_folder):
        video_clip = VideoFileClip(input_path)
        audio_clip = video_clip.audio
        output_path = os.path.join(output_folder, os.path.basename(input_path).rsplit('.', 1)[0] + ".mp3")
        audio_clip.write_audiofile(output_path, logger=None)
        audio_clip.close()

    def update_progress(self, value):
        self.progress_bar["value"] = value
        self.root.update_idletasks()

    def display_uploaded_files(self):
        uploaded_files_text = "\n".join(self.input_media_paths)
        self.input_media_label.config(text=f"Uploaded Media Files:\n\n{uploaded_files_text}")

def main():
    root = tk.Tk()
    app = MediaConverter(root)
    root.mainloop()

if __name__ == "__main__":
    main()
