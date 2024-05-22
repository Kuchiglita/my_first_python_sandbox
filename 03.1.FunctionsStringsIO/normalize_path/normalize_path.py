def normalize_path(path: str) -> str:
    """
    :param path: unix path to normalize
    :return: normalized path
    """
    is_root: bool = (path and path[0] == '/')
    path_ = path.split('/')
    stack = []
    for part in path_:
        if not part:
            continue
        if part == '.':
            continue
        if part == '..':
            if stack and stack[-1] != '..':
                stack.pop()
            else:
                if not is_root:
                    stack.append(part)
        else:
            stack.append(part)
    if is_root:
        return '/' + '/'.join(stack)
    if not stack:
        return '.'
    else:
        return '/'.join(stack)
