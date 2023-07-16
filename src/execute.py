from construction_tree import ConstructionTree
from utils import syntax_analysis
from storage import Storage
from block import Block




def read_text(file: str):
    try:
        with open(file, 'r') as f:
            text = f.read();
            return text
    except:
        return ''


def execute(file: str, storage: Storage):
    file += '.yer'
    text = read_text(file)
    if text:
        text = syntax_analysis(text)
        tree = ConstructionTree(text, storage)
        block = tree.reduce()
        block.run()
        return True
    return False
