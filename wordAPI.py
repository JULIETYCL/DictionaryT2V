import requests

def callAPI(term):
    # url = "https://wordsapiv1.p.rapidapi.com/words/{word}/definitions".format(word = str(term))
    url = "https://wordsapiv1.p.rapidapi.com/words/{word}".format(word = str(term))
    headers = {
        "X-Mashape-Key": "c446f5a19bmsh38981afb6eb6532p1f4534jsn62011499c96f",
        "Accept": "application/json"
     }
    response = requests.get(url, headers=headers)
    data = response.json()
    return data
