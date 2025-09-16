from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
import models, schemas, utils
from datetime import datetime
from fastapi import HTTPException, status

# --- Users ---
def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user_in: schemas.UserCreate):
    hashed = utils.get_password_hash(user_in.password)
    user_data = {
        'username': user_in.username,
        'password_hash': hashed,
        'first_name': user_in.first_name,
        'last_name': user_in.last_name,
    }
    
    # Only include email if it's provided
    if user_in.email:
        user_data['email'] = user_in.email
    
    user = models.User(**user_data)
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Create default settings
    setting = models.Setting(user_id=user.id, default_currency="UZS")
    db.add(setting)
    db.commit()
    return user

# --- Settings ---
def get_setting(db: Session, user_id: int):
    return db.query(models.Setting).filter(models.Setting.user_id == user_id).first()

def upsert_setting(db: Session, user_id: int, setting_in: schemas.SettingUpdate):
    s = get_setting(db, user_id)
    if not s:
        # Create new settings with default values if not exists
        s = models.Setting(
            user_id=user_id,
            notifications_enabled=getattr(setting_in, 'notifications_enabled', True),
            theme=getattr(setting_in, 'theme', 'light'),
            default_currency=getattr(setting_in, 'default_currency', 'UZS'),
            reminder_time=getattr(setting_in, 'reminder_time', None),
            reminder_enabled=getattr(setting_in, 'reminder_enabled', False)
        )
        db.add(s)
    else:
        # Update only provided fields
        for field in ['notifications_enabled', 'theme', 'default_currency', 'reminder_enabled']:
            if hasattr(setting_in, field) and getattr(setting_in, field) is not None:
                setattr(s, field, getattr(setting_in, field))
        
        # Handle reminder_time separately as it can be None
        if hasattr(setting_in, 'reminder_time'):
            s.reminder_time = setting_in.reminder_time
    
    db.commit()
    db.refresh(s)
    return s

# --- Debts ---
def create_debt(db: Session, debt_in: schemas.DebtCreate, user_id: int):
    # Create the debt with all required fields
    d = models.Debt(
        user_id=user_id,
        debt_type=debt_in.debt_type,
        person_name=debt_in.person_name,
        amount=debt_in.amount,
        currency=debt_in.currency,
        description=debt_in.description,
        due_date=debt_in.due_date,
        # start_date and created_at will be set automatically by the model
    )
    
    db.add(d)
    db.commit()
    db.refresh(d)
    return d

def update_debt(db: Session, debt_id: int, user_id: int, debt_in: schemas.DebtUpdate):
    d = db.query(models.Debt).filter(models.Debt.id == debt_id, models.Debt.user_id == user_id).first()
    if not d:
        return None
    
    # Only update fields that were provided in the request
    update_data = debt_in.model_dump(exclude_unset=True)
    
    for field, value in update_data.items():
        setattr(d, field, value)
    
    db.commit()
    db.refresh(d)
    return d

def delete_debt(db: Session, debt_id: int, user_id: int):
    d = db.query(models.Debt).filter(models.Debt.id == debt_id, models.Debt.user_id == user_id).first()
    if not d:
        return False
    db.delete(d)
    db.commit()
    return True

def get_user_debts(db: Session, user_id: int, debt_type: Optional[str] = None) -> List[models.Debt]:
    q = db.query(models.Debt).filter(models.Debt.user_id == user_id)
    if debt_type:
        # allow filtering by owed_to / owed_by / individual
        try:
            dt = models.DebtType(debt_type)
            q = q.filter(models.Debt.debt_type == dt)
        except ValueError:
            # unknown value -> return empty
            return []
    return q.order_by(models.Debt.start_date.desc()).all()

# --- Monitoring / Aggregation ---
def get_monitoring_summary(db: Session, user_id: int) -> List[Dict[str, Any]]:
    """
    Get a summary of all debts for a user, grouped by currency.
    
    Args:
        db: Database session
        user_id: ID of the user
        
    Returns:
        List of dictionaries containing summary information for each currency
        
    Raises:
        HTTPException: If there's an error processing the debts
    """
    try:
        debts = db.query(models.Debt).filter(models.Debt.user_id == user_id).all()
        summary = {}
        
        for d in debts:
            try:
                code = d.currency or "UZS"
                if code not in summary:
                    summary[code] = {"owed_to": 0, "owed_by": 0}
                
                # Safely convert amount to integer
                try:
                    amt = int(d.amount) if d.amount is not None else 0
                except (ValueError, TypeError):
                    amt = 0
                
                # Update summary based on debt type
                if d.debt_type == models.DebtType.owed_to:
                    summary[code]["owed_to"] += amt
                elif d.debt_type == models.DebtType.owed_by:
                    summary[code]["owed_by"] += amt
                else:
                    # Default to owed_by for unknown types
                    summary[code]["owed_by"] += amt
            except Exception as e:
                # Log the error but continue processing other debts
                print(f"Error processing debt {d.id}: {str(e)}")
                continue
        
        # Prepare the result
        result = []
        for code, vals in summary.items():
            result.append({
                "currency": code,
                "total_owed_to": vals["owed_to"],
                "total_owed_by": vals["owed_by"],
                "balance": vals["owed_to"] - vals["owed_by"]
            })
            
        return result
        
    except Exception as e:
        # Log the error and return a 500 error
        print(f"Error in get_monitoring_summary: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while processing your request"
        )
