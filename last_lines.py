import io


def last_lines(path: str, chunk_size: int = io.DEFAULT_BUFFER_SIZE):
    """
    Yields lines from a file in reverse order, similar to the `tac` command.

    This function reads the file in binary mode in chunks from end to start and
    handling of multi-byte UTF-8 characters.
    """
    with open(path, 'rb') as f:
        f.seek(0, io.SEEK_END)
        position = f.tell()

        # ignore last line if empty (user pressed enter)
        if position > 0:
            f.seek(position - 1)
            if f.read(1) == b'\n':
                position -= 1

        buffer = b''

        while position > 0:
            read_size = min(chunk_size, position)
            position -= read_size
            f.seek(position)

            buffer = f.read(read_size) + buffer

            while b'\n' in buffer:
                parts = buffer.rsplit(b'\n', 1)
                line = parts[1]
                buffer = parts[0]

                yield line.rstrip(b'\r').decode('utf-8') + '\n'

        if buffer:
            yield buffer.rstrip(b'\r').decode('utf-8') + '\n'
