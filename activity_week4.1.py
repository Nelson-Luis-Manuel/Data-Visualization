#!/usr/bin/env python
# coding: utf-8

# In[2]:


"""
Project for Week 4 of "Python Data Visualization".
Unify data via common country codes.

Be sure to read the project description page for further information
about the expected behavior of the program.
"""

import csv
import math
import pygal

def read_csv_as_nested_dict(filename, keyfield, separator, quote):
    """
    Inputs:
      filename  - name of CSV file
      keyfield  - field to use as key for rows
      separator - character that separates fields
      quote     - character used to optionally quote fields
    Output:
      Returns a dictionary of dictionaries where the outer dictionary
      maps the value in the key_field to the corresponding row in the
      CSV file.  The inner dictionaries map the field names to the
      field values for that row.
    """
    table = {}
    with open(filename, "rt", newline='') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=separator, quotechar=quote)
        for row in csv_reader:
            table[row[keyfield]] = row
    return table


def build_country_code_converter(codeinfo):


    dat = read_csv_as_nested_dict(codeinfo['codefile'],codeinfo['plot_codes'],codeinfo['separator'],codeinfo['quote'])

    table = {}

    for dit in dat:
        table[dit] = dat[dit][codeinfo['data_codes']]
        #print(dat[dit]['Code2'])
    return table



def reconcile_countries_by_code(codeinfo, plot_countries, gdp_countries):

    table = {}

    no_appear = set()

    # for key in plot_countries:
    #     table[key] = None

    for key,val in plot_countries.items():

        for key2,val2 in gdp_countries.items():

            if val == val2['Country Name']:
                table[key] = val2['Country Code']

    if len(plot_countries) == len(table):
        no_appear = set()
    else:
        for key in plot_countries:
            if not key in table:
                no_appear.add(key)
    return table, no_appear


# this function still has some bugs:

def build_map_dict_by_code(gdpinfo, codeinfo, plot_countries, year):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      codeinfo       - A country code information dictionary
      plot_countries - Dictionary mapping plot library country codes to country names
      year           - String year for which to create GDP mapping
    Output:
      A tuple containing a dictionary and two sets.  The dictionary
      maps country codes from plot_countries to the log (base 10) of
      the GDP value for that country in the specified year.  The first
      set contains the country codes from plot_countries that were not
      found in the GDP data file.  The second set contains the country
      codes from plot_countries that were found in the GDP data file, but
      have no GDP data for the specified year.
    """
    
    country_codes = {}
    copy_plot_countries = copy.deepcopy(plot_countries)
    no_value_countries = set()
    
    code_reader = read_csv_file(codeinfo.get("codefile"), codeinfo.get("separator"),
                                                          codeinfo.get("quote"))
    
    plot_code = code_reader[0].index(codeinfo.get("plot_codes"))
    data_code = code_reader[0].index(codeinfo.get("data_codes"))

    with open(gdpinfo.get("gdpfile"), 'r') as csvfile:
        gdp_reader = csv.DictReader(csvfile, delimiter=gdpinfo.get("separator"), 
                                                       quotechar=gdpinfo.get("quote"))
        
        for data in gdp_reader:
            for code in code_reader[1:]:
                if data[gdpinfo.get("country_code")].lower() == code[data_code].lower():
                    plt_code = [plot_c for plot_c in copy_plot_countries                                                   if code[plot_code].lower() == plot_c.lower()]
                    if not len(plt_code) == 0:
                        try:
                            country_codes[''.join(plt_code)] = math.log10(float(data.get(year)))
                        except ValueError:
                            no_value_countries.add(''.join(plt_code))
                        del copy_plot_countries[''.join(plt_code)]
                        
    return () + (country_codes, set(copy_plot_countries.keys()), no_value_countries, )

##TEST
#gdpinfo = {'country_code': 'CC', 'gdpfile': 'gdptable3.csv', 'quote': "'",
#           'separator': ';', 'country_name': 'ID', 'min_year': 20010, 'max_year': 20017}
#codeinfo = {'separator': ',', 'plot_codes': 'Code4', 'data_codes': 'Code3', 'quote': "'", 
#            'codefile': 'code1.csv'}
#plot_countries =  {'C3': 'c3', 'C2': 'c2', 'C1': 'c1'}
#if build_map_dict_by_code(gdpinfo, codeinfo, plot_countries, '20016') == \
#      ({'C3': 10.780708577050003, 'C2': 9.301029995663981, 'C1': 9.301029995663981}, set(), set()):
#    print("True")
#else:
#    print("False")

