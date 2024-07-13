import zlib
from dataclasses import dataclass
from enum import Enum
from pathlib import Path


class BlobType(Enum):
    """Helper class for holding blob type"""
    COMMIT = b'commit'
    TREE = b'tree'
    DATA = b'blob'

    @classmethod
    def from_bytes(cls, type_: bytes) -> 'BlobType':
        for member in cls:
            if member.value == type_:
                return member
        assert False, f'Unknown type {type_.decode("utf-8")}'


@dataclass
class Blob:
    """Any blob holder"""
    type_: BlobType
    content: bytes


@dataclass
class Commit:
    """Commit blob holder"""
    tree_hash: str
    parents: list[str]
    author: str
    committer: str
    message: str


@dataclass
class Tree:
    """Tree blob holder"""
    children: dict[str, Blob]


def read_blob(path: Path) -> Blob:
    """
    Read blob-file, decompress and parse header
    :param path: path to blob-file
    :return: blob-file type and content
    """
    by: list[bytes] = zlib.decompress(path.read_bytes()).split(b'\x00')
    type = by[0].split(bytes(' ', 'utf8'))[0]
    return Blob(type_=BlobType.from_bytes(type), content=by[1])


def traverse_objects(obj_dir: Path) -> dict[str, Blob]:
    """
    Traverse directory with git objects and load them
    :param obj_dir: path to git "objects" directory
    :return: mapping from hash to blob with every blob found
    """
    dict_out: dict[str, Blob] = {}
    objects = list(obj_dir.glob('**/*'))
    for obj in objects:
        for blob_file in list(obj.glob('**/*')):
            dict_out[str(blob_file)] = read_blob(blob_file)
    return dict_out


def parse_commit(blob: Blob) -> Commit:
    """
    Parse commit blob
    :param blob: blob with commit type
    :return: parsed commit
    """
    assert blob.type_ == BlobType.COMMIT
    c = blob.content.decode('utf8').split('\n')
    tree_hash = c.pop(0).split(' ')
    tree_hash.pop(0)
    tree_hash = ' '.join(tree_hash)
    parents = c.pop(0).split(' ')
    parents.pop(0)
    parents = [' '.join(parents)]
    author = c.pop(0).split(' ')
    author.pop(0)
    author = ' '.join(author)
    committer = c.pop(0).split(' ')
    committer.pop(0)
    committer = ' '.join(committer)
    c.pop(0)
    message = '\n'.join(c)
    return Commit(tree_hash=tree_hash, parents=parents, author=author, committer=committer, message=message)


def parse_tree(blobs: dict[str, Blob], tree_root: Blob, ignore_missing: bool = True) -> Tree:
    """
    Parse tree blob
    :param blobs: all read blobs (by traverse_objects)
    :param tree_root: tree blob to parse
    :param ignore_missing: ignore blobs which were not found in objects directory
    :return: tree contains children blobs (or only part of them found in objects directory)
    NB. Children blobs are not being parsed according to type.
        Also nested tree blobs are not being traversed.
    """
    assert tree_root.type_ == BlobType.TREE
    tree = tree_root.content.decode('utf8').split('\n')
    children = {}
    for child in tree:
        if child:
            child = child.split(' ')
            if ignore_missing:
                try:
                    children[child[1]] = blobs[child[1]]
                except KeyError:
                    pass
            else:
                children[child[1]] = blobs[child[1]]
    return Tree(children=children)


def find_initial_commit(blobs: dict[str, Blob]) -> Commit:
    """
    Iterate over blobs and find initial commit (without parents)
    :param blobs: blobs read from objects dir
    :return: initial commit
    """


def search_file(blobs: dict[str, Blob], tree_root: Blob, filename: str) -> Blob:
    """
    Traverse tree blob (can have nested tree blobs) and find requested file,
    check if file was not found (assertion).
    :param blobs: blobs read from objects dir
    :param tree_root: root blob for traversal
    :param filename: requested file
    :return: requested file blob
    """


p: Path = Path(r'C:\Users\Ильнур\PycharmProjects\my_first_python_sandbox\03.1.FunctionsStringsIOHard\git_blob\objects')
blob_path = Path(r'C:\Users\Ильнур\PycharmProjects\my_first_python_sandbox\03.1.FunctionsStringsIOHard\git_blob\objects\1b\d9ee3785043bb23af69523af7a59b43d1fe533')
#s = zlib.decompress(p.read_bytes()).decode('utf8')
#print(read_blob(p))
print(parse_commit(read_blob(blob_path)))
