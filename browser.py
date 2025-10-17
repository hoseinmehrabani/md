import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QPushButton, QVBoxLayout, QWidget, QHBoxLayout, QMessageBox, QListWidget, QTabWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("مرورگر وب پیشرفته")
        self.setGeometry(100, 100, 1200, 800)

        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.add_new_tab("http://www.google.com")

        # نوار جستجو
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)

        # دکمه‌ها
        back_button = QPushButton("قبلی")
        back_button.clicked.connect(self.browser.back)

        forward_button = QPushButton("بعدی")
        forward_button.clicked.connect(self.browser.forward)

        reload_button = QPushButton("بارگذاری مجدد")
        reload_button.clicked.connect(self.browser.reload)

        history_button = QPushButton("تاریخچه")
        history_button.clicked.connect(self.show_history)

        bookmark_button = QPushButton("بوک‌مارک")
        bookmark_button.clicked.connect(self.add_bookmark)

        new_tab_button = QPushButton("تب جدید")
        new_tab_button.clicked.connect(self.add_new_tab_from_url)

        # لایه‌بندی
        h_layout = QHBoxLayout()
        h_layout.addWidget(back_button)
        h_layout.addWidget(forward_button)
        h_layout.addWidget(reload_button)
        h_layout.addWidget(history_button)
        h_layout.addWidget(bookmark_button)
        h_layout.addWidget(new_tab_button)
        h_layout.addWidget(self.url_bar)

        v_layout = QVBoxLayout()
        v_layout.addLayout(h_layout)
        v_layout.addWidget(self.tabs)

        container = QWidget()
        container.setLayout(v_layout)

        self.setCentralWidget(container)

        # لیست‌های تاریخچه و بوک‌مارک
        self.history = []
        self.bookmarks = []

    def add_new_tab(self, url):
        self.browser = QWebEngineView()
        self.browser.setUrl(url)
        self.browser.urlChanged.connect(self.update_url_bar)

        self.tabs.addTab(self.browser, url)
        self.history.append(url)

    def add_new_tab_from_url(self):
        url = self.url_bar.text()
        if not url.startswith("http"):
            url = "http://" + url
        self.add_new_tab(url)

    def navigate_to_url(self):
        url = self.url_bar.text()
        if not url.startswith("http"):
            url = "http://" + url
        self.browser.setUrl(url)

    def update_url_bar(self, q):
        self.url_bar.setText(q.toString())

    def show_history(self):
        history_list = "\n".join(self.history)
        QMessageBox.information(self, "تاریخچه", history_list if history_list else "هیچ تاریخی وجود ندارد.")

    def add_bookmark(self):
        url = self.url_bar.text()
        if url and url not in self.bookmarks:
            self.bookmarks.append(url)
            QMessageBox.information(self, "بوک‌مارک", f"بوک‌مارک '{url}' اضافه شد!")
        else:
            QMessageBox.warning(self, "بوک‌مارک", "این URL قبلاً بوک‌مارک شده است یا خالی است.")

    def show_bookmarks(self):
        bookmark_list = "\n".join(self.bookmarks)
        QMessageBox.information(self, "بوک‌مارک‌ها", bookmark_list if bookmark_list else "هیچ بوک‌مارکی وجود ندارد.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Browser()
    window.show()
    sys.exit(app.exec_())
