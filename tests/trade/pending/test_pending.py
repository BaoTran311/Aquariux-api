def test_get_symbol(market_client):
    resp = market_client.pending.get(dict(symbol="DASHUSD.std"))
    resp.check_status_code(200)