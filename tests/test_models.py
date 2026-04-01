from app.models import PricePoint
from sqlmodel import select

def test_create_price_point(session):
    new_entry = PricePoint(
        retailer="TestShop",
        product_name="DDR5 RAM",
        model_number="TEST-MOD-123",
        price=150.00,
        in_stock=True,
        url="https://test.com"
    )
    session.add(new_entry)
    session.commit()
    
    saved_item = session.exec(select(PricePoint)).first()
    assert saved_item.retailer == "TestShop"
    assert saved_item.timestamp is not None # Verifies default_factory works

def test_bulk_self_healing_logic(session):
    """Ensures multiple UNKNOWN records are fixed when a correct model is found."""
    test_url = "https://newegg.com/verified-ram-kit"
    
    # 1. Setup: Insert 3 'broken' records
    for _ in range(3):
        session.add(PricePoint(
            retailer="Newegg",
            product_name="Mismatched RAM",
            model_number="UNKNOWN",
            price=155.99,
            in_stock=True,
            url=test_url
        ))
    session.commit()

    # 2. Action: Find all UNKNOWNs for this URL and fix them
    new_data = {"model_number": "CORSAIR-V-123"}
    
    statement = select(PricePoint).where(
        PricePoint.url == test_url,
        PricePoint.model_number == "UNKNOWN"
    )
    results = session.exec(statement).all()
    
    for entry in results:
        entry.model_number = new_data["model_number"]
        session.add(entry)
    session.commit()

    # 3. Assert: Verify every single one is now correct
    final_check = session.exec(select(PricePoint).where(PricePoint.url == test_url)).all()
    assert len(final_check) == 3
    for record in final_check:
        assert record.model_number == "CORSAIR-V-123"