from app.db.base import Base
from app.models import dish  # noqa: F401
from app.models import operation_snapshot  # noqa: F401
from app.models import operator  # noqa: F401
from app.models import production_event  # noqa: F401
from app.models import standard  # noqa: F401
from app.models import store  # noqa: F401

target_metadata = Base.metadata
