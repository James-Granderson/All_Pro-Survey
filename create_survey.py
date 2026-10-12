import csv
import io
import zipfile
import json
import os
import uuid

# Candidates the commissioner picks per position (from his forms), and votes each position gets on the ballot.
CANDIDATES = {"QB": 3, "RB": 3, "WR": 6, "TE": 3, "APO": 3,
              "EDGE": 5, "IDL": 4, "LB": 6, "CB": 5, "FS": 3, "SS": 3}
VOTE_SLOTS = {"QB": 1, "RB": 1, "APO": 1, "WR": 2, "TE": 1,
              "EDGE": 2, "IDL": 2, "LB": 3, "CB": 2, "FS": 1, "SS": 1}


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

    while len(qb_ballot_options) < CANDIDATES["QB"]:
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


def select_rbs(rushing_rows):
    # Master vault initialized at the very top so it never gets wiped out.
    rbs_ballot_options = []
    chosen_tags = set()  # rosterIds already picked, so nobody can be picked twice

    while len(rbs_ballot_options) < CANDIDATES["RB"]:
        selecting_player = input(f"\nEnter All-Pro RB Candidate #{len(rbs_ballot_options) + 1}: ")

        # lowercase for language type security; only this position's players; skip anyone already chosen
        matching_players = [row for row in rushing_rows
                            if selecting_player.lower() in row['player__fullName'].lower()
                            and row['player__position'] in ["HB"]
                            and row['player__rosterId'] not in chosen_tags]

        if not matching_players:
            print("No matching RB's. Try again.")
            continue

        shown = matching_players[:10]
        print(f"\nFound {len(matching_players)} matching RB's. Displaying first {len(shown)}:")

        for index, player in enumerate(shown):
            print(f"[{index}] {player['player__fullName']} ({player['player__position']} - {player['team__abbrName']})")

        max_index = len(shown) - 1  # indexed by what is actually in the list

        while True:
            user_choice = input(f"\nType the index number of the player you want (0-{max_index}): ")

            if user_choice.isdigit() and 0 <= int(user_choice) <= max_index:
                chosen_player = shown[int(user_choice)]
                chosen_tags.add(chosen_player['player__rosterId'])
                rbs_ballot_options.append(chosen_player)
                print(f"Player Chosen: {chosen_player['player__fullName']}!")
                break
            print(f"Invalid selection. Please choose a number from 0 to {max_index}.")

    return rbs_ballot_options


def select_apos(rushing_rows):
    # Master vault initialized at the very top so it never gets wiped out.
    apos_ballot_options = []
    chosen_tags = set()  # rosterIds already picked, so nobody can be picked twice

    while len(apos_ballot_options) < CANDIDATES["APO"]:
        selecting_player = input(f"\nEnter All-Pro APO Candidate #{len(apos_ballot_options) + 1}: ")

        # lowercase for language type security; only this position's players; skip anyone already chosen
        matching_players = [row for row in rushing_rows
                            if selecting_player.lower() in row['player__fullName'].lower()
                            and row['player__position'] in ["HB"]
                            and row['player__rosterId'] not in chosen_tags]

        if not matching_players:
            print("No matching APO's. Try again.")
            continue

        shown = matching_players[:10]
        print(f"\nFound {len(matching_players)} matching APO's. Displaying first {len(shown)}:")

        for index, player in enumerate(shown):
            print(f"[{index}] {player['player__fullName']} ({player['player__position']} - {player['team__abbrName']})")

        max_index = len(shown) - 1  # indexed by what is actually in the list

        while True:
            user_choice = input(f"\nType the index number of the player you want (0-{max_index}): ")

            if user_choice.isdigit() and 0 <= int(user_choice) <= max_index:
                chosen_player = shown[int(user_choice)]
                chosen_tags.add(chosen_player['player__rosterId'])
                apos_ballot_options.append(chosen_player)
                print(f"Player Chosen: {chosen_player['player__fullName']}!")
                break
            print(f"Invalid selection. Please choose a number from 0 to {max_index}.")

    return apos_ballot_options


