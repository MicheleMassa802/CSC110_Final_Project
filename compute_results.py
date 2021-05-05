"""CSC110 Fall 2020 Course Project: Computational Analysis

Authors: Michele Massa, Nischal Nair, Nathan Zavys-Cox

Description: this module contains functions that conduct the two different algorithms
to predict future levels of CO2 emissions for a given country using the Weighted Moving
Average and Related Rates algorithms.

This file is copyright (c) 2020 Michele Massa, Nischal Nair and Nathan Zavys-Cox."""

import math  # used for doctests
from typing import List, Dict, Tuple
from read_data import get_all_data, Country


#################################################################################
##############
# WMA Method #
##############
#################################################################################


#################################################################################
# Calculating the best n to predict future values (period our averages will be based on)
#################################################################################


def ma_period_cls(country_dict: Dict[str, Country]) -> int:
    """ Figure out the ideal length of the moving average period that will be used
    to predict the future CO2 values of the user-chosen country, by comparing their
    mean value deviation (average error when compared to the CSV actual values).

    >>> country_obj = Country(name = 'Canada', code= 'CAN', population= 35000000,\
     gdp_yearly = {2015: 5.346, 2016: 5.350, 2017: 5.247, 2018: 5.346, 2019: 5.350, 2020: 5.247}, \
     co2_yearly = {2015: 1020.50, 2016: 1067.50, 2017: 1004.75, 2018: 1020.00, 2019: 1040.0, 2020: 1018.0})
    >>> result = ma_period_cls({country_obj.name: country_obj})
    >>> result == 3
    True
    """

    country_stats = country_dict[list(country_dict.keys())[0]]
    time_period = len(country_stats.co2_yearly)
    n_upper_bound = min(time_period, 9)  # beyond 9, data is no longer too impactful

    possible_n = [n for n in range(0, time_period) if 1 < n < n_upper_bound]

    # Transform object co2 info into list of tuples
    years = list(country_stats.co2_yearly.keys())
    co2_values = [country_stats.co2_yearly[year] for year in years]
    value_list = [(years[i], co2_values[i]) for i in range(0, len(years))]

    # ACCUMULATOR: keeps track of our current moving_average and possible_n. It is a dict
    # with key possible_n and corresponding value list
    n_to_moving_average = {}

    # Generate a dict mapping n to its moving averages
    for n in possible_n:
        n_to_moving_average[n] = w_average_n_values_cls(n, value_list)

    # ACCUMULATOR: keeps track of the tuple of mad values to their corresponding n.
    mad_n_so_far = []

    # Generate mad to n tuples
    for n_value in n_to_moving_average:
        mad_n_so_far.append(mean_absolute_deviation_cls(n_value, value_list, n_to_moving_average[n_value]))

    possible_n_values = [item[0] for item in mad_n_so_far]
    lowest_error_average = min(possible_n_values)
    final_n = [item[1] for item in mad_n_so_far if item[0] == lowest_error_average]

    return final_n[0]


def w_average_n_values_cls(n: int, value_list: List[Tuple[int, float]]) -> List[Tuple[int, float]]:  # helper function
    """ Return averages of years based on the value n and the following weight distribution:
    - most recent item * 0.n
    - second most recent item * 0.n - 0.1
    - and so on until 0.1.

    Preconditions:
        - 1 < n <= 9
        - len(value_list) > 2

    As pointed in at in the preconditions, n has to be higher than 1, so that we are not just simply
    calculating the slope, and less than or equal to n, as that is the point where we have decided
    data is no longer too impactful.

    >>> year_to_co2 = [(2010, 170), (2011, 184.2), (2012, 192.1), (2013, 185.7),\
    (2014, 201.4), (2015, 195), (2016, 202.3), (2017, 208.7)]
    >>> result = w_average_n_values_cls(3, year_to_co2)
    >>> result[3][0] == 2016
    True
    >>> math.isclose(a=result[1][1], b=187.5, rel_tol=.1)
    True
    """

    # ACCUMULATOR: keeps track of of the year and moving averages according to n.
    year_to_ma_co2_so_far = []  # list of tuples

    for i in range(0, len(value_list) - n):
        current_years = value_list[i: i + n]
        current_co2_values = [value[1] for value in current_years]

        # ACCUMULATOR: keeps track of the current weighted co2 values.
        current_weighted_co2_values = []

        user_n = 0.1  # weight for the least impactful value
        k = 0  # iteration variable
        total_weight = 0  # keeps track of the total weight of a period.

        while (round(user_n * 10)) < n + 1:
            current_weighted_co2_values.append(current_co2_values[k] * user_n)
            total_weight = total_weight + user_n
            user_n = user_n + 0.1
            k = k + 1

        year_to_ma_co2_so_far.append((value_list[i][0] + n, sum(current_weighted_co2_values) / total_weight))

    return year_to_ma_co2_so_far


