import argparse
import logging

import harmony.parsers as parsers
import harmony.formatters as formatters


def parse_file(file_name):
    """Parse file and return a string"""
    with open(file_name, "r") as f:
        return f.read()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.info("Started")

    parser = argparse.ArgumentParser(description="Harmony Resume Parser")
    # parser.add_argument("resume", help="resume file to parse")
    # parser.add_argument("offer", help="offer file to parse")
    args = parser.parse_args()

    # args.resume = "./tests/resources/resume.md"
    args.resume = "/mnt/TARANIS/myCV/resume.md"
    resume_file_content = parse_file(args.resume)
    resume = parsers.resume_parser(resume_file_content)
    resume_formatted_raw = formatters.resume_formatter(resume)
    resume_formatted = parsers.resume_parser(resume_formatted_raw)

    logging.info(f"output:\n{resume}")
    logging.info(f"output:\n{resume_formatted}")

    # args.offer = "./tests/resources/offer.md"
    # raw_offer = parse_file(args.offer)
    # offer = Offer(raw=raw_offer)
    #
    # resume_aligned = resume.align(offer)
    # logging.info(f"output:\n{pyaml.dump(resume_aligned)}")
