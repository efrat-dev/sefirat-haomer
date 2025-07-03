
# data.py - Complete data file with transliteration and English support

OMER_TEXTS = {
    1: "הַיּוֹם יוֹם אֶחָד לָעֹמֶר",
    2: "הַיּוֹם שְׁנֵי יָמִים לָעֹמֶר",
    3: "הַיּוֹם שְׁלֹשָׁה יָמִים לָעֹמֶר",
    4: "הַיּוֹם אַרְבָּעָה יָמִים לָעֹמֶר",
    5: "הַיּוֹם חֲמִשָּׁה יָמִים לָעֹמֶר",
    6: "הַיּוֹם שִׁשָּׁה יָמִים לָעֹמֶר",
    7: "הַיּוֹם שִׁבְעָה יָמִים, שֶׁהֵם שָׁבוּעַ אֶחָד לָעֹמֶר",
    8: "הַיּוֹם שְׁמוֹנָה יָמִים, שֶׁהֵם שָׁבוּעַ אֶחָד וְיוֹם אֶחָד לָעֹמֶר",
    9: "הַיּוֹם תִּשְׁעָה יָמִים, שֶׁהֵם שָׁבוּעַ אֶחָד וּשְׁנֵי יָמִים לָעֹמֶר",
    10: "הַיּוֹם עֲשָׂרָה יָמִים, שֶׁהֵם שָׁבוּעַ אֶחָד וּשְׁלֹשָׁה יָמִים לָעֹמֶר",
    11: "הַיּוֹם אַחַד עָשָׂר יוֹם, שֶׁהֵם שָׁבוּעַ אֶחָד וְאַרְבָּעָה יָמִים לָעֹמֶר",
    12: "הַיּוֹם שְׁנֵים עָשָׂר יוֹם, שֶׁהֵם שָׁבוּעַ אֶחָד וַחֲמִשָּׁה יָמִים לָעֹמֶר",
    13: "הַיּוֹם שְׁלֹשָׁה עָשָׂר יוֹם, שֶׁהֵם שָׁבוּעַ אֶחָד וְשִׁשָּׁה יָמִים לָעֹמֶר",
    14: "הַיּוֹם אַרְבָּעָה עָשָׂר יוֹם, שֶׁהֵם שְׁנֵי שָׁבוּעוֹת לָעֹמֶר",
    15: "הַיּוֹם חֲמִשָּׁה עָשָׂר יוֹם, שֶׁהֵם שְׁנֵי שָׁבוּעוֹת וְיוֹם אֶחָד לָעֹמֶר",
    16: "הַיּוֹם שִׁשָּׁה עָשָׂר יוֹם, שֶׁהֵם שְׁנֵי שָׁבוּעוֹת וּשְׁנֵי יָמִים לָעֹמֶר",
    17: "הַיּוֹם שִׁבְעָה עָשָׂר יוֹם, שֶׁהֵם שְׁנֵי שָׁבוּעוֹת וּשְׁלֹשָׁה יָמִים לָעֹמֶר",
    18: "הַיּוֹם שְׁמוֹנָה עָשָׂר יוֹם, שֶׁהֵם שְׁנֵי שָׁבוּעוֹת וְאַרְבָּעָה יָמִים לָעֹמֶר",
    19: "הַיּוֹם תִּשְׁעָה עָשָׂר יוֹם, שֶׁהֵם שְׁנֵי שָׁבוּעוֹת וַחֲמִשָּׁה יָמִים לָעֹמֶר",
    20: "הַיּוֹם עֶשְׂרִים יוֹם, שֶׁהֵם שְׁנֵי שָׁבוּעוֹת וְשִׁשָּׁה יָמִים לָעֹמֶר",
    21: "הַיּוֹם עֶשְׂרִים וְאֶחָד יוֹם, שֶׁהֵם שְׁלֹשָׁה שָׁבוּעוֹת לָעֹמֶר",
    22: "הַיּוֹם עֶשְׂרִים וּשְׁנֵי יָמִים, שֶׁהֵם שְׁלֹשָׁה שָׁבוּעוֹת וְיוֹם אֶחָד לָעֹמֶר",
    23: "הַיּוֹם עֶשְׂרִים וּשְׁלֹשָׁה יָמִים, שֶׁהֵם שְׁלֹשָׁה שָׁבוּעוֹת וּשְׁנֵי יָמִים לָעֹמֶר",
    24: "הַיּוֹם עֶשְׂרִים וְאַרְבָּעָה יָמִים, שֶׁהֵם שְׁלֹשָׁה שָׁבוּעוֹת וּשְׁלֹשָׁה יָמִים לָעֹמֶר",
    25: "הַיּוֹם עֶשְׂרִים וַחֲמִשָּׁה יָמִים, שֶׁהֵם שְׁלֹשָׁה שָׁבוּעוֹת וְאַרְבָּעָה יָמִים לָעֹמֶר",
    26: "הַיּוֹם עֶשְׂרִים וְשִׁשָּׁה יָמִים, שֶׁהֵם שְׁלֹשָׁה שָׁבוּעוֹת וַחֲמִשָּׁה יָמִים לָעֹמֶר",
    27: "הַיּוֹם עֶשְׂרִים וְשִׁבְעָה יָמִים, שֶׁהֵם שְׁלֹשָׁה שָׁבוּעוֹת וְשִׁשָּׁה יָמִים לָעֹמֶר",
    28: "הַיּוֹם שְׁמוֹנָה וְעֶשְׂרִים יוֹם, שֶׁהֵם אַרְבָּעָה שָׁבוּעוֹת לָעֹמֶר",
    29: "הַיּוֹם תִּשְׁעָה וְעֶשְׂרִים יוֹם, שֶׁהֵם אַרְבָּעָה שָׁבוּעוֹת וְיוֹם אֶחָד לָעֹמֶר",
    30: "הַיּוֹם שְׁלֹשִׁים יוֹם, שֶׁהֵם אַרְבָּעָה שָׁבוּעוֹת וּשְׁנֵי יָמִים לָעֹמֶר",
    31: "הַיּוֹם אֶחָד וּשְׁלֹשִׁים יוֹם, שֶׁהֵם אַרְבָּעָה שָׁבוּעוֹת וּשְׁלֹשָׁה יָמִים לָעֹמֶר",
    32: "הַיּוֹם שְׁנַיִם וּשְׁלֹשִׁים יוֹם, שֶׁהֵם אַרְבָּעָה שָׁבוּעוֹת וְאַרְבָּעָה יָמִים לָעֹמֶר",
    33: "הַיּוֹם שְׁלֹשָׁה וּשְׁלֹשִׁים יוֹם, שֶׁהֵם אַרְבָּעָה שָׁבוּעוֹת וַחֲמִשָּׁה יָמִים לָעֹמֶר",
    34: "הַיּוֹם אַרְבָּעָה וּשְׁלֹשִׁים יוֹם, שֶׁהֵם אַרְבָּעָה שָׁבוּעוֹת וְשִׁשָּׁה יָמִים לָעֹמֶר",
    35: "הַיּוֹם חֲמִשָּׁה וּשְׁלֹשִׁים יוֹם, שֶׁהֵם חֲמִשָּׁה שָׁבוּעוֹת לָעֹמֶר",
    36: "הַיּוֹם שִׁשָּׁה וּשְׁלֹשִׁים יוֹם, שֶׁהֵם חֲמִשָּׁה שָׁבוּעוֹת וְיוֹם אֶחָד לָעֹמֶר",
    37: "הַיּוֹם שִׁבְעָה וּשְׁלֹשִׁים יוֹם, שֶׁהֵם חֲמִשָּׁה שָׁבוּעוֹת וּשְׁנֵי יָמִים לָעֹמֶר",
    38: "הַיּוֹם שְׁמוֹנָה וּשְׁלֹשִׁים יוֹם, שֶׁהֵם חֲמִשָּׁה שָׁבוּעוֹת וּשְׁלֹשָׁה יָמִים לָעֹמֶר",
    39: "הַיּוֹם תִּשְׁעָה וּשְׁלֹשִׁים יוֹם, שֶׁהֵם חֲמִשָּׁה שָׁבוּעוֹת וְאַרְבָּעָה יָמִים לָעֹמֶר",
    40: "הַיּוֹם אַרְבָּעִים יוֹם, שֶׁהֵם חֲמִשָּׁה שָׁבוּעוֹת וַחֲמִשָּׁה יָמִים לָעֹמֶר",
    41: "הַיּוֹם אֶחָד וְאַרְבָּעִים יוֹם, שֶׁהֵם חֲמִשָּׁה שָׁבוּעוֹת וְשִׁשָּׁה יָמִים לָעֹמֶר",
    42: "הַיּוֹם שְׁנַיִם וְאַרְבָּעִים יוֹם, שֶׁהֵם שִׁשָּׁה שָׁבוּעוֹת לָעֹמֶר",
    43: "הַיּוֹם שְׁלֹשָׁה וְאַרְבָּעִים יוֹם, שֶׁהֵם שִׁשָּׁה שָׁבוּעוֹת וְיוֹם אֶחָד לָעֹמֶר",
    44: "הַיּוֹם אַרְבָּעָה וְאַרְבָּעִים יוֹם, שֶׁהֵם שִׁשָּׁה שָׁבוּעוֹת וּשְׁנֵי יָמִים לָעֹמֶר",
    45: "הַיּוֹם חֲמִשָּׁה וְאַרְבָּעִים יוֹם, שֶׁהֵם שִׁשָּׁה שָׁבוּעוֹת וּשְׁלֹשָׁה יָמִים לָעֹמֶר",
    46: "הַיּוֹם שִׁשָּׁה וְאַרְבָּעִים יוֹם, שֶׁהֵם שִׁשָּׁה שָׁבוּעוֹת וְאַרְבָּעָה יָמִים לָעֹמֶר",
    47: "הַיּוֹם שִׁבְעָה וְאַרְבָּעִים יוֹם, שֶׁהֵם שִׁשָּׁה שָׁבוּעוֹת וַחֲמִשָּׁה יָמִים לָעֹמֶר",
    48: "הַיּוֹם שְׁמוֹנָה וְאַרְבָּעִים יוֹם, שֶׁהֵם שִׁשָּׁה שָׁבוּעוֹת וְשִׁשָּׁה יָמִים לָעֹמֶר",
    49: "הַיּוֹם תִּשְׁעָה וְאַרְבָּעִים יוֹם, שֶׁהֵם שִׁבְעָה שָׁבוּעוֹת לָעֹמֶר",
}

