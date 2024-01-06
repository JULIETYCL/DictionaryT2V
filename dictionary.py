import PySimpleGUI as sg
import textwrap
import wordAPI as ap

sg.theme('DarkAmber')

def getDefinitionLayout(word: str, definitions: list[object]):
    """Gets the layout for the defintion(s) of a given word."""

    # Create the layout for the UI
    layout = []

    # Add all of the definitions
    if definitions:
        layout.append([sg.Text('Definition of "{0}"'.format(word.upper()))])
        layout.append([sg.Text('Found {0} definitions.'.format(len(definitions)))])
        # Got definitions from the dictionary, use them
        defin_num = 1
        for defin in definitions:
            defin_text = '\n'.join(textwrap.wrap('{0}. {1} - {2}'.format(defin_num, defin["partOfSpeech"], defin["definition"]), width = 96))
            layout.append([sg.Text(defin_text)])
            if defin['examples']:
                # There are examples for the definition, display them
                for example in defin['examples']:
                    example_text = '\n'.join(textwrap.wrap(example, width = 96))
                    layout.append([sg.Text(example_text)])
                    layout.append([sg.Button('Example in Video',key = 'video_button{0}'.format(defin_num-1) , metadata = example)])
            defin_num = defin_num + 1
    else:
        # No definitions found
        layout.append([sg.Text('No definitions of "{0}" found.'.format(word.upper()))])

    return layout

def getVideoLayout(sentence: str):
    layout = [
        [sg.Text('visualize the sentence of "{0}"'.format(sentence))],
    ]
    return layout


def getHomeLayout():
    layout = [
        [sg.Text('Enter the word you want to define')],
        [sg.InputText(key = '-IN-')],
        [sg.Button('Look Up')]
    ]
    return layout

def lookupWord(word: str):
    # Look up the definition(s) of the word using the dictionary API
    definitions = []

    response = ap.callAPI(word)
    print(response)
    if response:
        if 'results' in response:
            results = response['results']
            # We got one or more results from the API, add them to the definitions list
            for r in results:
                d = {
                    'definition': r['definition'],
                    'examples': None,
                    'partOfSpeech': r['partOfSpeech']
                }
                if 'examples' in r:
                    # Result has examples, capture them
                    d['examples'] = r['examples']
                definitions.append(d)
        elif 'success' in response:
            # If we got 'success' then it means there was an error, get its message
            print(response['message'])

    return word, definitions

home_window = sg.Window("English Dictionary", getHomeLayout(), size = (300, 200))
definition_window = None
video_window = None

current_window = home_window

while True:
    event, values = current_window.read()
    # print(event, values)
    if current_window == home_window:
        if event == sg.WIN_CLOSED or event == "English Dictionary":
            break
        if event == "Look Up":
            # User gave us a word, look it up and display its definition(s)
            if '-IN-' in values:
                word, definitions = lookupWord(values['-IN-'])
                print(definitions)

            # Hide the main window
            home_window.Hide()

            # Create and display the window for the word definition
            if not definition_window:
                definition_window = sg.Window(
                    "Definition of '{0}'".format(word.upper()),
                    getDefinitionLayout(word, definitions),
                    size = (600, 600))
            else:
                definition_window.UnHide()
            current_window = definition_window
            print('definition_window')
    elif current_window == definition_window:
        if event == sg.WIN_CLOSED:
            print('definition window closed')
            definition_window.Close()
            definition_window = None
            home_window.UnHide()
            current_window = home_window
        if event.startswith('video_button'):
            print('video window')
            definition_window.Hide()
            if not video_window:
                example_sentence = definition_window[event].metadata
                video_window = sg.Window(
                    "Example of '{0}'".format(example_sentence),
                    getVideoLayout(example_sentence), size = (600, 600))
            else:
                video_window.UnHide()
            current_window = video_window
    elif current_window == video_window:
        if event ==sg.WIN_CLOSED:
            video_window.Close()
            video_window = None
            home_window.UnHide()
            current_window = home_window

if definition_window:
    definition_window.close()
    del definition_window

if home_window:
    home_window.close()
    del home_window

if video_window:
    video_window.close()
    del video_window
