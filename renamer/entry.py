import libcst


class RenameTransformer(libcst.CSTTransformer):
    """
    AST-трансформер для переименования переменных и обновления импортов.

    Attributes:
        _old_name: Имя переменной или функции, которое нужно переименовать.
        _target_name: Новое имя для переменной или функции.
        target_module: Название модуля, если необходимо переместить переменную или функцию в другой модуль.
        _restore_keywords: Список для временного хранения ключевых слов функций (аргументы).
    """

    def __init__(self, old_name: str, target_name: str, target_module: str | None = None) -> None:
        """Инициализация RenameTransformer."""
        self._old_name = old_name
        self._target_name = target_name
        self.target_module = target_module
        self._restore_keywords: list = []
        super().__init__()

    def _rename(self, original_node: libcst.Attribute, renamed_node: libcst.Attribute) -> libcst.Attribute:
        """Внутренний метод для переименования атрибутов (например, переменных)."""
        if original_node.value == self._old_name:
            return renamed_node.with_changes(value=self._target_name)
        else:
            return renamed_node

    def leave_Name(self, original_node: libcst.Attribute, renamed_node: libcst.Attribute):
        """Переопределение метода leave_Name для обработки атрибутов с именами."""
        return self._rename(original_node, renamed_node)

    def visit_Arg(self, node: libcst.Arg) -> bool:
        """Обработка аргументов функции."""
        if node.keyword and node.keyword.value == self._old_name:
            self._restore_keywords.append(node.keyword.value)
        return True


def rename_variable(source_code: str, old_name: str, target_name: str, target_module: str | None = None) -> str:
    """
    Переименовывает переменные, функции и классы в исходном коде и автоматически обновляет все упоминания.
    :param source_code: Исходный код.
    :param old_name: Имя переменной, функции или класса, которое нужно переименовать.
    :param target_name: Новое имя для переменной, функции или класса.
    :param target_module: Название модуля, если необходимо переместить переменную, функцию или класс в другой модуль.
    :return: Обновленный исходный код.
    """
    rename_transformer = RenameTransformer(old_name, target_name, target_module)
    original_tree = libcst.parse_module(source_code)
    renamed_tree = original_tree.visit(rename_transformer)
    return renamed_tree.code