# Transliterated texts (using standard transliteration)
OMER_TRANSLITERATIONS = {
    1: "Hayom yom echad la'omer",
    2: "Hayom shnei yamim la'omer",
    3: "Hayom shloshah yamim la'omer",
    4: "Hayom arba'ah yamim la'omer",
    5: "Hayom chamishah yamim la'omer",
    6: "Hayom shishah yamim la'omer",
    7: "Hayom shiv'ah yamim, shehem shavu'a echad la'omer",
    8: "Hayom shmonah yamim, shehem shavu'a echad v'yom echad la'omer",
    9: "Hayom tish'ah yamim, shehem shavu'a echad ushnei yamim la'omer",
    10: "Hayom asarah yamim, shehem shavu'a echad ushloshah yamim la'omer",
    11: "Hayom achad asar yom, shehem shavu'a echad v'arba'ah yamim la'omer",
    12: "Hayom shneim asar yom, shehem shavu'a echad vachamishah yamim la'omer",
    13: "Hayom shloshah asar yom, shehem shavu'a echad v'shishah yamim la'omer",
    14: "Hayom arba'ah asar yom, shehem shnei shavu'ot la'omer",
    15: "Hayom chamishah asar yom, shehem shnei shavu'ot v'yom echad la'omer",
    16: "Hayom shishah asar yom, shehem shnei shavu'ot ushnei yamim la'omer",
    17: "Hayom shiv'ah asar yom, shehem shnei shavu'ot ushloshah yamim la'omer",
    18: "Hayom shmonah asar yom, shehem shnei shavu'ot v'arba'ah yamim la'omer",
    19: "Hayom tish'ah asar yom, shehem shnei shavu'ot vachamishah yamim la'omer",
    20: "Hayom esrim yom, shehem shnei shavu'ot v'shishah yamim la'omer",
    21: "Hayom esrim v'echad yom, shehem shloshah shavu'ot la'omer",
    22: "Hayom esrim ushnei yamim, shehem shloshah shavu'ot v'yom echad la'omer",
    23: "Hayom esrim ushloshah yamim, shehem shloshah shavu'ot ushnei yamim la'omer",
    24: "Hayom esrim v'arba'ah yamim, shehem shloshah shavu'ot ushloshah yamim la'omer",
    25: "Hayom esrim vachamishah yamim, shehem shloshah shavu'ot v'arba'ah yamim la'omer",
    26: "Hayom esrim v'shishah yamim, shehem shloshah shavu'ot vachamishah yamim la'omer",
    27: "Hayom esrim v'shiv'ah yamim, shehem shloshah shavu'ot v'shishah yamim la'omer",
    28: "Hayom shmonah v'esrim yom, shehem arba'ah shavu'ot la'omer",
    29: "Hayom tish'ah v'esrim yom, shehem arba'ah shavu'ot v'yom echad la'omer",
    30: "Hayom shloshim yom, shehem arba'ah shavu'ot ushnei yamim la'omer",
    31: "Hayom echad ushloshim yom, shehem arba'ah shavu'ot ushloshah yamim la'omer",
    32: "Hayom shnayim ushloshim yom, shehem arba'ah shavu'ot v'arba'ah yamim la'omer",
    33: "Hayom shloshah ushloshim yom, shehem arba'ah shavu'ot vachamishah yamim la'omer",
    34: "Hayom arba'ah ushloshim yom, shehem arba'ah shavu'ot v'shishah yamim la'omer",
    35: "Hayom chamishah ushloshim yom, shehem chamishah shavu'ot la'omer",
    36: "Hayom shishah ushloshim yom, shehem chamishah shavu'ot v'yom echad la'omer",
    37: "Hayom shiv'ah ushloshim yom, shehem chamishah shavu'ot ushnei yamim la'omer",
    38: "Hayom shmonah ushloshim yom, shehem chamishah shavu'ot ushloshah yamim la'omer",
    39: "Hayom tish'ah ushloshim yom, shehem chamishah shavu'ot v'arba'ah yamim la'omer",
    40: "Hayom arba'im yom, shehem chamishah shavu'ot vachamishah yamim la'omer",
    41: "Hayom echad v'arba'im yom, shehem chamishah shavu'ot v'shishah yamim la'omer",
    42: "Hayom shnayim v'arba'im yom, shehem shishah shavu'ot la'omer",
    43: "Hayom shloshah v'arba'im yom, shehem shishah shavu'ot v'yom echad la'omer",
    44: "Hayom arba'ah v'arba'im yom, shehem shishah shavu'ot ushnei yamim la'omer",
    45: "Hayom chamishah v'arba'im yom, shehem shishah shavu'ot ushloshah yamim la'omer",
    46: "Hayom shishah v'arba'im yom, shehem shishah shavu'ot v'arba'ah yamim la'omer",
    47: "Hayom shiv'ah v'arba'im yom, shehem shishah shavu'ot vachamishah yamim la'omer",
    48: "Hayom shmonah v'arba'im yom, shehem shishah shavu'ot v'shishah yamim la'omer",
    49: "Hayom tish'ah v'arba'im yom, shehem shiv'ah shavu'ot la'omer",
}

