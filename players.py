import model
from pygame import mixer
from tkinter import filedialog
from mutagen.mp3 import MP3
import os


class Player:
    def __init__(self):
        mixer.init()
        self.my_model = model.Model()

    def get_db_status(self):
        return self.my_model.get_db_status()

    def close_player(self):
        mixer.music.stop()
        self.my_model.close_db_connection()

    def set_volume(self, volume_level):
        mixer.music.set_volume(volume_level)

    def add_song(self):
        song_path = filedialog.askopenfilenames(initialdir="D:/", title="Select your song..",
                                                filetype=[("mp3 file", "*.mp3")])
        if type(song_path) is tuple:
            str1 = []
            for x in song_path:
                song_name = os.path.basename(x)
                self.my_model.add_song(song_name, x)
                str1.append(song_name)
            return str1
        else:
            return



    def remove_song(self, song_name):
        self.my_model.remove_song(song_name)

    def get_song_length(self, song_name):
        self.song_path = self.my_model.get_song_path(song_name)
        self.audio_tag = MP3(self.song_path)
        song_length = self.audio_tag.info.length
        return song_length

    def play_song(self):
        mixer.quit()
        mixer.init(frequency=self.audio_tag.info.sample_rate)
        mixer.music.load(self.song_path)
        mixer.music.play()

    def set_posi(self, set_posi):
        mixer.music.set_pos(set_posi)

    def stop_song(self):
        mixer.music.stop()

    def pause_song(self):
        mixer.music.pause()

    def unpause_song(self):
        mixer.music.unpause()

    def get_song_count(self):
        return self.my_model.get_song_count()

    def add_song_to_favourites(self,song_name):
        song_path=self.my_model.get_song_path(song_name)
        result=self.my_model.add_song_to_favourite(song_name,song_path)
        return result

    def load_songs_from_favourites(self):
        result=self.my_model.load_songs_from_favourites()
        return  result,self.my_model.song_dict

    def remove_song_from_favourites(self,song_name):
        result=self.my_model.remove_song_from_favourites(song_name)
        return result

