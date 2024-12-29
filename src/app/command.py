

import click
from flask.cli import with_appcontext
from sqlalchemy.exc import IntegrityError
from app.app_modules.users.models import User

#to run this : flask seed

def register_commands(app):
    @app.cli.command("seed")
    @with_appcontext
    def seed():
        """Seed initial data for the application."""
        # Create superuser
        create_super_user(app)


def create_super_user(app):
    """Create a superuser account if it doesn't exist."""
    with app.app_context():
        admin_email = app.config.get("SUPER_USER", {}).get("ADMIN_EMAIL")
        admin_password = app.config.get("SUPER_USER", {}).get("ADMIN_PASSWORD")
        
        if not admin_email or not admin_password:
            click.echo("Superuser configuration missing.")
            return
        
        existing_user = User.query.filter_by(email=admin_email).first()
        
        if existing_user:
            click.echo(f"Admin account with email {admin_email} already exists.")
            return
        
        from app import db
        try:
            user = User(
                email=admin_email,
                role=User.SUPER_ADMIN,
                is_superuser=True
            )
            user.set_password(admin_password)  
            db.session.add(user)
            db.session.commit()
            click.echo(f"Created admin account with email {admin_email}.")
        except IntegrityError as e:
            db.session.rollback()
            click.echo(f"Error creating admin account: {e}")