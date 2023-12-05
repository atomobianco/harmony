# harmony
Tell your story with stochastic narratives.


# Description
The application curates a long and detailed list of information about the candidate into smaller bits and aligned with a position.


## Components
A service that holds and serves the positions, sorted by time.
A service that reads the candidate information from an external source.
A service that reads the position information from an external source.
A service that alignes the two and returns a curated version of the candidate full information.


## Models
Position: occupied at time t. It has a title, a description, a duration, a list of results issued during this position.
Result: A description of what was done.

```bash
python src/harmony/main.py --console --resume /mnt/TARANIS/myCV/resume.md --offer tests/resources/offer_mirakl.md
```
