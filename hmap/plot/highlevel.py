from . import basic
from .basic import colors
import pandas as pnd
from hmap.layout.layout import layoutGrid
from copy import deepcopy
import matplotlib.pyplot as plt

class HeatMap():
    """Heatmap class, that manages Dataframes, and their row and column
        annotations
    """

    def __init__(self,
             table: pnd.DataFrame,
             cmap: str = "seismic",
             distance_metric: str = "correlation",
             linkage_method: str = "complete",
             show_column_labels: bool = False,
             show_row_labels: bool = False,
             row_clustering: bool = True,
             column_clustering: bool = True,
             custom_row_clustering: list = None,
             custom_column_clustering: list = None,
             vmin: float = None,
             vmax: float = None,
             symmetric_color_scale: bool = False,
             symmetry_point: float = 0,
             optimal_row_ordering: bool = True,
             optimal_col_ordering: bool = True,
             row_annotations: pnd.DataFrame = None,
             column_annotations: pnd.DataFrame = None,
             row_annotation_colors: dict = None,
             col_annotation_colors: dict = None,
             row_annotation_ids: list = None,
             col_annotation_ids: list = None,
             row_annotation_types: list = None,
             col_annotation_types: list = None,
             plot_legends: bool = True,
             col_legends_width = 30,
             heatmap_width: int = 50,
             heatmap_height: int = 50,
             annotation_extension: int = 2,
             dendrogram_extension: int = 15,
             horizontal_space: int = 1,
             vertical_space: int = 1,
             bottom_margin: int = 25,
             top_margin: int = 25,
             left_margin: int = 25,
             right_margin: int = 25
            ):
        """Constructor
            :param table: Two dimensional array containing numerical values to be
                clustered.
            :type table: Object of type :class:`pandas.DataFrame`
            :param cmap: String representation of colormap to be used for
                plotting the heatmap, default "seismic"
            :type cmap: str, optional
            :param distance_metric: Distance metric used to determine distance
                between two vectors.The distance function can be either of
                'braycurtis', 'canberra', 'chebyshev', 'cityblock', 'correlation',
                'cosine', 'dice', 'euclidean', 'hamming', 'jaccard',
                'jensenshannon', 'kulsinski', 'mahalanobis', 'matching',
                'minkowski', 'rogerstanimoto', 'russellrao', 'seuclidean',
                'sokalmichener', 'sokalsneath', 'sqeuclidean', 'yule', defaults to
                'correlation'.
            :type distance_metric: str, optional
            :param linkage_method: methods for calculating the distance between the
                newly formed cluster u and each v. Possible methods are, 'single',
                'complete', 'average', 'weighted', and 'centroid', defaults to
                'complete'.
            :type linkage_method: str, optional
            :param show_column_labels: If true, show labels of columns, as defined
                in table, defaults to False.
            :type show_column_labels: bool, optional
            :param show_row_labels: If true, show labels of rows, as defined in
                table, defaults to False.
            :type show_row_labels: bool, optional
            :param row_clustering: If true, the rows a clustered according to
                distance_metric, and linkage_method, defaults to True.
            :type row_clustering: bool, optional
            :param column_clustering: If true, the columns are clustered according
                to distance_metric, and linkage_method, defaults to True.
            :type column_clustering: bool, optional
            :param custom_row_clustering: List of Row ids from table in the order
                they should appear in the heatmap. Only applies if row_clustering is
                False, defaults to None.
            :type custom_row_clustering: list, optional
            :param custom_column_clustering: List of column ids from table in the
                order they should appear in the heatmap. Only applies if
                column_clustering is False, defaults to None.
            :type custom_column_clustering: list, optional
            :param vmin: Minimal value of data_table, that has a color
                representation, defaults to None.
            :type vmin: float, optional
            :param vmax: Maximal value of data_table, that has a color
                representation, defaults to None.
            :type vmax: float, optional
            :param symmetric_color_scale: If true, vmin, and vmax will be set to
                have equal distance from symmetry point, defaults to False.
            :type symmetric_color_scale: bool, optional
            :param symmetry_point: Only used, when symmetric_color_scale is true. If
                symmetric_color_scale is true, and symmetry_point is not set,
                defaults to zero.
            :type symmetry_point: float, optional
            :param show_plot: If True, the heatmap will be shown on the given axis,
                else the function only returns the return values, defaults to True.
            :type show_plot: bool, optional
            :param optimal_row_ordering: If True, the rows will be ordered optimally
                with regards to the cluster separation. Be careuful: Can take a
                long time, depending on the number of rows, defaults to True.
            :type optimal_row_ordering: bool, optional
            :param optimal_col_ordering: If True, the columns will be ordered
                optimally with regards to the cluster separation. Be careuful:
                Can take a long time, depending on the number of columns, defaults
                to True.
            :type optimal_col_ordering: bool, optional
            :param row_annotations: Data frame containing row annotations.
                DataFrame must have the same index as the data table to be 
                clustered. There can be an arbitrary number of columns, 
                containing numerical or discrete annotations.
            :type row_annotations: Object of type :class:`pandas.DataFrame`, 
                optional
            :param column_annotations: Data frame containing row annotations. 
                Index of DataFrame must be the same as the columns of the data 
                table to be clustered. There can be an arbitrary number of 
                columns, containing numerical or discrete annotations.
            :type column_annotations: Object of type :class:`pandas.DataFrame`,
                optional
            :param row_annotation_colors: Colors used for plotting row 
                annotations. Colors can be either discrete or continuous. This
                means, for discrete annotations like gender you can define one 
                color per group, whereas for continues annotations like age, or
                some concentrations you can define a colormap. In case of
                discrete annotation groups, colors must be defined in a two
                level dictionary, where first level keys are the names of the
                annotation group, second level keys are the groups
                and their values are the colors (in a format matplotlib.pyplot
                understands). In case of continuous annotations, colors must be
                defined in a one-level dictionary, where the keys are the names
                of the annotation group and the values are strings defining the
                colormap to be used for displaying the continuous annotation
                values. For a list of available colormap ids see 
                `matplotlib.pyplot.colormaps()`
            :type row_annotation_colors: dict, optional
            :param col_annotation_colors: Colors used for plotting column 
                annotations. Colors can be either discrete or continuous. This
                means, for discrete annotations like gender you can define one 
                color per group, whereas for continues annotations like age, or
                some concentrations you can define a colormap. In case of
                discrete annotation groups, colors must be defined in a two
                level dictionary, where first level keys are the names of the
                annotation group, second level keys are the groups
                and their values are the colors (in a format matplotlib.pyplot
                understands). In case of continuous annotations, colors must be
                defined in a one-level dictionary, where the keys are the names
                of the annotation group and the values are strings defining the
                colormap to be used for displaying the continuous annotation
                values. For a list of available colormap ids see 
                `matplotlib.pyplot.colormaps()`
            :type col_annotation_colors: dict, optional
            :param row_annotation_ids: List of row annotation IDs from 
                row_annotations, that shall be plotted. If not given, none
                of the row_annotations will be plotted.
            :type row_annotation_ids: list, optional
            :param col_annotation_ids: List of column annotation IDs from 
                column_annotations, that shall be plotted. If not given, none
                of the column_annotations will be plotted.
            :type col_annotation_ids: list, optional
            :param row_annotation_types: List of row annotation types. Allowed
                annotation types are "categorical" and "non-categorical",
                default None
            :type row_annotation_types: list, optional
            :param col_annotation_types: List of column annotation types.
                Allowed annotation types are "categorical" and
                "non-categorical", default None
            :type col_annotation_types: list, optional
            :param plot_legends: Boolean value, defining if annotation legends
                shall be plotted, default True
            :type plot_legends: bool, optional
            :param col_legends_width: width of subplot that plots the annotation
                legends, default 30
            :type col_legends_width: int, optional
            :param heatmap_width: Width of heatmap in mm
            :type heatmap_width: int, optional
            :param heatmap_height: Height of heatmap in mm
            :type heatmap_height: int, optional
            :param annotation_extension: Extension of annotation plots in mm
            :type annotation_extension: int, optional
            :param dendrogram_extension: Extension of dendrogram plots in mm
            :type dendrogram_extension: int, optional
            :param horizontal_space: Horizontal space between subplots in mm
            :type horizontal_space: int, optional
            :param vertical_space: Vertical space between subplots in mm
            :type vertical_space: int, optional
            :param bottom_margin: Margin between bottom and plot in mm
            :type bottom_margin: int, optional
            :param top_margin: Margin between top and plot in mm
            :type top_margin: int, optional
            :param left_margin: Margin between left border and plot in mm
            :type left_margin: int, optional
            :param right_margin: Margin between right border and plot in mm
            :type right_margin: int, optional
        """
        ################
        # Set attributes

        # Attributes given by constructor arguments
        self.table = deepcopy(table)
        self.cmap = cmap
        self.distance_metric = distance_metric
        self.linkage_method = linkage_method
        self.show_column_labels = show_column_labels
        self.show_row_labels = show_row_labels
        self.row_clustering = row_clustering
        self.column_clustering = column_clustering
        self.custom_row_clustering = custom_row_clustering
        self.custom_column_clustering = custom_column_clustering
        self.vmin = vmin
        self.vmax = vmax
        self.symmetric_color_scale = symmetric_color_scale
        self.symmetry_point = symmetry_point
        self.optimal_row_ordering = optimal_row_ordering
        self.optimal_col_ordering = optimal_col_ordering
        self.row_annotations = row_annotations
        self.column_annotations = column_annotations
        self.row_annotation_colors = row_annotation_colors
        self.col_annotation_colors = col_annotation_colors
        self.row_annotation_ids = row_annotation_ids
        self.col_annotation_ids = col_annotation_ids
        self.row_annotation_types = row_annotation_types
        self.column_annotation_types = col_annotation_types
        self.plot_legends = plot_legends
        self.col_legends_width = col_legends_width
        self.heatmap_width = heatmap_width
        self.heatmap_height = heatmap_height
        self.annotation_extension = annotation_extension
        self.dendrogram_extension = dendrogram_extension
        self.horizontal_space = horizontal_space
        self.vertical_space = vertical_space
        self.bottom_margin = bottom_margin
        self.top_margin = top_margin
        self.left_margin = left_margin
        self.right_margin = right_margin

        # Other attributes

        # Linkage matrices used for hierarchical clustering need to be computed
        # only once and saved as attributes afterwards
        self.column_linkage_matrix = None
        self.row_linkage_matrix = None

        self.__row_ids_ordered = None
        self.__column_ids_ordered = None

        # Boolen variable that defines if rows, or columns have to be clustered
        self.__cluster_rows = True
        self.__cluster_columns = True

        # Grid defining layout of figure
        self.__grid = None
        self.__figure = None

    #############################
    # Getter and setter methods #
    #############################

    ########
    # Setter

    def set_distance_metric(self, distance_metric):
        """Method that sets distance metric
        """
        self.distance_metric = distance_metric

    def set_linkage_method(self, linkage_method):
        """Method that sets linkage method
        """
        self.linkage_method = linkage_method

    def set_show_column_labels(self, show_column_labels):
        """Method that sets show_column_labels
        """
        self.show_column_labels = show_column_labels

    def set_show_row_labels(self, show_row_labels):
        """Method that sets show_row_labels
        """
        self.show_row_labels = show_row_labels

    def set_row_clustering(self, row_clustering):
        """Method that sets row_clustering
        """
        self.row_clustering = row_clustering

    def set_column_clustering(self, column_clustering):
        """Method that sets column_clustering
        """
        self.column_clustering = column_clustering

    def set_custom_row_clustering(self, custom_row_clustering):
        """Method that sets custom_row_clustering
        """
        self.custom_row_clustering = custom_row_clustering

    def set_custom_column_clustering(self, custom_column_clustering):
        """Method that sets custom_column_clustering
        """
        self.custom_column_clustering = custom_column_clustering

    def set_vmin(self, vmin):
        """Method that sets vmin
        """
        self.vmin = vmin

    def set_vmax(self, vmax):
        """Method that sets vmax
        """
        self.vmax = vmax

    def set_symmetric_color_scale(self, symmetric_color_scale):
        """Method that sets symmetric_color_scale
        """
        self.symmetric_color_scale = symmetric_color_scale

    def set_symmetry_point(self, symmetry_point):
        """Method that sets symmetry_point
        """
        self.symmetry_point = symmetry_point

    def set_optimal_row_ordering(self, optimal_row_ordering):
        """Method that sets optimal_row_ordering
        """
        self.optimal_row_ordering = optimal_row_ordering

    def set_optimal_col_ordering(self, optimal_col_ordering):
        """Method that sets optimal_col_ordering
        """
        self.optimal_col_ordering = optimal_col_ordering

    def set_row_annotations(self, row_annotations):
        """Method that sets row_annotations
        """
        self.row_annotations = row_annotations

    def set_column_annotations(self, column_annotations):
        """Method that sets column_annotations
        """
        self.column_annotations = column_annotations

    def set_row_annotation_colors(self, row_annotation_colors):
        """Method that sets row_annotation_colors
        """
        self.row_annotation_colors = row_annotation_colors

    def set_col_annotation_colors(self, col_annotation_colors):
        """Method that sets col_annotation_colors
        """
        self.col_annotation_colors = col_annotation_colors

    def set_row_annotation_ids(self, row_annotation_ids):
        """Method that sets row_annotation_ids
        """
        self.row_annotation_ids = row_annotation_ids

    def set_col_annotation_ids(self, col_annotation_ids):
        """Method that sets col_annotation_ids
        """
        self.col_annotation_ids = col_annotation_ids

    def set_row_annotation_extension(self, row_annotation_extension):
        """Method that sets row_annotation_extension
        """
        self.row_annotation_extension = row_annotation_extension

    def set_dendrogram_extension(self, dendrogram_extension):
        """Method that sets dendrogram_extension
        """
        self.dendrogram_extension = dendrogram_extension

    def set_horizontal_space(self, horizontal_space):
        """Method that sets horizontal_space
        """
        self.horizontal_space = horizontal_space

    def set_vertical_space(self, vertical_space):
        """Method that sets vertical_space
        """
        self.vertical_space = vertical_space

    def set_bottom_margin(self, bottom_margin):
        """Method that sets bottom_margin
        """
        self.bottom_margin = bottom_margin

    def set_top_margin(self, top_margin):
        """Method that sets top_margin
        """
        self.top_margin = top_margin

    def set_left_margin(self, left_margin):
        """Method that sets left_margin
        """
        self.left_margin = left_margin

    def set_right_margin(self, right_margin):
        """Method that sets right_margin
        """
        self.right_margin = right_margin

    ########
    # Getter

    def get_cluster_rows(self):
        """Method that return cluster_rows
        """
        return self.__cluster_rows

    def get_cluster_columns(self):
        """Method that return cluster_columns
        """
        return self.__cluster_columns

    ##############
    # Plot Methods

    def __create_grid(self):
        """Method, that creates figure layout
        """
        # Define heights of rows
        row_heights = []
        if(not self.column_clustering is None):
            row_heights += [self.dendrogram_extension]
        if(not self.col_annotation_ids is None):
            row_heights += ([self.annotation_extension]*
                            len(self.col_annotation_ids))
        row_heights += [self.heatmap_height]
        n_rows = len(row_heights)

        # Define widths of columns
        col_widths = []
        if(not self.row_clustering is None):
            col_widths += [self.dendrogram_extension]
        if(not self.row_annotation_ids is None):
            col_widths += ([self.annotation_extension]*                                     
                            len(self.row_annotation_ids))
        col_widths += [self.heatmap_width]
        if(self.plot_legends):
            col_widths += [self.col_legends_width]
        n_cols = len(col_widths)

        self.__fig, self.__grid = layoutGrid(n_rows,
                                             n_cols,
                                             col_widths,
                                             row_heights,
                                             self.vertical_space,
                                             self.horizontal_space,
                                             self.bottom_margin,
                                             self.top_margin,
                                             self.left_margin,
                                             self.right_margin
                                            )

    def show(self):
        """Method that plots heatmap
        """
        # Create grid
        self.__create_grid()

        ###########
        # Plot rows
        col_index = 0
        if(not self.row_clustering is None):
            col_index += 1
        if(not self.row_annotation_ids is None):
            col_index += len(self.row_annotation_ids)

        row_index = 0
        # Plot column dendrogram
        ax = plt.subplot(self.__grid[row_index, col_index])
        if(self.column_clustering):
            (column_dendrogram_dict, column_linkage_matrix, 
             column_cluster_dict, column_ids_ordered) = \
                basic.Dendrogram(
                    self.table,
                    distance_metric=self.distance_metric,
                    linkage_method=self.linkage_method,
                    axis = 1,
                    lw = 1.,
                    n_clust = None,
                    optimal_row_ordering=self.optimal_row_ordering,
                    optimal_col_ordering=self.optimal_col_ordering,
                    linkage_matrix = self.column_linkage_matrix,
                    ax = ax
                )
            self.column_linkage_matrix = column_linkage_matrix
            self.__column_ids_ordered = column_ids_ordered
            row_index += 1

        # Plot annotations
        annotation_patch_dict = {}
        annotation_ids = []
        if(not self.col_annotation_ids is None):
            is_categorical_list = [ c == "categorical" for 
                                    c in self.column_annotation_types ]
            for col_annotation_id,is_categorical in zip(self.col_annotation_ids,
                                                        is_categorical_list):
                ax = plt.subplot(self.__grid[row_index, col_index])
                cmap = plt.cm.GnBu_r
                color_dict = None
                if(is_categorical):
                    color_dict = \
                        self.col_annotation_colors[col_annotation_id] if \
                        col_annotation_id in self.col_annotation_colors else \
                        None
                else:
                    cmap = \
                        self.col_annotation_colors[col_annotation_id] if \
                        col_annotation_id in self.col_annotation_colors else \
                        plt.cm.GnBu_r
                is_categorial, patch_list = \
                        basic.Annotation(
                          self.__column_ids_ordered,
                          self.column_annotations,
                          col_annotation_id,
                          axis = 1,
                          color_list = colors["xkcd"],
                          is_categorial=is_categorical,
                          cmap = cmap,
                          color_dict = color_dict,
                          ax = ax
                        )
                annotation_patch_dict[col_annotation_id] = \
                        [is_categorical, patch_list]
                annotation_ids += [col_annotation_id]
                row_index += 1 

        ##############
        # Plot columns
        row_index = 0
        if(not self.column_clustering is None):
            row_index += 1
        if(not self.col_annotation_ids is None):
            row_index += len(self.col_annotation_ids)

        col_index = 0
        # Plot row dendrogram
        ax = plt.subplot(self.__grid[row_index, col_index])
        if(self.row_clustering):
            (row_dendrogram_dict, row_linkage_matrix, 
             row_cluster_dict, row_ids_ordered) = \
                basic.Dendrogram(
                    self.table,
                    distance_metric=self.distance_metric,
                    linkage_method=self.linkage_method,
                    axis = 0,
                    lw = 1.,
                    n_clust = None,
                    optimal_row_ordering=self.optimal_row_ordering,
                    optimal_col_ordering=self.optimal_col_ordering,
                    linkage_matrix = self.row_linkage_matrix,
                    ax = ax
                )
            self.row_linkage_matrix = row_linkage_matrix
            self.__row_ids_ordered = row_ids_ordered
            col_index += 1

        # Plot annotations
        if(not self.row_annotation_ids is None):
            is_categorical_list = [ c == "categorical" for 
                                    c in self.row_annotation_types ]
            for row_annotation_id,is_categorical in zip(self.row_annotation_ids,
                                                        is_categorical_list):
                ax = plt.subplot(self.__grid[row_index, col_index])
                cmap = plt.cm.GnBu_r
                color_dict = None
                if(is_categorical):
                    color_dict = \
                        self.row_annotation_colors[row_annotation_id] if \
                        row_annotation_id in self.row_annotation_colors else \
                        None
                else:
                    cmap = \
                        plt.get_cmap(
                                self.row_annotation_colors[row_annotation_id]
                                ) if \
                        row_annotation_id in self.row_annotation_colors else \
                        plt.cm.GnBu_r
                is_categorial, patch_list = \
                        basic.Annotation(
                          self.__row_ids_ordered,
                          self.row_annotations,
                          row_annotation_id,
                          axis = 0,
                          color_list = colors["xkcd"],
                          is_categorial=is_categorical,
                          cmap = cmap,
                          color_dict = color_dict,
                          ax = ax
                        )
                annotation_patch_dict[row_annotation_id] = \
                        [is_categorial, patch_list]
                annotation_ids += [row_annotation_id]
                col_index += 1

        # Plot heatmap
        ax = plt.subplot(self.__grid[row_index, col_index])
        (column_ids_reordered,
         row_ids_reordered,
         vmin,
         vmax,
         column_linkage_matrix,
         row_linkage_matrix) = \
            basic.Heatmap(self.table,
                cmap = self.cmap,
                distance_metric = self.distance_metric,
                linkage_method = self.linkage_method,
                show_column_labels = self.show_column_labels,
                show_row_labels = self.show_row_labels,
                row_clustering = self.row_clustering,
                column_clustering = self.column_clustering,
                custom_row_clustering = self.custom_row_clustering,
                custom_column_clustering = self.custom_column_clustering,
                vmin = self.vmin,
                vmax = self.vmax,
                symmetric_color_scale = self.symmetric_color_scale,
                symmetry_point = self.symmetry_point,
                show_plot = True,
                optimal_row_ordering = self.optimal_row_ordering,
                optimal_col_ordering = self.optimal_col_ordering,
                row_linkage_matrix = self.row_linkage_matrix,
                column_linkage_matrix = self.column_linkage_matrix,
                ax = ax)

        # Plot annotation legends
        if(self.plot_legends):
            col_index += 1
            ax = plt.subplot(self.__grid[row_index, col_index])
            basic.Legends(annotation_patch_dict,
                          annotation_ids,
                          ax = ax
                         )

