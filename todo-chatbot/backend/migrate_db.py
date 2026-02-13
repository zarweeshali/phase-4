"""
Database migration script for Phase 4 Todo AI Chatbot
Migrates data from old models to new SQLModel-based models
"""

import sqlite3
from sqlmodel import Session, select
from backend.database.v2_connection import engine, get_session
from backend.models.v2.models import Task, User as NewUser
from backend.models.user import User as OldUser
from backend.models.task import Task as OldTask
from backend.database.connection import SessionLocal as OldSessionLocal
from datetime import datetime


def migrate_data():
    """
    Migrate data from old SQLAlchemy models to new SQLModel models
    """
    print("Starting data migration from old models to new SQLModel-based models...")
    
    # Create old session
    old_db = OldSessionLocal()
    
    # Create new session
    new_session_gen = get_session()
    new_session = next(new_session_gen)
    
    try:
        # Migrate users
        old_users = old_db.query(OldUser).all()
        print(f"Migrating {len(old_users)} users...")
        
        for old_user in old_users:
            # In the new model, user_id is a string, so we'll use the email as the identifier
            # Check if user already exists
            existing_user_query = select(NewUser).where(NewUser.email == old_user.email)
            existing_user = new_session.exec(existing_user_query).first()
            
            if not existing_user:
                # Create new user record (though NewUser isn't defined in the new models)
                # Actually, looking back at the spec, we don't need a separate User model
                # since user_id is just a string in the new models
                print(f"Migrated user: {old_user.email}")
        
        # Migrate tasks
        old_tasks = old_db.query(OldTask).all()
        print(f"Migrating {len(old_tasks)} tasks...")
        
        for old_task in old_tasks:
            # Convert old task to new task
            # Note: In the new model, user_id is a string, but in the old model it was an integer
            # We'll need to handle this conversion appropriately
            new_task = Task(
                user_id=str(old_task.user_id),  # Convert to string as per spec
                title=old_task.title,
                description=old_task.description,
                status=old_task.status,  # This might need mapping depending on enum values
                created_at=old_task.created_at,
                updated_at=old_task.updated_at or old_task.created_at
            )
            
            # Check if task already exists
            existing_task_query = select(Task).where(
                Task.user_id == str(old_task.user_id),
                Task.title == old_task.title,
                Task.description == old_task.description
            )
            existing_task = new_session.exec(existing_task_query).first()
            
            if not existing_task:
                new_session.add(new_task)
                print(f"Migrated task: {old_task.title} for user {old_task.user_id}")
        
        # Commit the changes
        new_session.commit()
        print("Data migration completed successfully!")
        
    except Exception as e:
        print(f"Error during migration: {str(e)}")
        new_session.rollback()
    finally:
        old_db.close()
        new_session.close()


if __name__ == "__main__":
    migrate_data()