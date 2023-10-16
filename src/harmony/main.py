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
    logging.basicConfig(filename=f"logs/harmony_{ts}_{uid}.log", level=logging.INFO)
    logging.basicConfig(level=logging.INFO)
    logging.info("Started")

    parser = argparse.ArgumentParser(description="Harmony Resume Parser")
    # parser.add_argument("resume", help="resume file to parse")
    # parser.add_argument("offer", help="offer file to parse")
    args = parser.parse_args()

    # Parse the resume
    args.resume = "./tests/resources/resume.md"
    # args.resume = "/mnt/TARANIS/myCV/resume.md"
    args.resume = "/mnt/TARANIS/myCV/stefano_perasso_fr.md"
    resume_file_content = parse_file(args.resume)
    resume = parsers.resume_parser(resume_file_content)
    logging.info(f"\n\n{dashes} resume: {dashes}\n{resume}\n\n")

    # Rework the resume
    resume_formatted = formatters.resume_formatter_by_chunks(resume)
    resume_final = resume_formatted
    logging.info(f"\n\n{dashes} resume_final: {dashes}\n{resume_final}\n\n")

    # args.offer = "./tests/resources/offer.md"
    # raw_offer = parse_file(args.offer)
    # offer = Offer(raw=raw_offer)
    #
    # resume_aligned = resume.align(offer)
    # logging.info(f"output:\n{pyaml.dump(resume_aligned)}")
