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
from PySide6.QtCore import Qt
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

current_track = music_files[0]

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

album_art.setAlignment(Qt.AlignCenter)
album_art.setFixedSize(350, 350)
album_art.setStyleSheet("""
    border: 2px solid #444;
    background-color: #222;
    font-size: 24px;
""")

audio = EasyID3(os.path.join(music_folder, current_track))

artist = audio.get("artist", ["Unknown Artist"])[0]
title = audio.get("title", ["Unknown Title"])[0]

track_info = QLabel(f"{artist} - {title}")
track_info.setAlignment(Qt.AlignCenter)

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

play_button.clicked.connect(play_music)

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