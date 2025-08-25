import io


def last_lines(path: str, chunk_size: int = io.DEFAULT_BUFFER_SIZE):
    """
    Yields lines from a file in reverse order, similar to the `tac` command.

    This function reads the file in binary mode in chunks from end to start,
    ensuring memory efficiency and correct handling of multi-byte UTF-8 characters.
    """
    with open(path, 'rb') as f:
        f.seek(0, io.SEEK_END)  # starting from the end
        position = f.tell()

        # ignorando quando o usuario pressiona enter depois da ultima palavra ()
        # isso é diferente de ter uma linha totalmente em branco (enter + enter)
        # simulando o comportamento do funcao tac
        if position > 0:
            f.seek(position - 1)
            if f.read(1) == b'\n':  # leio o ultimo byte pra ver se é uma linha vazia
                position -= 1  # se sim, ignoro esse byte

        buffer = b''

        while position > 0:  # vamos atualizando a posicao com o que ja foi lido
            read_size = min(chunk_size, position)
            position -= read_size
            f.seek(position)

            buffer = f.read(read_size) + buffer

            while b'\n' in buffer:
                parts = buffer.rsplit(b'\n', 1)
                line = parts[1]
                buffer = parts[0]

                yield line.rstrip(b'\r').decode('utf-8') + '\n'  # remove b'\r'

        # yields a primeira linha do arquivo (b'one\ntwo\nthree')
        if buffer:
            yield buffer.rstrip(b'\r').decode('utf-8') + '\n'
