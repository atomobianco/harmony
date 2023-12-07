import argparse
import logging
import uuid
from datetime import datetime
import harmony.parsers as parsers
import harmony.formatters as formatters
import harmony.writers as writers
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
        logging.basicConfig(level=logging.INFO, filename=f"logs/harmony_{ts}_{uid}.log")
    logging.info("Started")

    resume_file_content = parse_file(args.resume)
    logging.info(
        f"\n\n{dashes} resume_file_content: {dashes}\n{resume_file_content}\n\n"
    )

    resume = parsers.resume_parser(resume_file_content)
    logging.info(f"\n\n{dashes} resume: {dashes}\n{resume}\n\n")

    offer = None
    if args.offer:
        offer_file_content = parse_file(args.offer)
        offer = parsers.offer_parser(offer_file_content)
        logging.info(f"\n\n{dashes} offer: {dashes}\n{offer}\n\n")

    # Rework the resume without the offer
    resume_formatted = formatters.resume_formatter(resume)
    logging.info(f"\n\n{dashes} resume_formatted: {dashes}\n{resume_formatted}\n\n")

    if offer:
        # Rework the resume with the offer
        resume_formatted_aligned = formatters.resume_formatter(resume, offer=offer)
        logging.info(
            f"\n\n{dashes} resume_formatted_aligned: {dashes}\n{resume_formatted_aligned}\n\n"
        )

        cover_letter = writers.cover_letter_writer(resume_formatted_aligned, offer.raw)
        logging.info(f"\n\n{dashes} cover_letter: {dashes}\n{cover_letter}\n\n")

        strengths_weaknesses = writers.strengths_weaknesses_writer(
            resume_formatted, offer.raw
        )
        logging.info(
            f"\n\n{dashes} strengths_weaknesses: {dashes}\n{strengths_weaknesses}\n\n"
        )
