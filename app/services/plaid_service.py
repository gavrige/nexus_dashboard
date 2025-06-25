import os
import plaid
from plaid.api import plaid_api
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.accounts_balance_get_request import AccountsBalanceGetRequest
from app.models import db, PlaidAccount

# --- Plaid Client Configuration ---

# Configure the Plaid client
host = plaid.Environment.Sandbox if os.environ.get('PLAID_ENV') == 'sandbox' else plaid.Environment.Development
configuration = plaid.Configuration(
    host=host,
    api_key={
        'clientId': os.environ.get('PLAID_CLIENT_ID'),
        'secret': os.environ.get('PLAID_SECRET'),
    }
)
api_client = plaid.ApiClient(configuration)
client = plaid_api.PlaidApi(api_client)

# --- Authentication Flow Functions (to be called by routes) ---

def create_link_token():
    """
    [Future Implementation]
    Creates a link_token required to initialize the Plaid Link frontend.
    """
    # This will be called by a route to start the linking process.
    print("Plaid create_link_token not yet implemented.")
    pass

def exchange_public_token(public_token):
    """
    [Future Implementation]
    Exchanges a temporary public_token for a permanent access_token.
    The access_token will be stored securely.
    """
    # This will be called by a route after the user successfully links their account.
    print("Plaid exchange_public_token not yet implemented.")
    pass

# --- Data Fetching Function ---

def sync_plaid_accounts(item_id, access_token):
    """
    Fetches the latest balance for all accounts associated with a single item (institution).
    Updates the PlaidAccount table in the database.
    """
    try:
        request = AccountsBalanceGetRequest(access_token=access_token)
        response = client.accounts_balance_get(request)
        accounts = response['accounts']

        for acc in accounts:
            account_id = acc['account_id']
            # Check if this account already exists in our database
            plaid_account = PlaidAccount.query.get(account_id)
            if not plaid_account:
                # If it's a new account, create it
                plaid_account = PlaidAccount(id=account_id, item_id=item_id)
                db.session.add(plaid_account)

            # Update account details
            plaid_account.name = acc['name']
            plaid_account.mask = acc['mask']
            plaid_account.type = acc['type'].value
            plaid_account.subtype = acc['subtype'].value
            plaid_account.balance_current = acc['balances']['current']

        db.session.commit()
        print(f"Successfully synced {len(accounts)} accounts for item {item_id}.")
        return True, None # Success, no error
    except plaid.ApiException as e:
        error_response = e.body
        print(f"Error syncing Plaid accounts: {error_response}")
        db.session.rollback()
        return False, error_response # Failure, error message