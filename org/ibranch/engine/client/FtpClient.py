from ftplib import FTP, FTP_TLS
from urllib.parse import urlparse


class Client:
    def __init__(self):
        self._url = None
        self._handler = None
        self._usr = 'guest'
        self._pwd = 'guest'

    def set_url(self, url):
        parsed_result = urlparse(url)
        protocol = parsed_result.scheme
        domain = parsed_result.netloc
        dirs = parsed_result.path.split('/')
        file = dirs[-1]
        dirs = dirs[:-2]
        if not protocol.lower().startswith('ftp://'):
            raise AssertionError(f'Not a valid ftp resource, url: {url}')
        self._url = url
        self._domain = domain
        self._dirs = dirs
        self._file = file
        return self

    def login(self):
        self._handler = FTP(self._url)
        self._handler.login(self._usr, self._pwd)
        return self

    def login_tls(self):
        self._handler = FTP_TLS(self._url)
        self._handler.login(self._usr, self._pwd)
        return self

    def available(self):
        self._handler.cwd('pub1')
        a = self._handler.retrlines('LIST')
        return a
        # # ftp.cwd('debian')
        # ftp.retrlines('LIST')
        # with open('README', 'wb') as fp:
        #     ftp.retrbinary('RETR README', fp.write)
        #     ftp.quit()
        #     ftps = FTP_TLS('ftp.pureftpd.org')
        #
        # import ftplib
        # server = "localhost"
        # user = "user"
        # password = "test@email.com"
        # try:
        #     ftp = ftplib.FTP(server)
        #     ftp.login(user, password)
        # except Exception as e:
        #     print(e)
        # else:
        #     filelist = []  # to store all files
        #     ftp.retrlines('LIST', filelist.append)  # append to list
        #     f = 0
        #     for f in filelist:
        #         if "public_html" in f:
        #             # do something
        #             f = 1
        #     if f == 0:
        #         print("No public_html")
        #         # do your processing here


client = Client() \
    .set_url('ftp.sanger.ac.uk') \
    .login()

a = client.available()
print(a)