# English translations
OMER_ENGLISH_TRANSLATIONS = {
    1: "Today is one day of the Omer",
    2: "Today is two days of the Omer",
    3: "Today is three days of the Omer",
    4: "Today is four days of the Omer",
    5: "Today is five days of the Omer",
    6: "Today is six days of the Omer",
    7: "Today is seven days, which is one week of the Omer",
    8: "Today is eight days, which is one week and one day of the Omer",
    9: "Today is nine days, which is one week and two days of the Omer",
    10: "Today is ten days, which is one week and three days of the Omer",
    11: "Today is eleven days, which is one week and four days of the Omer",
    12: "Today is twelve days, which is one week and five days of the Omer",
    13: "Today is thirteen days, which is one week and six days of the Omer",
    14: "Today is fourteen days, which is two weeks of the Omer",
    15: "Today is fifteen days, which is two weeks and one day of the Omer",
    16: "Today is sixteen days, which is two weeks and two days of the Omer",
    17: "Today is seventeen days, which is two weeks and three days of the Omer",
    18: "Today is eighteen days, which is two weeks and four days of the Omer",
    19: "Today is nineteen days, which is two weeks and five days of the Omer",
    20: "Today is twenty days, which is two weeks and six days of the Omer",
    21: "Today is twenty-one days, which is three weeks of the Omer",
    22: "Today is twenty-two days, which is three weeks and one day of the Omer",
    23: "Today is twenty-three days, which is three weeks and two days of the Omer",
    24: "Today is twenty-four days, which is three weeks and three days of the Omer",
    25: "Today is twenty-five days, which is three weeks and four days of the Omer",
    26: "Today is twenty-six days, which is three weeks and five days of the Omer",
    27: "Today is twenty-seven days, which is three weeks and six days of the Omer",
    28: "Today is twenty-eight days, which is four weeks of the Omer",
    29: "Today is twenty-nine days, which is four weeks and one day of the Omer",
    30: "Today is thirty days, which is four weeks and two days of the Omer",
    31: "Today is thirty-one days, which is four weeks and three days of the Omer",
    32: "Today is thirty-two days, which is four weeks and four days of the Omer",
    33: "Today is thirty-three days, which is four weeks and five days of the Omer",
    34: "Today is thirty-four days, which is four weeks and six days of the Omer",
    35: "Today is thirty-five days, which is five weeks of the Omer",
    36: "Today is thirty-six days, which is five weeks and one day of the Omer",
    37: "Today is thirty-seven days, which is five weeks and two days of the Omer",
    38: "Today is thirty-eight days, which is five weeks and three days of the Omer",
    39: "Today is thirty-nine days, which is five weeks and four days of the Omer",
    40: "Today is forty days, which is five weeks and five days of the Omer",
    41: "Today is forty-one days, which is five weeks and six days of the Omer",
    42: "Today is forty-two days, which is six weeks of the Omer",
    43: "Today is forty-three days, which is six weeks and one day of the Omer",
    44: "Today is forty-four days, which is six weeks and two days of the Omer",
    45: "Today is forty-five days, which is six weeks and three days of the Omer",
    46: "Today is forty-six days, which is six weeks and four days of the Omer",
    47: "Today is forty-seven days, which is six weeks and five days of the Omer",
    48: "Today is forty-eight days, which is six weeks and six days of the Omer",
    49: "Today is forty-nine days, which is seven weeks of the Omer",
}

