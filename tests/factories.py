# import factory
# from .conftest import db_session
# from db.models import Event, Fight, Fighter
#
#
# def fighter_factory():
#     class FighterFactory(factory.alchemy.SQLAlchemyModelFactory):
#
#         name = factory.Faker("name")
#
#         class Meta:
#             model = Fighter
#             sqlalchemy_session = db_session
#     return FighterFactory
