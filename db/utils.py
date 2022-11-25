def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance


def does_exist(session, model, **kwargs):
    result = session.query(model).filter_by(**kwargs).count()
    return bool(result)
