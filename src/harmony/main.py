import argparse
import logging
import copy
import harmony.parsers as parsers
import harmony.formatters as formatters
from harmony.utils import parse_file

if __name__ == "__main__":
    dashes = "-" * 40
    logging.basicConfig(level=logging.INFO)
    logging.info("Started")

    parser = argparse.ArgumentParser(description="Harmony Resume Parser")
    # parser.add_argument("resume", help="resume file to parse")
    # parser.add_argument("offer", help="offer file to parse")
    args = parser.parse_args()

    # Parse the resume
    args.resume = "./tests/resources/resume.md"
    # args.resume = "/mnt/TARANIS/myCV/resume.md"
    resume_file_content = parse_file(args.resume)
    resume = parsers.resume_parser(resume_file_content)
    logging.info(f"{dashes} resume: {dashes}\n{resume}")

    # Rework the resume
    resume_formatted = parsers.resume_parser(formatters.resume_formatter(resume))
    logging.info(f"{dashes} resume_formatted: {dashes}\n{resume_formatted}")

    # Rework the positions one by one
    positions = []
    for position in resume.positions:
        position_formatted = parsers.positions_parser(
            formatters.position_formatter(position)
        )[0]
        positions.append(position_formatted)
    resume_copy = copy.deepcopy(resume)
    resume_copy.positions = positions
    logging.info(f"{dashes} resume_copy: {dashes}\n{resume_copy}")

    # args.offer = "./tests/resources/offer.md"
    # raw_offer = parse_file(args.offer)
    # offer = Offer(raw=raw_offer)
    #
    # resume_aligned = resume.align(offer)
    # logging.info(f"output:\n{pyaml.dump(resume_aligned)}")
