from abc import ABC, abstractmethod
from PIL import Image, UnidentifiedImageError
import concurrent.futures
import os
from log_factory import LoggerFactory


class MediaResizer(ABC):

    def __init__(self):
        log_level = "INFO"
        self.LOG = LoggerFactory.get_logger("user", log_level)

    @abstractmethod
    def save(self, media, media_name):
        pass

    def resize(self, image, max_width, max_height):
        pass


class ImageResizer(MediaResizer):
    def __init__(self):
        super().__init__()

    def resize(self, image_name, max_width, max_height):
        try:
            image = Image.open(image_name)
            image.thumbnail((max_width, max_height))
            self.save(image, image_name)
        except UnidentifiedImageError as e:
            self.LOG.error(e)
            return e

        return f"Resize {image_name} success"

    def save(self, image, image_name):
        file_suffix = "_thumb"
        name, file_extension = image_name.split(".")
        try:
            image.save(f"{name}{file_suffix}.{file_extension}")
        except AttributeError as e:
            self.LOG.info(f"Failed to save {name}{file_suffix}.{file_extension}")
            return e
        self.LOG.info(f"{name}{file_suffix}.{file_extension} saved. Resolution = {image.size[0]}x{image.size[1]}")

    def resize_parallel(self, file_names):

        max_width, max_height = 512, 512
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            self.LOG.info("New ThreadPoolExecutor created")
            future = [executor.submit(self.resize, key, max_width, max_height) for key in file_names]
            for future in concurrent.futures.as_completed(future):
                exception = future.exception()

                if not exception:
                    yield future.result()
                else:
                    yield exception

    def resize_all(self):

        responses = []

        file_names = [file for file in os.listdir(os.getcwd())
                      if file.split(".")[-1] in ["jpg", "png"]
                      and "_thumb" not in file]

        for response in self.resize_parallel(file_names):
            self.LOG.info(response)
            responses.append(response)

        if all(isinstance(response, str) for response in responses):
            return "Resize completed without errors"
        else:
            return "Resize completed with errors"


class VideoResizer(MediaResizer):
    pass


if __name__ == "__main__":
    pass
