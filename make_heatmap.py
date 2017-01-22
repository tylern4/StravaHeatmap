#!/usr/bin/env python
from download_data import *
import pandas as pd
import gmplot
try:
	import cPickle as pickle
except:
	import pickle

def heatmap():
	map_html = 'heatmap.html'

	all_act = get_data()
	print("Making heatmap")
	heatmap = pd.concat(all_act, ignore_index=False)

	center_lat, center_lon = heatmap['lat'].mode()[0], heatmap['lon'].mode()[0]
	heatmap = heatmap[heatmap['lat'] <= (center_lat+0.01*center_lat)]
	heatmap = heatmap[heatmap['lat'] >= (center_lat-0.01*center_lat)]
	heatmap = heatmap[heatmap['lon'] >= (center_lon+0.01*center_lon)]
	heatmap = heatmap[heatmap['lon'] <= (center_lon-0.01*center_lon)]
	center_lat, center_lon = heatmap['lat'].mean(), heatmap['lon'].mean()

	gmap = gmplot.GoogleMapPlotter(center_lat, center_lon, 13)
	gmap.heatmap(heatmap['lat'],heatmap['lon'])


if __name__ == '__main__':

	try:
		heatmap()
		print("Done")
	except:
		print("Error in making heatmap")