from typing import List, Dict, Any, Optional
import httpx
import redis
from bs4 import BeautifulSoup
from ..core.config import settings
from ..models.schemas import Product, ProductSpec, Price
import json
import asyncio
from datetime import timedelta
import re
from urllib.parse import quote_plus

class ProductService:
    def __init__(self):
        self.redis_client = redis.from_url(settings.REDIS_URL)
        self.cache_ttl = timedelta(hours=1)
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

    async def search_products(self, query: str, filters: Optional[Dict[str, Any]] = None) -> List[Product]:
        """Search for products across multiple sources."""
        # Try to get from cache first
        cache_key = f"products:{query}:{json.dumps(filters or {})}"
        cached_result = self.redis_client.get(cache_key)
        if cached_result:
            return json.loads(cached_result)

        # Search across multiple sources concurrently
        tasks = [
            self._search_jumia(query, filters),
            self._search_amazon(query, filters),
            self._search_ebay(query, filters)
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Combine results and remove duplicates
        products = []
        seen_urls = set()
        
        for result in results:
            if isinstance(result, list):
                for product in result:
                    if product.vendor_url not in seen_urls:
                        products.append(product)
                        seen_urls.add(product.vendor_url)

        # Sort by confidence score
        products.sort(key=lambda x: x.confidence_score, reverse=True)
        
        # Cache results
        self.redis_client.setex(
            cache_key,
            self.cache_ttl,
            json.dumps(products)
        )

        return products

    async def _search_jumia(self, query: str, filters: Optional[Dict[str, Any]] = None) -> List[Product]:
        """Search products on Jumia."""
        try:
            # Construct search URL
            search_url = f"https://www.jumia.co.ke/catalog/?q={quote_plus(query)}"
            if filters:
                search_url += "&" + "&".join(f"{k}={v}" for k, v in filters.items())

            async with httpx.AsyncClient() as client:
                response = await client.get(search_url, headers=self.headers)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.text, 'html.parser')
                products = []

                for item in soup.select('article.prd'):
                    try:
                        name = item.select_one('h3.name').text.strip()
                        price_text = item.select_one('div.prc').text.strip()
                        price_value = float(re.sub(r'[^\d.]', '', price_text))
                        
                        product = Product(
                            name=name,
                            description=item.select_one('div.desc').text.strip(),
                            specs=self._extract_specs(item),
                            image_url=item.select_one('img.img')['data-src'],
                            price=Price(value=price_value, currency="KES"),
                            vendor_url=item.select_one('a.core')['href'],
                            confidence_score=self._calculate_confidence_score(item, query)
                        )
                        products.append(product)
                    except Exception as e:
                        print(f"Error parsing Jumia product: {str(e)}")
                        continue

                return products

        except Exception as e:
            print(f"Error searching Jumia: {str(e)}")
            return []

    async def _search_amazon(self, query: str, filters: Optional[Dict[str, Any]] = None) -> List[Product]:
        """Search products on Amazon."""
        try:
            # Construct search URL
            search_url = f"https://www.amazon.com/s?k={quote_plus(query)}"
            
            async with httpx.AsyncClient() as client:
                response = await client.get(search_url, headers=self.headers)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.text, 'html.parser')
                products = []

                for item in soup.select('div[data-component-type="s-search-result"]'):
                    try:
                        name = item.select_one('h2 span').text.strip()
                        price_text = item.select_one('span.a-price-whole').text.strip()
                        price_value = float(re.sub(r'[^\d.]', '', price_text))
                        
                        product = Product(
                            name=name,
                            description=item.select_one('div.a-color-secondary').text.strip(),
                            specs=self._extract_amazon_specs(item),
                            image_url=item.select_one('img.s-image')['src'],
                            price=Price(value=price_value, currency="USD"),
                            vendor_url=f"https://www.amazon.com{item.select_one('a.a-link-normal')['href']}",
                            confidence_score=self._calculate_confidence_score(item, query)
                        )
                        products.append(product)
                    except Exception as e:
                        print(f"Error parsing Amazon product: {str(e)}")
                        continue

                return products

        except Exception as e:
            print(f"Error searching Amazon: {str(e)}")
            return []

    async def _search_ebay(self, query: str, filters: Optional[Dict[str, Any]] = None) -> List[Product]:
        """Search products on eBay."""
        try:
            # Construct search URL
            search_url = f"https://www.ebay.com/sch/i.html?_nkw={quote_plus(query)}"
            
            async with httpx.AsyncClient() as client:
                response = await client.get(search_url, headers=self.headers)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.text, 'html.parser')
                products = []

                for item in soup.select('div.s-item__info'):
                    try:
                        name = item.select_one('div.s-item__title').text.strip()
                        price_text = item.select_one('span.s-item__price').text.strip()
                        price_value = float(re.sub(r'[^\d.]', '', price_text))
                        
                        product = Product(
                            name=name,
                            description=item.select_one('div.s-item__subtitle').text.strip(),
                            specs=self._extract_ebay_specs(item),
                            image_url=item.select_one('img.s-item__image-img')['src'],
                            price=Price(value=price_value, currency="USD"),
                            vendor_url=item.select_one('a.s-item__link')['href'],
                            confidence_score=self._calculate_confidence_score(item, query)
                        )
                        products.append(product)
                    except Exception as e:
                        print(f"Error parsing eBay product: {str(e)}")
                        continue

                return products

        except Exception as e:
            print(f"Error searching eBay: {str(e)}")
            return []

    def _extract_specs(self, item: BeautifulSoup) -> List[ProductSpec]:
        """Extract product specifications from HTML."""
        specs = []
        try:
            specs_element = item.select_one('div.specs')
            if specs_element:
                for spec in specs_element.select('div.spec'):
                    key = spec.select_one('div.key').text.strip()
                    value = spec.select_one('div.value').text.strip()
                    specs.append(ProductSpec(key=key, value=value))
        except Exception as e:
            print(f"Error extracting specs: {str(e)}")
        return specs

    def _extract_amazon_specs(self, item: BeautifulSoup) -> List[ProductSpec]:
        """Extract specifications from Amazon product."""
        specs = []
        try:
            specs_element = item.select_one('div.a-section')
            if specs_element:
                for spec in specs_element.select('li'):
                    text = spec.text.strip()
                    if ':' in text:
                        key, value = text.split(':', 1)
                        specs.append(ProductSpec(key=key.strip(), value=value.strip()))
        except Exception as e:
            print(f"Error extracting Amazon specs: {str(e)}")
        return specs

    def _extract_ebay_specs(self, item: BeautifulSoup) -> List[ProductSpec]:
        """Extract specifications from eBay product."""
        specs = []
        try:
            specs_element = item.select_one('div.s-item__details')
            if specs_element:
                for spec in specs_element.select('div.s-item__detail'):
                    key = spec.select_one('span.s-item__label').text.strip()
                    value = spec.select_one('span.s-item__value').text.strip()
                    specs.append(ProductSpec(key=key, value=value))
        except Exception as e:
            print(f"Error extracting eBay specs: {str(e)}")
        return specs

    def _calculate_confidence_score(self, item: BeautifulSoup, query: str) -> float:
        """Calculate confidence score based on product relevance."""
        try:
            # Get product text
            product_text = item.get_text().lower()
            query_terms = query.lower().split()
            
            # Calculate term frequency
            term_frequency = sum(1 for term in query_terms if term in product_text)
            
            # Calculate base score
            base_score = term_frequency / len(query_terms)
            
            # Adjust score based on product details
            if item.select_one('img'):
                base_score += 0.1
            if item.select_one('div.price'):
                base_score += 0.1
            if item.select_one('div.description'):
                base_score += 0.1
                
            # Normalize score between 0 and 1
            return min(max(base_score, 0.0), 1.0)
            
        except Exception as e:
            print(f"Error calculating confidence score: {str(e)}")
            return 0.5

    async def get_product_details(self, product_id: str) -> Optional[Product]:
        """Get detailed information about a specific product."""
        cache_key = f"product:{product_id}"
        cached_result = self.redis_client.get(cache_key)
        if cached_result:
            return json.loads(cached_result)

        # Implementation for fetching detailed product information
        # This would typically involve making a request to the product's detail page
        return None

product_service = ProductService() 