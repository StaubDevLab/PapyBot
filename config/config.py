import logging


logging.basicConfig(
    filename="config/googleclient.log",
    filemode='w',
    level=logging.DEBUG,
    format='%(asctime)s :: %(levelname)s :: %(message)s',
    datefmt="%d/%m/%Y %I:%M:%S %p")


def read_log():
    lines = [line.split('::') for line in open('googleclient.log')]
    [print(f"DATE:{date} - LEVEL:{level} - MESSAGE:{message}".rstrip()) for date, level, message in lines]
