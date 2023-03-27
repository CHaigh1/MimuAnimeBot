from AnilistPython import Anilist
import random
import requests

def randomAnime(badAnime=False, goodAnime=False):
    anilist = Anilist()
    good_result = False
    rangeUpper = 100
    rangeLower = 0
    if badAnime:
        rangeUpper = 69
    if goodAnime:
        rangeLower = 70
    while not good_result:
        alist = anilist.search_anime(score=range(rangeLower, rangeUpper))
        result = alist[random.randrange(0, len(alist))]
        if (result['airing_format'] not in ['TV_SHORT', 'MOVIE', 'MUSIC']) and (result['airing_status'] != 'RELEASING') and ('Hentai' not in result['genres']):
            if result['name_english'] is None:
                return f"I found this:\n{result['name_romaji']}\nStart Date: {result['starting_time']}\nScore: {result['average_score']}%\nGenres: {result['genres']}\n{result['cover_image']}"
            else:
                return f"I found this:\n{result['name_english']}\nStart Date: {result['starting_time']}\nScore: {result['average_score']}%\nGenres: {result['genres']}\n{result['cover_image']}"
            good_result = True