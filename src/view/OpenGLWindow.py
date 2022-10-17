from PyQt5.QtWidgets import (QOpenGLWidget)
from PyQt5.QtGui import (QOpenGLShaderProgram, QOpenGLShader,
    QOpenGLContext, QOpenGLVertexArrayObject, QOpenGLBuffer, QOpenGLTexture)
from PyQt5.QtCore import(Qt)

import src.controller.MeshIO as mio
import src.controller.NumpyIO as nio
from src.model.Camera import Camera

import array
import os, array
import numpy as np
from PyQt5.QtGui import (QVector3D, QMatrix4x4)


class OpenGLWindow(QOpenGLWidget):

    def __init__(self, parent=None):
        super(OpenGLWindow, self).__init__(parent)


        # Set Window Properties
        self.bgColor = [0.1, 0.1, 0.12, 1.0]
        initH = self.height()
        initW = self.width()
        ratio = initH / initW
        self.setMinimumSize(initW, initH)

        # Set Mouse 
        self.mouse_pos = None

        #ALL Shader Paramters
        self.modelMat_unifLoc = -1
        self.viewMat_unifLoc = -1
        self.projMat_unifLoc = -1
        self.vsName = None
        self.fsName = None
        self.shaderProg = None

        #All OpenGL Parameters
        self.camera = Camera(initW, initH)
        self.pos_attribLoc = -1
        self.norm_attribLoc = -1
        self.text_attribLoc = -1
        self.vao = QOpenGLVertexArrayObject()
        self.vbo_vert = QOpenGLBuffer()
        self.vbo_norm = QOpenGLBuffer()
        self.vbo_texCoord = QOpenGLBuffer()
        self.vert_count = 0

        #TODO: Change it later. Want to initialize mesh when click some buttons.
        self.mesh = None
        self.texture = QOpenGLTexture(QOpenGLTexture.Target2D)
        self.img = None


       

    def initializeGL(self):
        f = QOpenGLContext.currentContext().versionFunctions()
        f.initializeOpenGLFunctions()

        self._initShaders()
        self._initVertexBuffers()



    def paintGL(self):
        self.makeCurrent()
        f = QOpenGLContext.currentContext().versionFunctions()
        f.initializeOpenGLFunctions()

        f.glEnable(f.GL_DEPTH_TEST);  

        f.glClearColor(self.bgColor[0], self.bgColor[1], self.bgColor[2], self.bgColor[3])
        f.glClear(f.GL_COLOR_BUFFER_BIT | f.GL_DEPTH_BUFFER_BIT)

        if self.vao.isCreated():
            self.shaderProg.bind()
            self.shaderProg.setUniformValue(self.viewMat_unifLoc, self.camera.viewMat)
            self.shaderProg.setUniformValue(self.modelMat_unifLoc, QMatrix4x4())
            self.shaderProg.setUniformValue(self.projMat_unifLoc, self.camera.projMat)
            self.shaderProg.setUniformValue(self.camPos_unifLoc, self.camera.get_cam_pos())
            self.texture.bind()
            
        self.vao.bind()
        f.glDrawArrays(f.GL_TRIANGLES, 0, self.vert_count * 3 )
        self.vao.release()
        self.doneCurrent() 



    def resizeGL(self, width, height):
        self.makeCurrent()
        f = QOpenGLContext.currentContext().versionFunctions()



    def _initShaders(self, vsName="shader/vs.glsl", fsName="shader/fs.glsl"):
        self.makeCurrent()  # Called when in custom function versus Qt's.

        print("OpenGLView.initShaders()")


        self.vsName = vsName
        self.fsName = fsName

        self.shaderProg = QOpenGLShaderProgram(self)

        if self.shaderProg.addShaderFromSourceFile(QOpenGLShader.Vertex, self.vsName):
            print("\tLoaded vertex shader.")
        if self.shaderProg.addShaderFromSourceFile(QOpenGLShader.Fragment, self.fsName):
            print("\tLoaded fragment shader.")
        if self.shaderProg.link():
            print("\tLinked shader program.")
        print(self.shaderProg.log())

        self.modelMat_unifLoc = self.shaderProg.uniformLocation("model_mat")
        if self.modelMat_unifLoc == -1:
            print("\tERROR: Cannot find shader uniform 'modelMat.'")
        self.viewMat_unifLoc = self.shaderProg.uniformLocation("view_mat")
        if self.viewMat_unifLoc == -1:
            print("\tERROR: Cannot find shader uniform 'viewMat.'")
        self.projMat_unifLoc = self.shaderProg.uniformLocation("proj_mat")
        if self.projMat_unifLoc == -1:
            print("\tERROR: Cannot find shader uniform 'projMat.'")


        self.camPos_unifLoc = self.shaderProg.uniformLocation("camera_pos")
        if self.projMat_unifLoc == -1:
            print("\tERROR: Cannot find shader uniform 'camera_pos.'")

        self.doneCurrent() 



    def _initVertexBuffers(self) -> None:
        self.makeCurrent()
        f = QOpenGLContext.currentContext().versionFunctions()
        
        

       
        if not self.vao.isCreated():
            self.vao.create()
        if self.vao.isCreated():
            self.vao.bind()

        if self.mesh is None:        
            vertices = array.array('f',[ -0.5, -0.5, 0.0,
                                          0.5, -0.5, 0.0,
                                          0.0,  0.5, 0.0])
            normals = array.array('f',[ 0.0, 0.0, 1.0,
                                        0.0, 0.0, 1.0,
                                        0.0, 0.0, 1.0])
            self.vert_count = 3
            self.camera.set_eye_pos(QVector3D(0.0, 0.0, 2.0))
        else:
            vertices = self.mesh.get_vertex()
            normals = self.mesh.get_normal()
            texCoord = self.mesh.get_texCoord()
            # TODO: Need move camera code to camera module
            self.vert_count = len(vertices) / 3
            lookat_pos = QVector3D(self.mesh.center[0], self.mesh.center[1], self.mesh.center[2])
            self.camera.set_view_pos(lookat_pos)
            zmax = self.mesh.bbox[5]
            eyePt = lookat_pos + QVector3D(0.0, 0.0, zmax * 3)
            self.camera.set_eye_pos(eyePt)
            
        self.shaderProg.bind()
        #----------------------------------------------- 
        self.vbo_vert.create()
        self.vbo_vert.setUsagePattern(QOpenGLBuffer.DynamicDraw)
        self.vbo_vert.bind()
        self.vbo_vert.allocate(vertices, self.vert_count * 3 * vertices.itemsize)
        self.pos_attribLoc = self.shaderProg.attributeLocation("vp")
        if self.pos_attribLoc == -1:
            print("\tERROR: Cannot find vertex attribute location.")
        self.shaderProg.enableAttributeArray(self.pos_attribLoc)
        self.shaderProg.setAttributeBuffer(self.pos_attribLoc, f.GL_FLOAT, 0, 3)

        #----------------------------------------------- 
        self.vbo_norm.create()
        self.vbo_norm.setUsagePattern(QOpenGLBuffer.DynamicDraw)
        self.vbo_norm.bind()
        self.vbo_norm.allocate(normals, self.vert_count * 3 * normals.itemsize)
        self.norm_attribLoc = self.shaderProg.attributeLocation("vn")
        if self.norm_attribLoc == -1:
            print("\tERROR: Cannot find normal attribute location.")
        self.shaderProg.enableAttributeArray(self.norm_attribLoc)
        self.shaderProg.setAttributeBuffer(self.norm_attribLoc, f.GL_FLOAT, 0, 3)
        

        #----------------------------------------------- 
        self.vbo_texCoord.create()
        self.vbo_texCoord.setUsagePattern(QOpenGLBuffer.DynamicDraw)
        self.vbo_texCoord.bind()
        self.vbo_texCoord.allocate(texCoord, self.vert_count * 2 * texCoord.itemsize)
        self.text_attribLoc = self.shaderProg.attributeLocation("vt")
        if self.text_attribLoc == -1:
            print("\tERROR: Cannot find normal attribute location.")
        self.shaderProg.enableAttributeArray(self.text_attribLoc)
        self.shaderProg.setAttributeBuffer(self.text_attribLoc, f.GL_FLOAT, 0, 2)
     

        #-----------------------------------------------
        self.texture.create()
        self.texture.bind()
        self.texture.setSize(self.img.width(), self.img.height(), self.img.depth())
        self.texture.setData(self.img)
        self.texture.setMinMagFilters(QOpenGLTexture.Linear, QOpenGLTexture.Linear)
        self.texture.setWrapMode(QOpenGLTexture.ClampToBorder)


        self.vbo_vert.release()
        self.vbo_norm.release()
        self.vbo_texCoord.release()
        self.shaderProg.release()
        self.doneCurrent()

    def updates_points(self):
        self.makeCurrent()
        f = QOpenGLContext.currentContext().versionFunctions()
        self.vbo_vert.bind()
        vertices = self.mesh.get_vertex()

        # f.glBufferSubData(f.GL_ARRAY_BUFFER, 0, self.vert_count * 3 * vertices.itemsize, vertices)
        self.vbo_vert.write(0, vertices, self.vert_count * 3 * vertices.itemsize) 
        self.vbo_vert.release()


        self.update()

        self.doneCurrent()
    
    def updates_diffuse(self):
        self.makeCurrent()



        self.texture.destroy()
        self.texture.setSize(self.img.width(), self.img.height(), self.img.depth())
        self.texture.setData(self.img)
        self.texture.setMinMagFilters(QOpenGLTexture.Linear, QOpenGLTexture.Linear)
        self.texture.setWrapMode(QOpenGLTexture.ClampToBorder)
        
        self.texture.release()
       
        self.update()
        self.doneCurrent()



    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.mouse_pos = event.pos()
            # self.leftDown = True
        elif event.button() == Qt.MiddleButton:
            print("middle")
            # self.middleDown = True
        elif event.button() == Qt.RightButton:
            # self.rightDown = True
            print("right")

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            offset = (self.mouse_pos - event.pos()) 
            self.camera.rotate_cam(offset.x(), offset.y())
            self.mouse_pos = event.pos()
            self.update()


    def closeEvent(self, event):
        self.makeCurrent()
        self.close()
