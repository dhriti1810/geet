from cx_Oracle import *
import traceback


class Model:
    def __init__(self):
        self.song_dict = {}
        self.db_status = True
        self.conn = None
        self.cur = None
        try:
            self.conn = connect("mouzikka/music@127.0.0.1/xe")
            self.cur = self.conn.cursor()
        except DatabaseError:
            self.db_status = False
            print(traceback.format_exc())

    def get_db_status(self):
        return self.db_status

    def close_db_connection(self):
        if self.cur is not None:
            self.cur.close()
        if self.conn is not None:
            self.conn.close()

    def add_song(self, song_name, song_path):
        self.song_dict[song_name] = song_path

    def get_song_path(self, song_name):
        return self.song_dict[song_name]

    def remove_song(self, song_name):
        self.song_dict.pop(song_name)

    def get_song_count(self):
        return len(self.song_dict)

    def search_song_in_favourites(self, song_name):
        self.cur.execute("Select song_name from Myfavourites where song_name=:1", (song_name,))
        song_tuple = self.cur.fetchone()
        if song_tuple is None:
            return False
        return True

    def add_song_to_favourite(self, song_name, song_path):
        is_song_present = self.search_song_in_favourites(song_name)
        if is_song_present:
            return "Song already present in your favourites"
        self.cur.execute("Select max(song_id) from Myfavourites")
        last_song_id = self.cur.fetchone()[0]
        next_song_id = 1
        if last_song_id is not None:
            next_song_id = last_song_id + 1
        self.cur.execute("Insert into Myfavourites values(:1,:2,:3)", (next_song_id, song_name, song_path))
        self.conn.commit()
        return "Song added to your favourites"

    def load_songs_from_favourites(self):
        self.cur.execute("Select song_name,song_path from Myfavourites")
        song_present = False
        for song_name, song_path in self.cur:
            self.song_dict[song_name] = song_path
            song_present = True
        if song_present:
            return "List populated from favourites"
        else:
            return "No song present in your favourites"

    def remove_song_from_favourites(self, song_name):
        self.cur.execute("delete from Myfavourites where song_name=:1 ", (song_name,))
        total = self.cur.rowcount
        if total == 0:
            return "song not present in your favourites"
        else:
            self.song_dict.pop(song_name)
            self.conn.commit()
            return "Song deleted from your favourites"
