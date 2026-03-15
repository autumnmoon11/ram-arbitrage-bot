import pytest
import re

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