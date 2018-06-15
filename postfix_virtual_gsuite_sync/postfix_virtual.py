from collections import defaultdict

from rex import rex


ALIAS_RE = rex('/^(?P<alias>[a-zA-Z0-9_.@-]+)(?:[\s]+)(?P<target>[a-zA-Z0-9_.@-]+),?.*?$/')


def parse_virtual_file(virtual_file, target_domain=''):
    result = defaultdict(set)
    for line in virtual_file:
        line: str = line.strip()
        if line.startswith('#'):
            continue
        match = ALIAS_RE(line)
        if match:
            target = match['target']
            if "@" not in target:
                target = f"{target}@{target_domain}"
            result[target].add(match['alias'])

    return result
