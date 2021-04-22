import csv
import logging
import re

INPUTCSV = "input.csv"

FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
logging.basicConfig(format=FORMAT, filename="Logfile.log", level=logging.INFO)

logger = logging.getLogger(__name__)


def normalize(value1, value2):
    """Remove whitespace and format values if necessary

    Args:
        value1 (String): any
        value2 (String): any

    Returns:
        String Tuple
    """
    value1 = value1.strip()
    value2 = value2.strip()
    if not re.match(r"special/", value2):
        value2 = "special/" + value2
    return value1, value2


def read_csv(filename):
    """CSV traversal function.
    Iterate over every row and handle data based on column

    Args:
        filename (csv file): input file

    Yields:
        tuple: found entries in csv file
    """
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=";")
        firstline = True
        for idx, row in enumerate(csv_reader):
            try:
                if firstline:
                    firstline = False
                    continue
                if not row[2] or not row[4]: # change columns
                    logger.error(f"Row has empty cells: {row}")
                    continue
                yield row[2], row[4]
            except Exception:
                logging.error(f"Failed to parse row: {row}")
    logger.info(f"Detected {idx} entries.")


def do_stuff(value1: str, value2: str):
    """Do Stuff here with the value(s) from the CSV file

    Args:
        value1 (str): any
        value2 (str): any

    Returns:
        Bool: Outcome of function; can be forwarded API call
    """
    value1, value2 = normalize(value1, value2)
    logger.info(f"Trying to do stuff with {value1} and {value2}")
    return True # call API here if needed


def main():
    logger.info("Start progress")
    for p1, p2 in read_csv(INPUTCSV):
        try:
            if not do_stuff(p1, p2):
                logger.error(f"Failed to do stuff for params: {p1} and {p2}")
            else:
                logger.info(f"Successfully did stuff")
        except Exception:
            logger.exception(f"Failed to access api {p1}:{p2}")


if __name__ == "__main__":
    main()
