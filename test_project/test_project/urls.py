from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI
from ninja_fsbr import FilesystemBasedRouter

api = NinjaAPI()

router = FilesystemBasedRouter(views_module="test_project.views")
router.auto_discover()

api.add_router("/api", router)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", api.urls),
]
