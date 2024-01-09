import sys


def chat() -> None:
    cli_input = " ".join(sys.argv[1:])
    print(cli_input)


if __name__ == "__main__":
    chat()
