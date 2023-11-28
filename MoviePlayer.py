import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap, QImage
import cv2
from PyQt5.QtCore import Qt


class VideoPlayer(QMainWindow):
    def __init__(self, video_path, window_size):
        super().__init__()

        self.setWindowFlag(Qt.FramelessWindowHint)  # 윈도우 타이틀 바 없애기

        self.video_path = video_path
        self.cap = cv2.VideoCapture(video_path)

        self.window_size = window_size
        self.setGeometry(0, 0, window_size[0], window_size[1])

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)

        layout = QVBoxLayout(self.central_widget)
        layout.addWidget(self.label)

        self.timer = self.startTimer(30)  # 30ms 간격으로 타이머 이벤트 발생

        # 마진과 패딩을 0으로 설정
        layout.setContentsMargins(0, 0, 0, 0)
        self.central_widget.setStyleSheet("QMainWindow {padding: 0px;}")

    def timerEvent(self, event):
        ret, frame = self.cap.read()

        if not ret:
            self.cap.release()
            self.close()

        height, width, channel = frame.shape

        # 영상 크기를 윈도우 크기에 맞게 조절
        frame_resized = cv2.resize(frame, (self.window_size[0], self.window_size[1]))

        bytes_per_line = 3 * self.window_size[0]
        q_image = QImage(frame_resized.data, self.window_size[0], self.window_size[1], bytes_per_line,
                         QImage.Format_RGB888).rgbSwapped()

        pixmap = QPixmap.fromImage(q_image)
        self.label.setPixmap(pixmap)

    def closeEvent(self, event):
        self.cap.release()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    video_file_path = "movies/movie_1.mp4"
    window_size = (640, 480)  # 내가 원하는 윈도우 사이즈로 설정
    player = VideoPlayer(video_file_path, window_size)
    player.show()
    sys.exit(app.exec_())
