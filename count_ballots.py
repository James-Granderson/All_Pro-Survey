# Counts the ballot zips voters sent back (put them in the ballots folder) and updates results.html.
# Only the FIRST ballot per team per survey counts. To free a team's slot, delete that team's wrong ballot file from ballots/.
import collections
import glob
import json
import os
import re
import zipfile

BALLOT_DIR = "ballots"


def read_ballot(path):
    if path.lower().endswith(".zip"):
        with zipfile.ZipFile(path) as z:
            return json.loads(z.read("ballot.json").decode("utf-8"))
    with open(path, encoding="utf-8") as f:  # the survey falls back to a plain .json if the zip library didn't load
        return json.load(f)


def read_ballots():
    ballots, ignored = {}, []  # (team, survey) -> the first ballot submitted; later ones are ignored
    os.makedirs(BALLOT_DIR, exist_ok=True)
    for path in sorted(glob.glob(os.path.join(BALLOT_DIR, "*.zip")) + glob.glob(os.path.join(BALLOT_DIR, "*.json"))):
        try:
            ballot = read_ballot(path)
            key = (ballot["team"].strip().lower(), ballot["survey"])
            ballot["picks"]
        except Exception:
            print("  skipped, not a ballot:", os.path.basename(path))
            continue
        ballot["file"] = os.path.basename(path)
        if key not in ballots:
            ballots[key] = ballot
        elif ballot.get("submitted", 0) < ballots[key].get("submitted", 0):
            ignored.append(ballots[key]["file"])
            ballots[key] = ballot
        else:
            ignored.append(ballot["file"])
    return ballots, ignored


def tally(ballots):
    counts = collections.defaultdict(collections.Counter)  # position -> player name -> votes
    for ballot in ballots.values():
        for position, names in ballot["picks"].items():
            counts[position].update(names)
    return [{"pos": pos, "ranked": c.most_common()} for pos, c in counts.items()]


def fill_results(positions, teams):
    with open("results.html", encoding="utf-8") as f:
        page = f.read()
    data = json.dumps({"teams": teams, "positions": positions})
    page = re.sub(r"const RESULTS = [^\n]*\n", lambda _: f"const RESULTS = {data};\n", page, count=1)
    with open("results.html", "w", encoding="utf-8") as f:
        f.write(page)


def main():
    ballots, ignored = read_ballots()
    teams = sorted({b["team"].strip() for b in ballots.values()})
    print(f"{len(ballots)} ballots from {len(teams)} teams: {', '.join(teams)}")
    if ignored:
        print("Ignored later duplicates (the first ballot per team counts):", ", ".join(ignored))
        print("If the first one was a mistake, delete its file from ballots/ and run this again.")
    fill_results(tally(ballots), teams)
    print("results.html updated")


main()