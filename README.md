# django-ninja-fsbr

File-System Based Routing for django-ninja

## Why

- To enforce an opinionated project structure, that does not make me think.
- To enable easily mapping routes/endpoints to files.
- For fun. :)

## Usage

The usage is most easily explained using an example.
Let's say you want to have the following API:

```
/products/ GET, POST
/products/<product_id>/ GET
/products/<product_id>/stock/ GET, PUT
```

You can achieve this using the following directory layout:

```
├── root.py
└── views
    └── products
        ├── index.py
        ├── __init__.py
        └── product_id
            ├── index.py
            ├── __init__.py
            └── stock.py
```

The `root` module contains the definition of a router which specifies the base directory, that your automatic routes
will be relative to:

```python
from ninja_fsbr import FilesystemBasedRouter

api = NinjaApi(
    ...
)

router = FilesystemBasedRouter(views_module="root.views")
router.auto_discover()

api.add_router("api/", router)
```

To define an "auto" route, just use the `@router.auto_route` decorator instead django-ninja's `@router.<method>` decorators:

```python
from root import router

@router.auto_route(
  methods=["GET"],  # optional, if method name starts with get_ (or any other HTTP method name)
  ... # other django-ninja arguments here
)
def get_stock(request, product_id):
  ...
```

## Conventions

- Any directory with the ending `_id` will be treated as a path parameter in the generated route.
- The `index.py` will resolve to the path itself.
- The supported HTTP method can be set by either passing a `methods` argument to `auto_route` or by prefixing the view function with the verbs i.e. get_put_stock (to support both GET and PUT requests)
- Routes are sorted by name
