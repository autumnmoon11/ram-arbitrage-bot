import pytest
import re
from app.scrapers.newegg import NeweggScraper

def clean_price(price_str: str) -> float:
    """Helper to test regex logic across scrapers"""
    return float(re.sub(r'[^\d.]', '', price_str))

def test_price_regex_logic():
    assert clean_price("$149.99") == 149.99
    assert clean_price("USD 149.99") == 149.99
    assert clean_price("149") == 149.0
    
def normalize_ram_title(title: str) -> set:
    """
    Turns a messy title into a set of normalized keywords.
    """
    t = title.lower()
    # Handle common variations
    t = t.replace("(2 x 16gb)", "32gb").replace("2x16gb", "32gb").replace("mhz", "")
    # Remove special characters
    import re
    t = re.sub(r'[^a-z0-9 ]', '', t)
    
    # Return a set of words, filtering out filler like 'of' or 'the'
    return {word for word in t.split() if len(word) > 1}

def test_ram_product_matching_logic():
    newegg_title = "CORSAIR Vengeance 32GB (2 x 16GB) DDR5 6000"
    amazon_title = "Corsair Vengeance DDR5 32GB 2x16GB 6000Mhz"
    
    assert normalize_ram_title(newegg_title) == normalize_ram_title(amazon_title)

def test_is_valid_model_logic():
    scraper = NeweggScraper()
    assert scraper._is_valid_model("CMK32GX5M2B6000C38") is True
    
    # These should now correctly return False
    assert scraper._is_valid_model("DDR5-MEMORY") is False 
    assert scraper._is_valid_model("12345") is False 

def test_model_extraction_regex_variants():
    # Updated pattern to handle colons and varied spacing
    pattern = r'(?i)model:?\s*([A-Z0-9-]+)'
    
    title_1 = "CORSAIR Vengeance 32GB Model CMK32GX5M2B6000C38"
    assert re.search(pattern, title_1).group(1) == "CMK32GX5M2B6000C38"
    
    title_2 = "G.SKILL Trident Z5 Model:F5-6000J3038F16GX2-TZ5NR"
    assert re.search(pattern, title_2).group(1) == "F5-6000J3038F16GX2-TZ5NR"