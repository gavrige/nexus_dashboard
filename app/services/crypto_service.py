import os
import requests
from pycoingecko import CoinGeckoAPI
from app.models import db, CryptoHolding

# Initialize the CoinGecko API client
cg = CoinGeckoAPI()

def get_crypto_holdings_by_source(source):
    """Gets all crypto holdings from a specific source (e.g., 'Kraken', 'Manual Wallet')."""
    return CryptoHolding.query.filter_by(source=source).all()

def get_all_crypto_holdings():
    """Gets all crypto holdings from the database."""
    return CryptoHolding.query.all()

def calculate_manual_crypto_values():
    """
    Fetches live prices for manually tracked crypto and calculates their total value.
    This function is for display purposes and doesn't write to the database.
    """
    # Get all holdings that are not on an automated exchange
    manual_wallets = CryptoHolding.query.filter(CryptoHolding.source.like('%Wallet%')).all()
    if not manual_wallets:
        return {}, 0.0 # Return empty dict and zero total

    # Create a list of unique asset IDs (e.g., 'bitcoin', 'ethereum')
    asset_ids = list(set([holding.asset_id for holding in manual_wallets]))

    try:
        # Make a single API call to CoinGecko to get all prices
        price_data = cg.get_price(ids=asset_ids, vs_currencies='usd')
    except Exception as e:
        print(f"Could not fetch crypto prices from CoinGecko: {e}")
        return {}, 0.0

    # Calculate total value and store individual values
    live_data = {}
    total_value = 0.0
    for holding in manual_wallets:
        try:
            price = price_data[holding.asset_id]['usd']
            value = holding.quantity * price
            total_value += value
            live_data[holding.id] = {'value': value, 'price': price}
        except KeyError:
            print(f"Warning: Price for asset '{holding.asset_id}' not found in CoinGecko response.")
            live_data[holding.id] = {'value': 0, 'price': 0}

    return live_data, total_value


# --- Placeholder Functions for Exchange Integration ---

def get_kraken_balances():
    """
    [Future Implementation]
    Fetches balances from Kraken using read-only API keys.
    Parses the response and updates the CryptoHolding table in the database.
    """
    # api_key = os.environ.get('KRAKEN_API_KEY')
    # private_key = os.environ.get('KRAKEN_PRIVATE_KEY')
    # Logic to make authenticated request to Kraken API will go here.
    print("Kraken balance sync not yet implemented.")
    pass

def get_coinbase_balances():
    """
    [Future Implementation]
    Fetches balances from Coinbase using read-only API keys.
    Parses the response and updates the CryptoHolding table in the database.
    """
    # api_key = os.environ.get('COINBASE_API_KEY')
    # secret_key = os.environ.get('COINBASE_API_SECRET')
    # Logic to make authenticated request to Coinbase API will go here.
    print("Coinbase balance sync not yet implemented.")
    pass