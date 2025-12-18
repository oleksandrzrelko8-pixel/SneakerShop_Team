import os
import importlib


def test_products_and_orders(tmp_path):
    # Isolated DB for test
    os.environ['DATABASE_PATH'] = str(tmp_path / 'test_models.sqlite')
    import models
    importlib.reload(models)

    models.init_db()

    # Initially no products
    assert models.get_all_products() == []

    # Add product
    models.add_product('Test Shoe', 100.0, '', 'Test')
    products = models.get_all_products()
    assert any(p['name'] == 'Test Shoe' for p in products)

    pid = products[0]['id']
    prod = models.get_product_by_id(pid)
    assert prod['name'] == 'Test Shoe'

    # Create order
    models.create_order(pid, 'Client', '+380123456789')
    orders = models.get_all_orders()
    assert len(orders) > 0
    assert orders[0]['product_name'] == 'Test Shoe'

    # Update status
    models.update_order_status(orders[0]['id'], 'Sent')
    orders2 = models.get_all_orders()
    assert orders2[0]['status'] == 'Sent'

    # Cleanup
    models.delete_product(pid)
    assert models.get_product_by_id(pid) is None
