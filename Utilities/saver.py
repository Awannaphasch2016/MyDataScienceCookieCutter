import os
import pickle
from typing import Any
import pathlib

def save_to_file(content: Any,
                 saved_file: pathlib.Path) -> None:

    path = str(pathlib.Path(saved_file).parent)

    if not os.path.exists(path):
        os.makedirs(path)

    with open(str(saved_file.resolve()), 'wb') as f :
        pickle.dump(content, f)
        print(f'saved at {f.name}')