def mean_absolute_deviation_cls(n: int, value_list: List[Tuple[int, float]],
                                ma_values: List[Tuple[int, float]]) -> Tuple[float, int]:  # helper function
    """ Return the mean absolute deviation. That is, the average of the differences between
    the ma_values that result from calling average_n_values on n and value_list (referring
    to CO2 emissions) and the values from the country_dictionary. This
    is used to decide which n value more appropriate in the function ma_period, as the smaller the error average, the
    better the n value is to predict the future values.

    Preconditions:
        - len(value_list) == len(ma_values) + n

    >>> year_to_co2 = [(2010, 170), (2011, 184.2), (2012, 192.1), (2013, 185.7),\
    (2014, 201.4), (2015, 195), (2016, 202.3), (2017, 208.7)]
    >>> ma_co2_values = [(2013, 185.8), (2014, 187.5), (2015, 194.6), (2016, 195.6),\
    (2017, 199.7)]
    >>> result = mean_absolute_deviation_cls(3, year_to_co2, ma_co2_values)
    >>> math.isclose(a=result[0], b=6.02, rel_tol=.1)
    True
    """
    # ACCUMULATOR: keeps track of the differences between the value_list and ma_values values (errors of forecast).
    differences_so_far = []

    for i in range(0, len(ma_values)):
        differences_so_far.append(abs(value_list[i + n][1] - ma_values[i][1]))

    mad = sum(differences_so_far) / len(ma_values)  # mad: Mean Absolute Deviation

    return (mad, n)


#################################################################################
# Applying the Weighted Moving Average to predict future values
#################################################################################


def wma_prediction_cls(n: int, country_dict: Dict[str, Country]) -> List[Tuple[int, float]]:
    """ Return the prediction for the following 5 years based on the ma period provided (n), in the form of
    a list of floats, as mentioned in the report, the WMA method works best for countries with fluctuating
    CO2 values, if a country's CO2 value trend is only incresing, the WMA will fail to reliably predict future
    CO2 emission values.

    >>> country_obj = Country(name = 'Canada', code= 'CAN', population= 35000000,\
     gdp_yearly = {2010: 5.246, 2011: 5.350, 2012: 5.247, 2013: 5.346, 2014: 5.350, 2015: 5.346, 2016: 5.350,\
      2017: 5.247},\
     co2_yearly = {2010: 170, 2011: 184.2, 2012: 192.1, 2013: 185.7, 2014: 201.4, 2015: 195, 2016: 202.3, \
     2017: 208.7})
    >>> result = wma_prediction_cls(3, {country_obj.name: country_obj})
    >>> math.isclose(a=result[-1][1], b=205.4, rel_tol=.1)
    True
    """

    country = list(country_dict.keys())[0]
    country_stats = country_dict[country]

    # Creating value list in form of tuples of int to float (for co2 emissions)
    years = list(country_stats.co2_yearly.keys())
    co2_values = [country_stats.co2_yearly[year] for year in years]
    value_list = [(years[i], co2_values[i]) for i in range(0, len(years))]

    # Slice value list such that only the needed values are present.
    new_value_list = value_list[-n: len(value_list)]

    # ACCUMULATOR: keeps track of of the year and moving averages according to n.
    year_to_ma_co2_so_far = value_list.copy()  # list of tuples

    i = 0  # iteration variable

    while len(year_to_ma_co2_so_far) <= len(value_list) + 4:

        # ACCUMULATOR: keeps track of the current weighted co2 values.
        current_weighted_co2_values = []

        user_n = 0.1  # weight for the least impactful value
        j = 0  # iteration variable
        total_weight = 0  # keeps track of the total weight of a period.

        while (user_n * 10) < n + 1:
            current_weighted_co2_values.append(new_value_list[j][1] * user_n)
            total_weight = total_weight + user_n
            user_n = user_n + 0.1
            j = j + 1

        current_weighted_average = sum(current_weighted_co2_values) / total_weight
        year_to_ma_co2_so_far.append((new_value_list[-1][0] + 1, current_weighted_average))
        new_value_list.append((new_value_list[-1][0] + 1, current_weighted_average))
        i = i + 1

        # Slice value list such that only the needed values are present.
        new_value_list = new_value_list[-n: len(new_value_list)]

    return year_to_ma_co2_so_far


