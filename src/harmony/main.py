import argparse
import logging
import uuid
from datetime import datetime
import harmony.parsers as parsers
import harmony.formatters as formatters
from harmony.utils import parse_file

if __name__ == "__main__":
    dashes = "-" * 40
    ts = datetime.now().strftime("%Y-%m-%dT%Hh%Mm")
    uid = str(uuid.uuid4())[:8]

    parser = argparse.ArgumentParser(description="Harmony Resume Parser")
    parser.add_argument("--resume", help="resume file to parse", required=False)
    parser.add_argument("--offer", help="offer file to parse", required=False)
    parser.add_argument(
        "--console", help="log to console", required=False, action="store_true"
    )

    args = parser.parse_args()
    if not args.resume:
        args.resume = "./tests/resources/resume.md"
    if not args.offer:
        args.offer = "./tests/resources/offer.md"
    if args.console:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(filename=f"logs/harmony_{ts}_{uid}.log", level=logging.INFO)
    logging.info("Started")

    # Parse the resume
    resume_file_content = parse_file(args.resume)
    resume = parsers.resume_parser(resume_file_content)
    logging.info(f"\n\n{dashes} resume: {dashes}\n{resume}\n\n")

    offer = None
    if args.offer:
        # Parse the offer
        offer_file_content = parse_file(args.offer)
        offer = parsers.offer_parser(offer_file_content)
        logging.info(f"\n\n{dashes} offer: {dashes}\n{offer}\n\n")

    # Rework the resume formatted alone
    resume_formatted = formatters.resume_formatter_by_chunks(resume)
    logging.info(f"\n\n{dashes} resume_formatted: {dashes}\n{resume_formatted}\n\n")

    if args.offer:
        # Rework the resume formatted aligning with the offer
        resume_formatted_aligned = formatters.resume_formatter_by_chunks(
            resume, offer=offer
        )
        logging.info(
            f"\n\n{dashes} resume_formatted_aligned: {dashes}\n{resume_formatted_aligned}\n\n"
        )

    # Strengths and Weaknesses
    # P.S. Consider the resume formatted alone against the offer and draw the strengths and weaknesses

    # Cover letter (About me, Why XYZ? Why Me?)
