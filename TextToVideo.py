import tempfile

class RepresentationGenerator:

    def representText(self, text: str) -> bytearray:
        pass


class ImageRepresentationGenerator:

    def representText(self, text: str) -> bytearray:
        import svd as ai
        img = ai.getImageForSentence(text)
        return img

class VideoRepresentationGenerator:

    def representImage(self, image_bytes: str) -> str:
        video_bytes = self.representImageRaw(image_bytes)
        # Write the video to a temp file
        with tempfile.NamedTemporaryFile(mode = 'wb', delete = False) as f:
            f.write(video_bytes)
            return f.name

    def representImageWithUrl(self, image_bytes: str) -> str:
        import svd as ai
        video_url = ai.getVideoUrlForImage(image_bytes)
        return video_url.decode("utf-8")

    def representImageRaw(self, image_bytes: str) -> bytearray:
        import svd as ai
        video_bytes = ai.getVideoForImage(image_bytes)
        return video_bytes
