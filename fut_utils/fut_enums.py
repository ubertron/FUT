from enum import Enum


class FutAttr(Enum):
    club: str = 'Club'
    id: str = 'Id'
    league: str = 'League'
    loans: str = 'Loans'
    name: str = 'Name'
    position: str = 'Position'
    rarity: str = 'Rarity'
    rating: str = 'Rating'
    surname: str = 'Lastname'


class Rarity(Enum):
    common: str = 'Common'
    rare: str = 'Rare'
    totw: str = 'Team of the Week'


class League(Enum):
    bundesliga = 'Bundesliga'
    bundesliga_2 = 'Bundesliga 2'
    bundesliga_frauen = 'Google Pixel Frauen-Bundesliga'
    calcio_a = 'Calcio A Femminile'
    d1_arkema = 'D1 Arkema'
    efl_championship = 'EFL Championship'
    efl_league_one = 'EFL League One'
    eredivisie = 'Eredivisie'
    icons = 'Icons'
    la_liga = 'LALIGA EA SPORTS'
    la_liga_2 = 'LALIGA HYPERMOTION'
    la_liga_f = 'Liga F'
    liga_portugal = 'Liga Portugal'
    ligue_1 = 'Ligue 1 Uber Eats'
    ligue_2 = 'Ligue 2 BKT'
    mls = 'Major League Soccer'
    nwsl = 'National Women\'s Soccer League'
    premier_league = 'Premier League'
    roshn = 'ROSHN Saudi League'
    scottish = 'cinch Premiership'
    serie_a = 'Serie A TIM'
    serie_b = 'Serie BKT'
    trendyol_super_lig = 'Trendyol Süper Lig'
    wsl = 'Barclays Women’s Super League'