def run_wma(country: str) -> List[Tuple[int, float]]:
    """ Performs the steps needed to take a country str input and return its CO2 values, including the predicted ones,
    as a list of tuples of the form (year, CO2 value), using the Weighted Moving Average method.

    >>> result = run_wma('Canada')
    >>> prediction = result[-1][1]
    >>> math.isclose(a=prediction, b=569.4, rel_tol=.1)
    True
    >>> result2 = run_wma('China')
    >>> prediction2 = result2[-5][1]
    >>> math.isclose(a=prediction2, b=9793.9, rel_tol=.1)
    True
    """

    data = get_all_data()

    # Calculate the ma_period to be used to estimate values using the WMA.
    ma_period = ma_period_cls({country: data[country]})

    # Use WMA to calculate future CO2 values.
    years_to_co2 = wma_prediction_cls(ma_period, {country: data[country]})

    return years_to_co2


#################################################################################
########################
# Related Rates Method #
########################
#################################################################################

#################################################################################
# Helper functions designed to aid the filtration process
#################################################################################


def analysing_input_country(country: str) -> list:
    """ Returns a list containing data extracted from the country's associated object
    within DATA.

    Preconditions
      - country != ''
      - country in DATA

    >>> result = analysing_input_country('Canada')
    >>> result[0] == 31100000
    True
    >>> result[5] == [2017, 2018, 2019, 2020, 2021]
    True
    """

    data = get_all_data()

    # extracting the corresponding Country object
    required_object = data[country]

    # using . methods to identify it's population
    input_population = required_object.population

    # identifying the latest year for which the Country object has GDP and CO2 values (2017)
    latest_year = list(required_object.gdp_yearly.keys())[-1]

    # identifying the GDP per capita of the country as of the latest year
    latest_gdp = required_object.gdp_yearly[latest_year]

    # identifying the CO2 emissions of the country as of the latest year
    latest_co2_level = required_object.co2_yearly[latest_year]

    # identifying the penultimate value of GDP per capita
    penultimate_gdp = required_object.gdp_yearly[latest_year - 1]

    # calculating the change in GDP per capita as a signal of economic trends
    gdp_growth_rate = calc_growth_rate(penultimate_gdp, latest_gdp)

    # creating a list of years that the program will be predicting CO2 emissions for (2018-21)
    prediction_years = [latest_year + n for n in range(0, 5)]

    return [input_population,
            latest_year,
            latest_gdp,
            latest_co2_level,
            gdp_growth_rate,
            prediction_years]


def calc_growth_rate(value1: float, value2: float) -> float:
    """Returns the year-on-year growth rate of two values as a float

    Preconditions
      - value1 > 0
      - value2 > 0

    >>> calc_growth_rate(1.0, 1.15)
    1.15
    """

    return value2 / value1


#################################################################################
# Identification and filtration of possible candidate comparison countries.
#################################################################################


def find_possible_comparisons(country: str) -> Dict[str, list]:
    """Returns a mapping of candidate countries to the year in which they were
    matched and the GDP per capita level that year.

    Preconditions
      - country != ''
      - country in DATA

    >>> result = find_possible_comparisons('India')
    >>> result['China'] ==  [2006, 6411.0425444815]
    True
    >>> find_possible_comparisons('United States')
    {}
    """

    data = get_all_data()

    # Analysing input country and identifying its population
    input_analysis = analysing_input_country(country)
    latest_gdp = input_analysis[2]

    # ACCUMULATOR: a dict that contains countries who at some point between
    # 1991 and 2012 had a similar GDP per capita level as the latest_gdp.
    possible_comparisons = {}

    # To ensure that possible comparisons doesn't include the input country,
    # it is removed from the dataset, it will be re-added after the for loop.
    country_object = data.pop(country)

    for candidate in data:
        for year in data[candidate].gdp_yearly:
            # The GDP per capita of a possible comparison must be close to the latest_GDP, and the
            # year must be between 1991 and 2012 inclusive because we need at least 4 years of CO2
            # levels to compute upon
            if abs(data[candidate].gdp_yearly[year] - latest_gdp) < 100 \
                    and 1991 <= year <= 2012 \
                    and candidate not in possible_comparisons:
                possible_comparisons[candidate] = [year, data[candidate].gdp_yearly[year]]

    # Adding the input country back into the dataset
    data[country] = country_object

    return possible_comparisons


