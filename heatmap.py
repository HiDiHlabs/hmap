from scipy.spatial.distance import pdist
from scipy.cluster.hierarchy import linkage, dendrogram

import matplotlib.pyplot as plt

import pandas as pnd

def plotClusteredHeatmap(table, cmap="Reds", distance_metric="correlation", linkage_method="complete", show_column_labels = False, show_row_labels = False, ax = None):
	"""
		Function that plots a two dimensional matrix as clustered heatmap. 
		Sorting of rows and columns is done by hierarchical clustering.

		args:
			table: pandas.DataFrame
				Two dimensional array containing numerical values to be clustered.
			distance_metric: str
				Distance metric used to determine distance between two vectors.
				The distance function can be either of 'braycurtis', 'canberra',
				'chebyshev', 'cityblock', 'correlation', 'cosine', 'dice', 'euclidean',
				'hamming', 'jaccard', 'jensenshannon', 'kulsinski', 'mahalanobis',
				'matching', 'minkowski', 'rogerstanimoto', 'russellrao', 'seuclidean',
				'sokalmichener', 'sokalsneath', 'sqeuclidean', 'yule'.
			linkage_method: str
				
	"""

	ax = ax if ax is not None else plt.gca()
	
	distance_matrix = pdist(table.T, metric=distance_metric)
	linkage_matrix = linkage(distance_matrix, metric=distance_metric, method=linkage_method)
	dendrogram_dict = dendrogram(linkage_matrix, no_plot=True)
	
	leaves = dendrogram_dict["leaves"]
	
	column_names = list(table.columns)
	column_names_reordered = [ column_names[i] for i in leaves ]
	row_names = list(table.index)
	
	plt.pcolor(table.loc[row_names, column_names_reordered], cmap=cmap)
	plt.ylim(0, len(row_names))
	
	if(show_column_labels):
		plt.xticks([ i+.5 for i in range(len(column_names_reordered))], column_names_reordered, rotation=90, fontsize=7)
	if(show_row_labels):
		ax.yaxis.tick_right()
		plt.yticks([ i+.5 for i in range(len(row_names))], row_names, fontsize=7)
		
	return [ table.columns[i] for i in leaves ]

def plotDendrogram(table, distance_metric="correlation", linkage_method="complete", ax = None):
	ax = ax if ax is not None else plt.gca()
	
	distance_matrix = pdist(table.T, metric=distance_metric)
	linkage_matrix = linkage(distance_matrix, metric=distance_metric, method=linkage_method)
	dendrogram_dict = dendrogram(linkage_matrix, color_threshold=0)
	
	ax.axis("off")

def plotAnnotation(ids_sorted, annotation_df, annotation_col_id, ax = None):
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
	ax.axis("off")
	
	return legend_dict
