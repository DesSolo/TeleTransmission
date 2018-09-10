from config import config
from transmission_connector import TransmissionCommands
from re import compile
from subprocess import Popen, PIPE

transmission = TransmissionCommands(**config['transmission'])


def get_commands():
    commands = {}
    for command in config['commands']:
        commands[compile(command)] = config['commands'][command]
    return commands


class ApiFunctions(object):
    def __init__(self, message):
        self.message = message
        self.parse_mode = 'Markdown'
        self.commands = get_commands()
        self.answer = self.hook()

    def hook(self, **kwargs):
        text = self.message['message']['text']
        for command in self.commands:
            if command.match(text):
                if 'message' in self.commands[command]:
                    return self.commands[command]['message']
                if 'shell' in self.commands[command]:
                    self.parse_mode = None
                    proc = Popen(self.commands[command]['shell'], shell=True, stdout=PIPE, stderr=PIPE)
                    return proc.stdout.read().decode('utf-8')
                group_dict = command.search(text).groupdict()
                return getattr(self, self.commands[command])(**group_dict)
        return f'Command "{text}" unsupported'

    @staticmethod
    def add_torrent(magnet, **kwargs):
        return str(transmission.add_torrent(torrent=magnet, download_dir=config['directories']['global']))

    @staticmethod
    def torrent_status(**kwargs):
        return transmission.torrents_list()

    @staticmethod
    def torrent_server_info(**kwargs):
        return transmission.server_info(config['directories']['global'])