# Hebrew months and their lengths
HEBREW_MONTHS = {
    1: "Nisan",
    2: "Iyyar",
    3: "Sivan"
}

HEBREW_MONTH_LENGTHS = {
    "Nisan": 30,
    "Iyyar": 29,
    "Sivan": 30
}

# Hebrew month names in Hebrew
HEBREW_MONTH_NAMES_HEBREW = {
    "Nisan": "נִיסָן",
    "Iyyar": "אִיָּר",
    "Sivan": "סִיוָן"
}

# Sefirot attributes for each week (Kabbalistic tradition)
SEFIROT_ATTRIBUTES = {
    1: {"hebrew": "חֶסֶד", "transliteration": "Chesed", "english": "Loving-kindness"},
    2: {"hebrew": "גְּבוּרָה", "transliteration": "Gevurah", "english": "Strength/Discipline"},
    3: {"hebrew": "תִּפְאֶרֶת", "transliteration": "Tiferet", "english": "Beauty/Harmony"},
    4: {"hebrew": "נֶצַח", "transliteration": "Netzach", "english": "Victory/Endurance"},
    5: {"hebrew": "הוֹד", "transliteration": "Hod", "english": "Splendor/Humility"},
    6: {"hebrew": "יְסוֹד", "transliteration": "Yesod", "english": "Foundation/Connection"},
    7: {"hebrew": "מַלְכוּת", "transliteration": "Malchut", "english": "Kingship/Sovereignty"}
}