def select_wrs(receiving_rows):
    # Master vault initialized at the very top so it never gets wiped out.
    wrs_ballot_options = []
    chosen_tags = set()  # rosterIds already picked, so nobody can be picked twice

    while len(wrs_ballot_options) < CANDIDATES["WR"]:
        selecting_player = input(f"\nEnter All-Pro WR Candidate #{len(wrs_ballot_options) + 1}: ")

        # lowercase for language type security; only this position's players; skip anyone already chosen
        matching_players = [row for row in receiving_rows
                            if selecting_player.lower() in row['player__fullName'].lower()
                            and row['player__position'] in ["WR"]
                            and row['player__rosterId'] not in chosen_tags]

        if not matching_players:
            print("No matching WR's. Try again.")
            continue

        shown = matching_players[:10]
        print(f"\nFound {len(matching_players)} matching WR's. Displaying first {len(shown)}:")

        for index, player in enumerate(shown):
            print(f"[{index}] {player['player__fullName']} ({player['player__position']} - {player['team__abbrName']})")

        max_index = len(shown) - 1  # indexed by what is actually in the list

        while True:
            user_choice = input(f"\nType the index number of the player you want (0-{max_index}): ")

            if user_choice.isdigit() and 0 <= int(user_choice) <= max_index:
                chosen_player = shown[int(user_choice)]
                chosen_tags.add(chosen_player['player__rosterId'])
                wrs_ballot_options.append(chosen_player)
                print(f"Player Chosen: {chosen_player['player__fullName']}!")
                break
            print(f"Invalid selection. Please choose a number from 0 to {max_index}.")

    return wrs_ballot_options


def select_tes(receiving_rows):
    # Master vault initialized at the very top so it never gets wiped out.
    tes_ballot_options = []
    chosen_tags = set()  # rosterIds already picked, so nobody can be picked twice

    while len(tes_ballot_options) < CANDIDATES["TE"]:
        selecting_player = input(f"\nEnter All-Pro TE Candidate #{len(tes_ballot_options) + 1}: ")

        # lowercase for language type security; only this position's players; skip anyone already chosen
        matching_players = [row for row in receiving_rows
                            if selecting_player.lower() in row['player__fullName'].lower()
                            and row['player__position'] in ["TE"]
                            and row['player__rosterId'] not in chosen_tags]

        if not matching_players:
            print("No matching TE's. Try again.")
            continue

        shown = matching_players[:10]
        print(f"\nFound {len(matching_players)} matching TE's. Displaying first {len(shown)}:")

        for index, player in enumerate(shown):
            print(f"[{index}] {player['player__fullName']} ({player['player__position']} - {player['team__abbrName']})")

        max_index = len(shown) - 1  # indexed by what is actually in the list

        while True:
            user_choice = input(f"\nType the index number of the player you want (0-{max_index}): ")

            if user_choice.isdigit() and 0 <= int(user_choice) <= max_index:
                chosen_player = shown[int(user_choice)]
                chosen_tags.add(chosen_player['player__rosterId'])
                tes_ballot_options.append(chosen_player)
                print(f"Player Chosen: {chosen_player['player__fullName']}!")
                break
            print(f"Invalid selection. Please choose a number from 0 to {max_index}.")

    return tes_ballot_options


