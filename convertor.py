#!/usr/bin/python3
import csv
import re
import sys
import os

# Check for command-line arguments
if len(sys.argv) < 2:
    print("Export vault to CSV from VaultWarden then provide path to the file as bellow")
    print("If second path not specified, it will export in current folder")
    print("Usage: python convertor.py <bitwarden_csv_file> [keepassxc_csv_file]")
    sys.exit(1)

# Get input Bitwarden CSV file
bitwarden_csv_file = sys.argv[1]

# Determine output file path
if len(sys.argv) > 2:
    output_path = sys.argv[2]
    # If the output path is a folder, save file as 'keepassxc-import.csv' inside it
    if os.path.isdir(output_path) or not output_path.lower().endswith(".csv"):
        keepassxc_csv_file = os.path.join(output_path, "keepassxc-import.csv")
    else:
        keepassxc_csv_file = output_path
else:
    keepassxc_csv_file = "keepassxc-import.csv"

# Check if the input file exists
if not os.path.isfile(bitwarden_csv_file):
    print(f"Error: The file '{bitwarden_csv_file}' does not exist.")
    sys.exit(1)

# Read Bitwarden CSV and process data
with open(bitwarden_csv_file, "r", encoding="utf-8") as infile, \
     open(keepassxc_csv_file, "w", encoding="utf-8", newline="") as outfile:
    
    reader = csv.DictReader(infile)
    writer = csv.writer(outfile)

    # KeePassXC CSV header
    writer.writerow(["Group", "Title", "Username", "Password", "URL", "Notes", "TOTP", "Icon", "Last Modified", "Created"])

    for row in reader:
        # Process only "login" and "note" types
        item_type = row.get("type", "").strip().lower()
        if item_type not in ["login", "note"]:
            continue

        group = row.get("folder", "").strip()
        
        # If the entry is a note and has no folder, set "Imported Notes"
        if item_type == "note" and not group:
            group = "Imported Notes"

        title = row.get("name", "").strip()
        username = row.get("login_username", "").strip()
        password = row.get("login_password", "").strip()
        
        # Process notes & fields
        notes = row.get("notes", "").strip()
        fields = row.get("fields", "").strip()
        if fields:
            notes = f"{notes}\n{fields}".strip()

        # Extract TOTP secret
        totp_secret = ""
        totp_url = row.get("login_totp", "").strip()
        if totp_url:
            match = re.search(r"secret=([A-Z0-9]+)", totp_url)
            if match:
                totp_secret = match.group(1)

        # Process URLs (split if multiple)
        urls = row.get("login_uri", "").strip()
        if urls:
            url_list = urls.split(",")  # Multiple URLs separated by ","
            for url in url_list:
                writer.writerow([group, title, username, password, url.strip(), notes, totp_secret, "", "", ""])
        else:
            # If no URL, write a single entry
            writer.writerow([group, title, username, password, "", notes, totp_secret, "", "", ""])

print(f"Conversion complete! Saved to '{keepassxc_csv_file}'.")
