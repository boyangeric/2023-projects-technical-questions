from dataclasses import dataclass
from enum import Enum
from typing import Union, NamedTuple, List
from flask import Flask, request
import json
import math

# SpaceCowboy models a cowboy in our super amazing system
@dataclass
class SpaceCowboy:
    name: str
    lassoLength: int

# SpaceAnimal models a single animal in our amazing system
@dataclass
class SpaceAnimal:
    # SpaceAnimalType is an enum of all possible space animals we may encounter
    class SpaceAnimalType(Enum):
        PIG = "pig"
        COW = "cow"
        FLYING_BURGER = "flying_burger"

    type: SpaceAnimalType

# SpaceEntity models an entity in the super amazing (ROUND UPPER 100) system
@dataclass
class SpaceEntity:
    class Location(NamedTuple):
        x: int
        y: int

    metadata: Union[SpaceCowboy, SpaceAnimal]
    location: Location

# ==== HTTP Endpoint Stubs ====
app = Flask(__name__)
space_database: List[SpaceEntity] = []

# the POST /entity endpoint adds an entity to your global space database
@app.route('/entity', methods=['POST'])
def create_entity():
    data = request.get_json()
    space_database.extend(data['entities'])
    return {}, 200

# lasooable returns all the space animals a space cowboy can lasso given their name
@app.route('/lassoable', methods=['GET'])
def lassoable():
    cowboyName = request.args.get('cowboy_name')
    animals = []
    for entity in space_database:
        if entity['type'] == "space_cowboy" and entity['metadata']['name'] == cowboyName:
            lassoLength = entity['metadata']['lassoLength']
            x_c = entity['location']['x']
            y_c = entity['location']['y']
        if entity['type'] == "space_animal":
            x_a = entity['location']['x']
            y_a = entity['location']['y']
            dis = math.sqrt((x_c - x_a)**2 + (y_c-y_a)**2)
            if dis <= lassoLength:
                animals.append({"type": entity['metadata']['type'], "location": entity['location']})
                
    return {"space_animals": animals}, 200

# DO NOT TOUCH ME, thanks :D
if __name__ == '__main__':
    app.run(debug=True, port=8080)