def select_edges(defense_rows):
    # Master vault initialized at the very top so it never gets wiped out.
    edges_ballot_options = []
    chosen_tags = set()  # rosterIds already picked, so nobody can be picked twice

    while len(edges_ballot_options) < CANDIDATES["EDGE"]:
        selecting_player = input(f"\nEnter All-Pro EDGE Candidate #{len(edges_ballot_options) + 1}: ")

        # lowercase for language type security; only this position's players; skip anyone already chosen
        matching_players = [row for row in defense_rows
                            if selecting_player.lower() in row['player__fullName'].lower()
                            and row['player__position'] in ["LEDGE", "REDGE"]
                            and row['player__rosterId'] not in chosen_tags]

        if not matching_players:
            print("No matching EDGE's. Try again.")
            continue

        shown = matching_players[:10]
        print(f"\nFound {len(matching_players)} matching EDGE's. Displaying first {len(shown)}:")

        for index, player in enumerate(shown):
            print(f"[{index}] {player['player__fullName']} ({player['player__position']} - {player['team__abbrName']})")

        max_index = len(shown) - 1  # indexed by what is actually in the list

        while True:
            user_choice = input(f"\nType the index number of the player you want (0-{max_index}): ")

            if user_choice.isdigit() and 0 <= int(user_choice) <= max_index:
                chosen_player = shown[int(user_choice)]
                chosen_tags.add(chosen_player['player__rosterId'])
                edges_ballot_options.append(chosen_player)
                print(f"Player Chosen: {chosen_player['player__fullName']}!")
                break
            print(f"Invalid selection. Please choose a number from 0 to {max_index}.")

    return edges_ballot_options


def select_idls(defense_rows):
    # Master vault initialized at the very top so it never gets wiped out.
    idls_ballot_options = []
    chosen_tags = set()  # rosterIds already picked, so nobody can be picked twice

    while len(idls_ballot_options) < CANDIDATES["IDL"]:
        selecting_player = input(f"\nEnter All-Pro IDL Candidate #{len(idls_ballot_options) + 1}: ")

        # lowercase for language type security; only this position's players; skip anyone already chosen
        matching_players = [row for row in defense_rows
                            if selecting_player.lower() in row['player__fullName'].lower()
                            and row['player__position'] in ["DT"]
                            and row['player__rosterId'] not in chosen_tags]

        if not matching_players:
            print("No matching IDL's. Try again.")
            continue

        shown = matching_players[:10]
        print(f"\nFound {len(matching_players)} matching IDL's. Displaying first {len(shown)}:")

        for index, player in enumerate(shown):
            print(f"[{index}] {player['player__fullName']} ({player['player__position']} - {player['team__abbrName']})")

        max_index = len(shown) - 1  # indexed by what is actually in the list

        while True:
            user_choice = input(f"\nType the index number of the player you want (0-{max_index}): ")

            if user_choice.isdigit() and 0 <= int(user_choice) <= max_index:
                chosen_player = shown[int(user_choice)]
                chosen_tags.add(chosen_player['player__rosterId'])
                idls_ballot_options.append(chosen_player)
                print(f"Player Chosen: {chosen_player['player__fullName']}!")
                break
            print(f"Invalid selection. Please choose a number from 0 to {max_index}.")

    return idls_ballot_options


def select_lbs(defense_rows):
    # Master vault initialized at the very top so it never gets wiped out.
    lbs_ballot_options = []
    chosen_tags = set()  # rosterIds already picked, so nobody can be picked twice

    while len(lbs_ballot_options) < CANDIDATES["LB"]:
        selecting_player = input(f"\nEnter All-Pro LB Candidate #{len(lbs_ballot_options) + 1}: ")

        # lowercase for language type security; only this position's players; skip anyone already chosen
        matching_players = [row for row in defense_rows
                            if selecting_player.lower() in row['player__fullName'].lower()
                            and row['player__position'] in ["MIKE", "WILL", "SAM"]
                            and row['player__rosterId'] not in chosen_tags]

        if not matching_players:
            print("No matching LB's. Try again.")
            continue

        shown = matching_players[:10]
        print(f"\nFound {len(matching_players)} matching LB's. Displaying first {len(shown)}:")

        for index, player in enumerate(shown):
            print(f"[{index}] {player['player__fullName']} ({player['player__position']} - {player['team__abbrName']})")

        max_index = len(shown) - 1  # indexed by what is actually in the list

        while True:
            user_choice = input(f"\nType the index number of the player you want (0-{max_index}): ")

            if user_choice.isdigit() and 0 <= int(user_choice) <= max_index:
                chosen_player = shown[int(user_choice)]
                chosen_tags.add(chosen_player['player__rosterId'])
                lbs_ballot_options.append(chosen_player)
                print(f"Player Chosen: {chosen_player['player__fullName']}!")
                break
            print(f"Invalid selection. Please choose a number from 0 to {max_index}.")

    return lbs_ballot_options


