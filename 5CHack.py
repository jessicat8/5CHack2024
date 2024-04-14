"""
    5C Hackathon: Restaurant Inspection and Health Code Violation Data Visualization

    Authors: Jessica Tong, Diane Nguyen, Amal Diabor, Sid Eramil

    Date: 4/13/2024

    This program analyzes trends in health inspection scores and health code violations from a dataset of Environmental
    health inspections and violations in LA County restaurants between 07/01/2015 and 12/29/2017 (dataset: https://www.kaggle.com/datasets/meganrisdal/la-county-restaurant-inspections-and-violations/data.

    This program maps average inspection scores across cities, and plots the top cities with most violations.

"""

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np


def dict_sort(dic):
    """
    sorts dictionary by value (increasing)
    :param dic: dictionary
    :return: sorted dictionary
    """
    # Source: https://realpython.com/sort-python-dictionary/
    dic = dict(sorted(dic.items(), key=lambda item: item[1]))
    return dic

def parse_city_scores(filename):
    """
    parses dataset to create a dictionary of cities and their average inspection scores
    :param filename: (str) of csv data file
    :return: (dict) of cities and their average inspection scores
    """
    with open(filename, "r") as file:

        #creates nested list for each row in file
        file_list = []
        for line in file:
            file_list.append(line.split(","))
        # removes first line with header
        file_list = file_list[1:]

        # creates dictionary with city and list of scores
        dic = {}
        for elem in file_list:
            if elem[3] not in dic:
                dic[elem[3]]=[int(elem[16])]
            else:
                dic[elem[3]].append(int(elem[16]))

        # averages scores
        for city in dic:
            dic[city] = round((sum(dic[city]) / len(dic[city])), 2)

        return dict_sort(dic)

def parse_serial_cities(filename):
    """
    parses dataset to create a dictionary of restaurant serial #s and their city
    :param filename: (str) of csv data file
    :return: (dict) of restaurant serial #s and their city
    """
    with open(filename, "r") as file:

        #creates nested list for each row in file
        file_list = []
        for line in file:
            file_list.append(line.split(","))
        # removes first line with header
        file_list = file_list[1:]

        # creates dictionary with serial number and city
        dic = {}
        for elem in file_list:
            if elem[17] not in dic:
                dic[elem[17]]=elem[3]

        return dic

def parse_serial_violations(filename):
    """
    parses dataset to create a dictionary of restaurant serial #s and their # of violations
    :param filename: (str) of csv data file
    :return: (dict) of restaurant serial #s and their # of violations
    """
    with open(filename, "r") as file:
        # creates nested list for each row in file
        file_list = []
        for line in file:
            file_list.append(line.split(","))
        # removes first line with header
        file_list = file_list[1:]

        # creates dictionary with serial number and violation code
        dic = {}
        for elem in file_list:
            if elem[1][1:-1] not in dic:
                dic[elem[1][1:-1]] = [int(elem[2][3:5])]
            else:
                dic[elem[1][1:-1]].append(int(elem[2][3:5]))

        # number of violations
        for elem in dic:
            dic[elem] = len(dic[elem])

        return dic

def parse_violation_count(filename):
    """
    parses dataset to create a dictionary of health code and number of violations
    :param filename: (str) of csv data file
    :return: (dict) of health code and number of violations
    """
    with open(filename, "r") as file:
        # creates nested list for each row in file
        file_list = []
        for line in file:
            file_list.append(line.split(","))
        # removes first line with header
        file_list = file_list[1:]

        # creates dictionary with serial number and violation code
        dic = {}
        for elem in file_list:
            if elem[2][3:5] not in dic:
                dic[elem[2][3:5]] = 1
            else:
                dic[elem[2][3:5]] += 1

        # take only top ten
        top10dic = {}
        count = 0
        for key, value in dic.items():
            if count >= 10:
                break
            top10dic[key] = value
            count += 1


        return dict_sort(top10dic)

def city_violations(cdic,vdic):
    """
    combines two dictionaries to get a new dictionary with cities and their number of violations
    :param cdic: (dict) of serial #s and city
    :param vdic: (dict) of serial #s and # of violations
    :return: (dict) of cities and # of violations
    """
    dic = {}
    for elem in vdic.keys():
        if elem in cdic.keys():
            dic[cdic[elem]] = vdic[elem]

    return dict_sort(dic)

