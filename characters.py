from dataclasses import field
from email.policy import default
from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.pydantic import pydantic_model_creator

class Character(Model):
    id=fields.IntField(pk=True)

    experience=fields.IntField(default=0)
    user=fields.ForeignKeyField('models.User', related_name='characters')
    name=fields.CharField(50, default='Anonymous')
    sex=fields.IntField(default=0)
    gender=fields.IntField(default=0)
    sex_orientation=fields.IntField(default=0)
    wallet=fields.FloatField(default=0)
    bank=fields.FloatField(default=0)

    concept=fields.CharField(50, default='')
    ambition=fields.CharField(50, default='')
    desire=fields.CharField(50, default='')

    strength=fields.IntField(default=0)
    dexterity=fields.IntField(default=0)
    stamina=fields.IntField(default=0)
    charisma=fields.IntField(default=0)
    manipulation=fields.IntField(default=0)
    composure=fields.IntField(default=0)
    intelligence=fields.IntField(default=0)
    wits=fields.IntField(default=0)
    resolve=fields.IntField(default=0)

    athletics=fields.IntField(default=0)
    brawl=fields.IntField(default=0)
    craft=fields.IntField(default=0)
    drive=fields.IntField(default=0)
    firearms=fields.IntField(default=0)
    melee=fields.IntField(default=0)
    larceny=fields.IntField(default=0)
    stealth=fields.IntField(default=0)
    survival=fields.IntField(default=0)
    animal_ken=fields.IntField(default=0)
    etiquette=fields.IntField(default=0)
    insight=fields.IntField(default=0)
    intimidation=fields.IntField(default=0)
    leadership=fields.IntField(default=0)
    performace=fields.IntField(default=0)
    persuasion=fields.IntField(default=0)
    streetwise=fields.IntField(default=0)
    subterfuge=fields.IntField(default=0)
    academics=fields.IntField(default=0)
    awareness=fields.IntField(default=0)
    finance=fields.IntField(default=0)
    investigation=fields.IntField(default=0)
    medicine=fields.IntField(default=0)
    occult=fields.IntField(default=0)
    politics=fields.IntField(default=0)
    science=fields.IntField(default=0)
    technology=fields.IntField(default=0)

    health_max=fields.IntField(default=0)
    health_current=fields.IntField(default=0)
    will_max=fields.IntField(default=0)
    will_current=fields.IntField(default=0)

    allies=fields.IntField(default=0)
    contacts=fields.IntField(default=0)
    fame=fields.IntField(default=0)
    haven=fields.IntField(default=0)
    influence=fields.IntField(default=0)
    loresheet=fields.IntField(default=0)
    mask=fields.IntField(default=0)
    resources=fields.IntField(default=0)
    retainers=fields.IntField(default=0)
    status=fields.IntField(default=0)

    linguistics=fields.IntField(default=0)
    looks=fields.IntField(default=0)
    substance_use=fields.IntField(default=0)
    bonding=fields.IntField(default=0)

    humanity=fields.IntField(default=0)
    stains=fields.IntField(default=0)

Character_Pydantic = pydantic_model_creator(
    Character
    )