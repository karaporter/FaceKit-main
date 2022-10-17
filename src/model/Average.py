from Mesh import Mesh
import src.controller.MeshIO as mio
import src.controller.NumpyIO as nio

from glob import glob
from copy import deepcopy
import os
import numpy as np
import csv


class Average:
    def __init__(self, attribute = None, obj_dir = './data/faces', npy_dir = './data/points',
                 np_v_dir = './faces/points', np_vt_dir = './data/jpgs'):
        self.attribute = attribute
        self.numpy_dir_v = np_v_dir
        self.npy_faces_v = npy_dir
        self.numpy_dir_vt = np_vt_dir
        
        #set file paths
        self.objs = glob(os.path.join(obj_dir, '*.OBJ'), recursive=True)
        self.faces_v = glob(os.path.join(self.numpy_dir_v, '*.npy'), recursive=True)
        
        self.eig_v = nio.readFile(os.path.join(self.npy_faces_v, 'eigenVector.npy'))
        self.mean_face_v = nio.readFile(os.path.join(self.npy_faces_v, 'mean.npy'))
        
        self.faces_vt = glob(os.path.join(self.numpy_dir_vt, '*.jpg'), recursive=True)
        self.file_name = [os.path.basename(file).split('.')[0] for file in self.objs]
        
        #find pca of files
        #points = self.calcNumpyFaces()

        print("this is working")

      
    def calcNumpyFaces(self):
        #read files and gather vertices
        for f in self.objs:
            
            m = Mesh()
            mio.readMesh(m, f)

            #place vertices into array
            v = np.array(m.vertices).flatten().reshape(-1,1)

            mean_adj = v - self.mean_face_v

            param = np.dot(self.eig_v.T, mean_adj) 

            filename = os.path.basename(f).split('.')[0]
            filename = './faces/points/' + filename + "_p.npy"
            
            with open(filename, 'wb') as i:
                np.save(i, v)
            

    def calc_avg_attr(self, attribute):
        attr_files = self.getFiles(attribute)
        
        self.attr_npy = []
        for f in attr_files:
            self.attr_npy.append(nio.readFile(f))
            
        self.attr_npy = np.array(self.attr_npy).T.reshape(-1, len(attr_files))
        
        self.meanAttr = np.mean(self.attr_npy, axis=1).reshape(-1, 1)

        return self.meanAttr
        
        
    def getFiles(self, attributeType, file_dir='./faces/'):
        filepath = os.path.join(file_dir, 'facescsv.csv')

        rows = []
        with open(filepath, 'r') as file:
            csvreader = csv.reader(file, delimiter=',')
            header = next(csvreader)
            for row in csvreader:
                rows.append(row)

        if attributeType == "females":
            attr_list = [i[0] for i in rows if i[1] == "F"]
        elif attributeType == "males":
            attr_list = [i[0] for i in rows if i[1] == "M"]


        f_base = [os.path.basename(i).split('.')[0] for i in attr_list]
        npy_attr = [j for i in f_base for j in self.faces_v if i == os.path.basename(j).split('.')[0]]
        return npy_attr
 


        file.close()

        

