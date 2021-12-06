from . import basic
import pandas as pnd
from hmap.layout.layout import layoutGrid

class HeatMap():
    """Heatmap class, that manages Dataframes, and their row and column
        annotations
    """

    def init(self,
             table: pnd.DataFrame,
             distance_metric: str ="correlation",
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
            ):
        """Constructor
           :param table: Two dimensional array containing numerical values to be
                clustered.
           :type table: Object of type :class:`pandas.DataFrame`
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
        """

        # Set attributes
        self.table = table
        self.distance_metric = distance_metric
        self.linkage_method = linkage_method
        self.show_column_labels = show_column_labels
        self.how_row_labels = show_row_labels
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

        # Linkage matrices used for hierarchical clustering need to be computed
        # only once and saved as attributes afterwards
        self.column_linkage_matrix = None
        self.row_linkage_matrix = None
