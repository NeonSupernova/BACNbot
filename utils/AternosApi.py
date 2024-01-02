from python_aternos import Client

class AternosApi:
    def __init__(self, file, motd):
        self.session = Client.restore_session(file=file)
        self._init_srv(motd)

    def _init_srv(self, motd):
        for svr in self.session.list_servers():
            svr.motd = motd
