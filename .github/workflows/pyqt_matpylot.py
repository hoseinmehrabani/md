import sys
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget

class MplCanvas(FigureCanvas):
    def __init__(self, parent=None):
        fig, self.ax = plt.subplots(figsize=(8, 6))
        super().__init__(fig)
        self.plot()

    def plot(self):
        data = {
            'Smoker': ['Yes', 'Yes', 'Yes', 'No', 'Yes', 'No', 'Yes', 'No', 'Yes', 'Yes']
        }

        df = pd.DataFrame(data)
        smoker_counts = df['Smoker'].value_counts()
        smoker_percentage = smoker_counts / smoker_counts.sum() * 100

        labels = smoker_percentage.index
        sizes = smoker_percentage.values
        colors = ['lightcoral', 'lightskyblue']
        explode = (0.1, 0)  # جدا کردن قسمت سیگاری‌ها

        self.ax.pie(sizes, explode=explode, labels=labels, colors=colors,
                    autopct='%1.1f%%', shadow=True, startangle=140)
        self.ax.axis('equal')  # برای دایره‌ای بودن نمودار
        self.ax.set_title('Percentage of Smokers vs Non-Smokers')

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Smoker vs Non-Smoker Pie Chart")
        self.setGeometry(100, 100, 800, 600)

        self.canvas = MplCanvas(self)
        self.setCentralWidget(self.canvas)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
