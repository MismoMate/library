import requests


class Downloader:
    """The application that is responsible for downloading ebooks from gutenberg"""
    def __init__(self) -> None:
        pass

    # fetches the catalog file from gutenberg project 
    def download_cat(self):
        print("Downloading catalog")
        url = "https://www.gutenberg.org/cache/epub/feeds/pg_catalog.csv"
        response = requests.get(url)
        with open("catalog/catalog.csv", "wb") as f:
            f.write(response.content)


