import argparse
import logging
import pyaml

from harmony.core import Resume


def parse_file(file_name):
    """Parse file and return a string"""
    with open(file_name, "r") as f:
        return f.read()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.info("started")

    parser = argparse.ArgumentParser(description="Harmony Resume Parser")
    # parser.add_argument("file", help="resume file to parse")
    args = parser.parse_args()

    # args.file = "./tests/resources/resume.md"
    args.file = "./tests/resources/dumb.md"
    raw = parse_file(args.file)
    resume = Resume(raw=raw)

    logging.info(f"output:\n{pyaml.dump(resume)}")
