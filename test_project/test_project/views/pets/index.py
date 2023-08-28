from test_project.urls import router
from ninja import Schema


class PetListItem(Schema):
    id: int
    name: str
    species: str


@router.auto_route(
    methods=["GET"],
    operation_id="pets_list",
    response=list[PetListItem],
)
def get_pet_list(request):
    return [
        {"id": 1, "name": "Fluffy", "species": "cat"},
        {"id": 2, "name": "Fido", "species": "dog"},
    ]


class PetCreateIn(Schema):
    name: str
    species: str


@router.auto_route(
    methods=["POST"],
    operation_id="pets_create",
    response=PetListItem,
)
def create_pet(request, data: PetCreateIn):
    return {"id": 3, "name": data.name, "species": data.species}
