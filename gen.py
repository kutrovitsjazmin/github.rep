import os
import lyricsgenius
import random


def genius_peldany_gyartasa():
    genius_token = os.getenv('GENIUS_TOKEN')
    return lyricsgenius.Genius(genius_token, verbose=True)


def eloado_id_megszerzese(genius_peldany, nev):
    eredmeny = genius_peldany.search(search_term=nev)
    eloado_id = eredmeny['hits'][0]['result']['primary_artist']['id']
    return eloado_id


def albumok_lekerese(genius_peldany, eloado_id):
    return [album['name'] for album in genius_peldany.artist_albums(artist_id=eloado_id)['albums']]


def album_id_megszerzese(genius_peldany, kivalasztott_album, eloado_id):
    return genius_peldany.artist_albums(artist_id=eloado_id)['albums'][kivalasztott_album]['id']


def albumok_kiirasa(albumcimek):
    print('\n'.join([f"{idx + 1}. {album_nev}" for idx, album_nev in enumerate(albumcimek)]))


def main():
    print('QUIZ: Egy általad választott előadó egyik dalát kell a dalszöveg alapján felismerni!!')

    genius = genius_peldany_gyartasa()
    eloado = input('Add meg az előadót, aki zenéjét ki szeretnéd találni!: ')
    eloado_id = eloado_id_megszerzese(genius, eloado)

    albumok_kiirasa(albumok_lekerese(genius, eloado_id))
    album_kviz = int(input('Az albumok sorszámát megadva válasszon egy albumot, amiből a dal származik '))
    album_id = album_id_megszerzese(genius, album_kviz - 1, eloado_id)

    zenek = genius.album_tracks(album_id=album_id)['tracks']
    random_szam = random.randint(0, len(zenek) - 1)

    zene = genius.search_song(song_id=zenek[random_szam]['song']['id'], get_full_info=False)
    dalszoveg = zene.to_dict()['lyrics']
    cim = zene.to_dict()['title']

    valasz = input(f'Lyrics:\n{dalszoveg}\nVálasz: ')

    if valasz == cim:
        print('Ügyes vagy!!')
    else:
        print(f'Nem jó válasz, a helyes megoldás {cim} lett volna, de ne csüggedj, próbáld ki a játékot újra!!')


main()
