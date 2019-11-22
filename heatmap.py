from scipy.spatial.distance import pdist
from scipy.cluster.hierarchy import linkage, dendrogram
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

import pandas as pnd

def plotHeatmap(table, 
		cmap="Reds", 
		distance_metric="correlation", 
		linkage_method="complete", 
		show_column_labels = False, 
		show_row_labels = False, 
		row_clustering = True,
		column_clustering = True,
		vmin = None,
		vmax = None,
		symmetric_color_scale = False,
		symmetry_point = 0,
		ax = None):
	"""
		Function that plots a two dimensional matrix as clustered heatmap. 
		Sorting of rows and columns is done by hierarchical clustering.

		args:
			table: pandas.DataFrame
				Two dimensional array containing numerical values to be clustered.
		kwargs:
			cmap: str
				Colormap used to produce color scale.
			distance_metric: str
				Distance metric used to determine distance between two vectors.
				The distance function can be either of 'braycurtis', 'canberra',
				'chebyshev', 'cityblock', 'correlation', 'cosine', 'dice', 'euclidean',
				'hamming', 'jaccard', 'jensenshannon', 'kulsinski', 'mahalanobis',
				'matching', 'minkowski', 'rogerstanimoto', 'russellrao', 'seuclidean',
				'sokalmichener', 'sokalsneath', 'sqeuclidean', 'yule'.
			linkage_method: str
				methods for calculating the distance between the newly formed cluster u 
				and each v. Possible methods are, 'single', 'complete', 'average',
				'weighted', and 'centroid'
			show_column_labels: bool
				If true, show labels of columns, as defined in table.
			show_row_labels: bool
				If true, show labels of rows, as defined in table
			row_clustering: bool
				If true, the rows a clustered according to distance_metric, and
				linkage_method.
			column_clustering; bool
				If true, the columns are clustered according to distance:metric, and
				linkage_method.
			vmin: float
				Minimal value of data_table, that has a color representation.
			vmax: float
				Maximal value of data_table, that has a color representation.
			symmetric_color_scale: bool
				If true, vmin, and vmax will be set to have equal distance from symmetry
				point
			symmetry_point: float
				Only used, when symmetric_color_scale is true. If symmetric_color_scale is
				true, and symmetry_point is not set, it defaults to zero.
			ax: matplotlib.axes.Axes
				Axes instance on which to plot heatmap.
				
	"""
	ax = ax if ax is not None else plt.gca()

	# Sort column names
	column_names_reordered = list(table.columns)
	if(column_clustering):
		distance_matrix = pdist(table.T, metric=distance_metric)
		linkage_matrix = linkage(distance_matrix, metric=distance_metric, method=linkage_method)
		dendrogram_dict = dendrogram(linkage_matrix, no_plot=True)
	
		leaves = dendrogram_dict["leaves"]
	
		column_names = list(table.columns)
		column_names_reordered = [ column_names[i] for i in leaves ]
	
	# Sort row names
	row_names_reordered = list(table.index)
	if(row_clustering):
		distance_matrix = pdist(table, metric=distance_metric)
		linkage_matrix = linkage(distance_matrix, metric=distance_metric, method=linkage_method)
		dendrogram_dict = dendrogram(linkage_matrix, no_plot=True)
	
		leaves = dendrogram_dict["leaves"]
	
		row_names = list(table.index)
		row_names_reordered = [ row_names[i] for i in leaves ]

	# Override vmin and vmax if symmetric_color_scale is True
	if(symmetric_color_scale):
		if(vmin is None):
			vmin = np.min(np.min(table))
		if(vmax is None):
			vmax = np.max(np.max(table))
		abs_max = max([abs(vmin-symmetry_point), abs(vmax-symmetry_point)])

		vmin = symmetry_point - abs_max
		vmax = symmetry_point + abs_max
	
	# Plot heatmap
	plt.pcolor(table.loc[row_names_reordered, column_names_reordered], vmin=vmin, vmax=vmax, cmap=cmap)
	plt.ylim(0, len(row_names_reordered))
	plt.xlim(0, len(column_names_reordered))
	
	# Plot column/ row labels
	if(show_column_labels):
		plt.xticks([ i+.5 for i in range(len(column_names_reordered))], column_names_reordered, rotation=90, fontsize=7)
	else:
		plt.xticks([], [])
	if(show_row_labels):
		ax.yaxis.tick_right()
		plt.yticks([ i+.5 for i in range(len(row_names_reordered))], row_names_reordered, fontsize=7)
	else:
		plt.yticks([], [])
		
	return column_names_reordered, row_names_reordered, vmin, vmax

