from .api import routes as api_routes
from .auth import routes as auth_routes
from .static import routes as static_routes


routes = [
    *api_routes,
    *auth_routes,
    *static_routes,
]
