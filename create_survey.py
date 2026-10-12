import csv
import io
import zipfile


def entering_survey():
    while True:
        enter_survey = input("Enter the corresponding zip file: ")

        if enter_survey.lower().endswith('.zip'):
            return enter_survey  # returns the filename so zipfile can open it.
        print("That is not a .zip file. Try again.")


def load_csv(archive, name):
    # Reads one CSV out of the zip ONCE into a list of rows (dicts), because a file stream can only be read once.
    # Matches the name ignoring upper/lower case, since zip lookups are case-sensitive.
    real_name = next(n for n in archive.namelist() if n.lower() == name.lower())
    with archive.open(real_name, 'r') as raw_file:
        # the stream is bytes, so wrap it as text before DictReader turns each line into a dict
        return list(csv.DictReader(io.TextIOWrapper(raw_file, encoding="utf-8")))


def select_qbs(passing_rows):
    # Master vault initialized at the very top so it never gets wiped out.
    qb_ballot_options = []
    chosen_tags = set()  # rosterIds already picked, so nobody can be picked twice across all three slots

    while len(qb_ballot_options) < 3:
        selecting_qb = input(f"\nEnter All-Pro QB Candidate #{len(qb_ballot_options) + 1}: ")

        # converting to lowercase for language type security; skip anyone already chosen
        matching_qbs = [row for row in passing_rows
                        if selecting_qb.lower() in row['player__fullName'].lower()
                        and row['player__rosterId'] not in chosen_tags]

        if not matching_qbs:
            print("No matching QB's. Try again.")
            continue

        shown = matching_qbs[:10]
        print(f"\nFound {len(matching_qbs)} matching QB's. Displaying first {len(shown)}:")

        # Enumerate tracks the index from the front of the list
        for index, player in enumerate(shown):
            print(f"[{index}] {player['player__fullName']} ({player['player__position']} - {player['team__abbrName']})")

        max_index = len(shown) - 1  # indexed by what is actually in the list

        # Selection Feature: Validated input instance
        while True:
            user_choice = input(f"\nType the index number of the player you want (0-{max_index}): ")

            if user_choice.isdigit() and 0 <= int(user_choice) <= max_index:
                chosen_player = shown[int(user_choice)]
                chosen_tags.add(chosen_player['player__rosterId'])
                qb_ballot_options.append(chosen_player)  # STORE: drops them into the permanent vault
                print(f"Player Chosen: {chosen_player['player__fullName']}!")
                break  # moves on to the next candidate slot
            print(f"Invalid selection. Please choose a number from 0 to {max_index}.")

    return qb_ballot_options


def creating_survey(zip_file):
    with zipfile.ZipFile(zip_file, "r") as archive:
        passing_rows = load_csv(archive, "BAWLS_passing.csv")
        rushing_rows = load_csv(archive, "BAWLS_rushing.csv")
        receiving_rows = load_csv(archive, "BAWLS_receiving.csv")
        defense_rows = load_csv(archive, "BAWLS_defense.csv")
        kicking_rows = load_csv(archive, "BAWLS_kicking.csv")
        punting_rows = load_csv(archive, "BAWLS_punting.csv")
    # the zip is closed here; everything lives in memory now

    return select_qbs(passing_rows)


zip_file = entering_survey()
creating_survey(zip_file)