def plotDendrogram(table,
		distance_metric="correlation",
		linkage_method="complete",
		axis = 1,
		lw = 1.,
		ax = None):
	"""
		Function that plots a dendrogram on on axis 0 (rows), or axis 1 (columns) of a
		pandas.DataFrame.

		args:
			table: pandas.DataFrame
				Data matrix used to calculate dendrograms.
		kwargs:
			distance_metric: str
				Distance metric used to determine distance between two vectors.
				The distance function can be either of 'braycurtis', 'canberra',
				'chebyshev', 'cityblock', 'correlation', 'cosine', 'dice', 'euclidean',
				'hamming', 'jaccard', 'jensenshannon', 'kulsinski', 'mahalanobis',
				'matching', 'minkowski', 'rogerstanimoto', 'russellrao', 'seuclidean',
				'sokalmichener', 'sokalsneath', 'sqeuclidean', 'yule'.
			linkage_method: str
				methods for calculating the distance between the newly formed cluster u 
				and each v. Possible methods are, 'single', 'complete', 'average',
				'weighted', and 'centroid'
			axis: int
				Axis of table used for plotting dendrogram (0 = rows, 1 = columns).
			lw: float
				width of the lines (in points) defining the dengrogram.
			ax: matplotlib.axes.Axes
				Axes n which to plot the dendrogram.
	"""
	ax = ax if ax is not None else plt.gca()

	if(axis == 0):
		distance_matrix = pdist(table, metric=distance_metric)
		linkage_matrix = linkage(distance_matrix, metric=distance_metric, method=linkage_method)
		with plt.rc_context({'lines.linewidth': 1}):
			dendrogram_dict = dendrogram(linkage_matrix, color_threshold=0, orientation="left")
	elif(axis == 1):
		distance_matrix = pdist(table.T, metric=distance_metric)
		linkage_matrix = linkage(distance_matrix, metric=distance_metric, method=linkage_method)
		with plt.rc_context({'lines.linewidth': 1}):
			dendrogram_dict = dendrogram(linkage_matrix, color_threshold=0)
	
	ax.axis("off")

