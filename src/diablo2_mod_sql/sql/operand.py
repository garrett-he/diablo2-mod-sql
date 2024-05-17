from abc import ABC, abstractmethod


def get_value(row, arg) -> str:
    if arg['type'] == 'operand':
        return arg['value'].test(row)
    elif arg['type'] == 'literal':
        return arg['value']
    elif arg['type'] == 'column':
        return row[arg['value']]


class Operand(ABC):
    args: list

    def __init__(self):
        self.args = []

    @abstractmethod
    def test(self, row: list) -> bool:  # pragma: no cover
        ...


class AndOperand(Operand):
    def test(self, row: list) -> bool:
        result = True

        for arg in self.args:
            if arg['type'] == 'operand':
                result = result and arg['value'].test(row)
            elif arg['type'] == 'literal':
                result = result and arg['value']

        return result


class OrOperand(Operand):
    def test(self, row: list) -> bool:
        result = False

        for arg in self.args:
            if arg['type'] == 'operand':
                result = result or arg['value'].test(row)
            elif arg['type'] == 'literal':
                result = result or arg['value']

        return result


class EqOperand(Operand):
    def test(self, row: list) -> bool:
        value1 = get_value(row, self.args[0])
        value2 = get_value(row, self.args[1])

        return value1 == value2


class EchoOperand(Operand):  # pragma: no cover
    def test(self, row: list) -> any:
        if len(self.args) != 1:
            raise ValueError(self.args)

        arg = self.args[0]
        if arg['type'] == 'operand':
            return arg['value'].test(row)
        elif arg['type'] == 'literal':
            return arg['value']
        elif arg['type'] == 'column':
            return row[arg['value']]
        else:
            raise ValueError(arg)


class InOperand(Operand):
    def test(self, row: list) -> bool:
        value1 = get_value(row, self.args[0])
        value2 = get_value(row, self.args[1])

        return value1 in value2


operand_map: dict[str, Operand.__class__] = {
    'and': AndOperand,
    'or': OrOperand,
    'eq': EqOperand,
    'echo': EchoOperand,
    'in': InOperand
}
