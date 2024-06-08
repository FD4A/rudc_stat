from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
from glob import glob

from Server.reqForm import RequestFrom, GetParams
from Source.Tournament import Tournament
from Source.LegendaryBase import LegendaryBase
from makeStat import make_stat


def make_stat_response(get_params: GetParams):
    stat = make_stat(get_params, MyServer.tournament_list)
    tr_str = ''
    tr_str += ''
    tr_str += '<details id="tournaments_list">'
    tr_str += f'<summary>Tournaments List</summary><pre>{stat.get_tournaments_names()}</pre>'
    tr_str += '</details>'

    tr_str += '<h2 id="stat">Stats</h2>'
    stat_str = ''
    if get_params.full_stat:
        stat_str += f'<pre  id="stat">{stat.to_str(get_params.sort_type, True, get_params.mach_threshold_for_full_matchup)}</pre>'
    else:
        stat_str += f'<pre  id="stat">{stat.to_str(get_params.sort_type, False)}</pre>'
    return [tr_str, stat_str]


class MyServer(BaseHTTPRequestHandler):
    legendBase = None
    req_form = None
    tournament_list = []

    @staticmethod
    def init():
        tournament_files_list = glob('../tournaments_json/*.json')
        for tournament_filename in tournament_files_list:
            MyServer.tournament_list.append(Tournament.load_from_json(tournament_filename))
        MyServer.legendBase = LegendaryBase('../ScryfallData/')
        MyServer.req_form = RequestFrom(MyServer.legendBase)

    def do_GET(self):
        path_ = self.path
        print(path_)
        if path_ == "/style.css":
            type_ = "text/css"
            self.send_response(200)
            self.send_header("Content-type", type_)
            self.end_headers()
        else:
            res = urlparse(self.path)
            self.req_form.parse_params(res.query.split('&'))
            [tr_str, stat_str] = make_stat_response(self.req_form.get_params_to_filtration())

            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            # self.wfile.write(bytes("<html><head><title>https://RussianDuelCommanderStatistics.org</title>"
            #                        "<style>#tournaments_list{color:red;text-align:center;}"
            #                        "#stat{color:red;text-align:center;}"
            #                        "</style></head>", "utf-8"))
            self.wfile.write(bytes("<html><head><title>https://RussianDuelCommanderStatistics.org</title></head>", "utf-8"))
            self.wfile.write(bytes("<p>Request: %s</p>" % path_, "utf-8"))
            self.wfile.write(bytes("<body>", "utf-8"))
            self.wfile.write(bytes(f"{tr_str}", "utf-8"))
            self.wfile.write(bytes(f"{self.req_form.get_http_form()}", "utf-8"))
            self.wfile.write(bytes(f"{stat_str}", "utf-8"))
            self.wfile.write(bytes("</body></html>", "utf-8"))


if __name__ == "__main__":
    hostName = "localhost"
    serverPort = 30080
    MyServer.init()
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print("Server started http://%s:%s" % (hostName, serverPort))

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")
