from module.crawler import Crawler, Database

# 메인 호출 함수 : 크롤러를 실행합니다.
def main():
    # 크롤러 객체를 생성하고 실행합니다.
    crawler = Crawler(db_name="doc_es.sqlite")
    
    # 크롤러를 실행합니다.
    crawler.crawl("https://www.elastic.co/guide/en/elasticsearch/reference/current/getting-started.html")

if __name__ == "__main__":
    main()