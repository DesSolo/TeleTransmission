import transmissionrpc
import math


class SizeConverter(int):
    def __format__(self, fmt):
        if fmt == "" or fmt[-1] != "S":
            if fmt[-1].tolower() in ['b', 'c', 'd', ' o', 'x', 'n', 'e', 'f', 'g', '%']:
                return int(self).__format__(fmt)
            else:
                return str(self).__format__(fmt)

        val, s = float(self), ["b ", "Kb", "Mb", "Gb", "Tb", "Pb"]
        if val < 1:
            i, v = 0, 0
        else:
            i = int(math.log(val, 1024)) + 1
            v = val / math.pow(1024, i)
            v, i = (v, i) if v > 0.5 else (v * 1024, i - 1)
        return ("{0:{1}f}" + s[i]).format(v, fmt[:-1])


class TransmissionCommands:
    def __init__(self, **kwargs):
        self.tc = transmissionrpc.Client(**kwargs)

    def torrents_list(self, non_formated=False):
        tor_list = []
        for t in self.tc.get_torrents():
            updated_date = t.date_added
            if t.status == 'downloading':
                try:
                    status = "(закач. %s%s осталось %s)" % ("{0:.2f}".format(t.progress), '%', t.eta)
                except:
                    status = str(t.progress)
            else:
                status = ''
            tor_list.append({'name': t.name, 'u_date': updated_date, 'status': status, 'id': t.id})
        s_tor_list = sorted(tor_list, key=lambda k: k['u_date'])
        if non_formated:
            return s_tor_list
        result_str = ''
        for st in reversed(s_tor_list):
            result_str += '_%s_ %s\n*%s* \n\n' % (str(st['u_date']), st['status'], st['name'])
        return result_str

    def server_info(self, path):
        size_is = "{0:.2S}".format(SizeConverter(int(self.tc.free_space(path))))
        result_str = 'Space available: %s' % size_is
        return result_str

    def add_torrent(self, download_dir, torrent):
        result = self.tc.add_torrent(torrent=torrent, download_dir=download_dir)
        return result

    def rm_torrent(self, torrent_name):
        result = self.tc.remove_torrent(ids=torrent_name, delete_data=True)
        return result
