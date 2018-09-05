""" Module for computing the Local Binary Pattern in EOPatch """

import numpy as np
from skimage.feature import local_binary_pattern
from eolearn.core import EOTask, FeatureType


class LocalBinaryPatternTask(EOTask):
    """
    Task to compute the Local Binary Pattern images

    LBP looks at points surrounding a central point and tests whether the surrounding points are greater than or less
    than the central point

    The task uses skimage.feature.local_binary_pattern to extract the texture features.
    """
    def __init__(self, feature, nb_points=24, radius=3):
        """
        :param feature: A feature that will be used and a new feature name where data will be saved. If new name is not
        specified it will be saved with name '<feature_name>_HARALICK'

        Example: (FeatureType.DATA, 'bands') or (FeatureType.DATA, 'bands', 'lbp')

        :param nb_points: Number of point to use
        :type nb_points: int
        :param radius: Radius of the circle of neighbors
        :type radius: int
        """
        self.feature = self._parse_features(feature, default_feature_type=FeatureType.DATA, new_names=True,
                                            rename_function='{}_HARALICK'.format)

        self.nb_points = nb_points
        self.radius = radius
        if nb_points < 1 or radius < 1:
            raise ValueError('Local binary pattern task parameters must be positives')

    def _compute_lbp(self, data):
        result = np.empty(data.shape, dtype=np.float)
        for time in range(data.shape[0]):
            for band in range(data.shape[3]):
                image = data[time, :, :, band]
                result[time, :, :, band] = local_binary_pattern(image, self.nb_points, self.radius, method='uniform')
        return result

    def execute(self, eopatch):

        for feature_type, feature_name, new_feature_name in self.feature:
            eopatch[feature_type][new_feature_name] = self._compute_lbp(eopatch[feature_type][feature_name])

        return eopatch
