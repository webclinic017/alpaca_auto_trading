import logging
import json

logger = logging.getLogger(__name__)


def info(**deco_kwargs):
    """
Basic definition of request method decorator for INFO-type logging

Usage:
---
from core.services import log

@log.info(custom_message='abc')
def get(self, request, *args, **kwargs):
    ...

    """
    def _decorator(func):
        def object_method_wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            msg_parts = [str(x) for x in args]
            msg_parts.extend([f"{k}:{str(v)}" for k, v in kwargs.items()])

            if len(deco_kwargs):
                msg_parts.extend([
                    f"{k}:{v}" if isinstance(v, str) else f"{k}:{str(v)}" for k, v in deco_kwargs.items()
                ])

            logger.info(";".join(msg_parts))
            return result
        return object_method_wrapper
    return _decorator

def debug(**deco_kwargs):
    """
Basic definition of request method decorator for DEBUG-type logging

Usage:
---
from core.services import log

@log.debug(custom_message='abc')
def get(self, request, *args, **kwargs):
    ...

    """
    def _decorator(func):
        def object_method_wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            msg_parts = [str(x) for x in args]
            msg_parts.extend([str(result)])
            msg_parts.extend([f"{k}:{str(v)}" for k, v in kwargs.items()])

            if len(deco_kwargs):
                msg_parts.extend([
                    f"{k}:{v}" if isinstance(v, str) else f"{k}:{str(v)}" for k, v in deco_kwargs.items()
                ])

            logger.debug(";".join(msg_parts))
            return result
        return object_method_wrapper
    return _decorator