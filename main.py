from module.crawler import Crawler, Database

def main():
    crawler = Crawler(db_name="elastic.sqlite")
    crawler.crawl("https://www.elastic.co/guide/index.html")

if __name__ == "__main__":
    main()