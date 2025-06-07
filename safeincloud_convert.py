import sys
import os
import json
import csv
import xml.etree.ElementTree as ET

def parse_sic_json(json_file):
    with open(json_file, encoding='utf-8') as f:
        data = json.load(f)
    cards = []
    if isinstance(data, dict):
        db = data.get("database", {})
        cards = db.get("card", [])
    elif isinstance(data, list):
        cards = data
    else:
        cards = []
    entries = []
    for card in cards:
        if card.get("@template") == "true":
            continue
        entry = {
            "Name": card.get("@title", ""),
            "Username": "",
            "Password": "",
            "URL": "",
            "Notes": "",
            "TOTP": ""
        }
        fields = card.get("field", [])
        if isinstance(fields, dict):
            fields = [fields]
        for field in fields:
            fname = field.get("@name", "").lower()
            fval = field.get("#text", "")
            if "login" in fname or "user" in fname or "email" in fname:
                entry["Username"] = fval
            elif "password" in fname:
                entry["Password"] = fval
            elif "website" in fname or "url" in fname:
                entry["URL"] = fval
            elif "one-time password" in fname or "otp" in fname or "totp" in fname:
                entry["TOTP"] = fval
            else:
                if fval:
                    entry["Notes"] += f"{fname.title()}: {fval}\n"
        notes = card.get("notes")
        if notes:
            if isinstance(notes, dict):
                entry["Notes"] += notes.get("#text", "")
            elif isinstance(notes, str):
                entry["Notes"] += notes
        entries.append(entry)
    return entries

def parse_sic_xml(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    entries = []
    for card in root.findall('card'):
        if card.get('template') == 'true':
            continue
        entry = {
            "Name": card.get("title", ""),
            "Username": "",
            "Password": "",
            "URL": "",
            "Notes": "",
            "TOTP": ""
        }
        for field in card.findall('field'):
            fname = field.get("name", "").lower()
            fval = field.text or ""
            if "login" in fname or "user" in fname or "email" in fname:
                entry["Username"] = fval
            elif "password" in fname:
                entry["Password"] = fval
            elif "website" in fname or "url" in fname:
                entry["URL"] = fval
            elif "one-time password" in fname or "otp" in fname or "totp" in fname:
                entry["TOTP"] = fval
            else:
                if fval:
                    entry["Notes"] += f"{fname.title()}: {fval}\n"
        notes_elem = card.find('notes')
        if notes_elem is not None and notes_elem.text:
            entry["Notes"] += notes_elem.text
        entries.append(entry)
    return entries

def parse_sic_csv(csv_file):
    entries = []
    with open(csv_file, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            entries.append(row)
    return entries

def write_csv(entries, csv_file):
    fieldnames = ["Name", "Username", "Password", "URL", "Notes", "TOTP"]
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for entry in entries:
            writer.writerow(entry)

def entries_to_notes(entries, outfile):
    with open(outfile, 'w', encoding='utf-8') as f:
        for entry in entries:
            f.write(f"Title: {entry.get('Name','')}\n")
            f.write(f"Username: {entry.get('Username','')}\n")
            f.write(f"Password: {entry.get('Password','')}\n")
            f.write(f"URL: {entry.get('URL','')}\n")
            notes = entry.get('Notes','').strip()
            f.write(f"Notes: {notes if notes else '(blank)'}\n")
            f.write(f"TOTP: {entry.get('TOTP','') or '(blank)'}\n")
            f.write('-' * 25 + '\n')

def main():
    if len(sys.argv) < 4:
        print("Usage: python safeincloud_convert.py <input.(json|xml|csv)> <output.(csv|txt)> <csv|notes>")
        sys.exit(1)
    infile = sys.argv[1]
    outfile = sys.argv[2]
    mode = sys.argv[3].lower()
    ext = os.path.splitext(infile)[1].lower()
    # Parse entries
    if ext == ".json":
        entries = parse_sic_json(infile)
    elif ext == ".xml":
        entries = parse_sic_xml(infile)
    elif ext == ".csv":
        entries = parse_sic_csv(infile)
    else:
        print("Input file must be .json, .xml, or .csv")
        sys.exit(1)
    # Output
    if mode == "csv":
        write_csv(entries, outfile)
        print(f"Exported {len(entries)} entries to {outfile}")
    elif mode == "notes":
        entries_to_notes(entries, outfile)
        print(f"Exported {len(entries)} entries to {outfile} (human readable notes)")
    else:
        print("Mode must be 'csv' or 'notes'")

if __name__ == "__main__":
    main()

