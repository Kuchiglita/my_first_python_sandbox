import typing as tp
from heapq import heapify, heappop, heappush
import io


def merge(input_streams: tp.Sequence[tp.IO[bytes]], output_stream: tp.IO[bytes]) -> None:
    """
    Merge input_streams in output_stream
    :param input_streams: list of input streams. Contains byte-strings separated by "\n". Nonempty stream ends with "\n"
    :param output_stream: output stream. Contains byte-strings separated by "\n". Nonempty stream ends with "\n"
    :return: None
    """
    n = len(input_streams)
    stack: list[tuple[int, tp.IO[bytes]]] = []
    for stream in input_streams:
        line = stream.readline()
        if line:
            heappush(stack, (int(line.decode("utf-8")), stream))
    heapify(stack)

    while stack:
        val, stream = heappop(stack)
        output_stream.write(bytes(f"{val}\n", "utf8"))
        s = stream.readline()
        if s:
            heappush(stack, (int(s.decode("utf-8")), stream))


list_ = [1, 5, 7, -1]
input_stream = io.BytesIO(b"".join(bytes(f"{value}\n", "utf8") for value in list_))
output_stream = io.BytesIO()
merge([input_stream], output_stream)