# Daily sefirah combinations (week x day)
DAILY_SEFIROT = {}
for week in range(1, 8):
    for day in range(1, 8):
        omer_day = (week - 1) * 7 + day
        if omer_day <= 49:
            week_attr = SEFIROT_ATTRIBUTES[week]
            day_attr = SEFIROT_ATTRIBUTES[day]
            DAILY_SEFIROT[omer_day] = {
                "week_sefirah": week_attr,
                "day_sefirah": day_attr,
                "combination": f"{day_attr['hebrew']} שֶׁבְּ{week_attr['hebrew']}",
                "combination_transliteration": f"{day_attr['transliteration']} sheb'{week_attr['transliteration']}",
                "combination_english": f"{day_attr['english']} within {week_attr['english']}"
            }
# המשך קובץ data.py מהמקום שעצרתי

# Special days during the Omer period
SPECIAL_DAYS = {
    33: {
        "name": "Lag BaOmer",
        "hebrew": "ל\"ג בעומר",
        "description": "33rd day of the Omer, a day of celebration",
        "description_hebrew": "יום השלושים ושלושה לעומר, יום שמחה"
    },
    18: {
        "name": "Pesach Sheni",
        "hebrew": "פסח שני",
        "description": "Second Passover",
        "description_hebrew": "פסח שני"
    }
}

