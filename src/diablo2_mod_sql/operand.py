from abc import ABC, abstractmethod


class Operand(ABC):
    args: list

    def __init__(self):
        self.args = []

    @abstractmethod
    def test(self, row: list) -> bool:
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
        def get_value(arg) -> str:
            if arg['type'] == 'operand':
                return str(arg['value'].test(row))
            elif arg['type'] == 'literal':
                return str(arg['value'])
            elif arg['type'] == 'column':
                return str(row[arg['value']])

        value1 = get_value(self.args[0])
        value2 = get_value(self.args[1])

        return value1 == value2


operand_map: dict[str, Operand.__class__] = {
    'and': AndOperand,
    'or': OrOperand,
    'eq': EqOperand
}
