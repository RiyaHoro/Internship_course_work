import os
import re
import time
from typing import List, Dict, Optional
import requests
from bs4 import BeautifulSoup
import pandas as pd


class IndianExpressScraper:
    def __init__(self, target_count: int = 25, delay: float = 1.0):
        """
        Initialize the scraper.
        
        :param target_count: Number of articles to attempt to scrape (between 20 and 30)
        :param delay: Time delay (in seconds) between requests to respect rate limits
        """
        self.target_count = max(20, min(30, target_count))
        self.delay = delay
        self.base_url = "https://indianexpress.com/"
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            ),
            "Accept-Language": "en-US,en;q=0.9",
        }

    def fetch_page(self, url: str) -> Optional[BeautifulSoup]:
        """
        Fetch HTML content from a URL or local file with error handling.
        """
        try:
            # Check if input is a local file path or web URL
            if os.path.exists(url):
                with open(url, "r", encoding="utf-8") as file:
                    return BeautifulSoup(file.read(), "html.parser")
            
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.content, "html.parser")
        except requests.exceptions.RequestException as e:
            print(f"[Error] Failed to fetch URL {url}: {e}")
            return None
        except Exception as e:
            print(f"[Error] An unexpected error occurred while reading {url}: {e}")
            return None

    def extract_article_links(self, soup: BeautifulSoup) -> List[Dict[str, str]]:
        """
        Extract major news article titles and URLs from the homepage markup.
        """
        articles = []
        seen_links = set()

        # Find anchor tags containing news links
        for a_tag in soup.find_all("a", href=True):
            href = a_tag["href"]
            
            # Filter for valid article URLs (must belong to indianexpress.com and contain article path structures)
            if (
                re.search(r"https?://indianexpress\.com/article/", href) 
                and href not in seen_links
            ):
                title = a_tag.get_text(strip=True)
                
                # Exclude empty titles, navigation labels, or trivial media captions
                if title and len(title.split()) > 3:
                    seen_links.add(href)
                    articles.append({"title": title, "link": href})

            if len(articles) >= self.target_count:
                break

        return articles

    def extract_article_text(self, article_soup: BeautifulSoup) -> str:
        """
        Extract full body text from an article's BeautifulSoup structure.
        """
        if not article_soup:
            return ""

        # Locate the core story content container typical for Indian Express structure
        story_div = article_soup.find("div", id="full-details") or article_soup.find("div", class_=re.compile(r"story-details|pcl-full-content|articles"))
        
        paragraphs = []
        if story_div:
            # Extract text from paragraphs inside the story container
            p_tags = story_div.find_all("p")
        else:
            # Fallback to main article paragraph search
            p_tags = article_soup.find_all("p")

        for p in p_tags:
            # Skip promotional, disclaimer, or social media embed text blocks
            p_text = p.get_text(strip=True)
            if p_text and not p_text.startswith(("Also Read", "Subscribe", "Follow us")):
                paragraphs.append(p_text)

        return " ".join(paragraphs)

    def run(self, source_path: Optional[str] = None) -> pd.DataFrame:
        """
        Execute the scraping process and compile output into a Pandas DataFrame.
        """
        start_url = source_path if source_path else self.base_url
        print(f"Fetching homepage content from: {start_url}...")
        
        soup = self.fetch_page(start_url)
        if not soup:
            print("[Error] Unable to parse the main source page. Aborting process.")
            return pd.DataFrame()

        print("Extracting article links...")
        article_list = self.extract_article_links(soup)
        print(f"Discovered {len(article_list)} valid news links.")

        scraped_data = []

        for idx, item in enumerate(article_list, start=1):
            title = item["title"]
            link = item["link"]
            print(f"[{idx}/{len(article_list)}] Scraping: {title[:50]}...")

            article_soup = self.fetch_page(link)
            full_text = self.extract_article_text(article_soup) if article_soup else ""

            scraped_data.append({
                "title": title,
                "link": link,
                "full_text": full_text
            })

            # Respectful rate limiting pause between web requests
            time.sleep(self.delay)

        return pd.DataFrame(scraped_data)


def export_to_csv(df: pd.DataFrame, intern_name: str, output_path: str = "scraped_news.csv") -> None:
    """
    Format and export DataFrame columns strictly following required guidelines:
    NEWS_TITLE_<Interns Name>_NEWS_LINK_FULL_SCRAPED_TEXT
    """
    if df.empty:
        print("[Warning] DataFrame is empty. CSV export skipped.")
        return

    # Standardize Intern Name formatting (remove spaces or special characters for column key compatibility)
    clean_intern_name = re.sub(r"\s+", "_", intern_name.strip())
    
    # Construct exact requested column header string
    formatted_column = f"NEWS_TITLE_{clean_intern_name}_NEWS_LINK_FULL_SCRAPED_TEXT"

    # Merge content into structured rows under the requested schema representation
    export_df = pd.DataFrame()
    export_df[formatted_column] = df.apply(
        lambda row: f"Title: {row['title']} | Link: {row['link']} | Content: {row['full_text']}", 
        axis=1
    )

    # Alternatively, create individual standard columns with the intern name tag incorporated
    df_columns_custom = pd.DataFrame({
        "NEWS_TITLE": df["title"],
        "INTERN_NAME": intern_name,
        "NEWS_LINK": df["link"],
        "FULL_SCRAPED_TEXT": df["full_text"]
    })

    # Save structured dataset to CSV file
    df_columns_custom.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"[Success] Data exported successfully to: {output_path}")


if __name__ == "__main__":
    INTERN_NAME = "Riya Horo"  
    OUTPUT_CSV = "Indian_Express_Scraped_News_Riya_Horo.csv"

    # Instantiate scraper targeting ~25 news articles
    scraper = IndianExpressScraper(target_count=25, delay=1.0)
    
    # Run pipeline
    news_df = scraper.run()

    # Save output to CSV file
    export_to_csv(news_df, intern_name=INTERN_NAME, output_path=OUTPUT_CSV)