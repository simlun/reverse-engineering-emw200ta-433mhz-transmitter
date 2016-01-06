Reverse Engineering the EMW200TA 433 MHz Transmitter
====================================================

This repository documents my work of reverse engineering an RF transmitter so I can control the receivers with a transmitter I build myself.

![Transmitters and receivers](img/transmitter_and_receivers.jpg)


Hello World
-----------

I captured the signal of pressing one button with my Rigol DS1052E oscilloscope:

![Oscilloscope screenshot](img/helloworld.png)

Then I saved it as CSV and using [Jupyter Notebook](http://jupyter.readthedocs.org) I parsed and manipulated the captured data. First let's compare the [Matplotlib](http://matplotlib.org) plot with the above scope screenshot:

![Plotted CSV data](img/helloworld_plot.png)

Now let's get rid of that noise:

![Clean plot](img/helloworld_clean_plot.png)

See the [HTML version](helloworld.html) of the [notebook](helloworld.ipnb) for the source code of generating the above plots.




Prerequisites
-------------

* Install [Anaconda](https://www.continuum.io/downloads) (v2.7.1 was used)
* Open the notebook with `jupyter notebook`


Documentation
-------------

* https://fetzerch.github.io/2014/11/15/reveng433/
* http://mightydevices.com/?p=300
* https://www.youtube.com/playlist?list=PLRJx8WOUx5Xd3_dgw5xRmABUd8MWdsA_C
* http://nbviewer.ipython.org/github/twistedhardware/mltutorial/blob/master/notebooks/IPython-Tutorial/
