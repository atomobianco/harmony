import argparse
import logging

import harmony.parsers as parsers
import harmony.formatters as formatters
from harmony.utils import parse_file

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
    resume_parsed = parsers.resume_parser(resume_file_content)
    resume_formatted_response = formatters.resume_formatter(resume_parsed)
    resume_formatted_parsed = parsers.resume_parser(resume_formatted_response)

    logging.info(f"output:\n{resume_parsed}")
    logging.info(f"output:\n{resume_formatted_parsed}")

    # args.offer = "./tests/resources/offer.md"
    # raw_offer = parse_file(args.offer)
    # offer = Offer(raw=raw_offer)
    #
    # resume_aligned = resume.align(offer)
    # logging.info(f"output:\n{pyaml.dump(resume_aligned)}")
