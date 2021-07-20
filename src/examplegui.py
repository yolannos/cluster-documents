import PySimpleGUI as sg
from time import sleep

sg.theme('Dark Blue 3')

"""
    Demonstration of simple and multiple one_line_progress_meter's as well as the Progress Meter Element
    
    There are 4 demos
    1. Manually updated progress bar
    2. Custom progress bar built into your window, updated in a loop
    3. one_line_progress_meters, nested meters showing how 2 can be run at the same time.
    4. An "iterable" style progress meter - a wrapper for one_line_progress_meters
    
    If the software determined that a meter should be cancelled early, 
        calling OneLineProgresMeterCancel(key) will cancel the meter with the matching key
"""


"""
    The simple case is that you want to add a single meter to your code.  The one-line solution.
    This demo function shows 3 different one_line_progress_meter tests
        1. A horizontal with red and white bar colors
        2. A vertical bar with default colors
        3. A test showing 2 running at the same time 
"""


def demo_one_line_progress_meter():
    # Display a progress meter. Allow user to break out of loop using cancel button
    for i in range(10000):
        if not sg.one_line_progress_meter('My 1-line progress meter',
                                          i+1, 10000,
                                          'meter key',
                                          'MY MESSAGE1',
                                          'MY MESSAGE 2',
                                          orientation='h',
                                          no_titlebar=True,
                                          grab_anywhere=True,
                                          bar_color=('white', 'red')):
            print('Hit the break')
            break
    for i in range(10000):
        if not sg.one_line_progress_meter('My 1-line progress meter',
                                          i+1, 10000,
                                          'meter key',
                                          'MY MESSAGE1',
                                          'MY MESSAGE 2',
                                          orientation='v'):
            print('Hit the break')
            break

    layout = [
        [sg.Text('One-Line Progress Meter Demo', font=('Any 18'))],

        [sg.Text('Outer Loop Count', size=(15, 1), justification='r'),
         sg.Input(default_text='100', size=(5, 1), key='CountOuter'),
         sg.Text('Delay'), sg.Input(default_text='10', key='TimeOuter', size=(5, 1)), sg.Text('ms')],

        [sg.Text('Inner Loop Count', size=(15, 1), justification='r'),
         sg.Input(default_text='100', size=(5, 1), key='CountInner'),
         sg.Text('Delay'), sg.Input(default_text='10', key='TimeInner', size=(5, 1)), sg.Text('ms')],

        [sg.Button('Show', pad=((0, 0), 3), bind_return_key=True),
         sg.Text('me the meters!')]
    ]

    window = sg.Window('One-Line Progress Meter Demo', layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        if event == 'Show':
            max_outer = int(values['CountOuter'])
            max_inner = int(values['CountInner'])
            delay_inner = int(values['TimeInner'])
            delay_outer = int(values['TimeOuter'])
            for i in range(max_outer):
                if not sg.one_line_progress_meter('Outer Loop', i+1, max_outer, 'outer'):
                    break
                sleep(delay_outer/1000)
                for j in range(max_inner):
                    if not sg.one_line_progress_meter('Inner Loop', j+1, max_inner, 'inner'):
                        break
                    sleep(delay_inner/1000)
    window.close()

demo_one_line_progress_meter()