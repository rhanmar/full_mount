from db.database import SessionLocal
from db.database import Base


def get_or_create(session: SessionLocal, model: Base, **kwargs) -> Base:
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance


def check_does_exist(session: SessionLocal, model: Base, **kwargs) -> bool:
    result = session.query(model).filter_by(**kwargs).count()
    return bool(result)


def get_ref_id_from_url(url: str) -> str:
    return url.split("/")[-1]
