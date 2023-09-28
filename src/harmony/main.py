import argparse
import logging
import pyaml

from harmony.core import Resume, Offer


def parse_file(file_name):
    """Parse file and return a string"""
    with open(file_name, "r") as f:
        return f.read()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.info("started")

    parser = argparse.ArgumentParser(description="Harmony Resume Parser")
    # parser.add_argument("resume", help="resume file to parse")
    # parser.add_argument("offer", help="offer file to parse")
    args = parser.parse_args()

    # args.resume = "./tests/resources/resume.md"
    args.resume = "./tests/resources/dumb.md"
    raw_resume = parse_file(args.resume)
    resume = Resume(raw=raw_resume)
    logging.info(f"output:\n{pyaml.dump(resume)}")

    args.offer = "./tests/resources/offer.md"
    raw_offer = parse_file(args.offer)
    offer = Offer(raw=raw_offer)

    resume_aligned = resume.align(offer)
    logging.info(f"output:\n{pyaml.dump(resume_aligned)}")
