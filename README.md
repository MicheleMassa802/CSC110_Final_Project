# CSC110_Final_Project
Program through which we have researched and analyzed how the developmental stage of a country impacts their CO2 emissions, while also contrasting different methods to predict future CO2 emissions.

Instructions: in the console
1. Run main.py in the console.
2. Create a tkinter window by calling: ’window = tkinter.Tk()’
3. Start the Gui object using window as the master argument: ’Gui(window)’
This opens up our GUI.

Instructions: in the GUI
1. Enter the desired valid input country (the ones resulting from calling get all data()) inside the textfield. Some
example calls can be:
2. Clicking the ’GET INFO’ button can yield any of the following two cases, resulting in different text outputs in
the text box:
• Inputting ’Canada’ in the textfield and pressing the ’GET INFO’ button.
• Inputting ’China’ in the textfield and pressing the ’GET INFO’ button.
3. Clicking the ’PLOT WMA DATA’ button can yield the following case:
• Inputting ’United Kingdom’ in the textfield and pressing the ’PLOT WMA DATA’ button, resulting in a
WMA graph.
4. Clicking the ’PLOT RELATED RATES DATA’ button can yield any of the following 3 cases:
• Inputting ’Canada’ in the textfield and pressing the ’PLOT RELATED RATES DATA’ button results in
two prediction traces.
• Inputting ’United Kingdom’ in the textfield and pressing the ’PLOT RELATED RATES DATA’ button
results in one prediction trace.
• Inputting ’Sweden’ in the textfield and pressing ’PLOT RELATED RATES DATA’ button results in an
error message within the text block that tells you that the input country has no countries that it could
use as a benchmark.
5. Clicking the ’PLOT DATA’ button can yield any of the following 2 cases:
• Inputting ’Russia’ in the textfield and pressing the ’PLOT RECOMMENDED DATA’ button results in
the plotting of a graph that would result from the WMA (same functionality as pressing the ’PLOT WMA
DATA’ button in this case).
• Inputting ’India’ in the textfield and pressing the ’PLOT RECOMMENDED DATA’ button results in the
plotting of a graph that would result from the related rates method (same functionality as pressing the
’PLOT RELATED RATES DATA’ button in this case).
