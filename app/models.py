from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone

db = SQLAlchemy()

class PlaidAccount(db.Model):
    id = db.Column(db.String, primary_key=True)  # Plaid's account_id
    item_id = db.Column(db.String, nullable=False)  # ID for the linked institution
    name = db.Column(db.String, nullable=False)
    mask = db.Column(db.String)
    type = db.Column(db.String)
    subtype = db.Column(db.String)
    balance_current = db.Column(db.Float)
    last_updated = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

class CryptoHolding(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.String, nullable=False)  # e.g., 'bitcoin', 'cardano' from CoinGecko
    symbol = db.Column(db.String, nullable=False)  # e.g., 'btc', 'ada'
    quantity = db.Column(db.Float, nullable=False)
    source = db.Column(db.String, nullable=False)  # e.g., 'Kraken', 'Coinbase', 'Yoroi Wallet'

class ManualAsset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)  # e.g., 'DraftKings', 'Acorns VOO'
    category = db.Column(db.String, nullable=False)  # e.g., 'Sportsbook', 'Referral Bonus'
    value = db.Column(db.Float, nullable=False)
    last_updated = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))