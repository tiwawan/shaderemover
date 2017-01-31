import matplotlib
import sys
matplotlib.rcParams['backend.qt5'] = 'PyQt5'
matplotlib.use('Qt5Agg')

import numpy as np
import scipy.misc as misc
from skimage import transform

import matplotlib.pyplot as plt

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, qApp, QFileDialog
from PyQt5.QtCore import Qt

from PIL import Image
from PIL import ImageOps

from separateTVAndL1 import *

class Main(QMainWindow):
    
    def __init__(self):
        super(Main, self).__init__()
        self.is_opened = False
        self.image = None
        self.initUI()

    def initUI(self):
        # toolbars
        act_open = QAction("Open", self)
        act_open.triggered.connect(self.openFile)

        act_save = QAction("Save", self)
        act_save.triggered.connect(self.saveFile)

        self.toolbar = self.addToolBar('File')
        self.toolbar.addAction(act_open)
        self.toolbar.addAction(act_save)

        # pyplot figure
        self.fig = plt.figure()
        canvas = FigureCanvas(self.fig)
        self.ax = self.fig.add_subplot(111)
        self.ax.get_xaxis().set_visible(False)
        self.ax.get_yaxis().set_visible(False)

        self.setCentralWidget(canvas)
        self.show()
        
    def openFile(self):
        filepath = QFileDialog.getOpenFileName(self, 'Open file', './')
        if filepath[0]:
            pass
        else:
            print("No file selected")
            return

        try:
            im_raw = Image.open(filepath[0])
        except:
            print("Cannot Open File")
            return

        if im_raw == None:
            print("Cannot Open File")
            return

        gray_img = ImageOps.grayscale(im_raw)
        gray_img = np.array(gray_img)
        gray_img = gray_img / 255.0

        S = removeShade(gray_img)

        self.ax.imshow(S, cmap="gray", vmin=0, vmax=1)
        self.fig.canvas.draw()
        self.is_opened = True
        print("Completed")
        

    def saveFile(self):
        pass



def removeShade(im_orig):
    w_orig = im_orig.shape[1]
    h_orig = im_orig.shape[0]

    im_resize = transform.resize(im_orig, (100,100))
    
    L, S = separateTVAndL1(im_resize, 0.2)

    L_origsize = transform.resize(L, (h_orig, w_orig))

    S_origsize = im_orig - L_origsize

    minS = np.min(S_origsize)

    S_origsize = S_origsize - minS
    S_origsize = S_origsize / (-minS)
    #S_origsize[S_origsize<0] = 0
    
    return S_origsize
    


if __name__ == "__main__":
    
    app = QApplication(sys.argv)
    m = Main()
    app.exec_()
    """
    im_raw = Image.open("../experimental/looseleaf_ss.jpg")
    gray_img = ImageOps.grayscale(im_raw)
    gray_img = np.array(gray_img)
    gray_img = gray_img / 255.0

    S = removeShade(gray_img)

    plt.imshow(S, cmap="gray", vmin=0, vmax=1)
    plt.colorbar()
    plt.show()
    """











    
    
