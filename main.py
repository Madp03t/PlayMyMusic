import sys
import os
import locale
locale.setlocale(locale.LC_ALL, "C")
import mpv
from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QSlider
)
from PySide6.QtCore import Qt, QTimer 
from PySide6.QtGui import QPixmap
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC


app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle("PlayMyMusic")
window.resize(700, 700)

layout = QVBoxLayout()
layout.setAlignment(Qt.AlignCenter)
layout.setSpacing(30)

album_art = QLabel()

music_folder = os.path.expanduser("~/Music")

music_files = [
    file for file in os.listdir(music_folder)
    if file.endswith(".mp3")
]

music_files.sort()

current_track_index = 0
current_track = music_files[current_track_index]


album_art.setAlignment(Qt.AlignCenter)
album_art.setFixedSize(350, 350)
album_art.setStyleSheet("""
    border: 2px solid #444;
    background-color: #222;
    font-size: 24px;
""")

def load_track():
    global artist, title

    track_path = os.path.join(music_folder, current_track)
    audio = EasyID3(track_path)

    artist = audio.get("artist", ["Unknown Artist"])[0]
    title = audio.get("title", ["Unknown Title"])[0]
    track_info.setText(f"{artist} - {title}")

    tags = ID3(os.path.join(music_folder, current_track))
    cover_data = None

    for tag in tags.values():
            if isinstance(tag, APIC):
                cover_data = tag.data
                break

    pixmap = QPixmap()
    pixmap.loadFromData(cover_data)

    album_art.setPixmap(
        pixmap.scaled(
            350,
            350,
            Qt.KeepAspectRatio,
            Qt.SmoothTransformation
        )
    )


track_info = QLabel("Loading track...")
track_info.setAlignment(Qt.AlignCenter)

load_track()

locale.setlocale(locale.LC_NUMERIC, "C")
player = mpv.MPV()


progress_bar = QSlider(Qt.Horizontal)
progress_bar.setRange(0, 100)
progress_bar.setValue(0)

prev_button = QPushButton("⏮")
play_button = QPushButton("▶")
next_button = QPushButton("⏭")
shuffle_button = QPushButton("Shuffle")

is_playing = False
has_started = False

def play_music():
    global is_playing, has_started

    if not has_started:
        print(current_track)
        player.play(os.path.join(music_folder, current_track))
        progress_bar.setValue(0)
        player.pause = False
        play_button.setText("⏸")
        is_playing = True
        has_started = True

    elif is_playing:
        player.pause = True
        play_button.setText("▶")
        is_playing = False

    else:
        player.pause = False
        play_button.setText("⏸")
        is_playing = True

def next_track():
    global current_track_index, current_track, is_playing, has_started

    current_track_index = (current_track_index + 1) % len(music_files)
    current_track = music_files[current_track_index]

    is_playing = False
    has_started = False
    load_track()
    play_music()

def previous_track():
    global current_track_index, current_track, is_playing, has_started

    current_track_index = (current_track_index - 1) % len(music_files)
    current_track = music_files[current_track_index]

    is_playing = False
    has_started = False
    load_track()
    play_music()

def seek_song(value):
    if has_started:
        player.time_pos = value

def update_progress():
    if has_started and player.time_pos is not None:
        progress_bar.setValue(int(player.time_pos))


play_button.clicked.connect(play_music)
next_button.clicked.connect(next_track)
prev_button.clicked.connect(previous_track)
progress_bar.sliderReleased.connect(lambda: seek_song(progress_bar.value()))
timer = QTimer()
timer.timeout.connect(update_progress)
timer.start(1000)

layout.addWidget(album_art, alignment=Qt.AlignCenter)
layout.addWidget(track_info)
layout.addWidget(progress_bar)

controls = QHBoxLayout()
controls.addWidget(prev_button)
controls.addWidget(play_button)
controls.addWidget(next_button)
controls.addWidget(shuffle_button)

layout.addLayout(controls)

window.setLayout(layout)

window.show()

sys.exit(app.exec())