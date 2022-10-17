from types import new_class
from PyQt5.QtGui import (QVector3D, QMatrix4x4, QQuaternion)
from math import cos, sin

class Camera:
    def __init__(self, width, height):

        self.__eyePt = QVector3D(0.0, 0.0, 0.5)
        self.__viewPt = QVector3D(0.0, 0.0, 0.0)
        self.fov = 60
        self.nearCP = 0.1
        self.farCP = 1000.0
        self.up = QVector3D(0.0, 1.0, 0.0)
        self.forward = (self.__viewPt - self.__eyePt).normalized()
        #self.right = (self.__viewPt - self.__eyePt).normalized()
        self.compute_up_for_right()

        self.width = width
        self.height = height

        self.viewMat = QMatrix4x4()
        self.viewMat.lookAt(self.__eyePt, self.__viewPt, QVector3D(self.up))

        self.projMat = QMatrix4x4()
        self.projMat.perspective(self.fov, self.width / self.height, self.nearCP, self.farCP)

    def _setViewMatrix(self):
        self.viewMat.setToIdentity()
        self.viewMat.lookAt(self.__eyePt, self.__viewPt, QVector3D(self.up))

    def _set_forward_vector(self):
        self.forward = (self.__viewPt - self.__eyePt).normalized()
        self.compute_up_for_right()

    def _setProjectMatrix(self):
        self.projMat.setToIdentity()
        self.projMat.perspective(self.fov, self.width / self.height, self.nearCP, self.farCP)
    
    def set_eye_pos(self, ep):
        self.__eyePt = ep
        self._set_forward_vector()
        self._setViewMatrix()
    
    def set_view_pos(self, vp):
        self.__viewPt = vp
        self._set_forward_vector()
        self._setViewMatrix()

    def rotate_cam(self, dx, dy):
        #Maybe put this into a model
        thetax =  dx * 0.01
        thetay =  dy * 0.01
        qx = QQuaternion(cos(thetax / 2), self.up * sin(thetax / 2))
        new_cam_pos = qx.rotatedVector(self.__eyePt)
        
        self.set_eye_pos(new_cam_pos)
    def get_cam_pos(self):
        return self.__eyePt
    def compute_up_for_right(self):
        self.right = QVector3D.crossProduct(self.forward, self.up).normalized()
        self.up = QVector3D.crossProduct(self.right, self.forward).normalized()