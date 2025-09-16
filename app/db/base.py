from sqlalchemy.orm import declarative_base

Base = declarative_base()


# import your models so that Base.metadata picks them up
# e.g. from app.models import item # noqa: F401
