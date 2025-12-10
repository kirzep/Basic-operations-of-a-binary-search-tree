from __future__ import annotations
from typing import Any

class TreeNode:
    """Узел бинарного дерева"""
    def __init__(self, key: int, value: Any):
        self.key: int = key
        self.value: Any = value
        self.left: TreeNode | None = None
        self.right: TreeNode | None = None

class BinarySearchTree:
    def __init__(self):
        self.root: TreeNode | None = None

    # --- Публичные методы ---

    def insert(self, key: int, value: Any) -> None:
        """Вставка новой пары ключ-значение"""
        if self.root is None:
            self.root = TreeNode(key, value)
        else:
            self._insert_recursive(self.root, key, value)

    def search(self, key: int) -> Any | None:
        """Поиск значения по ключу"""
        return self._search_recursive(self.root, key)

    def delete(self, key: int) -> None:
        """Удаление узла"""
        self.root = self._delete_recursive(self.root, key)

    def height(self) -> int:
        """Вычисление высоты дерева"""
        return self._height_recursive(self.root)

    def is_balanced(self) -> bool:
        """Проверка сбалансированности"""
        return self._is_balanced_recursive(self.root)

    # --- Внутренние методы ---

    def _insert_recursive(self, node: TreeNode, key: int, value: Any) -> None:
        if key < node.key:
            if node.left is None:
                node.left = TreeNode(key, value)
            else:
                self._insert_recursive(node.left, key, value)
        elif key > node.key:
            if node.right is None:
                node.right = TreeNode(key, value)
            else:
                self._insert_recursive(node.right, key, value)
        else:
            node.value = value

    def _search_recursive(self, node: TreeNode | None, key: int) -> Any | None:
        if node is None:
            return None
        if key == node.key:
            return node.value
        elif key < node.key:
            return self._search_recursive(node.left, key)
        else:
            return self._search_recursive(node.right, key)

    def _height_recursive(self, node: TreeNode | None) -> int:
        if node is None:
            return 0
        return 1 + max(self._height_recursive(node.left), self._height_recursive(node.right))

    def _is_balanced_recursive(self, node: TreeNode | None) -> bool:
        if node is None:
            return True
        
        left_h = self._height_recursive(node.left)
        right_h = self._height_recursive(node.right)

        if abs(left_h - right_h) <= 1:
            return self._is_balanced_recursive(node.left) and self._is_balanced_recursive(node.right)
        return False

    def _delete_recursive(self, node: TreeNode | None, key: int) -> TreeNode | None:
        if node is None:
            return None

        if key < node.key:
            node.left = self._delete_recursive(node.left, key)
        elif key > node.key:
            node.right = self._delete_recursive(node.right, key)
        else:
            # нашли узел
            
            # случай 1: нет детей или один ребенок
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            
            # случай 2: два ребенка, ищем замену справа
            min_larger_node = self._find_min(node.right)
            node.key = min_larger_node.key
            node.value = min_larger_node.value
            
            # удаляем дубликат замены
            node.right = self._delete_recursive(node.right, min_larger_node.key)
        
        return node

    def _find_min(self, node: TreeNode) -> TreeNode:
        current = node
        while current.left is not None:
            current = current.left
        return current

# --- Тесты ---

def run_tests():
    bst = BinarySearchTree()
    
    print("=== Тест 1: Базовая вставка и поиск ===")
    
    data = [
        (50, "Root"), (30, "Node 30"), (70, "Node 70"),
        (20, "Node 20"), (40, "Node 40"), (60, "Node 60"), (80, "Node 80")
    ]
    
    for k, v in data:
        bst.insert(k, v)
    
    # проверяем наличие и отсутствие
    print(f"Поиск 40: {bst.search(40)}")
    print(f"Поиск 99: {bst.search(99)}")
    print(f"Высота: {bst.height()}")
    print(f"Сбалансировано: {bst.is_balanced()}")

    print("\n=== Тест 2: Удаление ===")
    
    # удаление листа
    bst.delete(80)
    print(f"Удалили 80. Поиск: {bst.search(80)}")
    
    # добавляем узел для теста сложного удаления
    bst.insert(25, "Node 25") 
    
    # удаляем узел с одним потомком
    bst.delete(20)
    print(f"Удалили 20. Потомок 25 остался: {bst.search(25)}")

    # удаляем узел с двумя потомками
    bst.delete(30)
    print(f"Удалили 30. Проверка связности (ищем 40): {bst.search(40)}")

    print("\n=== Тест 3: Несбалансированное дерево ===")
    bst_linear = BinarySearchTree()
    # создаем "сосиску"
    for i in range(5):
        bst_linear.insert(i, f"Val {i}")
    
    print(f"Высота (должна быть 5): {bst_linear.height()}")
    print(f"Сбалансировано: {bst_linear.is_balanced()}")

if __name__ == "__main__":
    run_tests()