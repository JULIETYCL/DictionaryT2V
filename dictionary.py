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
    # print(response)
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

home_window = None
definition_window = None
video_window = None

current_window = None

window_history = []

def peek(list):
    if list:
        return list[len(list) - 1]
    return None

def showDefinitionWindow(word, definitions):
    global current_window, window_history
    if current_window:
        current_window.Close()
        current_window = None
    current_window = sg.Window(
        "Definition of '{0}'".format(word.upper()),
        getDefinitionLayout(word, definitions),
        size = (600, 600))
    window_history.append({
        'id': "definition",
        'params': {
            'word': word,
            'definitions': definitions
        }
    })
    return current_window

def showHomeWindow(params = None):
    global current_window, window_history
    if current_window:
        current_window.Close()
        current_window = None
    current_window = sg.Window("English Dictionary", getHomeLayout(), size = (300, 200))
    if not window_history:
        # Only add the home window to the history if the history is empty
        window_history.append({
            'id': "home",
            'params': params
        })
    return current_window

def showExampleWindow(example_sentence):
    global current_window, window_history
    if current_window:
        current_window.Close()
        current_window = None
    current_window = sg.Window(
        "Example of '{0}'".format(example_sentence),
        getVideoLayout(example_sentence), size = (600, 600))
    window_history.append({
        'id': "example",
        'params': {
            'example_sentence': example_sentence
        }
    })
    return current_window

def showPreviousWindow():
    global current_window, window_history
    # print("Window history: {0}".format(window_history))
    if window_history:
        # Remove the current window from the history
        window_history.pop()
        if window_history:
            # Look at the previous window before the current one
            previous_window = window_history.pop()
            print("Switching to previous window: {0}".format(previous_window['id']))
            if previous_window:
                params = previous_window['params']
                if previous_window['id'] == "home":
                    showHomeWindow()
                elif previous_window['id'] == "definition":
                    showDefinitionWindow(params['word'], params['definitions'])
                elif previous_window['id'] == "example":
                    showExampleWindow(params['example_sentence'])
            else:
                # No previous window
                current_window = None
    return current_window

showHomeWindow()

while True:
    # Get the state for the current window from the window history
    curr_window_state = peek(window_history)
    if not curr_window_state:
        # No windows in the history, user has closed the top-level window and wants to quit
        print("Goodbye")
        break
    # Get the id of the current window from the window state
    curr_window_id = curr_window_state['id']
    print("Current Window: {0}".format(curr_window_id))
    # Wait for an event from the current window
    event, values = current_window.read()
    # print(event, values)
    if event == sg.WIN_CLOSED:
        # The current window was closed, show the previous window
        showPreviousWindow()
    elif curr_window_id == "home":
        # The current window is the Home window
        if event == "Look Up":
            # User gave us a word, look it up and display its definition(s)
            if '-IN-' in values:
                word, definitions = lookupWord(values['-IN-'])
                print(definitions)
            # Create and display the window for the word definition
            showDefinitionWindow(word, definitions)
    elif curr_window_id == "definition":
        # The current window is the Definition window
        if event:
            if event.startswith('video_button'):
                showExampleWindow(current_window[event].metadata)
    elif curr_window_id == "example":
        # The current window is the Example window
        # TODO Implement this
        pass

if definition_window:
    definition_window.close()
    del definition_window

if home_window:
    home_window.close()
    del home_window

if video_window:
    video_window.close()
    del video_window
