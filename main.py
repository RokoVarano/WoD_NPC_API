from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, oauth2
from tortoise.models import Model
from tortoise import fields
from tortoise.contrib.fastapi import register_tortoise
from tortoise.contrib.pydantic import pydantic_model_creator
from passlib.hash import bcrypt
from characters import Character, Character_Pydantic, CharacterIn_Pydantic
from typing import List
import jwt
import copy

app = FastAPI()
app_test = copy.copy(app)

JWT_SECRET = 'myjwtsecret'

class User(Model):
    id = fields.IntField(pk=True)
    username = fields.CharField(50, unique=True)
    password_hash = fields.CharField(128)

    def verify_password(self, password):
        return bcrypt.verify(password, self.password_hash)

User_Pydantic = pydantic_model_creator(User, name='User')
UserIn_Pydantic = pydantic_model_creator(User, name='UserIn', exclude_readonly=True)

oauth2_scheme = oauth2.OAuth2PasswordBearer(tokenUrl='api/login/')

async def authenticate_user(username:str, password:str):
    user = await User.get(username=username)
    if not user:
        return False
    if not user.verify_password(password):
        return False
    return user

@app.post('/api/login')
async def generate_token(form_data:OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid username or password')
    
    user_obj = await User_Pydantic.from_tortoise_orm(user)

    token = jwt.encode(user_obj.dict(), JWT_SECRET)

    return {"id": user_obj.id, "username": user_obj.username, 'access_token': token, 'token_type' : 'bearer'}

async def get_user_current(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        user = await User.get(id=payload.get('id'))
    except:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid username or password')

    return await User_Pydantic.from_tortoise_orm(user)


@app.post('/api/users', response_model=User_Pydantic, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserIn_Pydantic):
    user_obj= User(username=user.username, password_hash=bcrypt.hash(user.password_hash))
    await user_obj.save()
    return await User_Pydantic.from_tortoise_orm(user_obj)

# @app.get('/api/users/me', response_model=User_Pydantic)
# async def get_user(user: User_Pydantic = Depends(get_user_current)):
#     return user

@app.post('/api/characters', response_model=Character_Pydantic, status_code=status.HTTP_201_CREATED)
async def create_character(character: CharacterIn_Pydantic, owner: User_Pydantic = Depends(get_user_current)):

    character_obj = Character(
        user_id=owner.id,
        name=character.name,
        sex=character.sex,
        gender=character.gender,
        sex_orientation=character.sex_orientation,
        wallet=character.wallet,
        bank=character.bank,
        concept=character.concept,
        ambition=character.ambition,
        desire=character.desire,
        strength=character.strength,
        dexterity=character.dexterity,
        stamina=character.stamina,
        charisma=character.charisma,
        manipulation=character.manipulation,
        composure=character.composure,
        intelligence=character.intelligence,
        wits=character.wits,
        resolve=character.resolve,
        athletics=character.athletics,
        brawl=character.brawl,
        craft=character.craft,
        drive=character.drive,
        firearms=character.firearms,
        melee=character.melee,
        larceny=character.larceny,
        stealth=character.stealth,
        survival=character.survival,
        animal_ken=character.animal_ken,
        etiquette=character.etiquette,
        insight=character.insight,
        intimidation=character.intimidation,
        leadership=character.leadership,
        performance=character.performance,
        persuasion=character.persuasion,
        streetwise=character.streetwise,
        subterfuge=character.subterfuge,
        academics=character.academics,
        awareness=character.awareness,
        finance=character.finance,
        investigation=character.investigation,
        medicine=character.medicine,
        occult=character.occult,
        politics=character.politics,
        science=character.science,
        technology=character.technology,
        health_max=character.health_max,
        health_current=character.health_current,
        will_max=character.will_max,
        will_current=character.will_current,
        allies=character.allies,
        contacts=character.contacts,
        fame=character.fame,
        haven=character.haven,
        influence=character.influence,
        loresheet=character.loresheet,
        mask=character.mask,
        resources=character.resources,
        retainers=character.retainers,
        status=character.status,
        linguistics=character.linguistics,
        looks=character.looks,
        substance_use=character.substance_use,
        bonding=character.bonding,
        humanity=character.humanity,
        stains=character.stains
    )
    await character_obj.save()
    return await Character_Pydantic.from_tortoise_orm(character_obj)

@app.get('/api/characters', response_model=List[Character_Pydantic], status_code=status.HTTP_200_OK)
async def get_characters(owner: User_Pydantic = Depends(get_user_current)):
    my_chars = await Character.filter(user_id = owner.id).all()
    return [await Character_Pydantic.from_tortoise_orm(character) for character in my_chars]

@app.delete('/api/characters', response_model=str, status_code=status.HTTP_202_ACCEPTED)
async def delete_character(id: int, owner = Depends(get_user_current)):
    if not owner:
        return "Not logged in"

    c = await Character.get(id=id)
    await c.delete()

@app.put('/api/characters', response_model=Character_Pydantic, status_code=status.HTTP_200_OK)
async def update_character(id: int, to_update: dict, owner = Depends(get_user_current)):
    if not owner:
        return "Not logged in"

    c = await Character.get(id=id)

    await c.update_from_dict(to_update)

    await c.save()

    return await Character_Pydantic.from_tortoise_orm(c)

register_tortoise(
    app,
    db_url="postgres://postgres:postgres@localhost:5432/wod_npc",
    modules={'models': ['main']},
    generate_schemas= True,
    add_exception_handlers=True
)