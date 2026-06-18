import sys
import os
import locale
import random
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
from PySide6.QtGui import QPixmap, QShortcut, QKeySequence
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
    artist_label.setText(artist)
    title_label.setText(title)

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


artist_label = QLabel("Loading artist...")
artist_label.setAlignment(Qt.AlignCenter)
artist_label.setStyleSheet("color: white; font-size: 20px; font-weight: bold;")

title_label = QLabel("Loading song...")
title_label.setAlignment(Qt.AlignCenter)
title_label.setStyleSheet("color: white; font-size: 18px;")

load_track()

locale.setlocale(locale.LC_NUMERIC, "C")
player = mpv.MPV()


progress_bar = QSlider(Qt.Horizontal)
progress_bar.setStyleSheet("""
    QSlider::groove:horizontal {
        height: 8px;
        background: #444;
        border-radius: 4px;
    }

    QSlider::sub-page:horizontal {
        background: palette(highlight);
        border-radius: 4px;
    }

    QSlider::add-page:horizontal {
        background: #444;
        border-radius: 4px;
    }

    QSlider::handle:horizontal {
        background: #ddd;
        width: 18px;
        margin: -6px 0;
        border-radius: 9px;
    }
""")
progress_bar.setRange(0, 100)
progress_bar.setValue(0)

time_label = QLabel("0:00")
duration_label = QLabel("0:00")
time_layout = QHBoxLayout()
time_layout.addWidget(time_label)
time_layout.addStretch()
time_layout.addWidget(duration_label)

time_label.setStyleSheet("color: white; font-size: 18px;")
duration_label.setStyleSheet("color: white; font-size: 18px;")

volume_label = QLabel("Volume")
volume_label.setStyleSheet("color: white; font-size: 18px;")

volume_slider = QSlider(Qt.Horizontal)
volume_slider.setRange(0, 100)
volume_slider.setValue(100)
player.volume = 100
volume_slider.valueChanged.connect(lambda value: setattr(player, "volume", value))
volume_slider.setStyleSheet(progress_bar.styleSheet())

prev_button = QPushButton("⏮")
play_button = QPushButton("▶")
next_button = QPushButton("⏭")
shuffle_button = QPushButton("⤮")

button_style = """
    QPushButton {
        background-color: transparent;
        border: none;
        font-size: 24px;
        padding: 8px;
    }

    QPushButton:hover {
        color: palette(highlight);
    }
"""

prev_button.setStyleSheet(button_style)
play_button.setStyleSheet(button_style)
next_button.setStyleSheet(button_style)
shuffle_button.setStyleSheet(button_style)

is_playing = False
has_started = False
shuffle_enabled = False

def play_music():
    global is_playing, has_started

    if not has_started:
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

    if shuffle_enabled:
        current_track_index = random.randrange(len(music_files))
    else:
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
        current_time = int(player.time_pos)
        duration = int(player.duration or 0)
        progress_bar.setRange(0, duration)

        duration_minutes = duration // 60
        duration_seconds = duration % 60

        remaining_time = max(duration - current_time, 0)
        remaining_minutes = remaining_time // 60
        remaining_seconds = remaining_time % 60

        duration_label.setText(f"-{remaining_minutes}:{remaining_seconds:02d}")

        if not progress_bar.isSliderDown():
            progress_bar.setValue(current_time)

        minutes = current_time // 60
        seconds = current_time % 60
        time_label.setText(f"{minutes}:{seconds:02d}")

        if has_started and player.time_pos is not None and player.duration is not None:
            if player.time_pos >= player.duration - 2:
                next_track()    

def toggle_shuffle():
    global shuffle_enabled

    shuffle_enabled = not shuffle_enabled

    if shuffle_enabled:
        shuffle_button.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                font-size: 24px;
                padding: 8px;
                color: palette(highlight);
            }
        """)
    else:
        shuffle_button.setStyleSheet(button_style)



play_button.clicked.connect(play_music)
next_button.clicked.connect(next_track)
prev_button.clicked.connect(previous_track)
shuffle_button.clicked.connect(toggle_shuffle)

progress_bar.sliderReleased.connect(lambda: seek_song(progress_bar.value()))

timer = QTimer()
timer.timeout.connect(update_progress)
timer.start(1000)

layout.addWidget(album_art, alignment=Qt.AlignCenter)
meta_layout = QVBoxLayout()
meta_layout.setSpacing(4)
meta_layout.addWidget(artist_label)
meta_layout.addWidget(title_label)

layout.addLayout(meta_layout)
layout.addWidget(progress_bar)
layout.addLayout(time_layout)
layout.addWidget(volume_label)
layout.addWidget(volume_slider)
time_layout.setContentsMargins(8, 0, 8, 12)


controls = QHBoxLayout()
controls.addWidget(prev_button)
controls.addWidget(play_button)
controls.addWidget(next_button)
controls.addWidget(shuffle_button)

layout.addLayout(controls)

space_shortcut = QShortcut(QKeySequence("Space"), window)
space_shortcut.activated.connect(play_music)

next_shortcut = QShortcut(QKeySequence("Right"), window)
next_shortcut.activated.connect(next_track)

prev_shortcut = QShortcut(QKeySequence("Left"), window)
prev_shortcut.activated.connect(previous_track)

window.setLayout(layout)

window.show()

sys.exit(app.exec())