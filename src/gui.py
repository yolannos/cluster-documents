import os
import sys
import utils.util as util
import model.model as cluster
import utils.extract_text as extract_text

import PySimpleGUIQt as sg
from time import sleep


def classification(foldername, filenames):
    # layout the form
    layout = [[sg.Text('A typical custom progress meter')],
              [sg.ProgressBar(1, orientation='h', auto_size_text= True, key='progress')],
              [sg.Cancel()]]

    # create the form`
    window = sg.Window('Classifying documents ...', layout, size=(400,50))
    progress_bar = window['progress']
    # loop that would normally do something useful

    for index, file in enumerate(filenames):
        # check to see if the cancel button was clicked and exit loop if clicked
        event, values = window.read(timeout=0)
        sleep(1)
        if event == 'Cancel' or event == None:
            break
        # call of the function to classifiy the documents
        in_path = os.path.join(foldername, file)
        out_path = os.path.join('output/')

        cluster = util.prediction(in_path)

        # create the directory if not already there
        os.makedirs(os.path.join(out_path,str(cluster[0])), exist_ok=True)
        # move to the document to the right directory
        os.rename(os.path.join(in_path), os.path.join(out_path,str(cluster[0]),file))

        progress_bar.update_bar(index+1, len(filenames))
    
    window.close()

def no_selection():
    layout = [[sg.Text('No folder selected!')],
               [sg.OK()]]
    window = sg.Window("Warning!", layout, size=(200, 50))
    while True:
        event, values = window.read()
        if event == 'OK' or event == sg.WIN_CLOSED:
            break
        
    window.close()

def make_window():

    # sg.theme('SystemDefaultForReal')

    layout = [
        [sg.Input(), sg.Button('FolderBrowse')],

        [sg.Text('Files')],
        [sg.Multiline(key='files', size=(60,30), autoscroll=True)],

        [sg.Button('Classify', auto_size_button=True), sg.Cancel()],    
    ]

    window = sg.Window('Document Classifier', layout, size=(400, 100))
    return window

def main():
    filenames = ''
    window = make_window()

    while True:
        event, values = window.read()
        
        if event == sg.WIN_CLOSED or event == 'Cancel':
            break

        if event == 'FolderBrowse':
            foldername = sg.PopupGetFolder('Select folder', no_window=True)
            if foldername: # `None` when clicked `Cancel` - so I skip it
                filenames = sorted([f for f in os.listdir(foldername) if f.endswith('.pdf')])
                # it use `key='files'` to `Multiline` widget
                window['files'].update("\n".join(filenames))
                # print(os.path(foldername))
        if event == 'Classify':
            if filenames:
                classification(foldername, filenames)
            else:
                no_selection()

    window.close()

# for presentation purpose
def restore():
    in_path = 'input/'

    for parent, _, filenames in os.walk('output/'):
        for fn in filenames:
            if fn.lower().endswith('.pdf'):
                os.rename(os.path.join(parent, fn), os.path.join(in_path, fn))

if __name__ == '__main__':
    # main()
    restore()