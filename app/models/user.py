from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.extension import db, login_manager


@login_manager.user_loader
def load_user(user):
    return User.query.get(user)


class User(db.Model):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    account: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
