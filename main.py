import json
import os

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt

SECONDS_IN_HOUR = 3600

METERS_IN_KILOMETERS = 1000

SCOPE_OF_BENCHMARK = "Vlaanderen"


def get_nested_value(data, keys):
    if not keys:
        return data
    return get_nested_value(data.get(keys[0], {}), keys[1:])


def read_json_file(file_path, keys):
    with open(file_path, 'r') as file:
        data = json.load(file)
        return get_nested_value(data, keys)


def calculate_mean(param):
    if isinstance(param, dict):
        return np.mean(list(param.values()))
    else:
        return param


def create_bar_chart(file_paths_gh, file_paths_ors, file_paths_slv, keys_to_compare, unit_conversion, ylabel,
                     title, vrpvariant):
    data_set_GH = [calculate_mean(read_json_file(file_path, keys_to_compare)) / unit_conversion for file_path in file_paths_gh]
    data_set_ORS = [calculate_mean(read_json_file(file_path, keys_to_compare)) / unit_conversion for file_path in file_paths_ors]
    data_set_SLV = [calculate_mean(read_json_file(file_path, keys_to_compare)) / unit_conversion for file_path in file_paths_slv]

    bar_width = 0.30
    index = range(len(file_paths_GH))

    fig, ax = plt.subplots()
    bars1 = ax.bar(index, data_set_GH, bar_width, label='GraphHopper')
    bars2 = ax.bar([i + bar_width for i in index], data_set_ORS, bar_width, label='OpenRouteService')
    bars3 = ax.bar([i + 2*bar_width for i in index], data_set_SLV, bar_width, label='Solvice')

    ax.set_xlabel('Files')
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.set_xticks([i + bar_width for i in index])
    ax.set_xticklabels(
        [file.split('fullAnalysisResult_')[-1].split('-')[0].split("benchmark")[-1] for file in file_paths_gh])

    ax.legend()

    figname = vrpvariant + "/"+keys_to_compare[1] + "_" + vrpvariant+ "_" + SCOPE_OF_BENCHMARK

    plt.setp(ax.get_xticklabels(), fontsize=10, rotation='vertical')
    plt.tight_layout()
    plt.savefig(figname)

    plt.show()


# Specify the file paths for the JSON files of each routing engine
file_paths_GH = []
file_paths_ORS = []
file_paths_SLV = []


def add_files_to_set(path, file_paths, enginename):
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)) and enginename in file and "Brussel" not in file:
            file_path = os.path.join(path, file)
            file_paths.append(file_path)


variant = "MultiDepot"

add_files_to_set(
    "C:\\Users\\lucas\\Documents\\masterproef2023_2024\\metavrp-toolkit\\cli\\etc\\demoproblems\\analysisResultsJSON\\"+variant+"\\",
    file_paths_GH, "GH")
add_files_to_set(
    "C:\\Users\\lucas\\Documents\\masterproef2023_2024\\metavrp-toolkit\\cli\\etc\\demoproblems\\analysisResultsJSON\\"+variant+"\\",
    file_paths_ORS, "ORS")
add_files_to_set(
    "C:\\Users\\lucas\\Documents\\masterproef2023_2024\\metavrp-toolkit\\cli\\etc\\demoproblems\\analysisResultsJSON\\"+variant+"\\",
    file_paths_SLV, "SLV")

# depending on the analysis, these values will differ.
meanworkingshift_keys = ['WorkingShiftAnalysisResult', 'meanworkingShift']
stddevworkingshift_keys = ['WorkingShiftAnalysisResult', 'stddevWorkingShifts']
shortestworkingshift_keys = ['WorkingShiftAnalysisResult', 'shortestWorkingShift']
longestworkingshift_keys = ['WorkingShiftAnalysisResult', 'longestWorkingShift']

totaldistancekm_keys = ['RouteCompositionAnalysisResult', 'totalDistanceMeters']
totalruntime_keys = ['RouteCompositionAnalysisResult', 'runTime']
failurerate_keys = ['RouteCompositionAnalysisResult', 'failureRate']
numberOfRoutes_keys = ['RouteCompositionAnalysisResult', 'numberOfRoutes']
longestroute_keys = ['RouteCompositionAnalysisResult', 'stopsLongestRoute']
shortestroute_keys = ['RouteCompositionAnalysisResult', 'stopsShortestRoute']
meanstops_keys = ['RouteCompositionAnalysisResult', 'meanStops']
stddevstops_keys = ['RouteCompositionAnalysisResult', 'stdDevStops']

biggestLoad_keys = ['CargoAnalysisResult', 'biggestLoad']
biggestLoadVolume_keys = ['CargoAnalysisResult', 'biggestLoadVolume']
smallestLoad_keys = ['CargoAnalysisResult', 'smallestLoad']
smallestLoadVolume_keys = ['CargoAnalysisResult', 'smallestLoadVolume']
meanLoad_keys = ['CargoAnalysisResult', 'meanLoad']
meanLoadVolume_keys = ['CargoAnalysisResult', 'meanLoadVolume']


meanDistanceToGeoCenter_keys = ['VisualAttractivenessAnalysisResult', 'meanDistanceToGeographicCenter']
meanTravelTimeBetweenStops_keys = ['VisualAttractivenessAnalysisResult', 'meanTravelTimeBetweenStops']
meanDistanceToConvexHull_keys = ['VisualAttractivenessAnalysisResult', 'meanDistanceToConvexHull']


ylabel_duration = 'Duration (hours)'
ylabel_distance = 'Distance (km)'
ylabel_runtime = 'Duration (ms)'
ylabel_failurerate = 'Rate of failure (%)'
ylabel_numberOfRoutes = 'Number of used vehicles'
ylabel_stops = 'Amount of stops'
ylabel_kgs = 'Load (kg)'
ylabel_volume = 'Load (dm³)'


