import requests
import urllib

class StableVideoDiffusion:

    def generate_for_image(self, image_data: bytearray) -> requests.Response:
        # Request generated video from SVD server and return response
        response = requests.post("http://localhost:8080/generate", files = {
            'image' : image_data
        })
        return response

    def generate_image_for_text(self, prompt: str) -> requests.Response:
        # Request generated image from SVD server and return response
        response = requests.get("http://localhost:8080/img/", params = {
            'prompt' : prompt,
            'steps' : 20
        })
        return response

client = StableVideoDiffusion()

def getImageForSentence(sentence: str) -> bytearray:
  response = client.generate_image_for_text(
    prompt = sentence,
  )
  return response.content

def getVideoForImage(image_bytes: bytearray) -> bytearray:
    response = client.generate_for_image(image_data = image_bytes)
    if response:
        video_bytes = response.content
        return video_bytes
    return None
