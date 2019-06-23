import argparse
import importlib
import os

import torch.nn as nn

from .base_task import BaseTask

TASK_REGISTRY = {}


def build_task(args):
    return TASK_REGISTRY[args.task](args)


def register_task(name):
    """
    New task types can be added to cognitive_graph with the :func:`register_task`
    function decorator.

    For example::

        @register_task('node_classification')
        class NodeClassification(BaseTask):
            (...)

    Args:
        name (str): the name of the task
    """

    def register_task_cls(cls):
        if name in TASK_REGISTRY:
            raise ValueError("Cannot register duplicate task ({})".format(name))
        if not issubclass(cls, BaseTask):
            raise ValueError(
                "Task ({}: {}) must extend BaseTask".format(name, cls.__name__)
            )
        TASK_REGISTRY[name] = cls
        return cls

    return register_task_cls


# automatically import any Python files in the tasks/ directory
for file in os.listdir(os.path.dirname(__file__)):
    if file.endswith(".py") and not file.startswith("_"):
        task_name = file[: file.find(".py")]
        module = importlib.import_module("cognitive_graph.tasks." + task_name)
