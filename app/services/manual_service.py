from app.models import db, ManualAsset

def get_all_manual_assets():
    """Fetches all manual assets from the database."""
    return ManualAsset.query.all()

def add_manual_asset(name, category, value):
    """Adds a new manual asset to the database."""
    try:
        # Ensure value is a float
        value_float = float(value)
        new_asset = ManualAsset(name=name, category=category, value=value_float)
        db.session.add(new_asset)
        db.session.commit()
        return new_asset, None # Return asset, no error
    except (ValueError, TypeError) as e:
        db.session.rollback()
        return None, f"Invalid value provided: {e}" # Return no asset, error message
    except Exception as e:
        db.session.rollback()
        return None, f"An unexpected error occurred: {e}"

def get_manual_asset_by_id(asset_id):
    """Fetches a single manual asset by its ID."""
    return ManualAsset.query.get(asset_id)

def update_manual_asset(asset_id, name, category, value):
    """Updates an existing manual asset."""
    asset = get_manual_asset_by_id(asset_id)
    if asset:
        try:
            asset.name = name
            asset.category = category
            asset.value = float(value)
            db.session.commit()
            return asset, None
        except (ValueError, TypeError) as e:
            db.session.rollback()
            return None, f"Invalid value provided: {e}"
        except Exception as e:
            db.session.rollback()
            return None, f"An unexpected error occurred: {e}"
    return None, "Asset not found"

def delete_manual_asset(asset_id):
    """Deletes a manual asset from the database."""
    asset = get_manual_asset_by_id(asset_id)
    if asset:
        db.session.delete(asset)
        db.session.commit()
        return True # Success
    return False # Asset not found