import json
import pathlib


class FileInteraction:
    @staticmethod
    def read_info(path: str) -> dict:
        """
        Method reads info from json file.
        :param path: Path to file.
        :return: Data from file as a dictionary.
        """
        with open(path, "r") as fh:
            try:
                file_data = json.load(fh)
            except ValueError:
                return {}
            return file_data

    @staticmethod
    def save_info(path: str, data: dict) -> None:
        """
        Method saves dictionary to json file.
        :param data: Dictionary that should be saved.
        :param path: Path to file in which the data should be saved.
        """
        with open(path, mode="w") as fh:
            json.dump(data, fh)
