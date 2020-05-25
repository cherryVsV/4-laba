'''Напишите скрипт, читающий во всех mp3-файлах указанной
директории ID3v1-теги и выводящий информацию о каждом файле в
виде: [имя исполнителя] - [название трека] - [название альбома].
Если пользователь при вызове скрипта задает ключ -d, то выведите
для каждого файла также 16-ричный дамп тега. Скрипт должен
также автоматически проставить номера треков и жанр (номер
жанра задается в параметре командной строки), если они не
проставлены. Используйте модуль struct.
ID3v1-заголовки располагаются в последних 128 байтах mp3-файла. '''
from os import listdir
import os
from os.path import join, isfile
from struct import unpack, pack
import argparse
import MusGenres

# Call example: 1.py C:/Users/User/Desktop/4 лаба питон/Music -d -g 7
class Tag(object):
    def __init__(self, unpacked_tag):
        (title,artist,album,year,comment,track,genre) = unpacked_tag
        (self.title,
         self.artist,
         self.album,
         self.comment) = [_.decode('utf-8')
                          for _ in (title,artist,album,comment)]
        self.year = int(year)
        self.track = int(track)
        g = int(genre)
        self.genre = (MusGenres.genres[g]
                      if g < len(MusGenres.genres)
                      else 255)

    def __str__(self):
        return ' - '.join((self.title,
                           self.artist,
                           self.album,
                           self.comment,
                           str(self.year),
                           str(self.track),
                           self.genre))


class TagReader(object):
    def __init__(self, dirname, **kwargs):
        self.__dir = dirname
        try:
            self.__dump = kwargs['dump']
            self.__genre = kwargs['genre']
        except KeyError:
            self.__dump = False
            self.__genre = None
        self.tags = list()
        self.counter = 0
        for file in self.__get_files():
            tag = self.__open_file(file)
            if tag is not None:
                self.tags.append((tag))

    def __get_files(self):
        return (join(self.__dir, item)
                for item in listdir(self.__dir)
                if isfile(join(self.__dir, item)))

    def __open_file(self, file):
        with open(file, "rb+") as bfile:
            _bytes = bfile.read()[-128:]
            mask = '=3s30s30s30s4s28s?BB'      #struct ID3v1
            unpacked = unpack(mask, _bytes)
            if(unpacked[0] != b'TAG'):
                return None
            self.counter += 1
            unpacked = unpacked[1:]
            tag = Tag(unpacked)
            if not tag.track:
                tag.track = self.counter
                print(tag.track)
                bfile.seek(bfile.tell() - 2)
                bfile.write(bytes([tag.track]))
            if tag.genre == 255 and \
               self.__genre is not None:
                print(repr(self.__genre))
                if self.__genre < len(MusGenres.genres):
                    tag.genre = MusGenres.genres[self.__genre]
                bfile.write(bytes([self.__genre]))
            if not self.__dump:
                return tag
            return tag, self.__make_dump(_bytes)

    def __make_dump(self, _bytes):
        def _make_dump_line(dump):
            while len(dump) > 0:
                yield ' '.join(dump[:8])
                dump = dump[8:]
        dump = [hex(byte)[2:].rjust(2, '0') for byte in _bytes]
        return '\n'.join(_make_dump_line(dump))


class TagArgParser(object):
    def __init__(self):
        self.parser = argparse.ArgumentParser(
                      description='Get ID3v1 tags from audiofiles.')

        self.parser.add_argument('dirname',
                                 help='dir to scan for audiofiles',
                                 metavar="<dirname>",
                                 default='.')

        self.parser.add_argument('-g', '--genre',
                                 help="number of genre",
                                 metavar='<genre number>',
                                 default=None,
                                 type=int)

        self.parser.add_argument('-d', '--dump',
                                 help="print hex-dump of tag",
                                 action="store_true")

    def ask(self):
        parsed = self.parser.parse_args()
        (self.dirname,
         self.genre,
         self.dump) = (parsed.dirname,
                       parsed.genre,
                       parsed.dump)
        return iter(self)

    def __iter__(self):
        return iter((self.dirname,
                     self.genre,
                     self.dump))


if __name__ == '__main__':
    dirname, default_genre, with_dump = TagArgParser().ask()
    tr = TagReader(dirname, dump=with_dump, genre=default_genre)
    if with_dump:
        for tag, dump in sorted(tr.tags, key=lambda x: x[0].track):
            print('{}\n{}\n\n'.format(' - '.join((tag.artist,
                                                  tag.title,
                                                  tag.album)), dump))
    else:
        for tag in sorted(tr.tags, key=lambda x: x.track):
            print('{}\n'.format(' - '.join((tag.artist,
                                            tag.title,
                                            tag.album))))

