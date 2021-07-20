import os
import sys
import utils.util as util
import model.model as cluster
import utils.extract_text as extract_text

import PySimpleGUIQt as sg
from time import sleep


def classification(foldername, filenames):
    # layout the form
    layout = [[sg.Text('Processing ... ', key='-IN-')],
              [sg.ProgressBar(1, orientation='h', auto_size_text= True, key='+PROGRESS+')],
              [sg.Cancel()]]

    # create the form`
    window = sg.Window('Classifying documents ...', layout, size=(400,50))
    texte = window['-IN-']
    progress_bar = window['+PROGRESS+']
    # loop that would normally do something useful
    try:

        for index, file in enumerate(filenames):
            # check to see if the cancel button was clicked and exit loop if clicked
            event, values = window.read(timeout=0)

            if event == 'Cancel' or event == None:
                return 2
                
            sleep(0.5) #for testing
            # # call of the function to classifiy the documents
            # in_path = os.path.join(foldername, file)
            # out_path = os.path.join('output/')

            # cluster = util.prediction(in_path)

            # # create the directory if not already there
            # os.makedirs(os.path.join(out_path,str(cluster[0])), exist_ok=True)
            # # move to the document to the right directory
            # os.rename(os.path.join(in_path), os.path.join(out_path,str(cluster[0]),file))

            # progress_bar.update_bar(index+1, len(filenames))
            progress_bar.UpdateBar(index+1, len(filenames))
            texte.Update(f'Processing ... {file}')
        window.close()
        return 1

    except Exception as e:
        print(e)
        window.close()
        return 2

    

def no_selection():
    layout = [[sg.Text('No folder selected or no PDF\'s in selected folder.')],
               [sg.OK()]]
    window = sg.Window("Warning!", layout, size=(200, 50))
    while True:
        event, values = window.read()
        if event == 'OK' or event == sg.WIN_CLOSED:
            break
        
    window.close()

def done():
    layout = [[sg.Text('Classification has been processed')],
               [sg.OK()]]
    window = sg.Window("Success!", layout, size=(200, 50))
    while True:
        event, values = window.read()
        if event == 'OK' or event == sg.WIN_CLOSED:
            break
        
    window.close()

def error():
    layout = [[sg.Text('The process was interrupted or an error occured. Please contact your favourite dev.')],
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
        [sg.Text('Please select a folder:', key='_SELECT_'), sg.Button('Browse', size=(80,40))],

        [sg.Text('List of files:')],
        [sg.Multiline(key='files', size=(60,30), autoscroll=True)],

        [sg.Button('Classify', auto_size_button=True), sg.Cancel()],    
    ]

    window = sg.Window('Document Classifier', layout, size=(400, 100))
    return window

def main():

    filenames = ''
    window = make_window()
    texte_folder = window.FindElement('_SELECT_')
    while True:
        event, values = window.read()
        
        if event == sg.WIN_CLOSED or event == 'Cancel':
            break

        if event == 'Browse':
            foldername = sg.PopupGetFolder('Please select a folder', no_window=True)
            if foldername: # `None` when clicked `Cancel` - so I skip it
                filenames = sorted([f for f in os.listdir(foldername) if f.endswith('.pdf')])
                # it use `key='files'` to `Multiline` widget
                window['files'].update("\n".join(filenames))
                texte_folder.Update(foldername)
                # print(os.path(foldername))
        if event == 'Classify':
            if filenames:
                window.close()
                if classification(foldername, filenames)==1:
                    done()
                    break
                else:
                    error()
                    break
            else:
                no_selection()

    window.close()

def starting_window():
    layout = [
            [sg.ProgressBar(1, orientation='h', auto_size_text= True, key='+PROGRESS+', bar_color=('blue',None))],
            [sg.Text('', key='-IN-', justification='center')]
            ]
    window = sg.Window("YoCorp", layout, size=(950, 550), background_image='../assets/logo.png')
    progress_bar = window['+PROGRESS+']
    text_bar = window['-IN-']
    
    text = {0:"Loading unecessary files ...",
            3:"Trying to not make inconsistent clusters ...",
            5:"Trying to not make inconsistent clusters: Failed.",
            10:"Loading some other components ...",
            11: "Almost there",
            13: "Here you go, motors launched!"}

    for i in range(16):
        # check to see if the cancel button was clicked and exit loop if clicked
        event, values = window.read(timeout=0)

        if event == 'Cancel' or event == None:
            break
        sleep(0.5)    
        progress_bar.UpdateBar(i+1, 16)
        try:
            text_bar.Update(text[i])
        except:
            pass

    window.close()
    main()
    
# for presentation purpose
def restore():
    in_path = 'input/'

    for parent, _, filenames in os.walk('output/'):
        for fn in filenames:
            if fn.lower().endswith('.pdf'):
                os.rename(os.path.join(parent, fn), os.path.join(in_path, fn))

if __name__ == '__main__':
    # main()
    # restore()
    # sg.main()
    starting_window()