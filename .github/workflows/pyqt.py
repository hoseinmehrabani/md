import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel


class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Simple PyQt5 App')
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        self.label = QLabel('Hello, PyQt5!', self)
        self.label.setStyleSheet("font-size: 20px;")

        btn = QPushButton('Click Me', self)
        btn.setStyleSheet("font-size: 16px; background-color: lightblue;")
        btn.clicked.connect(self.on_button_click)

        layout.addWidget(self.label)
        layout.addWidget(btn)

        self.setLayout(layout)

    def on_button_click(self):
        self.label.setText('Button Clicked!')
        self.label.setStyleSheet("font-size: 20px; color: red;")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    my_app = MyApp()
    my_app.show()
    sys.exit(app.exec_())
