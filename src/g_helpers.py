import datetime
from collections import defaultdict

data = {
    "ברכות": 63,
    "שבת": 156,
    "עירובין": 104,
    "פסחים": 120,
    "שקלים": 21,
    "ראש_השנה": 34,
    "יומא": 87,
    "סוכה": 55,
    "ביצה": 39,
    "תענית": 30,
    "מגילה": 31,
    "מועד_קטן": 28,
    "חגיגה": 26,
    "יבמות": 121,
    "כתובות": 111,
    "נדרים": 90,
    "נזיר": 65,
    "סוטה": 48,
    "גיטין": 89,
    "קידושין": 81,
    "בבא_קמא": 118,
    "בבא_מציעא": 118,
    "בבא_בתרא": 175,
    "סנהדרין": 112,
    "מכות": 23,
    "שבועות": 48,
    "עבודה_זרה": 75,
    "הוריות": 13,
    "זבחים": 119,
    "מנחות": 109,
    "חולין": 141,
    "בכורות": 60,
    "ערכין": 33,
    "תמורה": 33,
    "כריתות": 27,
    "מעילה": 20,
    "קינים": 3,
    "מדות": 4,
    "תמיד": 9,
    "נדה": 72,
}


def maschtot_names():
    return list(data.keys())


def number_of_pages(masechet):
    return data[masechet]


_heb_letters = [
    ("א", 1),
    ("ב", 2),
    ("ג", 3),
    ("ד", 4),
    ("ה", 5),
    ("ו", 6),
    ("ז", 7),
    ("ח", 8),
    ("ט", 9),
    ("י", 10),
    ("כ", 20),
    ("ל", 30),
    ("מ", 40),
    ("נ", 50),
    ("ס", 60),
    ("ע", 70),
    ("פ", 80),
    ("צ", 90),
    ("ק", 100),
    ("ר", 200),
    ("ש", 300),
    ("ת", 400)
    ]

def number_to_hebrew(number):
    if number <= 0:
        raise Exception("Number must be bigger than zero")
    if number >= 1000:
        raise Exception("Number bigger than 999 is not supported yet")

    remainder = number
    heb_sum = ""
    while remainder > 0:
        for heb_letter, val in _heb_letters[::-1]:
            if val <= remainder:
                if remainder == 15:
                    heb_sum += "טו"
                    remainder = 0
                elif remainder == 16:
                    heb_sum += "טז"
                    remainder = 0
                else:
                    heb_sum += heb_letter
                    remainder -= val
                break
    return heb_sum


dapim = []
masechet_to_dapim = defaultdict(list)
for maschet, num_of_pages in data.items():
    for i in range(num_of_pages):
        dapim.append((maschet, number_to_hebrew(i+2)))
        masechet_to_dapim[maschet].append(number_to_hebrew(i+2))
print(len(dapim))

def date_to_daf(date):
    """
    >>> import datetime
    >>> date = datetime.date(2024, 7, 12)
    >>> date_to_daf(date)
    ('בבא_בתרא', 'יז')
    """
    start_of_daf_yomi = datetime.date(2020, 1, 5)
    days = (date - start_of_daf_yomi).days
    days = days % len(dapim)
    return dapim[days]

