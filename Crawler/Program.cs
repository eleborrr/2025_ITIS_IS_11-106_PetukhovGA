using Crawler;

if (args.Length == 0)
{
    return;
}

var crawler = new WebCrawler(args.ToList());
await crawler.CrawlAsync();
 