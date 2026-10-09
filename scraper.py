from __future__ import annotations

import csv
import json
import os
from datetime import datetime, timezone
from pathlib import Path

import requests
from bs4 import BeautifulSoup


DEFAULT_URL = "https://books.toscrape.com/"
OUTPUT_DIR = Path("data")


def fetch_html(url: str) -> str:
    headers = {
        "User-Agent": "github-actions-learning-scraper/1.0 (+https://github.com/)"
    }
    response = requests.get(url, headers=headers, timeout=20)
    response.raise_for_status()
    return response.text


def parse_books(html: str) -> list[dict[str, str]]:
    soup = BeautifulSoup(html, "html.parser")
    books: list[dict[str, str]] = []

    for article in soup.select("article.product_pod"):
        title = article.select_one("h3 a")
        price = article.select_one(".price_color")
        availability = article.select_one(".availability")
        rating = article.select_one("p.star-rating")

        books.append(
            {
                "title": title["title"].strip() if title else "",
                "price": price.get_text(strip=True) if price else "",
                "availability": availability.get_text(strip=True) if availability else "",
                "rating": rating["class"][-1] if rating and rating.has_attr("class") else "",
            }
        )

    return books


def save_results(books: list[dict[str, str]], source_url: str) -> tuple[Path, Path]:
    OUTPUT_DIR.mkdir(exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    csv_path = OUTPUT_DIR / f"books_{timestamp}.csv"
    json_path = OUTPUT_DIR / f"books_{timestamp}.json"

    with csv_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(
            csv_file, fieldnames=["title", "price", "availability", "rating"]
        )
        writer.writeheader()
        writer.writerows(books)

    payload = {
        "source_url": source_url,
        "scraped_at_utc": datetime.now(timezone.utc).isoformat(),
        "total": len(books),
        "items": books,
    }
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    return csv_path, json_path


def main() -> None:
    url = os.environ.get("SCRAPER_URL", DEFAULT_URL)
    html = fetch_html(url)
    books = parse_books(html)

    if not books:
        raise RuntimeError("No se encontraron libros. Revisa el selector CSS o la URL.")

    csv_path, json_path = save_results(books, url)
    print(f"Scraping completado: {len(books)} libros encontrados.")
    print(f"CSV: {csv_path}")
    print(f"JSON: {json_path}")


if __name__ == "__main__":
    main()
