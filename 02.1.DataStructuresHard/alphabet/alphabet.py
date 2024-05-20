import enum
import itertools
import queue
from collections import defaultdict


class Status(enum.Enum):
    NEW = 0
    EXTRACTED = 1
    FINISHED = 2


def extract_alphabet(
        graph: dict[str, set[str]]
) -> list[str]:
    """
    Extract alphabet from graph
    :param graph: graph with partial order
    :return: alphabet
    """
    if len(graph) == 0:
        return []
    alphabet: list[str] = []
    status: dict[str, Status] = {letter: Status.NEW for letter in graph}
    q: queue = []
    possible_start = [letter for letter in graph if len(graph[letter]) == 0]
    for letter in possible_start:
        q.append(letter)
        status[letter] = Status.EXTRACTED
        while len(q) != 0:
            cur_letter = q.pop()
            if status[cur_letter] == Status.EXTRACTED:
                q.append(cur_letter)
                status[cur_letter] = Status.FINISHED
            for next_letter in graph[cur_letter]:
                if status[next_letter] == Status.NEW:
                    q.append(next_letter)
                    status[next_letter] = Status.EXTRACTED
                elif status[next_letter] == Status.FINISHED:
                    continue
                else:
                    return []

    return list(reversed(alphabet))


def build_graph(
        words: list[str]
) -> dict[str, set[str]]:
    """
    Build graph from ordered words. Graph should contain all letters from words
    :param words: ordered words
    :return: graph
    """
    gr: dict[str, set[str]] = defaultdict(set)
    gr = {letter: set() for letter in set(itertools.chain(*words))}

    for word_id in range(len(words) - 1):
        for sym_pair in zip(words[word_id], words[word_id + 1]):
            if sym_pair[0] != sym_pair[1]:
                gr[sym_pair[0]].add(sym_pair[1])
                break
    return dict(gr)


#########################
# Don't change this code
#########################

def get_alphabet(
        words: list[str]
) -> list[str]:
    """
    Extract alphabet from sorted words
    :param words: sorted words
    :return: alphabet
    """
    graph = build_graph(words)
    return extract_alphabet(graph)


#########################
