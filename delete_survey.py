# Ends the cycle: removes both live surveys and the collected ballots, and resets results.html to the blank template.
import glob
import os
import re

LIVE_SURVEYS = ["live_survey_offense.html", "live_survey_defense.html"]
BALLOT_DIR = "ballots"


def remove_file(path):
    os.chmod(path, 0o666)  # the live surveys are locked read-only
    os.remove(path)
    print("Removed", path)


def reset_results():
    with open("results.html", encoding="utf-8") as f:
        page = f.read()
    page = re.sub(r"const RESULTS = [^\n]*\n", "const RESULTS = /*RESULTS*/null;\n", page, count=1)
    with open("results.html", "w", encoding="utf-8") as f:
        f.write(page)
    print("results.html is a blank template again")


def main():
    if input("Delete both live surveys, all ballots, and the results? This can't be undone. Type YES: ") != "YES":
        print("Cancelled.")
        return
    for path in LIVE_SURVEYS + glob.glob(os.path.join(BALLOT_DIR, "*.zip")) + glob.glob(os.path.join(BALLOT_DIR, "*.json")):
        if os.path.exists(path):
            remove_file(path)
    print("Everything under ballots has been deleted.")
    reset_results()


main()