def plotAnnotation(ids_sorted, annotation_df, annotation_col_id, axis = 1, ax = None):
	"""
		Function that plots annotations.

		args:
			ids_sorted: list
				List of ids in the order in which the annotation shall be plotted.
			annotation_df: pandas.DataFrame
				DataFrame containing grouping informatation for the ids for which
				the annotation shall be plotted. Columns: groups, rows: ids
			annotation_col_id: str
				the column id of the group in annotation_df, for which the annotation
				shall be plotted.
		kwargs:
			axis: int
				If 0, then the annotation is plotted vertically, i.e. for rows of a
				DataFrame. If 1, then the annotation is plotted horizontally, i.e. for
				columns of a DataFrame.
			ax: matplotlib.axes.Axes
				Axes on which to plot the annotation.
	"""
	ax = ax if ax is not None else plt.gca()
	
	color_single = "w"
	
	color_list = ["#a6cee3", "#2076b4", "#b2df8a", "#33a02c", "#fb9a99", "#e31a1c", "#fdbf6f", "#ff7f00", "#cab2d6", "#653d9a", "#ffff99", "#d6604d", "#8dd3c7", "#ffffb3", "#bdbbdb", "#fb8072", "#80b1d3", "#fdb462", "#b3de69", "#f8cce5", "#d9d9d9", "#bc80bd"]
	
	groups = list(set(annotation_df.loc[:, annotation_col_id]))
	
	groups_color_dict = {}
	
	color_counter = 0
	for group in groups:
		if(len(annotation_df[annotation_df[annotation_col_id] == group].index) == 1):
			groups_color_dict[group] = color_single
		else:
			groups_color_dict[group] = color_list[color_counter % len(color_list)]
			color_counter += 1
			
	idx_counter = 0
	legend_dict = {}
	if(axis == 1):
		for id_current in ids_sorted:
			color = groups_color_dict[annotation_df.loc[id_current, annotation_col_id]]
			patch = Rectangle((idx_counter, 0), 1, 1, color=color)
			ax.add_patch(patch)
			idx_counter += 1
			
			if(not color in legend_dict):
				if(color == "w"):
					legend_dict[color] = [ patch, "singleton" ]
				else:
					legend_dict[color] = [ patch, annotation_df.loc[id_current, annotation_col_id] ]
		plt.xlim(0, len(ids_sorted))
		plt.ylim(0, 1)
		ax.yaxis.set_label_position("right")
		plt.ylabel(annotation_col_id, rotation=0, verticalalignment="center", horizontalalignment="left", fontsize=7)
	elif(axis == 0):
		for id_current in ids_sorted:
			color = groups_color_dict[annotation_df.loc[id_current, annotation_col_id]]
			patch = Rectangle((0, idx_counter), 1, 1, color=color)
			ax.add_patch(patch)
			idx_counter += 1
			
			if(not color in legend_dict):
				if(color == "w"):
					legend_dict[color] = [ patch, "singleton" ]
				else:
					legend_dict[color] = [ patch, annotation_df.loc[id_current, annotation_col_id] ]
		plt.ylim(0, len(ids_sorted))
		plt.xlim(0, 1)
		plt.xlabel(annotation_col_id, rotation=90, verticalalignment="top", horizontalalignment="center", fontsize=7)

	ax.axes.spines["top"].set_visible(False)
	ax.axes.spines["bottom"].set_visible(False)
	ax.axes.spines["left"].set_visible(False)
	ax.axes.spines["right"].set_visible(False)
	plt.xticks([] ,[])
	plt.yticks([] ,[])
	
	return legend_dict

def plotColorScale(table, 
		cmap="Reds", 
		symmetric_color_scale = True, 
		symmetry_point=0., 
		vmin = None, 
		vmax = None, 
		ax = None):
	'''
		Function that plots the color scale of values inside a dataframe.

		args:
			table: pandas.DataFrame
				Table containing numerical values.
		
		kwargs:
			cmap: str
				Colormap used to produce color scale.
			symmetric_color_scale: bool
				If true, vmin, and vmax will be set to have equal distance from symmetry
				point
			symmetry_point: float
				Only used, when symmetric_color_scale is true. If symmetric_color_scale is
				true, and symmetry_point is not set, it defaults to zero.
			vmin: float
				Minimal value of data_table, that has a color representation.
			vmax: float
				Maximal value of data_table, that has a color representation.
			ax: matplotlib.axes.Axes
				Axes instance on which to plot the color scale.
			
	'''
	ax = ax if ax is not None else plt.gca()

	# Calculate min and max value from table
	if(vmin is None):
		vmin = np.min(np.min(table))
	if(vmax is None):
		vmax = np.max(np.max(table))

	# Calculate maximal distance to symmetry point
	max_dist = max([np.abs(vmax-symmetry_point), np.abs(vmin-symmetry_point)])

	# Calculate x axis extensions
	xlim = [0, 256]
	if(symmetric_color_scale):
		xlim = [(0.5-(np.abs(vmin-symmetry_point)/max_dist)*.5)*256, 
			(.5+np.abs(np.abs(vmax-symmetry_point)/max_dist)*.5)*256]

	# Plot color scale
	gradient = np.linspace(0, 1, 256)
	gradient = np.vstack((gradient, gradient))
	plt.imshow(gradient, cmap=cmap, aspect="auto")
	plt.xlim(xlim)

	plt.xticks(xlim, [round(vmin, 2), round(vmax, 2)], fontsize=6)
	ax.xaxis.set_ticks_position('top')
	plt.title("Values", fontsize=7)
	plt.yticks([], [])