# Blessing for counting the Omer
OMER_BLESSING = {
    "hebrew": "בָּרוּךְ אַתָּה הַשֵּׁם אֱלֹקֵינוּ מֶלֶךְ הָעוֹלָם, אֲשֶׁר קִדְּשָׁנוּ בְּמִצְווֹתָיו וְצִוָּנוּ עַל סְפִירַת הָעֹמֶר",
    "transliteration": "Baruch atah HaShem Elokeinu melech ha'olam, asher kid'shanu b'mitzvotav v'tzivanu al sfirat ha'omer",
    "english": "Blessed are You, Lord our God, King of the universe, who has sanctified us with His commandments and commanded us concerning the counting of the Omer"
}

# Prayer said after the blessing and counting
OMER_PRAYER = {
    "hebrew": "הָרַחֲמָן הוּא יַחֲזִיר לָנוּ עֲבוֹדַת בֵּית הַמִּקְדָּש לִמְקוֹמָהּ בִּמְהֵרָה בְיָמֵינוּ אָמֵן",
    "transliteration": "HaRachaman hu yachazir lanu avodat beit hamikdash limkoma bimhera b'yameinu amen",
    "english": "May the Merciful One restore the service of the Holy Temple to its place, speedily in our days, Amen"
}

# Ana BeKoach prayer (often recited during Omer)
ANA_BEKOACH = {
    "hebrew": [
        "אָנָּא בְכֹחַ גְּדֻלַּת יְמִינְךָ תַּתִּיר צְרוּרָה",
        "קַבֵּל רִנַּת עַמְּךָ שַׂגְּבֵנוּ טַהֲרֵנוּ נוֹרָא",
        "נָא גִבּוֹר דּוֹרְשֵׁי יִחוּדְךָ כְּבָבַת שָׁמְרֵם",
        "בָּרְכֵם טַהֲרֵם רַחֲמֵי צִדְקָתְךָ תָּמִיד גָּמְלֵם",
        "חֲסִין קָדוֹשׁ בְּרוֹב טוּבְךָ נַהֵל עֲדָתֶךָ",
        "יָחִיד גֵּאֶה לְעַמְּךָ פְּנֵה זוֹכְרֵי קְדֻשָּׁתֶךָ",
        "שַׁוְעָתֵנוּ קַבֵּל וּשְׁמַע צַעֲקָתֵנוּ יוֹדֵעַ תַּעֲלֻמוֹת"
    ],
    "transliteration": [
        "Ana b'koach g'dulat y'mincha tatir tz'rurah",
        "Kabel rinat amcha sagveinu tahareinu nora",
        "Na gibor dorshei yichudcha k'bavat shamrem",
        "Barchem tahrem rachamei tzidkatcha tamid gamlem",
        "Chasin kadosh b'rov tuvcha nahel adatecha",
        "Yachid ge'eh l'amcha p'neh zochrei k'dushatecha",
        "Shavateinu kabel ushma tza'akateinu yode'a ta'alumot"
    ],
    "english": [
        "Please, by the power of Your great right hand, release the bound",
        "Accept the song of Your people, strengthen us, purify us, Awesome One",
        "Please, Mighty One, those who seek Your unity, guard them like the apple of Your eye",
        "Bless them, purify them, Your mercy and righteousness always reward them",
        "Mighty Holy One, in Your abundant goodness, guide Your congregation",
        "Unique and Exalted One, turn to Your people who remember Your holiness",
        "Accept our supplication and hear our cry, You who know all hidden things"
    ]
}

