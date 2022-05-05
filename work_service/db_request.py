import sqlite3

class Request:
    def __init__(self):
        self.con = sqlite3.connect('subtitles.db')
        self.cur = self.con.cursor()
        self.con.row_factory = self._dict_factory

    def _dict_factory(self, cursor, row):
        d = {}
        for idx, col in enumerate(cursor.description):
            d[col[0]] = row[idx]
        return d

    def find_usage(self, request: str):
        usages_dict = self.con.execute(
            f'''
            select * from subtitles
            where content like '%{request}%'
            '''
        ).fetchall()
        return self._format(usages_dict)

    def _format(self, res):
        return [self._format_dict(d) for d in res]

    def _format_dict(self, d):
        res_d = {}
        res_d['video_id'] = d['video_id']
        res_d['link'] = f'https://www.ted.com/talks/{d["video_id"]}'
        res_d['content'] = d['content']
        res_d['startTime'] = self._convert_time(d['startTime'])
        return res_d

    def _convert_time(self, time: str):
        time = int(time) / 1000
        min = int(time // 60)
        sec = int(time % 60)
        return f'{min}m{sec}s'

    def close(self):
        self.con.close()

def db_request(request: str):
    req = Request()
    res = req.find_usage(request)
    req.close()
    return res

if __name__ == "__main__":
    result = db_request(' ought to ')
    content = [d['content'] for d in result]
    print(*content, sep='\n')
    print(len(result))