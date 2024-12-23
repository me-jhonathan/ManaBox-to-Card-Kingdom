import os
import re
import csv
import sys


#  replace manabox set name for cardkingdom standards (ignoring case)
REPLACEMENT_DICT = {
    "crimson vow commander": "Innistrad: Vow Commander Decks",
    "tales of middle-earth commander": "The Lord of the Rings: Tales of Middle-earth Commander Decks",
    "modern horizons 3 commander": "Modern Horizons 3 Commander Decks",
    "outlaws of thunder junction commander": "Outlaws Of Thunder Junction Commander Decks",
    "fallout": "Universes Beyond: Fallout",
    "doctor who": "Universes Beyond: Doctor Who",
    "assassin's creed": "Universes Beyond: Assassin's Creed",
    "warhammer 40,000 commander": "Universes Beyond: Warhammer 40,000",
    "murders at karlov manor commander": "Murders at Karlov Manor Commander Decks",
    "wilds of eldraine commander": "Wilds of Eldraine Commander Decks",
    "dominaria united commander": "Dominaria United Commander Decks"
}


RARITY_CATEGORIES = {"common", "uncommon", "rare", "mythic"}


def replace_set_name_for_cardkingdom_standard(set_name):
    lower_set_name = set_name.lower()
    for key, replacement in REPLACEMENT_DICT.items():
        if re.search(key, lower_set_name):
            return replacement
    return set_name


def check_for_input_file(input_file):
    if not os.path.isfile(input_file):
        print(f"\nERROR: Input_file: `{input_file}` does not exist please add then retry.\n")
    sys.exit(1) 


    OUTPUT_FOLDER = 'Manabox to Cardkingdom'
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def process_csv(input_file):
    """
    Process the collection CSV file, split cards by rarity,
    and generate a combined rarities file.
    """

    check_for_input_file(input_file)

    output_files = {
        'common': os.path.join(OUTPUT_FOLDER, 'common_cards.csv'),
        'uncommon': os.path.join(OUTPUT_FOLDER, 'uncommon_cards.csv'),
        'rare': os.path.join(OUTPUT_FOLDER, 'rare_cards.csv'),
        'mythic': os.path.join(OUTPUT_FOLDER, 'mythic_cards.csv'),
        'other': os.path.join(OUTPUT_FOLDER, 'other_cards.csv'),
        'all_rarities': os.path.join(OUTPUT_FOLDER, 'all_rarities.csv')
    }

    writers = {rarity: open(file, mode='w', newline='', encoding='utf-8') for rarity, file in output_files.items()}
    csv_writers = {rarity: csv.writer(file) for rarity, file in writers.items()}

    combined_rarities = []

    with open(input_file, mode='r', newline='', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        headers = next(reader, None)  # Skip header row

        for row in reader:
            name = f'"{row[2]}"'
            set_name = replace_set_name_for_cardkingdom_standard(row[4])
            foil = '0' if row[6] == 'normal' else '1'
            quantity = row[8]
            rarity = row[7].lower()

            combined_rarities.append([name, set_name, foil, quantity])

            if rarity in RARITY_CATEGORIES:
                csv_writers[rarity].writerow([name, set_name, foil, quantity])
            else:
                csv_writers['other'].writerow([name, set_name, foil, quantity])

    with open(output_files['all_rarities'], mode='w', newline='', encoding='utf-8') as rarities_file:
        writer = csv.writer(rarities_file)
        for row in combined_rarities:
            writer.writerow(row)

    for writer in writers.values():
        writer.close()

    # post-process to fix triple quotes issue
    for output_file in output_files.values():
        with open(output_file, mode='r', newline='', encoding='utf-8') as file:
            data = file.read()
        data = data.replace('"""', '"')
        with open(output_file, mode='w', newline='', encoding='utf-8') as file:
            file.write(data)

    print(f"Processed '{input_file}' and saved outputs in '{OUTPUT_FOLDER}'.")


input_file = 'ManaBox_Collection.csv'

process_csv(input_file)