title_meanworkingshift = 'Bar chart of mean duration of the working shifts for different solutions. '
title_meanTTBetweenStops = 'Bar chart of mean travel time between stops for different solutions. '
title_totaldistance = 'Bar chart of total distance for different solutions. '
title_meandistancetogeocenter = 'Bar chart of mean distance to geographic center for different solutions. '
title_runtime = 'Bar chart of run time of the routing engine for different solutions. '
title_failurerate = 'Bar chart of failure rate for different solutions. '
title_numberOfRoutes = 'Number of used vehicles for different solutions. '
title_stddevworkingshift = 'Bar chart of standard deviation of the working shifts for different solutions. '
title_shortestworkingshift = 'Bar chart of the shortest shift for different solutions. '
title_longestworkingshift = 'Bar chart of the longest shift for different solutions. '
title_longestroute = 'Bar chart of route with most stops for different solutions. '
title_shortestroute = 'Bar chart of route with least stops for different solutions. '
title_meanstops = 'Bar chart of mean amount of stops for different solutions. '
title_stddevstops = 'Number of standard deviation of the amount of stops for different solutions. '
title_convexhull = 'Number of mean distance to convex hull for different solutions. '
title_biggestLoad = 'Bar chart of biggest amount of cargo for different solutions. '
title_smallestLoad = 'Bar chart of smallest amount of cargo for different solutions. '
title_meanLoad = 'Bar chart of mean amount of cargo for different solutions. '


# Create the bar charts
# before running, make sure that the variable "SCOPE_OF_BENCHMARK" is named correctly!
create_bar_chart(file_paths_GH, file_paths_ORS, file_paths_SLV, meanworkingshift_keys, SECONDS_IN_HOUR, ylabel_duration,
                 title_meanworkingshift, variant)
create_bar_chart(file_paths_GH, file_paths_ORS, file_paths_SLV, meanTravelTimeBetweenStops_keys, SECONDS_IN_HOUR, ylabel_duration,
                 title_meanTTBetweenStops, variant)
create_bar_chart(file_paths_GH, file_paths_ORS, file_paths_SLV, totaldistancekm_keys, METERS_IN_KILOMETERS, ylabel_distance,
                 title_totaldistance, variant)
create_bar_chart(file_paths_GH, file_paths_ORS, file_paths_SLV, totalruntime_keys, 1, ylabel_runtime,
                 title_runtime, variant)
create_bar_chart(file_paths_GH, file_paths_ORS, file_paths_SLV, failurerate_keys, 0.01, ylabel_failurerate,
                 title_failurerate, variant)
create_bar_chart(file_paths_GH, file_paths_ORS, file_paths_SLV, numberOfRoutes_keys, 1, ylabel_numberOfRoutes,
                 title_numberOfRoutes, variant)
create_bar_chart(file_paths_GH, file_paths_ORS, file_paths_SLV, meanDistanceToGeoCenter_keys, METERS_IN_KILOMETERS,
                 ylabel_distance,  title_meandistancetogeocenter, variant)
create_bar_chart(file_paths_GH, file_paths_ORS, file_paths_SLV, stddevworkingshift_keys, SECONDS_IN_HOUR, ylabel_duration,
                 title_stddevworkingshift, variant)
create_bar_chart(file_paths_GH, file_paths_ORS, file_paths_SLV, shortestworkingshift_keys, SECONDS_IN_HOUR, ylabel_duration,
                 title_shortestworkingshift, variant)
create_bar_chart(file_paths_GH, file_paths_ORS, file_paths_SLV, longestworkingshift_keys, SECONDS_IN_HOUR, ylabel_duration,
                 title_longestworkingshift, variant)
create_bar_chart(file_paths_GH, file_paths_ORS, file_paths_SLV, longestroute_keys, 1, ylabel_stops,
                 title_longestroute, variant)
create_bar_chart(file_paths_GH, file_paths_ORS, file_paths_SLV, shortestroute_keys, 1, ylabel_stops,
                 title_shortestroute, variant)
create_bar_chart(file_paths_GH, file_paths_ORS, file_paths_SLV, meanstops_keys, 1, ylabel_stops,
                 title_meanstops, variant)
create_bar_chart(file_paths_GH, file_paths_ORS, file_paths_SLV, stddevstops_keys, 1,
                 ylabel_stops,  title_stddevstops, variant)
create_bar_chart(file_paths_GH, file_paths_ORS, file_paths_SLV, meanDistanceToConvexHull_keys, METERS_IN_KILOMETERS,
                 ylabel_distance,  title_convexhull, variant)
create_bar_chart(file_paths_GH, file_paths_ORS, file_paths_SLV, biggestLoad_keys, 1, ylabel_kgs,
                 title_biggestLoad, variant)
create_bar_chart(file_paths_GH, file_paths_ORS, file_paths_SLV, biggestLoadVolume_keys, 1, ylabel_volume,
                 title_biggestLoad, variant)
create_bar_chart(file_paths_GH, file_paths_ORS, file_paths_SLV, smallestLoad_keys, 1, ylabel_kgs,
                 title_smallestLoad, variant)
create_bar_chart(file_paths_GH, file_paths_ORS, file_paths_SLV, smallestLoadVolume_keys, 1, ylabel_volume,
                 title_smallestLoad, variant)
create_bar_chart(file_paths_GH, file_paths_ORS, file_paths_SLV, meanLoad_keys, 1,
                 ylabel_kgs,  title_meanLoad, variant)
create_bar_chart(file_paths_GH, file_paths_ORS, file_paths_SLV, meanLoadVolume_keys, 1,
                 ylabel_volume,  title_meanLoad, variant)
