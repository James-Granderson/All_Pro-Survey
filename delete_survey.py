# End of a voting cycle: removes the live surveys, wipes the votes, and resets results.html to the blank template.
import os
import re

LIVE_SURVEYS = ["live_survey_offense.html", "live_survey_defense.html"]


def remove_file(path):
    if os.path.exists(path):
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
    if input("Delete the live surveys and all votes? This can't be undone. Type YES: ") != "YES":
        print("Cancelled.")
        return
    for survey in LIVE_SURVEYS:
        remove_file(survey)
    remove_file("votes.txt")
    reset_results()


main()