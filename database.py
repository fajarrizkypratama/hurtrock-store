from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from flask_migrate import Migrate

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
migrate = Migrate()  # <--- tambah ini

def configure_database(app):
    import os

    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        default_db_url = "postgresql://postgres:fajar@localhost:5432/hurtrock"
        os.environ['DATABASE_URL'] = default_db_url
        database_url = default_db_url
        print(f"[INFO] Generated DATABASE_URL: {database_url}")

    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate.init_app(app, db)  # <--- init Flask-Migrate

    return True

def upgrade():
    # Tambah kolom baru ke orders
    op.add_column('orders', sa.Column('local_transaction_id', sa.String(length=100), nullable=True))
    op.add_column('orders', sa.Column('pos_user_id', sa.Integer(), nullable=True))


def downgrade():
    op.drop_column('orders', 'local_transaction_id')
    op.drop_column('orders', 'pos_user_id')
