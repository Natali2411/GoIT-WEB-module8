import enum
from typing import Tuple

from db_connect import connect_mongo_db
from models import QueryData


class CLI_COMMANDS(enum.Enum):
    NAME = "name"
    TAG = "tag"
    TAGS = "tags"
    EXIT = "exit"


METHODS = {
    CLI_COMMANDS.NAME.value: QueryData.get_quotes_by_name,
    CLI_COMMANDS.TAG.value: QueryData.get_quotes_by_tags,
    CLI_COMMANDS.TAGS.value: QueryData.get_quotes_by_tags,
}


def parse_cli_input(console_input: str) -> Tuple[str, list]:
    console_attrs = console_input.split(":")
    method = METHODS.get(console_attrs[0])
    arguments = [attr.strip() for attr in console_attrs[1].split(",")]
    return method, arguments


if __name__ == "__main__":
    console_input = input("Type a command >>> ")
    while console_input and console_input != CLI_COMMANDS.EXIT.value:
        connect_mongo_db()
        method, arguments = parse_cli_input(console_input=console_input)
        rows = method(*arguments)
        print(rows)
        console_input = input("Type a command >>> ")
