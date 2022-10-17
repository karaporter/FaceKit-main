from OpenGLWindow import OpenGLWindow

from PyQt5.QtWidgets import (QLayout, QWidget, QHBoxLayout, QVBoxLayout, QPushButton,
                        QLabel, QSlider, QComboBox, QGroupBox, QGridLayout, QSizePolicy)
from PyQt5.QtGui import (QSurfaceFormat, QOpenGLVersionProfile, QPalette)
from PyQt5.QtCore import(Qt, pyqtSlot)


from PCAFace import PCAFace
from PCAtoGL import ViewPortHandler
from Slider import Slider

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("CU Face Kit")
        self.setFixedSize(1280, 720)
        self.pca_model = PCAFace()
        self.sliderMax = 1000000
        self.sliderMin = -1000000
        #slider bar lists
        self.sliders = []


        
        glFormat = QSurfaceFormat()
        glFormat.setSwapBehavior(QSurfaceFormat.DoubleBuffer)
        glFormat.setSwapInterval(1)
        glFormat.setVersion(4, 1)
        glFormat.setProfile(QSurfaceFormat.CoreProfile)
        glFormat.setSamples(4)
        QSurfaceFormat.setDefaultFormat(glFormat)
        vp = QOpenGLVersionProfile()
        vp.setVersion(4, 1)
        vp.setProfile(QSurfaceFormat.CoreProfile)
        

        view_Layout = QHBoxLayout(self)
        view_Layout.setContentsMargins(2,2,2,2)
        

        # view port setup
        self.glwindow = OpenGLWindow()
        view_Layout.addWidget(self.glwindow, 75)

        # Sliders section
        sample_grid = QVBoxLayout()
        self.mesh_group = Slider("Mesh")
        sample_grid.addWidget(self.mesh_group.group)
        

        self.diffuse_group = Slider('Diffuse')
        sample_grid.addWidget(self.diffuse_group.group)
    
       # Buttons section
        self.saveButton = QPushButton(self)
        self.saveButton.setText("Save Params")
        sample_grid.addWidget(self.saveButton)
        
        self.loadButton = QPushButton(self)
        self.loadButton.setText("Load Params")
        sample_grid.addWidget(self.loadButton)
        
        

        view_Layout.addLayout(sample_grid, 25) 
        view_Layout.addStretch(1)


        #-------------------------------Model - View Setup-------------------------------------------------

        self.view_port_handler = ViewPortHandler(self.glwindow, self.pca_model)
        
        #--------------------------------Signal Setup-------------------------------------------------
        '''
        self.sliders[0].valueChanged.connect(
            lambda: self._sliderChanging(0, 0) 
            )

        self.sliders[1].valueChanged.connect(
            lambda: self._sliderChanging(1, 1) 
            )

        self.sliders[2].valueChanged.connect(
            lambda: self._sliderChanging(2, 2) 
        )

        self.sliders[3].valueChanged.connect(
            lambda: self._sliderChanging(3, 3) 
        )

        self.sliders[4].valueChanged.connect(
            lambda: self._sliderChanging(4, 4) 
        )

        self.sliders[5].valueChanged.connect(
            self._combobox_slider_changing 
        ) 

        self.combo.currentTextChanged[str].connect(
            self._comboboxChanged
        )
        '''
        self._set_slider_initV()
        self.mesh_group.slider_sig.connect(self._mesh_slider_chaning)
        self.diffuse_group.slider_sig.connect(self._diffuse_slider_chaning)
        self.saveButton.clicked.connect(self.saveParam)
        self.loadButton.clicked.connect(self.loadParam)
        self.show()

        

    '''
    def _set_combobox(self, cb):
        numParams = self.pca_model.getnumParams()
        items = list(map(str, range(6,numParams)))
        cb.addItems(items)
        asixNum = int(cb.currentText()) - 1
        v = self.pca_model.getParamByAxis(asixNum) * (self.sliderMax - self.sliderMin)
        self.sliders[5].setValue(v)

    def _comboboxChanged(self, axis):
        axis = int(axis) - 1
        v = self.pca_model.getParamByAxis(axis) * (self.sliderMax - self.sliderMin)
        self.sliders[5].setValue(v)        

    def _combobox_slider_changing(self):
        axisNum = int(self.combo.currentText()) - 1
        self._sliderChanging(5, axisNum)
    def _sliderChanging(self, sliderNum, axisNum):
        v = self.sliders[sliderNum].value()
        v = (v + self.sliderMax) / (self.sliderMax - self.sliderMin)
        self.pca_model.sampleFace(v, axisNum)
        self.glwindow.updates_points()
    '''

    def _set_slider_initV(self):
        for ind, s in enumerate(self.mesh_group.sliders):
            v = self.pca_model.getFacePramByAxis(ind, "mesh")
            self.mesh_group.setSliderValue(v, ind)
        for ind, s in enumerate(self.diffuse_group.sliders):
            v = self.pca_model.getFacePramByAxis(ind, "diffuse")
            self.diffuse_group.setSliderValue(v, ind)
        
       
    def loadParam(self):
        for ind, s in enumerate(self.value):
            self.mesh_group.setSliderValue(s, ind)
            self.pca_model.samplePoint(s, ind)
        self.glwindow.updates_points()

    def saveParam(self):
        self.value = []
        for ind, s in enumerate(self.mesh_group.sliders):
            self.value.append(self.pca_model.getFacePramByAxis(ind, "mesh"))
 
    #TODO: Need to change the function, be more general, not only for diffuse
    @pyqtSlot(tuple)
    def _mesh_slider_chaning(self, axis_value):
        axis, value = axis_value
        self.pca_model.samplePoint(value, axis)
        self.glwindow.updates_points()
    
    @pyqtSlot(tuple)
    def _diffuse_slider_chaning(self, axis_value):
        axis, value = axis_value
        self.pca_model.sampleDiffuse(value, axis)
        self.glwindow.img = self.pca_model.diffuse
        self.glwindow.updates_diffuse()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape or event.key() == Qt.Key_Q:
            self.close()
    
   
    def closeEvent(self, event):
        self.glwindow.close()
        
        