def select_cbs(defense_rows):
    # Master vault initialized at the very top so it never gets wiped out.
    cbs_ballot_options = []
    chosen_tags = set()  # rosterIds already picked, so nobody can be picked twice

    while len(cbs_ballot_options) < CANDIDATES["CB"]:
        selecting_player = input(f"\nEnter All-Pro CB Candidate #{len(cbs_ballot_options) + 1}: ")

        # lowercase for language type security; only this position's players; skip anyone already chosen
        matching_players = [row for row in defense_rows
                            if selecting_player.lower() in row['player__fullName'].lower()
                            and row['player__position'] in ["CB"]
                            and row['player__rosterId'] not in chosen_tags]

        if not matching_players:
            print("No matching CB's. Try again.")
            continue

        shown = matching_players[:10]
        print(f"\nFound {len(matching_players)} matching CB's. Displaying first {len(shown)}:")

        for index, player in enumerate(shown):
            print(f"[{index}] {player['player__fullName']} ({player['player__position']} - {player['team__abbrName']})")

        max_index = len(shown) - 1  # indexed by what is actually in the list

        while True:
            user_choice = input(f"\nType the index number of the player you want (0-{max_index}): ")

            if user_choice.isdigit() and 0 <= int(user_choice) <= max_index:
                chosen_player = shown[int(user_choice)]
                chosen_tags.add(chosen_player['player__rosterId'])
                cbs_ballot_options.append(chosen_player)
                print(f"Player Chosen: {chosen_player['player__fullName']}!")
                break
            print(f"Invalid selection. Please choose a number from 0 to {max_index}.")

    return cbs_ballot_options


def select_fss(defense_rows):
    # Master vault initialized at the very top so it never gets wiped out.
    fss_ballot_options = []
    chosen_tags = set()  # rosterIds already picked, so nobody can be picked twice

    while len(fss_ballot_options) < CANDIDATES["FS"]:
        selecting_player = input(f"\nEnter All-Pro FS Candidate #{len(fss_ballot_options) + 1}: ")

        # lowercase for language type security; only this position's players; skip anyone already chosen
        matching_players = [row for row in defense_rows
                            if selecting_player.lower() in row['player__fullName'].lower()
                            and row['player__position'] in ["FS"]
                            and row['player__rosterId'] not in chosen_tags]

        if not matching_players:
            print("No matching FS's. Try again.")
            continue

        shown = matching_players[:10]
        print(f"\nFound {len(matching_players)} matching FS's. Displaying first {len(shown)}:")

        for index, player in enumerate(shown):
            print(f"[{index}] {player['player__fullName']} ({player['player__position']} - {player['team__abbrName']})")

        max_index = len(shown) - 1  # indexed by what is actually in the list

        while True:
            user_choice = input(f"\nType the index number of the player you want (0-{max_index}): ")

            if user_choice.isdigit() and 0 <= int(user_choice) <= max_index:
                chosen_player = shown[int(user_choice)]
                chosen_tags.add(chosen_player['player__rosterId'])
                fss_ballot_options.append(chosen_player)
                print(f"Player Chosen: {chosen_player['player__fullName']}!")
                break
            print(f"Invalid selection. Please choose a number from 0 to {max_index}.")

    return fss_ballot_options


