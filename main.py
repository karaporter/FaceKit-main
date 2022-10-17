import sys

from PyQt5.QtWidgets import QApplication

sys.path.append('src/model/')
sys.path.append('src/controller/')
sys.path.append('src/view/')

from MainWindow import MainWindow




OBJDIR = './tempOBJ/'
DATAMATRIXDIR = './data/points/'
DATAOBJDIR = './data/obj/'




if __name__ == '__main__':
    app = QApplication(sys.argv)
   
    main = MainWindow()

    sys.exit(app.exec())
    
   

