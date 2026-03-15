from app.models import PricePoint
from sqlmodel import select

def test_create_price_point(session):
    new_entry = PricePoint(
        retailer="TestShop",
        product_name="DDR5 RAM",
        price=150.00,
        in_stock=True,
        url="https://test.com"
    )
    session.add(new_entry)
    session.commit()
    
    saved_item = session.exec(select(PricePoint)).first()
    assert saved_item.retailer == "TestShop"
    assert saved_item.timestamp is not None # Verifies default_factory works