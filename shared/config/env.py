from __future__ import annotations

"""
環境設定工具
- 使用 ESG_ENV 區分 dev / prod
"""

import os
from enum import Enum


class AppEnv(str, Enum):
    DEV = "dev"
    PROD = "prod"


def get_app_env() -> AppEnv:
    """
    取得目前執行環境。
    - 預設為 dev，方便本機開發。
    - 當 ESG_ENV=prod 時視為正式環境。
    """
    value = os.environ.get("ESG_ENV", "dev").lower()
    if value == "prod":
        return AppEnv.PROD
    return AppEnv.DEV

