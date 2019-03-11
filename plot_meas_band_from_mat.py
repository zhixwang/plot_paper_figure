# -*- coding: utf-8 -*-
"""
Library for plotting 2D line
Created on Sat Jun  2 08:53:36 2018

@author: zxwan
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib import cm
import os
import scipy.io as sio
from scipy.interpolate import interp2d
import math
import sys


class plot_meas_band_from_mat:             # One class for one figure
    def create_fig(self):
        mpl.rcParams['pdf.fonttype'] = 42
        mpl.rcParams.update({'font.size': self.info['fontsize'],'font.family':self.info['fontname'],'font.weight':self.info['fontweight']})      #default: 24
        mpl.rcParams['axes.linewidth'] = 1.5
        # set tick width
        #mpl.rcParams['xtick.major.size'] = 20
        mpl.rcParams['xtick.major.width'] = 1.5
        #mpl.rcParams['xtick.minor.size'] = 10
        #mpl.rcParams['xtick.minor.width'] = 2
        mpl.rcParams['ytick.major.width'] = 1.5
        self.fig = plt.figure(figsize=(self.info['figwidth'],self.info['figheight']))
        self.ax = self.fig.gca()
        #self.ax = self.fig.add_subplot(111)
        self.showtime = 0.1       # image closes in 5 s

    def interpolate(self):
        print('Interpolation started')
        f_interp = interp2d(self.angs, self.f_selected, self.Data_print, kind='cubic')
        d_ang = (np.amax(self.angs) - np.amin(self.angs))/np.size(self.angs)    # delta_angle
        d_f = (np.amax(self.f_selected) - np.amin(self.f_selected))/np.size(self.f_selected)            # delta_freq
        angs_new = np.arange(np.amin(self.angs),np.amax(self.angs),d_ang*self.info['interp'])
        f_new = np.arange(np.amin(self.f_selected), np.amax(self.f_selected),d_f*self.info['interp'])
        Data_new = f_interp(angs_new,f_new)
        k_new = self.ang_to_k(angs_new,f_new)
        """
        k_new = np.zeros(shape = (np.size(f_new), np.size(angs_new)) )
        i = 0
        for angle in angs_new:
            k_new[:,i] = f_new*np.sin(angle*math.pi/180)
            i = i + 1
        """
        self.k = k_new
        self.f_selected = f_new
        self.Data_print = Data_new
        print('Interpolation done :)')


    def plot_band(self,*args,**kwargs):
        """
        default = {'cmap':'hot','antialiased':False,'edgecolor':'none','colorbar':False}
        for item in default:
            if item in kwargs:
                default[item] = kwargs[item]
        """
        for item in kwargs:
            if item in self.info:
                self.info[item] = kwargs[item]
        if self.info['interp'] == 1:
            print("No interpolation")
            #self.surf = self.ax.pcolor(self.k, self.f_selected, self.Data_print, cmap=default['cmap'],antialiased=default['antialiased'],edgecolor = default['edgecolor'],*args,**kwargs)
        else:
            self.interpolate()
            print("Interp activated")
        if self.info['reverse'] == True:
            self.k = self.k*(-1)
            print('k reversed!')
        self.surf = self.ax.pcolor(self.k, self.f_selected, self.Data_print, cmap=self.info['cmap'],antialiased=self.info['antialiased'],edgecolor = self.info['edgecolor'],*args,**kwargs)
        if (self.info['xlim'] != None):
            self.ax.set_xlim(self.info['xlim'])
        self.ax.set_ylim(self.info['ylim'])
        if len(self.info['clim']) == 2:
            self.surf.set_clim(self.info['clim'][0],self.info['clim'][1])
        if self.info['colorbar'] == True:
            self.fig.colorbar(self.surf)#, shrink=0.5, aspect=5)
    
    def show_figure(self,*args):
        self.fig.show()
        if (len(args) > 0):
            try:
                if float(args[0]) > 0:
                    self.showtime = float(args[0])
            except:
                pass
        plt.pause(self.showtime)            # show for n seconds, default:5


    def save_figure(self,foldername,filename,*args):
        self.fig.savefig(foldername + "/" + filename + r'.pdf')
        self.fig.savefig(foldername + "/" + filename + r'.png',dpi = 200)
        if (len(args) > 0):
            try:
                if float(args[0]) > 0:
                    self.showtime = float(args[0])
            except:
                pass
        self.show_figure()

    def ang_to_k(self,angs,f):      # generate k matrix
        k =  np.zeros(shape = (np.size(f), np.size(angs)) )
        i = 0
        for angle in angs:
            k[:,i] = np.squeeze(f*np.sin(angle*math.pi/180))       # change the dimension from [N,1] to N
            i = i+1       
        return k 

    # read data from the .mat file
    def read_data(self):
        self.data = sio.loadmat(self.info['folder'] + "/" + self.info['file'])             # data get from .mat file
        self.f_range = np.where((self.data['Norm_freq'] > self.info['f_min']) & (self.data['Norm_freq'] < self.info['f_max']))[0]
        self.f_selected = self.data['Norm_freq'][self.f_range]
        self.angs = self.data['angs'][0]
        self.k = self.data['k'][self.f_range,:]
        self.Data_print = self.data['Data'][self.f_range,:]
        print('Data reading finished :)')
        if self.info['zero'] != 0:          # shift the k
            self.angs = self.angs - self.info['zero']
            self.k = self.ang_to_k(self.angs,self.f_selected)
            """
            self.k = np.zeros(shape = (np.size(self.f_selected), np.size(self.angs)) )
            i = 0
            for angle in self.angs:
                self.k[:,i] = np.squeeze(self.f_selected*np.sin(angle*math.pi/180))       # change the dimension from [N,1] to N
                i = i+1
            """
            print('Gamma-point shifted :)')
        # select data in certain range, to minimize the output file size & replace 'neg', 'pos'
        idx = np.argmin(np.abs(self.angs))  # idx of the minimum element
        if self.info['xlim'] != None:
            buffer_k = 0.001
            if self.info['reverse'] == False:
                k_min = self.info['xlim'][0] - buffer_k
                k_max = self.info['xlim'][1] + buffer_k
            else:
                k_min = self.info['xlim'][1]*(-1) - buffer_k
                k_max = self.info['xlim'][0]*(-1) + buffer_k
            ang_max = np.arcsin(k_max/np.amin(self.f_selected))*180/math.pi
            ang_min = np.arcsin(k_min/np.amax(self.f_selected))*180/math.pi
            idx_min = np.argmin(np.abs(self.angs-ang_min))
            idx_max = np.argmin(np.abs(self.angs-ang_max))
            self.angs = self.angs[idx_min : idx_max+1]  # 0 deg included
            self.k = self.k[:,idx_min : idx_max+1] 
            self.Data_print = self.Data_print[:, idx_min : idx_max+1]              
        """
        if self.info['neg'] == True:
            self.angs = self.angs[0 : idx+2]  # 0 deg included
            self.k = self.k[:,0 : idx+2] 
            self.Data_print = self.Data_print[:,0 : idx+2]
            print('Draw the left part of the band only')
        elif self.info['pos'] == True:
            self.angs = self.angs[ idx-2: ]  # 0 deg included
            self.k = self.k[:, idx-2: ] 
            self.Data_print = self.Data_print[:, idx-2: ]
            print('Draw the right part of the band only')
        """




    def __init__(self,*args,**kwargs):
        default = {'reverse':False, 'zero':0,'title':"", 'clim':(),  \
                    'xlabel': "k$_{\parallel}$a/2$\pi$",'cmap':'hot','antialiased':False,'edgecolor':'none',    \
                    'colorbar':False,'fontsize':25, 'fontname':'Segoe UI','fontweight':'medium','ylabel': "Frequency, $\omega$a/2$\pi$c",   \
                    'folder':"", 'file':"",'xlim':None, 'ylim':None, 'figwidth': 8,'figheight':8,'interp':1, 'f_min': 0.310, 'f_max': 0.325}
        # 'reverse': if need to reverse k or not; 'zero': the real angle of Gamma point, zero=0 means no shift
        # abandoned function! replaced by xlim 'neg': draw only the left part of band (-inf to 0); 'pos': draw only the right part of band (0 to inf);
        for item in default:
            if item in kwargs:
                default[item] = kwargs[item]
        default['ylim'] = [default['f_min'], default['f_max']]
        if kwargs['ylim'] !=  None:
            default['ylim'] = kwargs['ylim']
        self.info = default
        # Error treatment
        if (self.info['folder'] == "") or (self.info['file'] == ""):
            print("Error: folder/file name incomplete! :(")
            sys.exit()
        """
        if (self.info['neg'] == True) and (self.info['pos'] == True):
            print("Error: Draw left & right parts of the band confliting! :(")
            sys.exit()
        """
        self.create_fig()
        self.ax.set(title=default['title'], xlabel=default['xlabel'], ylabel=default['ylabel'])
        self.read_data()
    





