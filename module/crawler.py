import logging
import sqlite3
import requests
from urllib.parse import urljoin
from urllib.robotparser import RobotFileParser
from bs4 import BeautifulSoup

# Fetcher 클래스: 웹 페이지를 가져오는 역할을 합니다.
class Fetcher:
    def __init__(self):
        self.robot_parser = RobotFileParser()

    # fetch 메서드: 주어진 URL의 웹 페이지를 가져옵니다.
    def fetch(self, url):
        try:
            self.robot_parser.set_url(urljoin(url, "/robots.txt"))
            self.robot_parser.read()
            can_fetch = self.robot_parser.can_fetch("*", url)
        except Exception:
            can_fetch = True

        if can_fetch:
            response = requests.get(url)
            return response.text
        else:
            return None

# Parser 클래스: 웹 페이지에서 URL을 파싱하는 역할을 합니다.
class Parser:
    # parse 메서드: 주어진 HTML에서 URL을 파싱합니다.
    def parse(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        urls = [a['href'] for a in soup.find_all('a', href=True)]
        return urls

# DupUrlElim 클래스: 중복된 URL을 제거하는 역할을 합니다.
class DupUrlElim:
    # eliminate 메서드: 주어진 URL 리스트에서 중복된 URL을 제거합니다.
    def eliminate(self, urls, visited):
        return [url for url in urls if url not in visited]

# Database 클래스: SQLite 데이터베이스와의 연결을 관리합니다.
class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS pages (
                url TEXT PRIMARY KEY,
                content TEXT
            )
        """)

    # insert 메서드: 주어진 URL과 내용을 데이터베이스에 저장합니다.
    def insert(self, url, content):
        self.cursor.execute("INSERT INTO pages VALUES (?, ?)", (url, content))
        self.conn.commit()
    
    # close 메서드: 데이터베이스 연결을 닫습니다.
    def close(self):
        self.conn.close()

# Crawler 클래스: 웹 크롤링을 수행합니다.
class Crawler:
    def __init__(self, db_name):
        self.fetcher = Fetcher()
        self.parser = Parser()
        self.dup_elim = DupUrlElim()
        self.visited = set()
        self.db = Database(db_name)
        logging.basicConfig(level=logging.INFO)

    # crawl 메서드: 주어진 시작 URL에서 시작하여 웹 크롤링을 수행합니다.
    def crawl(self, start_url):
        self.visited.add(start_url)
        queue = [start_url]

        while queue:
            url = queue.pop(0)
            logging.info(f"Crawling: {url}")
            html = self.fetcher.fetch(url)
            if html is not None:
                self.db.insert(url, html)
                new_urls = self.parser.parse(html)
                new_urls = self.dup_elim.eliminate(new_urls, self.visited)
                self.visited.update(new_urls)
                queue.extend(new_urls)
                logging.info(f"Found {len(new_urls)} new URLs.")
            else:
                logging.info(f"Skipping: {url}")

        self.db.close()