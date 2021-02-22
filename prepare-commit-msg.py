#!/usr/bin/env python3
import sys, os
import json


def main():
    sys.stdin = open("/dev/tty", "r")
    NOJIRA = "NOJIRA"

    commit_msg_filepath = sys.argv[1]

    commit_type = sys.argv[2] if len(sys.argv) > 2 else None
    commit_types_to_ignore = ["commit", "merge", "sqaush"]

    if commit_type is not None and any(
        x in commit_type for x in commit_types_to_ignore
    ):
        exit(0)

    home_path = os.environ["HOME"]
    project_specs_filepath = f"{home_path}/commit_info.json"

    commit_info = {
        "project": "Default project",
        "card_number": "Default card_number",
        "pairs": "Default pairs",
        "message": "Default message",
    }

    if not os.path.exists(project_specs_filepath):
        project_name = input(">>> What project are you working on? ")
        card_number = input(">>> What's the card number? ")
        initials_long = input(">>> What's the pair's initials (space delimited)? ")
        message = input(">>> What's the message for this commit? ")

        commit_info["project"] = project_name.upper()
        commit_info["card_number"] = card_number
        commit_info["pairs"] = initials_long.upper().split()
        commit_info["message"] = message

        with open(project_specs_filepath, "w") as outfile:
            json.dump(commit_info, outfile)
    else:
        with open(project_specs_filepath) as json_file:
            data = json.load(json_file)
            commit_info["project"] = data["project"]
            commit_info["card_number"] = data["card_number"]
            commit_info["pairs"] = data["pairs"]
            commit_info["message"] = data["message"]

        print(">>> Leave blank to use current... <<<")
        project_name = input(f">>> Project? Current - {commit_info['project']}: ")
        card_number = input(
            f">>> Card Number? Current - {commit_info['card_number']}: "
        )
        initials_long = input(
            f">>> Pairs? Current - {'|'.join(commit_info['pairs'])}: "
        )
        message = input(f">>> Message? Current - \"{commit_info['message']}\": ")

        if project_name:
            commit_info["project"] = project_name
        if card_number:
            commit_info["card_number"] = card_number
        if initials_long:
            commit_info["pairs"] = initials_long.split()
        if message:
            commit_info["message"] = message

        with open(project_specs_filepath, "w") as outfile:
            json.dump(commit_info, outfile)

    with open(commit_msg_filepath, "w") as file:
        if NOJIRA in {
            commit_info["project"].upper(),
            commit_info["card_number"].upper(),
        }:
            file.write(
                f"[{NOJIRA}][{'|'.join(commit_info['pairs'])}] {commit_info['message']}"
            )
        else:
            file.write(
                f"[{commit_info['project']}-{commit_info['card_number']}][{'|'.join(commit_info['pairs'])}] {commit_info['message']}"
            )


if __name__ == "__main__":
    main()
