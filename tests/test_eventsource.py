from laktory._testing import StockPriceSource


def test_eventsource():
    source = StockPriceSource()
    print(source)

    assert source.producer.name == "yahoo-finance"
    assert source.read_as_stream
    assert source.dirpath == "/mnt/landing/events/yahoo-finance/stock_price/"
    assert source.fmt == "JSON"


if __name__ == "__main__":
    test_eventsource()
