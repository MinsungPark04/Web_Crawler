from module.crawler import Crawler, Database

def main():
    crawler = Crawler(db_name="test.db")
    crawler.crawl("https://www.yahoo.com")

if __name__ == "__main__":
    main()