def population_filter(country: str, possible_comparisons: Dict[str, list]) \
        -> Tuple[str, int]:
    """Returns the name of a country identified as the closest match in terms of
    population and the year in which it had a similar GDP per capita level.

    Preconditions
      - country in DATA
      - possible_comparisons != {}

    >>> candidates = find_possible_comparisons('India')
    >>> population_filter('India', candidates)
    ('China', 2006)
    """

    data = get_all_data()

    # Analysing input country and identifying its population
    input_analysis = analysing_input_country(country)
    input_population = input_analysis[0]

    # Calculating and storing the values for the absolute differences in population
    population_gaps = [abs(data[candidate].population - input_population) for candidate in
                       possible_comparisons]

    # Identiyfing the country with the smallest absolute difference in population
    smallest_difference = min(population_gaps)
    identified_country = [candidate for candidate in possible_comparisons
                          if (abs(data[candidate].population - input_population))
                          == smallest_difference][0]

    identified_year = possible_comparisons[identified_country][0]

    return (identified_country, identified_year)


def growth_rate_filter(country: str, possible_comparisons: dict) -> Tuple[str, int]:
    """Returns an identified country who has the closest GDP per capita
    growth rate to the input country's GDP per capita growth rate

    Preconditions
      - country in DATA
      - possible_comparisons != {}

    >>> candidates = find_possible_comparisons('India')
    >>> growth_rate_filter('India', candidates)
    ('Sri Lanka', 2005)
    """

    data = get_all_data()

    # Analysing input country and identifying its GDP per capita growth rate
    input_analysis = analysing_input_country(country)
    input_growth_rate = input_analysis[4]

    # ACCUMULATOR: stores the candidate mapped to its growth rate from the
    # identified year and the year before that.
    candidate_growth_rates = {}
    for candidate in possible_comparisons:
        year = possible_comparisons[candidate][0]
        candidate_growth_rates[candidate] = \
            calc_growth_rate(data[candidate].gdp_yearly[year - 1],
                             data[candidate].gdp_yearly[year])

    # Identifying the country with the lowest absolute difference in growth rate
    lowest_growth_rate_delta = min(abs(input_growth_rate - candidate_growth_rates[candidate])
                                   for candidate in
                                   candidate_growth_rates)

    identified_country = [candidate for candidate in candidate_growth_rates
                          if abs(input_growth_rate - candidate_growth_rates[candidate])
                          == lowest_growth_rate_delta][0]

    identified_year = possible_comparisons[identified_country][0]

    return (identified_country, identified_year)


#################################################################################
# Analysis of chosen comparisons and the prediction of future CO2 Levels
# for the input_country
#################################################################################


def comparison_country_analysis(candidate_info: Tuple[str, int]) -> List[float]:
    """Returns a list of the year-on-year growth rate of CO2 emissions of the identified candidate
     country starting from the matched year

     Preconditions
       - candidate_info != ()
       - 1991 <= candidate_info[1] <= 2012
       - candidate_info[0] in DATA

    >>> comparison_country_analysis(('China', 2006))
    [1.0758892691880853, 1.0748262770012413, 1.0520151841291427, 1.0955985206470857]
     """

    data = get_all_data()

    # Looking up the country object within DATA and identifying the matched year
    candidate_country = data[candidate_info[0]]
    candidate_year = candidate_info[1]

    # Calculating the next 4 years after the identified year
    comparative_years = [candidate_year + n for n in range(0, 5)]

    # ACCUMULATOR: stores the CO2 emission level for each year in comparative_years
    co2_levels = []

    for year in comparative_years:
        co2_levels.append(candidate_country.co2_yearly[year])

    # ACCUMULATOR: stores the year-on-year growth rate for CO2 emission levels in co2_levels
    # initialised to a list of 4 values to allow for index assignments
    growth_rates = [0, 0, 0, 0]

    for i in range(0, 4):
        growth_rates[i] = calc_growth_rate(co2_levels[i], co2_levels[i + 1])

    return growth_rates


def predict_co2_levels(country: str, growth_rates: List[float]) -> List[tuple]:
    """Returns the list of tuples containing the future years of an input country
    and their predicted CO2 emission level

    Preconditions
      - country in DATA
      - growth_rates != []

    >>> growth_rate_list = comparison_country_analysis(('China', 2006))
    >>> result = predict_co2_levels('India', growth_rate_list)
    >>> result[3][0] == 2020
    True
    >>> result[3][1] == 2988.9935011283746
    True
    """

    # Analysing input country and identifying its latest CO2 level and the years to predict
    input_analysis = analysing_input_country(country)
    latest_co2_level = input_analysis[3]
    predictive_years = input_analysis[5]

    # ACCUMULATOR: Initialised to a list with the latest CO2 level at index 0 and 4 0s in
    # indexes 1-4 to allow for ease of index assignments
    predicted_co2_levels = [latest_co2_level, 0, 0, 0, 0]

    for i in range(1, 5):
        predicted_co2_levels[i] = predicted_co2_levels[i - 1] * growth_rates[i - 1]

    # List of tuples where each tuple is of the form (year, predicted CO2 emission level
    x_y_values = [(predictive_years[i], predicted_co2_levels[i]) for i in range(0, 5)]

    return x_y_values


