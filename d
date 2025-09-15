Please extract the table from this image and return it in CSV format. 
Make sure the output is clean, with column headers and properly separated rows, so it can be copied directly into a CSV file.

    # French
    "janvier": 1, "février": 2, "mars": 3, "avril": 4, "mai": 5,
    "juin": 6, "juillet": 7, "août": 8, "septembre": 9,
    "octobre": 10, "novembre": 11, "décembre": 12,
    # English
    "january": 1, "february": 2, "march": 3, "april": 4, "may": 5,
    "june": 6, "july": 7, "august": 8, "september": 9,
    "october": 10, "november": 11, "december": 12,
}

# Regex for "day month year [hh:mm]"
pattern = r"\b(?:lundi|mardi|mercredi|jeudi|vendredi|samedi|dimanche|monday|tuesday|wednesday|thursday|friday|saturday|sunday)\s+\d{1,2}\s+[a-zA-Zéû]+\s+\d{4}\s+\d{1,2}:\d{2}\b'

for match in re.finditer(pattern, text, re.IGNORECASE):
    dow, day, month_name, year, hour, minute = match.groups()
    month_num = months.get(month_name.lower())
    if month_num:
        if hour and minute:
            dt = datetime(int(year), month_num, int(day), int(hour), int(minute))
            date_str = dt.strftime("%Y-%m-%d %H:%M")
