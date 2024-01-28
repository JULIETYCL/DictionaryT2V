import base64
import paling
import TextToVideo
import wordAPI

# Paling has bug in its _get_real_path method so monkey patch it here
def _fixed_paling_get_real_path(path: str) -> str:
    import sys, os
    if getattr(sys, 'frozen', False):
        if hasattr(sys, '_MEIPASS'):
            # sys._MEIPASS is dynamically added by PyInstaller
            return os.path.join(sys._MEIPASS, path)
        elif hasattr(sys, 'executable'):
            # sys.executable is dynamically added by cx-freeze
            return os.path.join(os.path.dirname(sys.executable), path)
    else:
        return os.path.abspath(path)
paling._get_real_path = _fixed_paling_get_real_path

# Set web files folder
paling.init('web', allowed_extensions=['.js', '.html'])

# Create our image generator
imageGen = TextToVideo.ImageRepresentationGenerator()

# Create our video generator
videoGen = TextToVideo.VideoRepresentationGenerator()

#
# Functions that can be called from Javascript via the paling library
#

@paling.expose
def lookup_word(word: str):

    def upperfirst(x, i = 1):
        return x[:i].upper() + x[i:]

    print(f"Executing lookup for '{word}'")

    # Look up the definition(s) of the word using the dictionary API
    definitions = []

    response = wordAPI.lookup_word(word)
    # print(response)
    if response:
        if 'results' in response:
            results = response['results']
            # We got one or more results from the API, add them to the definitions list
            for r in results:
                d = {
                    'definition': upperfirst(r['definition']),
                    'examples': None,
                    'partOfSpeech': r['partOfSpeech']
                }
                if 'examples' in r:
                    # Result has examples, capture them
                    d['examples'] = [upperfirst(ex) for ex in r['examples']]
                definitions.append(d)
        elif 'success' in response:
            # If we got 'success' then it means there was an error, get its message
            print(response['message'])

    return word, definitions

@paling.expose
def represent_image(image_data_b64: str):
    print(f"Representing image data")
    # Convert from b64 string to bytearray
    image_data = base64.b64decode(image_data_b64)
    # Get the url of the video representation of the given image
    video_url = videoGen.representImageWithUrl(image_data)
    return video_url

@paling.expose
def represent_text(sentence: str):
    print(f"Representing '{sentence}'")
    # Get the image representation of the given sentence
    image_data = imageGen.representText(sentence)
    # Encode the image data as bas64 to send back to client side
    image_data_b64 = base64.b64encode(image_data).decode('utf-8')
    return image_data_b64

#
# Main application entrypoint
#

if __name__ == "__main__":
    # Show the GUI and start the main app (this blocks and enters loop)
    paling.start('dictionary.html', cmdline_args = [
        '--window-size=600,800'
    ])
