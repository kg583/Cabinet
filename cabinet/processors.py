import json
import re


class Processors:
    processors = []

    @classmethod
    def apply_all(cls, string: str):
        for processor in cls.processors:
            if processor.ignores:
                ignores = re.findall(processor.ignores, string)
                string = re.sub(processor.ignores, "%%ignore", string)

            else:
                ignores = []

            string = processor.apply(string)

            for ignored in ignores:
                string = string.replace("%%ignore", ignored, 1)

        return string


class Processor:
    # String literals
    ignores = r"\"[^\"]*\""

    @classmethod
    def apply(cls, string: str) -> str:
        raise NotImplementedError

    def __init_subclass__(cls, **kwargs):
        Processors.processors.append(cls)


class RemoveWhitespace(Processor):
    @classmethod
    def apply(cls, string: str) -> str:
        return "\n".join(line for line in map(str.rstrip, string.split("\n")) if line)


class RemoveComments(Processor):
    @classmethod
    def apply(cls, string: str) -> str:
        return "\n".join(line for line in string.split("\n") if not re.search(r"^\s*#", line))


class RemoveParentheses(Processor):
    @classmethod
    def apply(cls, string: str) -> str:
        return re.sub(r"\s*[()]\s*", " ", string)


class ContinueLines(Processor):
    @classmethod
    def apply(cls, string: str) -> str:
        return re.sub(r"\\\n\s*", "", string)


class DedentDecorators(Processor):
    @classmethod
    def apply(cls, string: str) -> str:
        return re.sub(r"^(?=[^%])", "\t", string, flags=re.MULTILINE)


class TabsToSpaces(Processor):
    @classmethod
    def apply(cls, string: str) -> str:
        return string.replace("\t", "  ")


class ResolveNames(Processor):
    @classmethod
    def apply(cls, string: str) -> str:
        return re.sub(r"(?<=\W)(:+)(?=\w)",
                      lambda match: f"%%namespace.{'%%function.' if len(match[1]) > 1 else ''}", string)


class ReplaceSelectors(Processor):
    @classmethod
    def apply(cls, string: str) -> str:
        return re.sub(r"@([\w%.]+)(\[)?",
                      lambda match: match[0] if match[1] in ("a", "e", "p", "r", "s")
                      else f"@e[tag={match[1]}{',' if match[2] else ']'}", string)


class ImplicitDummy(Processor):
    @classmethod
    def apply(cls, string: str) -> str:
        return re.sub(r" objectives add \S+$", lambda match: f"{match[0]} dummy", string)


class ExtraneousWith(Processor):
    @classmethod
    def apply(cls, string: str) -> str:
        return re.sub(r" with (?=\W)", " ", string)


class CalledKeyword(Processor):
    @classmethod
    def apply(cls, string: str) -> str:
        return re.sub(r" called (\S+)", lambda match: f" run tag @s add {match[1]}", string)


class RevokeKeyword(Processor):
    @classmethod
    def apply(cls, string: str) -> str:
        return re.sub(r"^(\s)*revoke$", lambda match: f"{match[1]}advancement revoke @s only %%path", string,
                      flags=re.MULTILINE)


class FlattenJSON(Processor):
    ignores = None

    @staticmethod
    def is_valid_json(string: str) -> bool:
        try:
            json.JSONDecoder().raw_decode(string)
            return True

        except json.JSONDecodeError:
            pass

    @classmethod
    def apply(cls, string: str) -> str:
        out = ""

        lines = iter(string.split("\n"))
        for line in lines:
            if match := re.match(r"(%\S+ )?(\{.*)", line):
                out += match[1]

                block = match[2]
                while not cls.is_valid_json(block):
                    block += next(lines).strip()

                out += block + "\n"

            else:
                out += line + "\n"

        return out
