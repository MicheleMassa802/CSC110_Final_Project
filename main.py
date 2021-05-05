"""CSC110 Fall 2020 Course Project: Manager

Authors: Michele Massa, Nischal Nair, Nathan Zavys-Cox

Description: this module contains the class that manages how all of our
program is connected, from data transformation to computations to visualizations.

This file is copyright (c) 2020 Michele Massa, Nischal Nair and Nathan Zavys-Cox."""

import tkinter
from read_data import get_all_data
from compute_results import co2_increase_rate, ma_period_cls, wma_prediction_cls, run_wma, run_related_rates, \
    determine_algorithm
from display_results import plot_wma_co2_emissions, plot_rr_co2_emissions
from read_scraped_data import output_disease_data, output_disease_data_condition

#################################################################################################################
#######
# GUI #     the country to object dict is global
#######
#################################################################################################################


class Gui:
    """ A class for the GUI implementation for this project.

    Instance Attributes:
        - self.instructions: str for providing instructions to the user.
        - self.instructions1: str for a second set of instructions.
        - self.data_button: button that calls run_data method.
        - self.plot_wma_button: button that calls run_wma_plot method.
        - self.plot_recommended_button: button that calls plot_data method.
        - self.plot_rates_button: button that calls run_related_rates_plot method.
        - self.reset_button: button that calls reset country method.
        - self.textfield: textfield for user to input the value for attribute self.country.
        - self.country: str representing the user's country of interest.
        - self.message: the text box where textual information is output.

    Instructions: in the console
         - 1. Create a tkinter window by calling:
            'window = tkinter.Tk()
         - 2. Start the Gui object using window as the master argument:
            'Gui(window)'
    This opens up our GUI.
    """

    def __init__(self, master: tkinter.Tk) -> None:
        """ Initialize the Graphical User Interface (GUI), including all the widgets (items on screen),
        and all the commands executed when button are pressed.
        """

        instructions = "Input one of the valid countries (case sensitive). Depending on the country's CO2 \n " \
                       "emissions, we'll give you information about air pollution influenced diseases that \n" \
                       "people in that country might be more exposed to as a result of air pollution."

        self.instructions = tkinter.Label(text=instructions, fg='black', font=('Helvetica', 11))
        self.instructions.grid(row=0, column=1)
        self.instructions1 = tkinter.Label(text='Press a button to get results', fg='black', font=('Helvetica', 11))
        self.instructions1.grid(row=2, column=1)

        self.data_button = tkinter.Button(text='GET INFO', width=24, command=self.run_data)
        self.data_button.grid(row=4, column=1)

        self.plot_wma_button = tkinter.Button(text='PLOT WMA DATA', width=24, command=self.run_wma_plot)
        self.plot_wma_button.grid(row=5, column=1)

        self.plot_recommended_button = tkinter.Button(text='PLOT RECOMMENDED DATA', width=24, command=self.plot_data)
        self.plot_recommended_button.grid(row=3, column=1)

        self.plot_rates_button = tkinter.Button(text='PLOT RELATED RATES DATA', width=24,
                                                command=self.run_related_rates_plot)
        self.plot_rates_button.grid(row=6, column=1)

        self.reset_button = tkinter.Button(text='RESET', width=24, command=self.reset_country)
        self.reset_button.grid(row=7, column=1)

        self.textfield = tkinter.Entry(width=25)
        self.textfield.grid(row=1, column=1)

        self.country = ''

        self.message = tkinter.Text(height=50, width=100)
        self.message.config(state='disabled')
        self.message.grid(row=8, column=1)

        master.mainloop()

    def run_data(self) -> None:
        """ Performs the needed calculations to determine what kind of message should be
         output to the user. The two options are:
            - Key facts about the 3 most common air pollution influenced diseases.
            - A message stating that the user's input country CO2 levels are not hazardous.

        Instructions: in the GUI
         - 1. This method is triggered when the 'GET INFO' button is pressed using a valid
            country, so input any of the countries available in the dictionary that results
            from calling 'get_all_data', and see how the two options mentioned above might be
            executed.
         - 2. The two cases that you can get as the user are (examples):
            - Inputting 'Canada' in the textfield and pressing the 'GET INFO' button.
            - Inputting 'China' in the textfield and pressing the 'GET INFO' button.
        """
        # Getting user input from textfield
        self.country = self.textfield.get()

        # Determine whether user should be made aware of diseases' key facts.
        condition = output_disease_data_condition(self.country)

        # Output (or don't the key facts)
        text = output_disease_data(condition)

        # Modifying the string to be returned
        # ACCUMULATOR: Keeps track of the modified inner lists.
        new_text_so_far = []

        for i in range(0, len(text)):
            for k in range(0, len(text[i])):
                # Takes out commas to avoid interference with next steps.
                new_str = text[i][k].replace(',', '')
                new_text_so_far.append(new_str)

        new_text = str(new_text_so_far).replace(',', ' \n ')
        new_text1 = new_text.replace('[', '')
        new_text2 = new_text1.replace(']', '')

        if condition is True:
            self.message.config(state='normal')
            self.message.insert('1.0', new_text2)
            self.message.config(state='disabled')
        else:
            self.message.config(state='normal')
            self.message.insert('1.0', text)
            self.message.config(state='disabled')

    def run_wma_plot(self) -> None:
        """ Performs the needed calculations to output CO2 emissions data through plotly.

        This includes:
            - A trace of current CO2 values graph of the form years to CO2 emissions.
            - A trace of predicted future CO2 values (WMA algorithm) of the form years to CO2 emissions.

        Instructions: in the GUI
         - 1. This method is triggered when the 'PLOT WMA DATA' button is pressed using a valid
            country, so input any of the countries available in the dictionary that results
            from calling 'get_all_data', and see the generated graph that due to the nature
            of the WMA, will start to average out the values as the program starts making
            predictions based on past predicted values.
         - 2. The only case that you can get as the user is (examples):
            - Inputting 'United Kingdom' in the textfield and pressing the 'PLOT WMA DATA' button,
            resulting in what the 'This includes description above highlights'.
        """
        data = get_all_data()

        self.country = self.textfield.get()

        # Calculate the ma_period to be used to estimate values using the WMA.
        ma_period = ma_period_cls({self.country: data[self.country]})

        # Use WMA to calculate future CO2 values.
        years_to_co2 = wma_prediction_cls(ma_period, {self.country: data[self.country]})

        # Plot the past and future year to CO2 values using plotly.
        plot_wma_co2_emissions(country=self.country, coords_list=years_to_co2)

    def run_related_rates_plot(self) -> None:
        """ Performs the needed calculations to output CO2 emissions data through plotly.

        This includes:
            - A trace of CO2 values graph of the user-chosen country of the form years to CO2 emissions,
            including predicted ones using similar rates algorithm (this can result in 1 or 2 prediction
            traces depending on the country).

        Instructions: in the GUI
         - 1. This method is triggered when the 'PLOT RELATED RATES DATA' button is pressed using a
            valid country, and for an input to be valid in this method, it must be one of the countries
            available in the dictionary that results from calling 'get_all_data', and it must have at
            least one similar GDP or population country. With this valid input, press the
            'PLOT RELATED RATES DATA' button and test the following cases.
         - 2. The three cases that you can get as the user are (examples):
            - Inputting 'Canada' in the textfield and pressing the 'PLOT RELATED RATES DATA' button results
            in two prediction traces.
            - Inputting 'United Kingdom' in the textfield and pressing the 'PLOT RELATED RATES DATA' button
            results in one prediction trace.
            - Inputting 'Sweden' in the textfield and pressing 'PLOT RELATED RATES DATA' button results in an
            error message within the text block that tells you that the input country has no countries that it
            could use as a benchmark.
        """
        self.country = self.textfield.get()

        # Calculate the coordinates dictionary that includes past values, and GDP based and population based future
        # CO2 value predictions.
        coord_dict = run_related_rates(self.country)

        if coord_dict == {}:
            self.message.config(state='normal')
            self.message.insert('1.0', 'The input country is invalid due to not having any possible comparisons.')
            self.message.config(state='disabled')
        else:
            # Plot the past and future year to CO2 values using plotly.
            plot_rr_co2_emissions(country=self.country, coords_dict=coord_dict)

    def plot_data(self) -> None:
        """ Evaluates which method will be better to predict the future CO2 values and output the corresponding
        graph.

        Instructions: in the GUI
         - 1. This method is triggered when the 'PLOT RECOMMENDED DATA' button is pressed using a
            valid country, so it must be one of the countries available in the dictionary that results
            from calling 'get_all_data'. With this valid input, press the 'PLOT RECOMMENDED DATA' button and
            test the following cases.
         - 2. The two cases that you can get as the user are (examples):
            - Inputting 'Russia' in the textfield and pressing the 'PLOT RECOMMENDED DATA' button results
            in the plotting of a graph that would result from the WMA (same functionality as pressing the
             'PLOT WMA DATA' button in this case).
            - Inputting 'India' in the textfield and pressing the 'PLOT RECOMMENDED DATA' button
            results in the plotting of a graph that would result from the related rates method (same
            functionality as pressing the 'PLOT RELATED RATES DATA' button in this case).
        """

        data = get_all_data()

        self.country = self.textfield.get()

        # Determine which method to use:

        n = ma_period_cls({self.country: data[self.country]})
        past_increase_rate = co2_increase_rate(self.country, n)

        if determine_algorithm(past_increase_rate) == 'RR':
            future_co2 = run_related_rates(self.country)
            self.run_related_rates_plot()
        else:
            future_co2 = run_wma(self.country)
            self.run_wma_plot()

    def reset_country(self) -> None:
        """ Reset the textfield so that the user can input the next country. """
        self.textfield.delete(0, 'end')  # deletes current text
        self.country = self.textfield.get()  # sets current text to ''

        self.message.config(state='normal')
        self.message.delete('1.0', 'end')  # deletes current text displayed
        self.message.config(state='disabled')

# Testing for this module is basically done by using the GUI as explained in the method docstrings, nonetheless,
# all procedures implemented in the GUI's methods have been tested already in their respective functions.


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'max-line-length': 120,
        'extra-imports': ['python_ta.contracts', 'tkinter', 'read_data', 'compute_results', 'read_scraped_data',
                          'display_results'],
        'disable': ['E9973', 'R0902', 'C0200', 'E9994', 'W0612']
    })

    import python_ta.contracts

    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()
