#!/usr/bin/python3
"""
To use this script, there should be N files
named 1.txt, 2.txt, 3.txt, ..., N.txt
in quest_stages folder
(number of them can be passed to gen_hashes function)
with header (name of quest stages) in first line and
all info starting from second line.
Passwords (hashes) will be writen on screen
and in file hashes.txt

Script will ask about hashes which one to use:
random one or get them from keyboard
"""
import json

import os
import random

project_folder = os.path.dirname(__file__)

def random_word(length, allowed_characters="qwertyuiopasdfghjklzxcvbnm"):
   return ''.join(random.choice(allowed_characters) for _ in range(length))

def gen_hashes(number_of_quest_stages=6, number_of_teams = 6, length_of_keys=8):

    random_keys_switch_character = input("Would you use random keys? (y/n)\n")
    random_keys = False
    if random_keys_switch_character == 'y':
        print("Using random keys")
        random_keys = True
    elif random_keys_switch_character == 'n':
        print("Using self-writen keys")
    else:
        print("Unrecognised value, using self-writen keys")

    stages = []
    for stage_id in range(1, number_of_quest_stages + 1):
        with open(os.path.join(project_folder, 'quest_stages', "{}.txt".format(stage_id))) as in_file:
            stage = {
                'title': in_file.readline().strip(),
                'body' : in_file.read()
            }
        if random_keys:
            stage['key'] = random_word(length_of_keys)
        else:
            stage['key'] = input("Enter key for quest stages {} ({}):\n".format(stage_id, stage['title']))
        print("Stage number {} ({}) key: {}\n".format(stage_id, stage['title'], stage['key']))
        stages.append(stage)

    teams = []
    for team_id in range(1, number_of_teams + 1):
        team = {
            'id': team_id,
            'start_hash': input("Enter first hash for team number {}:\n".format(team_id)),
        }
        teams.append(team)

    quest_hashes_map = {}
    team_first_stage_id = 0
    for team in teams:
        prev_hash = None
        for stage_id in range(team_first_stage_id, team_first_stage_id + number_of_quest_stages):
            stage = stages[stage_id % number_of_quest_stages]
            if prev_hash is None:
                quest_hashes_map[team['start_hash']] = {
                    'stage': stage,
                }
                prev_hash = team['start_hash']
            else:
                cur_hash = random_word(length_of_keys)
                quest_hashes_map[prev_hash]['next_hash'] = cur_hash
                quest_hashes_map[cur_hash] = {
                    'stage': stage,
                }
                prev_hash = cur_hash
        team['last_hash'] = prev_hash
        team_first_stage_id += 1

    last_stage_switch_character = input('Add last stage, same for all teams? (y/n)\n')
    if last_stage_switch_character == 'y':
        loaded_file = False
        while not loaded_file:
            last_stage_file_name = input('Enter last stage file name (file should be inside quest_stages folder):\n')
            try:
                last_stage_file = open(os.path.join(project_folder, 'quest_stages', last_stage_file_name))
                last_stage = {
                    'title': last_stage_file.readline().strip(),
                    'body': last_stage_file.read()
                }
                loaded_file = True
            except FileNotFoundError:
                print("File not found!\n")
                try_again_switch_character = input("Try again? (y/n)\n")
                if try_again_switch_character == 'n':
                    return

        last_stage_hash = random_word(length_of_keys)
        for team in teams:
            quest_hashes_map[team['last_hash']]['next_hash'] = last_stage_hash
        quest_hashes_map[last_stage_hash] = {
            'stage': last_stage,
        }

    with open(os.path.join(project_folder, 'hashes_map.json'), 'w') as hashes_map_file:
        hashes_map_file.write(json.dumps(quest_hashes_map))

if __name__ == '__main__':
    gen_hashes()

