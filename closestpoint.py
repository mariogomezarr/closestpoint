#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Mario Andrés Gómez-Arroyo
@email: mariogomezarr@gmail.com

A tool for finding the shortest distance of a point data set from one category to many other categories.
----
Una herramienta para encontrar la distancia más corta de un conjunto de datos de puntos de una categoría a muchas otras categorías.
----
Un outil pour trouver la distance la plus courte entre un ensemble de données de points d'une catégorie à de nombreuses autres catégories.
"""

import pandas as pd
import scipy.spatial
import numpy as np

def upload_xy_data(str):

    """ Function that allows uploading csv files through Pandas.
    
    :param str: This is the static points file path.
    
    """

    temp_xy_data = pd.read_csv(str)
    xy_data = temp_xy_data[['id','X','Y']]

    return xy_data


def upload_target_data(str):
    
    """ Function that allows uploading csv files through Pandas.
    
    :param str: This is the target points file path.

    """

    temp_target_data = pd.read_csv(str)
    target_data = temp_target_data[['id', 'X', 'Y', 'category']]

    return target_data


def find_closest_points(dataset1, dataset2, output_unite = 'kilometers'):

    """ Function that relates xy_data and target_data and finds the closest point between the first dataframe and the categories of the second one.

    :param dataset1: This is the static point dataframe, in terms of id, x, and y.
    :param dataset2: This is the target point dataframe, in terms of id, x, y, and category.
    :param output_unit: Defines the unit of measure in which the shortest distance will be calculated. Kilometers by default. Later versions: meters, degrees.

    """
    
    all_names = dataset2['category'].unique()
    
    for i in all_names:
        type_i = dataset2[dataset2['category'].isin([i])]
        nearest_point_i = scipy.spatial.distance.cdist(dataset1[['X','Y']], 
                                type_i[['X','Y']], metric = 'euclidean')
        df = pd.DataFrame(nearest_point_i, index = dataset1['id'], columns = type_i['id'])
        df2 = df.min(axis = 1)
        df2.name = i
        df2 = df2/0.009
        dataset1[i] = df2.values
        title_i = 'nearest_' + i
        dataset1.rename(columns = {i: title_i}, inplace = True)

    return dataset1

def save_csv(df, str_path):

    df.to_csv(str_path)