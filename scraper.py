import newspaper

def scrape_articles(urls):
    """
    Scrapes articles from a list of URLs and returns a list of article texts.
    """
    articles = []
    for url in urls:
        try:
            paper = newspaper.build(url, memoize_articles=False)
            for article in paper.articles:
                try:
                    article.download()
                    article.parse()
                    articles.append(article.text)
                except newspaper.article.ArticleException:
                    print(f"Could not download or parse article: {article.url}")
        except Exception as e:
            print(f"Could not build newspaper from URL: {url}. Error: {e}")
    return articles
