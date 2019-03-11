# -*- coding: utf-8 -*-
"""
Library for plotting 2D line
Created on Sat Jun  2 08:53:36 2018

@author: zxwan
"""

import matplotlib.pyplot as plt
import matplotlib as mpl
import os 

class plot_2D_line:             # One class for one figure
    def create_fig(self):
        mpl.rcParams['pdf.fonttype'] = 42
        mpl.rcParams.update({'font.size': self.default['fontsize'],'font.family':self.default['fontname'],'font.weight':self.default['fontweight']})
        mpl.rcParams['axes.linewidth'] = 1.5
        # set tick width
        #mpl.rcParams['xtick.major.size'] = 20
        mpl.rcParams['xtick.major.width'] = 1.5
        #mpl.rcParams['xtick.minor.size'] = 10
        #mpl.rcParams['xtick.minor.width'] = 2
        mpl.rcParams['ytick.major.width'] = 1.5
        self.fig = plt.figure(figsize=(self.default['figwidth'],self.default['figheight']))
        self.ax = self.fig.add_subplot(111)
        self.showtime = 0.1       # image closes in 5 s

    def plot_curve(self,xdata,ydata,*args,**kwargs):
        self.ax.plot(xdata,ydata,*args,**kwargs)
        if ('label' in kwargs):
            self.ax.legend(loc='best',frameon=False)
        if ('xlim' in kwargs):
            self.default['xlim'] = kwargs['xlim']
        if ('ylim' in kwargs):
            self.default['ylim'] = kwargs['ylim']
        if (self.default['xlim'] != None):
            self.ax.set_xlim(self.default['xlim'])
        if (self.default['ylim'] != None):
            self.ax.set_ylim(self.default['ylim'])
        if (self.default['xscale'] == 'log'):
            plt.xscale('log')
        if (self.default['yscale'] == 'log'):
            plt.yscale('log')            
    
    def show_figure(self,*args):
        self.fig.show()
        if (len(args) > 0):
            try:
                if float(args[0]) > 0:
                    self.showtime = float(args[0])
            except:
                pass
        plt.pause(self.showtime)            # show for n s, default:5


    def save_figure(self,*args):    # if input two keywords: folder, filename; if only input one keyword: filename (current folder as default)
        if len(args) >=2:
            foldername = args[0]
            filename = args[1]
            self.fig.savefig(foldername + "/" + filename + r'.eps')
            self.fig.savefig(foldername + "/" + filename + r'.pdf')
            self.fig.savefig(foldername + "/" + filename + r'.png',dpi = 150)
        elif len(args) == 1:
            filename = args[0]
            self.fig.savefig(filename + r'.eps')
            self.fig.savefig(filename + r'.pdf')
            self.fig.savefig(filename + r'.png',dpi = 150)
        else:
            print('Input file information insufficient!')
            return
        if (len(args) > 0):
            try:
                if float(args[0]) > 0:
                    self.showtime = float(args[0])
            except:
                pass
        self.show_figure()


    def __init__(self,*args,**kwargs):
        self.default = {'title':"", 'xlabel':"",'ylabel':"", 'xlim':None, 'ylim': None, 'figwidth': 9, 'figheight':8, \
        'fontsize':20,'fontname':'Segoe UI','fontweight':'medium','xscale':'linear','yscale':'linear'}
        """
        self.title = 
        self.xlabel = ""
        self.ylabel = ""
        self.xlim = None
        self.ylim = None
        self.figwidth = 9
        self.figheight = 8
        """
        if len(args) >= 2:                      # first two arguments are supposed to be figure size
            self.tpl_size_txt = args[0:2]
        try:
            self.tpl_fig_size = [float(x) for x in self.tpl_size_txt]
            if (min(self.tpl_fig_size) > 0):         # figure size
                self.default['figwidth'] = self.tpl_fig_size[0]
                self.default['figheight']  = self.tpl_fig_size[1]
        except:
            pass
        for item in self.default:
            if item in kwargs:
                self.default[item] = kwargs[item]

        self.create_fig()
        self.ax.set(title=self.default['title'], xlabel=self.default['xlabel'], ylabel=self.default['ylabel'])

    