# Additional prayers and readings for special days
SPECIAL_PRAYERS = {
    "lag_baomer": {
        "hebrew": "בָּרוּךְ אַתָּה הַשֵּׁם אֱלֹקֵינוּ מֶלֶךְ הָעוֹלָם שֶׁהֶחֱיָנוּ וְקִיְּמָנוּ וְהִגִּיעָנוּ לַזְּמַן הַזֶּה",
        "transliteration": "Baruch atah HaShem Elokeinu melech ha'olam shehecheyanu v'kiyemanu v'higianu lazman hazeh",
        "english": "Blessed are You, Lord our God, King of the universe, who has kept us alive, sustained us, and brought us to this season"
    }
}

# Hebrew date calculations helper data
HEBREW_DATE_INFO = {
    "epoch_offset": 3761,  # Hebrew calendar epoch relative to Common Era
    "leap_year_cycle": 19,  # Metonic cycle
    "leap_years_in_cycle": [3, 6, 8, 11, 14, 17, 19]  # Leap years in 19-year cycle
}

# Day of week names in Hebrew
HEBREW_WEEKDAYS = {
    0: {"hebrew": "יוֹם רִאשׁוֹן", "transliteration": "Yom Rishon", "english": "Sunday"},
    1: {"hebrew": "יוֹם שֵׁנִי", "transliteration": "Yom Sheni", "english": "Monday"},
    2: {"hebrew": "יוֹם שְׁלִישִׁי", "transliteration": "Yom Shlishi", "english": "Tuesday"},
    3: {"hebrew": "יוֹם רְבִיעִי", "transliteration": "Yom Revi'i", "english": "Wednesday"},
    4: {"hebrew": "יוֹם חֲמִישִׁי", "transliteration": "Yom Chamishi", "english": "Thursday"},
    5: {"hebrew": "יוֹם שִׁשִּׁי", "transliteration": "Yom Shishi", "english": "Friday"},
    6: {"hebrew": "שַׁבָּת", "transliteration": "Shabbat", "english": "Sabbath"}
}

# Omer period astronomical and halachic times
OMER_TIMES = {
    "preferred_counting_time": "after_nightfall",
    "latest_counting_time": "before_dawn",
    "makeup_blessing": "without_blessing_if_missed_night"
}

# Custom texts for different traditions
CUSTOM_TEXTS = {
    "sefardi": {
        "omer_intro": "בְּמִצְוַת עֲשֵׂה שֶׁנִּצְטַוֵּינוּ עַל יְדֵי מֹשֶׁה רַבֵּנוּ",
        "omer_intro_transliteration": "B'mitzvat aseh she'nitzta'vinu al yedei Moshe rabbeinu",
        "omer_intro_english": "With the positive commandment that we were commanded through Moses our teacher"
    },
    "ashkenazi": {
        "omer_intro": "הִנְנִי מוּכָן וּמְזֻמָּן לְקַיֵּם מִצְוַת עֲשֵׂה שֶׁל סְפִירַת הָעֹמֶר",
        "omer_intro_transliteration": "Hineni muchan umzuman l'kayem mitzvat aseh shel sfirat ha'omer",
        "omer_intro_english": "Behold, I am ready and prepared to fulfill the positive commandment of counting the Omer"
    },
    "chassidic": {
        "additional_prayer": "לְשֵׁם יִחוּד קוּדְשָׁא בְּרִיךְ הוּא וּשְׁכִינְתֵּהּ",
        "additional_prayer_transliteration": "L'shem yichud Kudsha Brich Hu ushchinteih",
        "additional_prayer_english": "For the sake of the unification of the Holy One, blessed be He, and His Divine Presence"
    }
}

