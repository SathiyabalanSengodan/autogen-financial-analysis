"""Helper functions handed to the code executor.

The executor copies these functions into its working directory, and the
LLM-written code imports them from there. That is why each import sits
inside the function body. The executor copies only the function source,
not this module's top-level imports.
"""


def get_stock_prices(stock_symbols, start_date, end_date):
    """Get the closing prices for the given stock symbols between two dates.

    Args:
        stock_symbols (str or list): The stock symbols to get prices for.
        start_date (str): The start date, 'YYYY-MM-DD'.
        end_date (str): The end date, 'YYYY-MM-DD'.

    Returns:
        pandas.DataFrame: Closing prices indexed by date, one column per symbol.
    """
    import yfinance

    stock_data = yfinance.download(stock_symbols, start=start_date, end=end_date)
    return stock_data.get("Close")


def plot_stock_prices(stock_prices, filename):
    """Plot stock prices and save the figure to a file.

    Args:
        stock_prices (pandas.DataFrame): Prices indexed by date, one column per symbol.
        filename (str): Where to save the figure.
    """
    import matplotlib.pyplot as plt

    plt.figure(figsize=(10, 5))
    for column in stock_prices.columns:
        plt.plot(stock_prices.index, stock_prices[column], label=column)
    plt.title("Stock Prices")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.grid(True)
    plt.savefig(filename)
