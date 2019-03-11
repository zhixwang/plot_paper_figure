This is a Python3 library for plotting figures, especially for 1D-lines.

Without abandant settings, and get paper quality figures.

Example:

~~~~
from figure_library.plot_2D_line import plot_2D_line as p2l

fig1 = p2l(figheight = 9, figwidth = 8, xlabel = 'Xlabel',xlim=xlim, ylabel = 'Ylabel', fontsize = 20, fontname = 'Segoe UI')
~~~~

or

~~~~
fig1 = p2l(8,8,xlabel ='Xlabel',ylabel='Ylabel')
~~~~

and later:

~~~~
fig1.plot_curve(xdata,ydata,color = '#1f77b4', markersize = 10, linestyle = '--', marker = 'X', label = 'Curve 1')
fig1.show_figure(5)							# Show the figure for 5s and then it disappears
fig1.save_figure(folder,filename)			# Save as .png, .pdf and .eps
~~~~
