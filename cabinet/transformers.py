import re


def make_blocks(string: str) -> dict:
    return {match[0].strip(): make_blocks(match[2])
            for match in re.findall(rf"(( *).+)((\n\2 +.*)*)(?!\n\2 +)", string)}


class Transformers:
    transformers = []

    @classmethod
    def apply_all(cls, blocks: dict):
        done = False

        while not done:
            prev = blocks
            for transformer in cls.transformers:
                blocks = transformer.apply(blocks)

            done = blocks == prev

        return blocks


class Transformer:
    recur = True
    once = False

    def __init_subclass__(cls, **kwargs):
        Transformers.transformers.append(cls)

    @classmethod
    def apply(cls, blocks: dict) -> dict:
        done = False

        while not done:
            if cls.recur:
                for header, body in blocks.items():
                    blocks[header] = cls.apply(body)

            transformed = {}
            for header, body in blocks.items():
                if cls.can_transform(header, body):
                    transformed |= cls.transform(header, body)

                else:
                    transformed |= {header: body}

            done = transformed == blocks or cls.once
            blocks = transformed

        return blocks

    @classmethod
    def can_transform(cls, header: str, body: dict) -> bool:
        raise NotImplementedError

    @classmethod
    def transform(cls, header: str, body: dict) -> dict:
        raise NotImplementedError


class WithKeyword(Transformer):
    @classmethod
    def can_transform(cls, header: str, body: dict) -> bool:
        return " with " in header and not re.search(r"function \S+ with (block|entity|storage)", header)

    @classmethod
    def transform(cls, header: str, body: dict) -> dict:
        command, directive = re.split(r" with\s?", header, maxsplit=2)
        return {f"execute {directive or 'run'}": {f"{command} {line}": lines for line, lines in body.items()}}


class RandomFrom(Transformer):
    @classmethod
    def can_transform(cls, header: str, body: dict) -> bool:
        return header.endswith(" random from")

    @classmethod
    def transform(cls, header: str, body: dict) -> dict:
        return {re.sub(r" random from", " run", header): {
            f"execute store result score %%local rand run random value 1..{len(body)}": {},
            "execute if score %%local rand matches": {
                f"{i + 1} run {line}": lines for i, (line, lines) in enumerate(body.items())
            }
        }}


class ScheduleInline(Transformer):
    @classmethod
    def can_transform(cls, header: str, body: dict) -> bool:
        return bool(re.search(r"^schedule (?!function)\S+ (append|replace) (?!run)\S+", header))

    @classmethod
    def transform(cls, header: str, body: dict) -> dict:
        params, inline = re.search(r"^schedule (\S+ \S+) (.*)", header).groups()
        return {f"schedule function %%block {params} run": {inline: body}}


class DistributiveBlock(Transformer):
    @classmethod
    def can_transform(cls, header: str, body: dict) -> bool:
        return not header.startswith("%") and not header.endswith(" run") and body

    @classmethod
    def transform(cls, header: str, body: dict) -> dict:
        return {f"{header} {line}": lines for line, lines in body.items()}


class Decorators(Transformer):
    @classmethod
    def can_transform(cls, header: str, body: dict) -> bool:
        return header.startswith("%") and body

    @classmethod
    def transform(cls, header: str, body: dict) -> dict:
        decorator, params = re.search(r"^(%\w+)\s?(.*)$", header).groups()

        if params:
            return {decorator: {params: {}, **body}}

        else:
            return {header: body}
