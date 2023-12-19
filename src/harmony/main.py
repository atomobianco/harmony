import argparse
import logging
import uuid
from datetime import datetime
import harmony.parsers as parsers
import harmony.formatters as formatters
import harmony.writers as writers
from harmony.utils import parse_file
from rich.console import Console


def build_args():
    parser = argparse.ArgumentParser(description="Harmony Resume Parser")
    parser.add_argument("--resume", help="resume file to parse", required=False)
    parser.add_argument("--offer", help="offer file to parse", required=False)
    _args = parser.parse_args()
    if not _args.resume:
        _args.resume = "./tests/resources/resume.md"
    if not _args.offer:
        _args.offer = "./tests/resources/offer.md"
    return _args


def log_info(content: str, heading: str, console: Console):
    dashes = "-" * 40
    logging.info(f"\n\n{dashes} {heading}: {dashes}\n{content}\n\n")
    console.rule(f"[bold]{heading}")
    console.print(content, end="\n\n")


if __name__ == "__main__":
    ts = datetime.now().strftime("%Y-%m-%dT%Hh%Mm")
    uid = str(uuid.uuid4())[:8]
    logging.basicConfig(level=logging.INFO, filename=f"logs/harmony_{ts}_{uid}.log")
    console = Console()
    args = build_args()

    offer = None
    if args.offer:
        offer_file_content = parse_file(args.offer)
        offer = parsers.offer_parser(offer_file_content)
        log_info(str(offer), "OFFER", console)

    resume_original = parse_file(args.resume)
    log_info(resume_original, "RESUME (ORIGINAL)", console)

    with console.status("Parsing the resume..."):
        resume = parsers.resume_parser(resume_original)
        log_info(str(resume), "RESUME (PARSED)", console)

    # Format the resume alone
    with console.status("Formatting the resume..."):
        resume_formatted = formatters.resume_formatter(resume)
        log_info(resume_formatted, "RESUME (FORMATTED)", console)

    if offer:
        # Format the resume with the offer
        with console.status("Formatting the resume with the offer..."):
            resume_formatted_aligned = formatters.resume_formatter(resume, offer=offer)
            log_info(resume_formatted_aligned, "RESUME (FORMATTED, ALIGNED)", console)

        with console.status("Writing the cover letter..."):
            cover_letter = writers.cover_letter_writer(resume, offer.raw)
            log_info(cover_letter, "COVER LETTER", console)

        with console.status("Writing the strengths and weaknesses..."):
            strengths_weaknesses = writers.strengths_weaknesses_writer(
                resume, offer.raw
            )
            log_info(strengths_weaknesses, "STRENGTHS AND WEAKNESSES", console)
