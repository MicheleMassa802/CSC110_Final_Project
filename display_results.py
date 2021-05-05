"""CSC110 Fall 2020 Course Project: Data Visualization

Authors: Michele Massa, Nischal Nair, Nathan Zavys-Cox

Description: this module contains functions that conduct the necessary procedures
to take the results from our CO2 predictions, to visualize the generated data as
plotly graphs.

This file is copyright (c) 2020 Michele Massa, Nischal Nair and Nathan Zavys-Cox."""

from typing import Dict, List, Tuple
import plotly

#################################################################################################################
#################
# Plotting data #
#################
#################################################################################################################


def plot_wma_co2_emissions(country: str, coords_list: List[Tuple[int, float]]) -> None:
    """" Plot the given coordinates and future prediction coordinates
    according to the Weighted Moving Average model using plotly.

    >>> co2_values = [(2010, 170), (2011, 184.2), (2012, 192.1), (2013, 185.7), (2014, 201.4), (2015, 195),\
     (2016, 202.3), (2017, 208.7), (2018, 204.3), (2019, 205.4), (2020, 205.6), (2021, 205.3), (2022, 205.4)]
    >>> plot_wma_co2_emissions('Canada', co2_values)
    """

    # Dividing dataset graph from the WMA predicted values graph

    dataset_values_coords = coords_list[0: len(coords_list) - 5]
    wma_predicted_values_coords = coords_list[len(coords_list) - 6: len(coords_list)]

    # Transform data into valid plotly inputs

    dataset_x_coords = [coord[0] for coord in dataset_values_coords]
    dataset_y_coords = [coord[1] for coord in dataset_values_coords]

    wma_x_coords = [coord[0] for coord in wma_predicted_values_coords]
    wma_y_coords = [coord[1] for coord in wma_predicted_values_coords]

    # Create a blank figure
    fig = plotly.graph_objs.Figure()

    # Add the traces to the graph

    fig.add_trace(plotly.graph_objs.Scatter(
        x=wma_x_coords,
        y=wma_y_coords,
        name='WMA Future Values',
        line=dict(color='purple', width=3, dash='dot')
    ))

    fig.add_trace(plotly.graph_objs.Scatter(
        x=dataset_x_coords,
        y=dataset_y_coords,
        name='Dataset Values',
        line=dict(color='blue', width=3)
    ))

    fig.update_layout(title='Known and WMA predicted CO2 emissions for ' + country,
                      xaxis_title='Time (years)',
                      yaxis_title='CO2 emissions (tonnes)')

    # Display image
    fig.show()


def plot_rr_co2_emissions(country: str, coords_dict: Dict[str, List[Tuple[int, float]]]) -> None:
    """" Plot the gdp and population based related rates CO2 emission coordinates using plotly. First element
    of the tuple must be the population based coordinates.

    The dictionary input has either 2 or 3 items, those being:
        - A key to a corresponding value of a list of year to CO2 emissions coordinates from the original dataset.
        - A key to a corresponding value of a list of year to CO2 emissions coordinates predicted using the related
        rates algorithm based on another country's population (used as benchmark).
        - A key to a corresponding value of a list of year to CO2 emissions coordinates predicted using the related
        rates algorithm based on another country's GDP (used as benchmark).

    Preconditions:
        - len(coords_list[0]) == len(coords_list[1])
        - coords_list
    """
    # Create a blank figure
    fig = plotly.graph_objs.Figure()

    # Implementation when the benchmark country is the same for population and GDP
    if len(coords_dict) == 2:
        keys = list(coords_dict.keys())
        dataset_coords_list = coords_dict[keys[0]]
        rr_coords_list = coords_dict[keys[1]]

        # Transform data into valid plotly inputs
        x_dataset_coords = [coord[0] for coord in dataset_coords_list]  # same for both gdp and population based
        y_dataset_coords = [coord[1] for coord in dataset_coords_list]  # same for both gdp and population based

        x_rr_coords = [coord[0] for coord in rr_coords_list]
        y_rr_coords = [coord[1] for coord in rr_coords_list]

        # Add the traces to the graph

        # Population based prediction trace
        fig.add_trace(plotly.graph_objs.Scatter(
            x=x_rr_coords,
            y=y_rr_coords,
            name='Population/GDP Based Prediction ' + keys[1],
            line=dict(color='purple', width=3, dash='dot')
        ))

        # Base trace (dataset values)
        fig.add_trace(plotly.graph_objs.Scatter(
            x=x_dataset_coords,
            y=y_dataset_coords,
            name='Dataset Values',
            line=dict(color='black', width=4)
        ))

        fig.update_layout(title='GDP and population based related rates CO2 emissions ' + country,
                          xaxis_title='Time (years)',
                          yaxis_title='CO2 emissions (tonnes)')

        # Display image
        fig.show()

    # Implementation when the benchmark countries are different for population and GDP
    else:
        keys = list(coords_dict.keys())
        dataset_coords_list = coords_dict[keys[0]]
        rr_pop_coords_list = coords_dict[keys[1]]
        rr_gdp_coords_list = coords_dict[keys[2]]

        # Transform data into valid plotly inputs
        x_dataset_coords = [coord[0] for coord in dataset_coords_list]  # same for both gdp and population based
        y_dataset_coords = [coord[1] for coord in dataset_coords_list]  # same for both gdp and population based

        x_rr_pop_coords = [coord[0] for coord in rr_pop_coords_list]
        y_rr_pop_coords = [coord[1] for coord in rr_pop_coords_list]

        x_rr_gdp_coords = [coord[0] for coord in rr_gdp_coords_list]
        y_rr_gdp_coords = [coord[1] for coord in rr_gdp_coords_list]

        # Add the traces to the graph

        # Population based prediction trace
        fig.add_trace(plotly.graph_objs.Scatter(
            x=x_rr_pop_coords,
            y=y_rr_pop_coords,
            name='Population Based Prediction ' + keys[1],
            line=dict(color='purple', width=3, dash='dot')
        ))

        # GDP based prediction trace
        fig.add_trace(plotly.graph_objs.Scatter(
            x=x_rr_gdp_coords,
            y=y_rr_gdp_coords,
            name='GDP Based Prediction ' + keys[2],
            line=dict(color='green', width=3, dash='dot')
        ))

        # Base trace (dataset values)
        fig.add_trace(plotly.graph_objs.Scatter(
            x=x_dataset_coords,
            y=y_dataset_coords,
            name='Dataset Values',
            line=dict(color='black', width=4)
        ))

        fig.update_layout(title='GDP and population based related rates CO2 emissions ' + country,
                          xaxis_title='Time (years)',
                          yaxis_title='CO2 emissions (tonnes)')

        # Display image
        fig.show()


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'max-line-length': 120,
        'extra-imports': ['python_ta.contracts', 'plotly', 'typing'],
        'disable': ['R0914']
    })

    import python_ta.contracts

    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()

    import doctest

    doctest.testmod()
