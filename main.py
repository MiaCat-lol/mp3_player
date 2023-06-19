from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
 
from qtwidgets import EqualizerBar
 
import random
import os
 
 
 
class Window(QMainWindow):
    def __init__(self):
        super().__init__()
 
        self.init_ui()
 
    def init_ui(self):
        self.equalizer = EqualizerBar(5, ['#0C0786', '#40039C', '#6A00A7', '#8F0DA3', '#B02A8F', '#CA4678', '#E06461',
                                    '#F1824C', '#FCA635', '#FCCC25', '#EFF821'])
 
        self.player = QMediaPlayer()
 
        FileMenu = self.menuBar().addMenu('&File')
 
        OpenFileAction = QAction('Open...', self)
        OpenFileAction.setStatusTip('Open')
        OpenFileAction.setShortcut(QKeySequence.Open)
        OpenFileAction.triggered.connect(self.open_file)
        FileMenu.addAction(OpenFileAction)
 
        QuitFileAction = QAction('Quit...', self)
        QuitFileAction.setStatusTip('Quit')
        QuitFileAction.setShortcut(QKeySequence.Close)
        QuitFileAction.triggered.connect(self.quit_function)
        FileMenu.addAction(QuitFileAction)
 
        PreferenceMenu = self.menuBar().addMenu('&Preference')
 
        StartPreferenceAction = QAction('Play', self)
        StartPreferenceAction.setStatusTip('Play')
        StartPreferenceAction.triggered.connect(self.play_audio)
        PreferenceMenu.addAction(StartPreferenceAction)
 
        PausePreferenceAction = QAction('Pause', self)
        PausePreferenceAction.setStatusTip('Pause')
        PausePreferenceAction.triggered.connect(self.pause_audio)
        PreferenceMenu.addAction(PausePreferenceAction)
 
        StopPreferenceAction = QAction('Stop', self)
        StopPreferenceAction.setStatusTip('Stop')
        StopPreferenceAction.triggered.connect(lambda: self.player.stop())
        PreferenceMenu.addAction(StopPreferenceAction)
 
        self.play_button = QPushButton()
        self.play_button.setEnabled(False)
        self.play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.play_button.clicked.connect(self.play_audio)
 
        self.stop_button = QPushButton()
        self.stop_button.setEnabled(False)
        self.stop_button.setIcon(self.style().standardIcon(QStyle.SP_MediaStop))
        self.stop_button.clicked.connect(self.stop_function)
 
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 0)
        self.slider.sliderMoved.connect(self.set_position)      
 
        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setMaximum(1)
        self.volume_slider.setMaximum(100)
        self.volume_slider.setValue(70)
        self.volume_slider.setEnabled(False)
 
        self.volume_slider.sliderMoved.connect(self.player.setVolume)
        self.volume_slider.valueChanged.connect(self.volume_change)
 
        self.volume_label = QLabel()
        self.volume_label.setText('70')
 
        self.muted_checkbox = QCheckBox()
        self.muted_checkbox.setEnabled(False)
        self.muted_checkbox.setIcon(self.style().standardIcon(QStyle.SP_MediaVolumeMuted))
        self.muted_checkbox.toggled.connect(self.muted_cheking)
 
        wid = QWidget(self)
        self.setCentralWidget(wid)
 
        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)
        controlLayout.addWidget(self.play_button)
        controlLayout.addWidget(self.stop_button)
        controlLayout.addWidget(self.slider)
        controlLayout.addWidget(self.volume_label)
        controlLayout.addWidget(self.volume_slider)
        controlLayout.addWidget(self.muted_checkbox)
 
        layout = QVBoxLayout()
        layout.addWidget(self.equalizer)
        layout.addLayout(controlLayout)
 
        wid.setLayout(layout)
        self.player.stateChanged.connect(self.logo_change)
        self.player.positionChanged.connect(self.position_changed)
        self.player.durationChanged.connect(self.position_changed)
 
        self.PlayList = QListView()
        model = QStandardItemModel()
        self.PlayList.setModel(model)
        self.PlayList.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.PlayList.clicked.connect(self.playlist_clicked)
 
        self.playList_window = QDockWidget('PlayList', self)
        self.playList_window.setAllowedAreas(Qt.RightDockWidgetArea)
        self.playList_window.setWidget(self.PlayList)
        self.addDockWidget(Qt.RightDockWidgetArea, self.playList_window)
 
 
    def open_file(self):
        self.fileName, _ = QFileDialog.getOpenFileName(self, "Open", QDir.homePath(), "Files (*.wav, *.mp3)")
 
        if self.fileName != '':
            self.player.setMedia(QMediaContent(QUrl.fromLocalFile(self.fileName)))
            self.play_button.setEnabled(True)
            self.stop_button.setEnabled(True)
            self.muted_checkbox.setEnabled(True)
            self.volume_slider.setEnabled(True)
 
            self.timer = QTimer()
            self.timer.setInterval(100)
            self.timer.timeout.connect(self.update_values)
 
            item = QStandardItem(os.path.basename(self.fileName))
            self.PlayList.model().appendRow(item)
 
    def playlist_clicked(self, index):
        self.player.stop()
        filename = self.PlayList.model().itemFromIndex(index).text()
        self.fileName = os.path.join(os.path.dirname(self.fileName), fileName)
        self.player.setMedia(QMediaContent(QUrl.fromLocalFile(self.fileName)))
        self.play_audio()
 
    def play_audio(self):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.player.pause()
            self.timer.stop()
        else:
            self.player.play()
            self.timer.start()
 
    def logo_change(self, state):
        if self.player.state() == QMediaPlayer.PlayingState:
            self.play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
 
    def pause_audio(self):
        self.player.pause()
        self.timer.stop()
 
    def volume_change(self):
        self.value = self.volume_slider.value()
        self.volume_label.setText(str(self.value))
 
    def muted_cheking(self):
        if self.muted_checkbox.isChecked():
            self.player.setMuted(True)
        else:
            self.player.setMuted(False)
 
    def stop_function(self):
        self.player.stop()
        self.timer.stop()
 
    def quit_function(self):
        sys.exit(app.exec_())
 
    def position_changed(self, position):
        self.slider.setValue(position)
 
    def duration_changed(self, duration):
        self.slider.setRange(0, duration)
 
    def set_position(self, position):
        self.player.setPosition(position)
 
    def update_values(self):
        self.equalizer.setValues([
            min(100, v + random.randint(0, 50)
            if random.randint(0, 5) > 2 else v)
            for v in self.equalizer.values()])
 
 
app = QApplication([])
app.setApplicationName("Audio Player")
app.setStyle("Fusion")
Equalizer = Window()
Equalizer.setFixedSize(600, 400)
Equalizer.show()
app.exec_()