def select_sss(defense_rows):
    # Master vault initialized at the very top so it never gets wiped out.
    sss_ballot_options = []
    chosen_tags = set()  # rosterIds already picked, so nobody can be picked twice

    while len(sss_ballot_options) < CANDIDATES["SS"]:
        selecting_player = input(f"\nEnter All-Pro SS Candidate #{len(sss_ballot_options) + 1}: ")

        # lowercase for language type security; only this position's players; skip anyone already chosen
        matching_players = [row for row in defense_rows
                            if selecting_player.lower() in row['player__fullName'].lower()
                            and row['player__position'] in ["SS"]
                            and row['player__rosterId'] not in chosen_tags]

        if not matching_players:
            print("No matching SS's. Try again.")
            continue

        shown = matching_players[:10]
        print(f"\nFound {len(matching_players)} matching SS's. Displaying first {len(shown)}:")

        for index, player in enumerate(shown):
            print(f"[{index}] {player['player__fullName']} ({player['player__position']} - {player['team__abbrName']})")

        max_index = len(shown) - 1  # indexed by what is actually in the list

        while True:
            user_choice = input(f"\nType the index number of the player you want (0-{max_index}): ")

            if user_choice.isdigit() and 0 <= int(user_choice) <= max_index:
                chosen_player = shown[int(user_choice)]
                chosen_tags.add(chosen_player['player__rosterId'])
                sss_ballot_options.append(chosen_player)
                print(f"Player Chosen: {chosen_player['player__fullName']}!")
                break
            print(f"Invalid selection. Please choose a number from 0 to {max_index}.")

    return sss_ballot_options


def index_players(files):
    # One record per player: every file's columns joined on rosterId, so an RB has rushing AND receiving stats.
    by_tag = {}
    for rows in files.values():
        for row in rows:
            by_tag.setdefault(row["player__rosterId"], {}).update(row)
    return by_tag


def team_names(files):
    # The team dropdown on the survey.
    return sorted({row["team__displayName"] for rows in files.values() for row in rows})


def build_live_survey(title, picks, files, filename):
    # Fills the survey.html template with the picks and writes the live instance.
    if os.path.exists(filename):
        raise FileExistsError(f"{filename} already exists. Delete it first.")
    by_tag = index_players(files)
    positions = [{"pos": pos, "slots": VOTE_SLOTS[pos], "cands": [by_tag[r["player__rosterId"]] for r in rows]}
                 for pos, rows in picks.items() if rows]
    ballot = {"id": uuid.uuid4().hex[:8], "title": title, "teams": team_names(files), "positions": positions}
    with open("survey.html", encoding="utf-8") as f:
        template = f.read()
    if "/*BALLOT*/null" not in template:
        raise ValueError("survey.html is not the blank template.")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(template.replace("/*BALLOT*/null", json.dumps(ballot)))
    os.chmod(filename, 0o444)  # locked until delete_survey.py removes it
    print(f"Built {filename}")


def creating_survey(zip_file):
    with zipfile.ZipFile(zip_file, "r") as archive:
        files = {name: load_csv(archive, f"BAWLS_{name}.csv")
                 for name in ("passing", "rushing", "receiving", "defense", "kicking", "punting")}
    # the zip is closed here; everything lives in memory now

    offense = {"QB": select_qbs(files["passing"]), "RB": select_rbs(files["rushing"]),
               "WR": select_wrs(files["receiving"]), "TE": select_tes(files["receiving"]),
               "APO": select_apos(files["rushing"])}
    defense = {"EDGE": select_edges(files["defense"]), "IDL": select_idls(files["defense"]),
               "LB": select_lbs(files["defense"]), "CB": select_cbs(files["defense"]),
               "FS": select_fss(files["defense"]), "SS": select_sss(files["defense"])}

    # the end of create_survey: fill survey.html into the live instances
    build_live_survey("Offensive All-Pro", offense, files, "live_survey_offense.html")
    build_live_survey("Defensive All-Pro", defense, files, "live_survey_defense.html")


zip_file = entering_survey()
creating_survey(zip_file)