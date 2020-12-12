import argparse
import pickle

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def create_index(output_file, max_pages):
    crawler_process = CrawlerProcess(get_project_settings())
    crawler_process.crawl('concordia', max_pages=max_pages)

    concordia_crawler = None
    for crawler in crawler_process.crawlers:
        concordia_crawler = crawler.spider

    crawler_process.start()

    final_index = concordia_crawler.get_indexer().get_index()
    pickle.dump(final_index, open(output_file, 'wb'))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="Concordia.ca indexer", description="crawls www.concordia.ca and creates an inverted index")
    parser.add_argument('--output', '-o', help="File path for the final index", type=str, default="index/index.pickle")
    parser.add_argument('--maxpages', '-m', help="The max number of pages to crawl", type=int, default=-1)
    args = parser.parse_args()

    create_index(args.output, args.maxpages)
