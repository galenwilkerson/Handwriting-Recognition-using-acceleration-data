'''
run like:
> python2.7 -u test_plot_hists.py >& out &
'''

import plot_hists

filename = "../data/MarieTherese_jul31_and_Aug07_all.pkl"

plot_hists.plot_hists(filename)
