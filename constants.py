NUMBER_OF_RACES = 24

PREDICTION_KEYS_2024 = set(
    [
        "QH2H",
        "RH2H",

        "CChamp",
        "DChamp",
        "NAfterN",

        "Podiums",
        "Poles",
        "FLs",
        "Q1",
        "Monaco",

        "MaxDNF",
        "MinLaps",
        "DeltaPos",
        "DeltaPts",
        "MaxPS",
        "SlowStarter",
        "EngineComps",
        "FastestPS",
        "QCons",

        "Gasly",
        "Hulk",
        "BlowyEngines"
    ]
)

PREDICTION_TYPES_2024 = {
    "H2H": ["QH2H","RH2H"],
    "Champs": ["CChamp", "DChamp"],
    "True/False": ["Podiums", "Poles", "FLs", "Q1", "Monaco"],
    "PickN": ["NAfterN","Gasly","Hulk","BlowyEngines"],
    "SuperlativesDrivers": ["MaxDNF", "MinLaps", "DeltaPos", "DeltaPts", "MaxPS", "SlowStarter"],
    "SuperlativesTeams":  ["EngineComps", "FastestPS", "QCons"]
}

PLAYERS_TO_COLOURS = {
    "Benedict": (4, 2, 115), #"midnightblue",
    "Carla": (232, 0, 45), #"red",
    "Damian": (250, 194, 5), #"yellow",
    "Jarek": (2, 143, 30), #"forestgreen",
    "Josh": (255, 91, 0), #"orange",
    "Kacper": (19, 234, 201), #"cyan",
    "Suley": (154, 14, 234) #"purple"
}