# Kabbalistic intentions for each day
KAVANNOT = {
    "general": {
        "hebrew": "יְהִי רָצוֹן מִלְּפָנֶיךָ הַשֵּׁם אֱלֹקֵינוּ וֵאלֹקֵי אֲבוֹתֵינוּ שֶׁבִּזְכוּת סְפִירַת הָעֹמֶר שֶׁסָּפַרְתִּי הַיּוֹם",
        "transliteration": "Yehi ratzon milfanecha HaShem Elokeinu vElokei avoteinu shebizchut sfirat ha'omer shesafarti hayom",
        "english": "May it be Your will, Lord our God and God of our fathers, that in the merit of the Omer counting that I counted today"
    }
}

# Formatting templates for different output styles
FORMAT_TEMPLATES = {
    "simple": "{hebrew_text}",
    "with_transliteration": "{hebrew_text}\n{transliteration}",
    "with_english": "{hebrew_text}\n{english_translation}",
    "full": "{hebrew_text}\n{transliteration}\n{english_translation}",
    "compact": "{day_number} - {hebrew_text}",
    "detailed": """
יום {day_number} לעומר
{hebrew_text}
{transliteration}
{english_translation}
{sefirah_info}
"""
}

# Error messages in multiple languages
ERROR_MESSAGES = {
    "invalid_day": {
        "hebrew": "יום לא חוקי לעומר",
        "english": "Invalid day for Omer counting",
        "transliteration": "Yom lo chuki la'omer"
    },
    "out_of_range": {
        "hebrew": "יום חייב להיות בין 1 ל-49",
        "english": "Day must be between 1 and 49",
        "transliteration": "Yom chayav lihiyot bein 1 l'49"
    },
    "date_error": {
        "hebrew": "שגיאת תאריך",
        "english": "Date error",
        "transliteration": "Shgiat ta'arikh"
    }
}

# Success messages
SUCCESS_MESSAGES = {
    "counted": {
        "hebrew": "נספר בהצלחה",
        "english": "Counted successfully",
        "transliteration": "Nispar b'hatzlacha"
    },
    "blessing_recited": {
        "hebrew": "הברכה נאמרה",
        "english": "Blessing recited",
        "transliteration": "Habracha ne'emrah"
    }
}

# Configuration validation rules
VALIDATION_RULES = {
    "day_range": (1, 49),
    "required_fields": ["hebrew_text"],
    "optional_fields": ["transliteration", "english_translation", "sefirah_info"]
}

# Data integrity checks
def validate_data_integrity():
    """Validate that all required data is present and consistent"""
    errors = []
    
    # Check that all days 1-49 are present
    for day in range(1, 50):
        if day not in OMER_TEXTS:
            errors.append(f"Missing Hebrew text for day {day}")
        if day not in OMER_TRANSLITERATIONS:
            errors.append(f"Missing transliteration for day {day}")
        if day not in OMER_ENGLISH_TRANSLATIONS:
            errors.append(f"Missing English translation for day {day}")
        if day not in DAILY_SEFIROT:
            errors.append(f"Missing sefirah information for day {day}")
    
    # Check sefirot consistency
    for week in range(1, 8):
        if week not in SEFIROT_ATTRIBUTES:
            errors.append(f"Missing sefirah attributes for week {week}")
    
    return errors

# Export lists for easy importing
__all__ = [
    'OMER_TEXTS',
    'OMER_TRANSLITERATIONS', 
    'OMER_ENGLISH_TRANSLATIONS',
    'DAILY_SEFIROT',
    'SEFIROT_ATTRIBUTES',
    'SPECIAL_DAYS',
    'OMER_BLESSING',
    'OMER_PRAYER',
    'ANA_BEKOACH',
    'HEBREW_MONTHS',
    'HEBREW_MONTH_LENGTHS',
    'HEBREW_MONTH_NAMES_HEBREW',
    'HEBREW_WEEKDAYS',
    'CUSTOM_TEXTS',
    'FORMAT_TEMPLATES',
    'ERROR_MESSAGES',
    'SUCCESS_MESSAGES',
    'validate_data_integrity'
]