#################################################################################
# Complete data analysis and prediction for a given input country
#################################################################################


def run_related_rates(country: str) -> Dict[str, List[Tuple[int, float]]]:
    """ Returns a dictionary which maps identified candidate countries to a list of tuples
    which contain predicted values of CO2 emissions over a set of 4 years.

    Preconditions
      - country in DATA

    >>> result = run_related_rates('Russia')
    >>> 'Greece' in result
    True
    >>> result['Greece'][2] == (2019, 1679.4933661416997)
    True
    """

    data = get_all_data()

    # Finding possible comparisons for the input country
    comparisons = find_possible_comparisons(country)

    # Early raise of exception if the user fails the preconditions of choosing a valid input country
    if comparisons == {}:
        return comparisons

    # Identifying two countries and their relevant information
    candidate_a_info = population_filter(country, comparisons)
    candidate_b_info = growth_rate_filter(country, comparisons)
    candidate_a = candidate_a_info[0]
    candidate_b = candidate_b_info[0]

    # Calculating the growth rates of CO2 for the two countries
    growth_a = comparison_country_analysis(candidate_a_info)
    growth_b = comparison_country_analysis(candidate_b_info)

    # Predicting the future CO2 levels of the input country using the growth rates
    prediction_a = predict_co2_levels(country, growth_a)
    prediction_b = predict_co2_levels(country, growth_b)

    # Accessing past data to visualize the user-chosen country's past 5 co2 values (2013-2017)
    all_co2_values = data[country].co2_yearly
    years = list(all_co2_values.keys())
    co2_values = [all_co2_values[year] for year in years]
    all_co2_values_list = [(years[i], co2_values[i]) for i in range(0, len(years))]
    previous_co2_to_show = all_co2_values_list[-5: len(all_co2_values_list)]

    # To distinguish between cases where there are two identified countries and cases where there is only one

    return {'dataset': previous_co2_to_show, candidate_a: prediction_a, candidate_b: prediction_b}


#################################################################################
####################
# Algorithm to use #
####################
#################################################################################


def co2_increase_rate(country: str, n: int) -> List[float]:
    """ Determine how CO2 emission values behave before performing the prediction algorithms (from up to n years
    before the last value in the country's CO2 value. This returned list is of the length of n.

    >>> result = co2_increase_rate('Canada', 2)
    >>> math.isclose(a=result[0], b=-12.6885, rel_tol=.1)
    True
    >>> math.isclose(a=result[1], b=7.0705, rel_tol=.1)
    True
    """

    data = get_all_data()

    country_stats = data[country]

    # Transform object co2 info into list of tuples
    years = list(country_stats.co2_yearly.keys())
    co2_values = [country_stats.co2_yearly[year] for year in years]
    value_list = [co2_values[i] for i in range(0, len(years))]

    # Slice list into the needed section
    value_list_len = len(value_list)
    usable_list = value_list[value_list_len - n - 1: value_list_len]

    # Calculate rate of change
    # ACCUMULATOR: keeps track of the rates of change between the values in usable_list
    roc_so_far = []

    for i in range(0, len(usable_list) - 1):
        roc_so_far.append(usable_list[i + 1] - usable_list[i])

    return roc_so_far


def determine_algorithm(roc_so_far: List[float]) -> str:
    """ Determine which algorithm should be used based on the past rates of change:
        - A high rate of change means that the WMA will not be accurate, as it works best with fluctuating values.
        - A low rate of change means that the WMA will be better and it is based around averaging past values.
    """

    average_roc = sum(roc_so_far) / len(roc_so_far)

    if abs(average_roc) >= 20:
        return 'RR'  # for Related Rates

    return 'WMA'  # for Weighted Moving Average


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'max-line-length': 120,
        'extra-imports': ['python_ta.contracts', 'read_data', 'typing', 'math'],
        'disable': ['C0200', 'R0914', 'W0611', 'E9988', 'E9969']
    })

    import python_ta.contracts

    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()

    import doctest

    doctest.testmod()
