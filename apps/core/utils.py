import os
from alembic.command import upgrade
from alembic.config import Config

def get_path(relative_path=None):
    """Get absolute path to resource. If relative_path is not specified, return the current working directory
    """
    base_path = os.getcwd()

    if relative_path:
        joined_path = os.path.join(base_path, relative_path)
    else:
        joined_path = base_path

    return joined_path


def alembic_upgrade_to_head():
    """Auto-upgrade alembic head to the final database revision
    """
    # Changing the working directory is required as alembic use relative path
    alembic_ini_path = get_path("database/alembic.ini")
    alembic_config = Config(alembic_ini_path)
    upgrade(alembic_config, "head")