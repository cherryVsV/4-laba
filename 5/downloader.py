import urllib.request as req
from urllib.parse import unquote
from os import path
from datetime import datetime
from hashlib import md5
import threading


class DownloadThread(threading.Thread):
    _counter = 0
    when_all_finished = threading.Event()

    def __init__(self, url, update_callback):
        threading.Thread.__init__(self)
        DownloadThread._counter += 1
        self.url = url
        self.name = md5(url.encode()).hexdigest()
        self.filename = unquote(self.url).split('/')[-1]
        self._percentage = 0
        self._update = update_callback

    def _download(self, response, count):
        start_time = datetime.now()
        while response.length:
            yield response.read(count)
        self.timedelta = datetime.now() - start_time

    def run(self):
        u = req.urlopen(self.url)
        count = 4096
        self.file_size = u.length
        downloaded = 0
        with open(path.join('downloads', self.filename), 'wb') as output:
            for frame in self._download(u, count):
                downloaded += count
                output.write(frame)
                self._update(downloaded / self.file_size)
            self._update(1)
        DownloadThread._counter -= 1
        if DownloadThread._counter == 0:
            self.when_all_finished.set()