from flask import Blueprint, render_template, request, redirect, url_for, flash
from .services import plaid_service, crypto_service, manual_service
from .models import PlaidAccount # We'll need this for querying

# A Blueprint is a way to organize a group of related views and other code.
# We register the blueprint with the application in __init__.py.
bp = Blueprint('routes', __name__)

@bp.route('/')
@bp.route('/dashboard')
def dashboard():
    """The main dashboard page."""
    # --- Fetch Data from Services ---
    # Plaid accounts (from our database)
    plaid_accounts = PlaidAccount.query.all()
    plaid_total = sum(acc.balance_current or 0 for acc in plaid_accounts)

    # Crypto holdings (from our database)
    crypto_holdings = crypto_service.get_all_crypto_holdings()
    # Get live values for non-exchange holdings
    live_crypto_data, crypto_total = crypto_service.calculate_manual_crypto_values()

    # Manual assets (from our database)
    manual_assets = manual_service.get_all_manual_assets()
    manual_total = sum(asset.value or 0 for asset in manual_assets)

    # --- Calculate Totals ---
    net_worth = plaid_total + crypto_total + manual_total

    # --- Prepare Chart Data ---
    chart_data = {
        'labels': ['Traditional', 'Crypto', 'Manual'],
        'values': [round(plaid_total, 2), round(crypto_total, 2), round(manual_total, 2)]
    }

    return render_template(
        'dashboard.html',
        plaid_accounts=plaid_accounts,
        plaid_total=plaid_total,
        crypto_holdings=crypto_holdings,
        live_crypto_data=live_crypto_data,
        crypto_total=crypto_total,
        manual_assets=manual_assets,
        manual_total=manual_total,
        net_worth=net_worth,
        chart_data=chart_data
    )

@bp.route('/manual-entry', methods=['GET', 'POST'])
def manual_entry():
    """Page for manually adding an asset."""
    if request.method == 'POST':
        name = request.form.get('name')
        category = request.form.get('category')
        value = request.form.get('value')

        if not name or not category or not value:
            flash('All fields are required.', 'error')
        else:
            asset, error = manual_service.add_manual_asset(name, category, value)
            if error:
                flash(f'Error adding asset: {error}', 'error')
            else:
                flash(f'Successfully added asset: {asset.name}', 'success')
            return redirect(url_for('routes.dashboard'))

    return render_template('manual_entry.html')