import ast
import os
import importlib.util
from typing import Dict, Type, Optional
import backtrader as bt

def get_class_from_file(file_path: str) -> Optional[Type[bt.Strategy]]:
    # Extract module name from file path
    module_name = os.path.basename(file_path).replace('.py', '')
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    # Parse the file to find the class name
    with open(file_path, "r") as file:
        node = ast.parse(file.read(), filename=file_path)
        for item in ast.walk(node):
            if isinstance(item, ast.ClassDef):
                # Return the class object if it inherits from bt.Strategy
                cls = getattr(module, item.name, None)
                if isinstance(cls, type) and issubclass(cls, bt.Strategy):
                    return cls
    return None

def get_all_class_objects(directory: str) -> Dict[str, Type[bt.Strategy]]:
    all_classes: Dict[str, Type[bt.Strategy]] = {}
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                cls = get_class_from_file(file_path)
                if cls:
                    all_classes[cls.__name__] = cls
    return all_classes