def top_violation_cities(dic):
    """
    creates a dictionary of top 6 cities with most violations
    :param dic: (dict) of cities and # of violations
    :return: a dictionary of top 6 cities with most violations
    """

    #list of (top 6) cities with most violations
    cities_list = ['RANCHO DOMINGUEZ','WEST LOS ANGELES','HOLLYWOOD', 'ARLETA','TERMINAL ISLAND','SEPULVEDA']

    # create a new dict with only the cities on the map
    new_dic = {}
    for city in dic.keys():
        if city in cities_list:
            new_dic[city] = dic[city]
    return new_dic

def map_cities(dic):
    """
    creates a dictionary of the cities on the map
    :param dic: (dict) of cities and average scores
    :return: dictionary with only cities displayed on the map
    """
    #list of cities on the map
    map_cities_list = ['LOS ANGELES','LONG BEACH','SANTA CLARITA', 'GLENDALE','LANCASTER','POMONA','TORRANCE','PASADENA','DOWNEY','MALIBU','COVINA','EL MONTE','BURBANK','SANTA MONICA','CARSON','COMPTON','LA MIRADA']

    # create a new dict with only the cities on the map
    new_dic = {}
    for city in dic.keys():
        if city in map_cities_list:
            new_dic[city] = dic[city]
    return new_dic


def city_violations_barplot(dic):
    """
    generates a bar graph of the top 6 cities with most violations
    :param dic: (dict) of cities and their # of violations
    :return: None
    """

    fig, ax = plt.subplots(figsize=(7, 7))
    bars = ax.barh(list(dic.keys()), list(dic.values()))
    #plt.rc('ytick',labelsize = 5)
    plt.title("Restaurant Health Code Violations by City")
    plt.xlabel("Number of Violations")
    #plt.ylabel("City", fontsize=12)
    plt.subplots_adjust(left=0.3)
    plt.xticks(fontsize=12)
    #plt.yticks(fontsize=12)

    #plt.bar_label(bars, padding=0.5)
    plt.show()

def plot_map_scores(dic):
    """
    plots the average scores of major cities on a map of LA county
    :param dic: (dict) of cities and their average ratings
    :return: None
    """
    # Load the image
    img = mpimg.imread("map.png")
    # Plot the image
    plt.imshow(img)

    # Define points to plot (coordinates of each city)
    points_x = [581,787,649,612,531,696,674,595,893,627,778,408,997,682,158,551,365]
    points_y = [1008,927,1065,800,1006,903,185,710,761,950,781,827,796,708,836,675,466]
    labels = dic.keys()
    scores = dic.values()

    # size of the point according to score
    sizes = []
    for score in scores:
        score = ((score-92.47)/3.21+0.1)*350
        sizes.append(score)
    print(sizes)

    # Colorbar
    # from https://stackoverflow.com/questions/45947971/overlay-scatter-plot-on-map-img
    tick_values = np.linspace(92.47, 95.68, 11)
    cbar = plt.colorbar()
    cbar.ax.set_yticklabels(["%d" % (v) for v in tick_values], fontsize=12)
    cbar.set_label('Average Restaurant Inspection Scores', fontsize=12)

    # Plot points on the image
    plt.scatter(points_x, points_y, sizes, c=scores)

    # Add labels to points
    for i, label in enumerate(labels):
        plt.annotate(label, (points_x[i], points_y[i]), textcoords="offset points", xytext=(0, 15), ha='center', fontsize=5)

    # show
    plt.show()


def main():
    # Map of Cities and Average Restaurant Health Inspection Scores
    score_dic = map_cities(parse_city_scores("inspections_cleaned.csv"))
    plot_map_scores(score_dic)

    # Bar Plot of Cities and Number of Health Code Violations
    vdic = parse_serial_violations("violations.csv")
    cdic = parse_serial_cities("inspections_cleaned.csv")
    dic = top_violation_cities(city_violations(cdic,vdic))
    city_violations_barplot(dic)


if __name__ == '__main__':
    main()
