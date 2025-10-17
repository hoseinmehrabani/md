import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
 
 
def window():
  app = QApplication(sys.argv)
  widget = QWidget()
 
  textLabel = QLabel(widget)
  textLabel.setText('آموزش پايتون')
  textLabel.move(100,85)
 
  widget.setGeometry(50,25,500,250)
  widget.setWindowTitle('تراشه')
  widget.show()
  sys.exit(app.exec_())
window()
