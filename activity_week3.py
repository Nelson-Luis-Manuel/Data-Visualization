#!/usr/bin/env python
# coding: utf-8

# In[5]:


"""
Project for Week 3 of "Python Data Visualization".
Unify data via common country name.

Be sure to read the project description page for further information
about the expected behavior of the program.
"""

import csv
import math
import pygal

    

def reconcile_countries_by_name(plot_countries, gdp_countries):
    "returns dictionary that has countryId and countryName touples which are not present in the gdp_countries"""
    #initialising 
    dic = {}
    lis = []
    #iterating values
    for keys in plot_countries:
        for key in gdp_countries:
            if plot_countries[keys] == key:
                dic[keys] = key
    for keys in plot_countries:
        if keys not in dic.keys():
            lis.append(keys)
    return dic, set(lis)

def build_map_dict_by_name(gdpinfo, plot_countries, year):
    """building all the values"""
    dic = {}
    code = set()
    values = set()
    fileinput = {}
    with open(gdpinfo["gdpfile"], newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=gdpinfo["separator"],quotechar=gdpinfo["quote"])
        for row in reader:
            fileinput[row[gdpinfo["country_name"]]] = row

    for keys in plot_countries:
        if plot_countries[keys] in fileinput:
            if year in fileinput[plot_countries[keys]]:
                if fileinput[plot_countries[keys]][year] != '':
                    dic[keys] = math.log10(float(fileinput[plot_countries[keys]][year]))
                else:
                    values.add(keys)
        else:
            code.add(keys)		
    return dic, code, values

def render_world_map(gdpinfo, plot_countries, year, map_file):
    """rendering map"""
    dic, code, values = build_map_dict_by_name(gdpinfo, plot_countries, year)
    chart = pygal.maps.world.World()
    chart.title = "GDP datas {}".format(year)
    chart.add('GDP for {}'.format(year), dic)
    chart.add('Missing from World Bank Data', code)
    chart.add('No GDP data', values)
    chart.render_in_browser()

