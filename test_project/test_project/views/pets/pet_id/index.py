from test_project.urls import router
from ninja import Schema


class PetDetail(Schema):
    id: int
    name: str
    species: str
    breed: str
    description: str
    age: int
    photo: str


@router.auto_route(
    methods=["GET"],
    operation_id="pet_detail",
    response=PetDetail,
)
def get_pet_detail(request, pet_id: int):
    return {
        "id": pet_id,
        "name": "Fluffy",
        "species": "cat",
        "breed": "Domestic Shorthair",
        "description": "Fluffy is a very fluffy cat.",
        "age": 5,
        "photo": "https://www.pexels.com/photo/adorable-animal-cat-cat-s-eyes-208984/",
    }
