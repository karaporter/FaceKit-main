from PyQt5.QtWidgets import (QGroupBox, QLayout, QVBoxLayout, QHBoxLayout, QSlider, QWidget,QSizePolicy, QLabel)
from PyQt5.QtCore import(Qt)
from PyQt5.QtCore import (pyqtSignal, pyqtSlot)
import functools

class Slider(QWidget):
    slider_sig = pyqtSignal(tuple)
    def __init__(self, sliderType, parent = None):
        
        super(Slider, self).__init__(parent)
        self.sliderMax =  100000
        self.sliderMin = 0
        self.sliders = []
        self.type = sliderType

       
        
        self.group = QGroupBox(self.type, self)

        
        bars_layout = QVBoxLayout()
        bars_layout.setContentsMargins(0, 0, 0, 0) 
        hbox = QHBoxLayout()
        label = QLabel("1<sup>nd</sup> Axis: ")
        self.sliders.append(QSlider(Qt.Horizontal))
        self._init_slider(0)
        hbox.addWidget(label)
        hbox.addWidget(self.sliders[0])
        bars_layout.addLayout(hbox)
        bars_layout.addStretch(1)

        hbox = QHBoxLayout()
        label = QLabel("2<sup>nd</sup>  Axis: ")
        self.sliders.append(QSlider(Qt.Horizontal))
        self._init_slider(1)
        # palette = QPalette()
        # palette.setColor(QPalette.Highlight, slider.palette().dark().color())
        # slider.setPalette(palette)
        # print(slider.palette().button().color().name())
        hbox.addWidget(label)
        hbox.addWidget(self.sliders[1])
        bars_layout.addLayout(hbox)
        bars_layout.addStretch(1)


        hbox = QHBoxLayout()
        label = QLabel("3<sup>rd</sup>  Axis: ")
        self.sliders.append(QSlider(Qt.Horizontal))
        self._init_slider(2)
        hbox.addWidget(label)
        hbox.addWidget(self.sliders[2]) 
        bars_layout.addLayout(hbox)
        bars_layout.addStretch(1)
        
        hbox = QHBoxLayout()
        label = QLabel("4<sup>th</sup>  Axis: ")
        self.sliders.append(QSlider(Qt.Horizontal))
        self._init_slider(3)
        hbox.addWidget(label)
        hbox.addWidget(self.sliders[3])  
        bars_layout.addLayout(hbox)
        bars_layout.addStretch(1) 

        hbox = QHBoxLayout()
        label = QLabel("5<sup>th</sup>  Axis: ")
        self.sliders.append(QSlider(Qt.Horizontal))
        self._init_slider(4)
        hbox.addWidget(label)
        hbox.addWidget(self.sliders[4]) 
        bars_layout.addLayout(hbox)
        bars_layout.addStretch(1)

        self.group.setLayout(bars_layout)

        for i, s in enumerate(self.sliders):
            s.sliderMoved.connect(
                lambda v, ind = i: self._sliderChanging(v, ind)
            )
            
            


    def _init_slider(self, sNum):
        self.sliders[sNum].setMinimum(self.sliderMin)
        self.sliders[sNum].setMaximum(self.sliderMax)
        # self.sliders[sNum].setValue(0)
        self.sliders[sNum].setSingleStep(1)

    def resizeWidget(self, w, h):
        self.resize(w, h)
        
    def setSliderValue(self, value, ind):
        v = self._returnSliderValue(value)
        self.sliders[ind].setValue(int(v))

    def _returnSliderValue(self, v):
        return v * (self.sliderMax - self.sliderMin) + self.sliderMin

    @pyqtSlot(int)
    def _sliderChanging(self, value, sliderNum):
        v = (value - self.sliderMin) / (self.sliderMax - self.sliderMin)
        self.slider_sig.emit((sliderNum, v))
        
