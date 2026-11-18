# Shared story data for all news-image-20261117 variants.
# SAME content as v2.1 — only the presentation differs per variant.
# Do not change headlines, numbers, or counts.

LEAD_KICKER = "LEAD STORY — EUROPE"
LEAD_HEADLINE = ("KERCH BRIDGE", "FALLS")  # second word is the red accent word
LEAD_SUB = "Road span collapses as Kyiv bridges burn"
LEAD_SUMMARY = ("Ukraine struck the 19 km bridge to Crimea for a second straight "
                "night. Russia hit two Kyiv bridges, killing at least two.")

TOP3 = [
    ("2", "IRAN DRONES AT US RADAR IN BAHRAIN",
     "Third attack in five days on the Gulf island, home of the US 5th Fleet. Bahrain says it intercepted the drones; no casualties reported."),
    ("3", "TRUMP, XI & PUTIN TO MEET IN SHENZHEN",
     "China confirms a trilateral summit on Thursday, 19 Nov, on the APEC sidelines. Trump is in Manila; Xi cuts $280m of Canada tariffs."),
    ("4", "TANKERS HIT BY MINES NEAR HORMUZ",
     "A fourth tanker catches fire in 24 hours on routes Tehran calls unauthorised. A third US carrier, USS Theodore Roosevelt, arrives."),
]

# (name, stories) — 6 regions x 5 stories = 30, + lead 1 + top3 3 + also-today 2 = 36
SECTIONS = [
    ("EUROPE", [
        ("5", "Russia hits Kyiv bridges, 2 killed in overnight strikes"),
        ("6", "Five EU states plan Rwanda return hub for 2027"),
        ("7", "Depardieu admits sexual assault, drops appeal"),
        ("8", "UK sanctions 8 firms building West Bank settlements"),
        ("9", "UN: 128 states debate ban on killer robots in Geneva"),
    ]),
    ("MIDDLE EAST", [
        ("10", "Houthis take Bab al-Mandab coast as forces fall back to Aden"),
        ("11", "Jordan bans Telegram over national security"),
        ("12", "UK, Australia, Canada, Italy urge Israel to open Gaza aid"),
        ("13", "Settler kills 72-year-old woman in Jericho, West Bank"),
        ("14", "UN: rebuilding Syria will cost $216bn; 4m have returned"),
    ]),
    ("ASIA-PACIFIC", [
        ("15", "Japan scrambles jets as suspected Russian planes enter airspace"),
        ("16", "Taiwan and S. Korea also track Russian aircraft"),
        ("17", "US closes AI-chip rental loophole aimed at China"),
        ("18", "Singapore seeks trusted access to advanced AI chips"),
        ("19", "India bus plunges into ravine, 6-8 dead in Uttarakhand"),
    ]),
    ("AFRICA", [
        ("20", "S. Africa: 17 dead in two separate mass shootings"),
        ("21", "DR Congo Ebola out of control: 5,500 dead, 11,200 cases"),
        ("22", "Guinea arrests 1,263 in gold-mining crackdown"),
        ("23", "Sudan: drones cause ~3 in 4 war deaths this year, UN says"),
        ("24", "S. Sudan: 3 abducted aid workers freed after $2,500 ransom"),
    ]),
    ("NORTH AMERICA", [
        ("25", "Pentagon fails 9th audit in a row — $4.8tn unverified"),
        ("26", "US measles hits 5,412 cases, most since 1991; 13 babies born with it"),
        ("27", "White House: agencies need approval to testify to Congress"),
        ("28", "Supreme Court declines to revive $59m UC grant cuts"),
        ("29", "US banks hit by outages; Apple and Marriott systems down"),
    ]),
    ("LATIN AMERICA & OCEANIA", [
        ("30", "Pope Leo XIV ends Peru trip, forgives rosary thrower"),
        ("31", "Pope demands justice for murdered Amazon defenders"),
        ("32", "Costa Rica journalist shot dead after probing drug links"),
        ("33", "Pacific workers need stronger protection, COP31 report warns"),
        ("34", "Scotland edges Australia 15-12; Wales beat NZ after 73 years"),
    ]),
]

ALSO_TODAY = ("35", "COP31 climate summit continues in Antalya, Turkey",
               "36", "AFCON 2027 qualifiers: Senegal & Cameroon win")

DATE_LINE = "TUESDAY, 17 NOVEMBER 2026"
MASTHEAD = "THE WORLD IN ONE DAY"
FOOTER = "36 stories  •  6 continents  •  Sources: AP, Reuters, AFP, BBC, Guardian, Al Jazeera — full list in README"
