from typing import Annotated
from fastapi import Depends

from src.users.models import User
from .service import get_current_admin

# Dependency that restricts endpoint access to admin users only
AdminOnly = Annotated[User, Depends(get_current_admin)]
