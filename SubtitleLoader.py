import sqlite3
from urllib.request import urlopen
from urllib.error import HTTPError
import json
from tqdm import tqdm

class SubtitleLoader():
    def __init__(self, name):
        self.db_name = name
        self.lang = 'en'
        
        self.con = sqlite3.connect(name)
        self.cur = self.con.cursor()
        if not self._table_exist():
            self._create_subtitles_table()
        
    def _create_subtitles_table(self): 
        self.cur.execute(
            '''
            CREATE TABLE subtitles
            (video_id integer, duration integer, content text, 
            startOfParagraph integer, startTime integer)
            ''')
            
    def set_lang(self, lang: str):
        self.lang = lang
            
    def _table_exist(self):
        self.cur.execute('''SELECT name FROM sqlite_master WHERE type='table';''')
        tables = self.cur.fetchall()
        return tables and ('subtitles' in tables[0])
    
    def add_ids(self, id_start, id_end):
        for video_id in tqdm(range(id_start, id_end)):
            self.add_id(video_id)
    
    def add_id(self, video_id):
        self.parse_subtitles(video_id)
    
    def parse_subtitles(self, video_id):
        if self._id_exist(video_id):
            return
        
        url = f'https://www.ted.com/talks/subtitles/id/{video_id}/lang/{self.lang}'
        
        try:
            ted = urlopen(url)
        except HTTPError as e:
            return None
        
        content_json = ted.read().decode('utf8')
        content = json.loads(content_json)
        self._add_content(video_id, content)
            
    def _add_content(self, video_id, content):
        rows = []
        for indict in content['captions']:
            rows.append([
                video_id, 
                indict['duration'],
                indict['content'],
                indict['startOfParagraph'],
                indict['startTime']])   
        self.cur.executemany("insert into subtitles values (?, ?, ?, ?, ?)", rows)
            
    def _id_exist(self, video_id: int):
        query = f"""
            SELECT EXISTS(SELECT {video_id} FROM subtitles WHERE video_id={video_id});
        """
        self.cur.execute(query)
        res = self.cur.fetchall()
        return res[0][0]
    
    def commit(self):
        self.con.commit()
        
    def close(self):
        self.con.close()
        
if __name__ == "__main__":
    sub_load = SubtitleLoader("subtitles.db")
    sub_load.add_ids(1, 1000)
    sub_load.commit()
    sub_load.close()