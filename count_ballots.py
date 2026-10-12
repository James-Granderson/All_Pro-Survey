# Collects what each live_survey.html instance produced and hands it to count_votes.
import base64
import json

from count_votes import count_votes


def read_ballots(path):
    ballots = {}  # team -> picks; a later line from the same team replaces the earlier one
    with open(path, encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            try:
                ballot = json.loads(base64.b64decode(line.strip()).decode("utf-8"))
                ballots[ballot["v"].strip().lower()] = ballot["p"]
            except Exception:
                print("Skipped an unreadable line:", line.strip()[:30])
    return ballots


def main():
    ballots = read_ballots("votes.txt")
    print(f"{len(ballots)} teams have voted: {', '.join(sorted(ballots))}")
    count_votes(ballots)
    print("results.html updated")


main()