"""Wrapper around NinjaAPI that adds file based routing and endpoint auto-discovery.

Usage:
    # in your/api/file.py

    api = NinjaAutoApi(
        views_module="your.api.views",
        ...
    )

    api.auto_discover()
"""
import importlib
import inspect
import os
from itertools import takewhile
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured
from ninja import NinjaAPI

__version__ = "0.1.1"


class NinjaFsbrAPI(NinjaAPI):
    def __init__(self, *args, views_module, **kwargs):
        super().__init__(*args, **kwargs)
        self.views_module = views_module

    def auto_route(self, *, methods=None, **kwargs):
        def decorator(view_func):
            nonlocal methods

            parts = (
                view_func.__module__.removeprefix(self.views_module)
                .removeprefix(".")
                .split(".")
            )

            for i, part in enumerate(parts):
                is_path_parameter = part.endswith("id")

                if is_path_parameter:
                    parts[i] = f"{{{part}}}"
                else:
                    parts[i] = part.replace("_", "-")

            path = "/".join(parts)
            path = path.removesuffix("/index")
            path = f"/{path}/"

            if methods is None:
                # The supported methods are encoded in the function name as the prefix.
                # Multiple methods can be specified, using an underscore as a separator.
                # Extract those methods and save them in the methods variable.
                method_names = [
                    "get",
                    "post",
                    "put",
                    "patch",
                    "delete",
                    "options",
                    "head",
                ]
                methods = [
                    method.upper()
                    for method in takewhile(
                        lambda x: x in method_names, view_func.__name__.split("_")
                    )
                ]

            if not methods:
                raise ImproperlyConfigured(
                    f"Could not determine methods for view {view_func.__name__}"
                )

            return self.api_operation(methods, path, **kwargs)(view_func)

        return decorator

    def auto_discover(self) -> None:
        stack = inspect.stack()
        caller_module = inspect.getmodule(stack[1][0])
        if not caller_module:
            raise ImproperlyConfigured(
                "Could not determine caller module for auto_discover"
            )

        base_path = Path(os.getcwd())

        api_dir: str = os.path.dirname(caller_module.__file__)  # type: ignore
        api_path = Path(api_dir)

        for file_path in sorted(api_path.rglob("*.py")):
            if file_path.name == "__init__.py":
                continue

            import_path = (
                str(file_path.relative_to(base_path))
                .removesuffix(".py")
                .replace(os.path.sep, ".")
            )
            importlib.import_module(import_path)
