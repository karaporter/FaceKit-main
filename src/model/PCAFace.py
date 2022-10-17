from Mesh import Mesh
import src.controller.MeshIO as mio
import src.controller.NumpyIO as nio
from Average import Average

from glob import glob
import os
import numpy as np
from math import sqrt
from PyQt5.QtGui import (QImage)
import csv

#TODO: Clean up code.
class PCAFace:
    def __init__(self, objDir = './data/refObj/', ImgDir = './data/tempImg',  pointMatrix = './data/points/',   diffuseMatrix = './data/diffuse/', dataObjDir = './data/obj',
                 faceDir = './faces/param', faceDifDir = './faces/diffuse', facePointDir = './faces/points'):
        self.obj_dir = objDir
        self.point_matrix_dir = pointMatrix 
        self.diffuse_matrix_dir = diffuseMatrix
        self.data_obj_dir = dataObjDir
        self.img_dir = ImgDir
        self.faceTest_dir = faceDir
        self.faceTest_dif_dir = faceDifDir
        self.face_point_test_dir = facePointDir

        objs = glob(os.path.join(self.obj_dir, '*.obj'))

        
        #read One mesh for faces
        m = Mesh()
        mio.readMesh(m, objs[0])

        self.avg = Average()

        
        #--------------------------------------------------------------------------------------
        
        self.diffuse_eigenV = nio.readFile(os.path.join(self.diffuse_matrix_dir, 'eigenVector.npy'))
        #48 * 48: each column is a face
        self.diffuse_params = nio.readFile(os.path.join(self.diffuse_matrix_dir, 'param.npy'))
        self.mean_face_vt = nio.readFile(os.path.join(self.diffuse_matrix_dir, 'mean.npy'))
        self.test_face_vt = nio.readFile(os.path.join(self.faceTest_dif_dir, 'Head_M_12.npy'))
        #print("self.mean_face_vt:", np.shape(self.mean_face_vt))
        #print("self.test_face_vt:", np.shape(self.test_face_vt))
        
        w = int(sqrt(self.mean_face_vt.shape[0] / 3))
        mean_diffuse = self.mean_face_vt.reshape((w, w, 3)) * 255
        mean_diffuse = mean_diffuse.astype('uint8')
        self.diffuse =  QImage(mean_diffuse.data, mean_diffuse.shape[1], mean_diffuse.shape[0], mean_diffuse.strides[0], QImage.Format_RGB888).mirrored()
        self.diffuseParam = np.dot(self.diffuse_eigenV.T, (self.mean_face_vt - self.mean_face_vt))
        """
        w = int(sqrt(self.test_face_vt.shape[0] / 3))
        mean_diffuse = self.test_face_vt.reshape((w, w, 3)) * 255
        mean_diffuse = mean_diffuse.astype('uint8')
        self.diffuse =  QImage(mean_diffuse.data, mean_diffuse.shape[1], mean_diffuse.shape[0], mean_diffuse.strides[0], QImage.Format_RGB888).mirrored()
        self.diffuseParam = np.dot(self.diffuse_eigenV.T, (self.test_face_vt - self.mean_face_vt))
        """
        
        
        #--------------------------------------------------------------------------------------
        self.point_eigenV = nio.readFile(os.path.join(self.point_matrix_dir, 'eigenVector.npy'))    #[37000,48]
        self.point_params = nio.readFile(os.path.join(self.point_matrix_dir, 'param.npy'))          #[48,48]
        self.mean_face_v =  nio.readFile(os.path.join(self.point_matrix_dir, 'mean.npy'))           #[37000,1]
        
        self.pointParam = nio.readFile(os.path.join(self.faceTest_dir, 'Head_M_12.npy'))            #[48,1]
        self.test_face_v = nio.readFile(os.path.join(self.face_point_test_dir, 'Head_M_12_p.npy'))     #[37000,1]

        print("test_face:", np.shape(self.test_face_v))
        print("pointparam:", np.shape(self.pointParam))
        
        #self.mean_attr_v = self.avg.calc_avg_attr("females")
        #print(self.mean_attr_v[0])

        #self.pointParam = np.dot(self.point_eigenV.T, (self.mean_face_v - self.mean_face_v))        #[48,1]
        #self.pointParam = np.dot(self.point_eigenV.T, (self.test_face_v - self.mean_face_v))
        #self.pointParam = np.dot(self.point_eigenV.T, (self.mean_attr_v - self.mean_face_v))

       
        #self.mesh = Mesh(self.mean_face_v.reshape(-1, 3).tolist(), f = m.faces, vt = m.texCoord)
        self.mesh = Mesh(self.test_face_v.reshape(-1, 3).tolist(), f = m.faces, vt = m.texCoord)
        #self.mesh = Mesh(self.mean_attr_v.reshape(-1, 3).tolist(), f = m.faces, vt = m.texCoord)

    
        
    """
    def getParamByAxis(self, axis):
        maxv = self.maxVal[axis]
        minv = self.minVal[axis]
        return (self.pointParam[axis][0] / (maxv - minv))
    """
    def getFacePramByAxis(self, axis, faceComponent):
        params = None 
        data_pram = None
        if faceComponent == "mesh":
            params = self.point_params
            data_param = self.pointParam
        elif faceComponent == "diffuse":
            params = self.diffuse_params
            data_param = self.diffuseParam
        maxV = np.max(params[axis])
        minV = np.min(params[axis])
        v = data_param.flatten()[axis]
        x = (v - minV) / (maxV - minV)
        #print("v:", v)
        #print("x:", x)
        return x
        
        

    def samplePoint(self, value, axis):
        maxVal = np.amax(self.point_params, axis = 1)[axis]
        minVal = np.amin(self.point_params, axis = 1)[axis]
        v = value * (maxVal - minVal) + minVal
        # clipValue = max(min(value * (maxv - minv) + minv, maxv), minv) 
        self.pointParam[axis][0] = v
        newpoints = self.mean_face_v + np.dot(self.point_eigenV, self.pointParam)
        self.mesh.updateVert(newpoints.reshape(-1,3).tolist())


    def getnumParams(self):
        return (self.point_params.shape[0] + 1)

    def sampleDiffuse(self, value, axis):
        maxVal = np.amax(self.diffuse_params, axis = 1)[axis]
        minVal = np.amin(self.diffuse_params, axis = 1)[axis]
        self.diffuseParam[axis][0] = value * (maxVal - minVal) + minVal

        newtexture = self.mean_face_vt + np.dot(self.diffuse_eigenV, self.diffuseParam)
        w = int(sqrt(newtexture.shape[0] / 3))
        mean_diffuse = newtexture.reshape((w, w, 3)) * 255.0
        mean_diffuse = mean_diffuse.astype('uint8')
        self.diffuse =  QImage(mean_diffuse.data, mean_diffuse.shape[1], mean_diffuse.shape[0], mean_diffuse.strides[0], QImage.Format_RGB888).mirrored()
         

      
