# import symbols
from Librarian.regex import *
from Librarian.regex import regex

class RegEx():
    def __init__(self, regex):
        self.regex = regex

    def __str__(self):
        return self.regex

    def __repr__(self):
        return "RegEx(" + self.regex + ")"

    def parsex(self):
        result = []
        for c in self.regex:
            result.append(RegExTree(RegEx.char_to_root(c), []))
        return RegEx.parse(result)

    @staticmethod
    def parse(result):
        while RegEx.contains_parenthesis(result):
            result = RegEx.process_parenthesis(result)
        while RegEx.contains_star(result):
            result = RegEx.process_star(result)
        while RegEx.contains_plus(result):
            result = RegEx.process_plus(result)
        while RegEx.contains_question(result):
            result = RegEx.process_question(result)
        while RegEx.contains_concat(result):
            result = RegEx.process_concat(result)
        while RegEx.contains_altern(result):
            result = RegEx.process_altern(result)
        if len(result) > 1:
            raise Exception("Result size can't exceed 1")
        return RegEx.remove_protection(result[0])

    @staticmethod
    def char_to_root(c):
        switcher = {
            ".": symbols.DOT,
            "*": symbols.STAR,
            "+": symbols.PLUS,
            "?": symbols.QUESTION,
            "|": symbols.ALTERN,
            "(": symbols.LEFT_PARENTHESIS,
            ")": symbols.RIGHT_PARENTHESIS,
            "default": ord(c)
        }
        if c in switcher:
            return switcher.get(c)
        return switcher.get("default")

    @staticmethod
    def contains_parenthesis(trees):
        for t in trees:
            if t.root == symbols.LEFT_PARENTHESIS or t.root == symbols.RIGHT_PARENTHESIS:
                return True
        return False

    @staticmethod
    def process_parenthesis(trees):
        result = []
        found = False
        for t in trees:
            if not found and t.root == symbols.RIGHT_PARENTHESIS:
                done = False
                content = []
                while not done and len(result) != 0:
                    if result[len(result) - 1].root == symbols.LEFT_PARENTHESIS:
                        done = True
                        result.pop()
                    else:
                        content.insert(0, result.pop())
                if not done:
                    raise Exception("Error while processing parenthesis")
                found = True
                sub_trees = [RegEx.parse(content)]
                result.append(RegExTree(symbols.PROTECTION, sub_trees))
            else:
                result.append(t)
        if not found:
            raise Exception("Matching parenthesis not found")
        return result

    @staticmethod
    def contains_star(trees):
        for t in trees:
            if t.root == symbols.STAR and len(t.sub_trees) == 0:
                return True
        return False

    @staticmethod
    def process_star(trees):
        result = []
        found = False
        for t in trees:
            if not found and t.root == symbols.STAR and len(t.sub_trees) == 0:
                if len(result) == 0:
                    raise Exception("Error while processing Star")
                found = True
                sub_trees = [result.pop()]
                result.append(RegExTree(symbols.STAR, sub_trees))
            else:
                result.append(t)
        return result

    @staticmethod
    def contains_plus(trees):
        for t in trees:
            if t.root == symbols.PLUS and len(t.sub_trees) == 0:
                return True
        return False

    @staticmethod
    def process_plus(trees):
        result = []
        found = False
        for t in trees:
            if not found and t.root == symbols.PLUS and len(t.sub_trees) == 0:
                if len(result) == 0:
                    raise Exception("Error while processing Plus")
                found = True
                sub_trees = [result.pop()]
                result.append(RegExTree(symbols.PLUS, sub_trees))
            else:
                result.append(t)
        return result

    @staticmethod
    def contains_question(trees):
        for t in trees:
            if t.root == symbols.QUESTION and len(t.sub_trees) == 0:
                return True
        return False

    @staticmethod
    def process_question(trees):
        result = []
        found = False
        for t in trees:
            if not found and t.root == symbols.QUESTION and len(t.sub_trees) == 0:
                if len(result) == 0:
                    raise Exception("Error while processing Question")
                found = True
                sub_trees = [result.pop()]
                result.append(RegExTree(symbols.QUESTION, sub_trees))
            else:
                result.append(t)
        return result

    @staticmethod
    def contains_concat(trees):
        already_found = False
        for t in trees:
            if not already_found and t.root != symbols.ALTERN:
                already_found = True
                continue
            if already_found:
                if t.root != symbols.ALTERN:
                    return True
                else:
                    already_found = False
        return False

    @staticmethod
    def process_concat(trees):
        result = []
        found = False
        already_found = False
        for t in trees:
            if not found and not already_found and t.root != symbols.ALTERN:
                already_found = True
                result.append(t)
                continue
            if not found and already_found and t.root == symbols.ALTERN:
                already_found = False
                result.append(t)
                continue
            if not found and already_found and t.root != symbols.ALTERN:
                found = True
                sub_trees = [result.pop(), t]
                result.append(RegExTree(symbols.CONCAT, sub_trees))
            else:
                result.append(t)
        return result

    @staticmethod
    def contains_altern(trees):
        for t in trees:
            if t.root == symbols.ALTERN and len(t.sub_trees) == 0:
                return True
        return False

    @staticmethod
    def process_altern(trees):
        result = []
        left_operand = None
        found = False
        done = False
        for t in trees:
            if not found and t.root == symbols.ALTERN and len(t.sub_trees) == 0:
                if len(result) == 0:
                    raise Exception("Error while processing Altern")
                found = True
                left_operand = result[len(result) - 1]
                result.pop()
                continue
            if found and not done:
                if left_operand is None:
                    raise Exception("Left part is None")
                done = True
                sub_trees = [left_operand, t]
                result.append(RegExTree(symbols.ALTERN, sub_trees))
            else:
                result.append(t)
        return result

    @staticmethod
    def remove_protection(tree):
        if tree.root == symbols.PROTECTION and len(tree.sub_trees) != 1:
            raise Exception("Protection error")
        if len(tree.sub_trees) == 0:
            return tree
        if tree.root == symbols.PROTECTION:
            return RegEx.remove_protection(tree.sub_trees[0])
        sub_trees = []
        for t in tree.sub_trees:
            sub_trees.append(RegEx.remove_protection(t))
        return RegExTree(tree.root, sub_trees)

class RegExTree():
    def __init__(self, root, sub_trees):
        self.root = root
        self.sub_trees = sub_trees

    def __str__(self):
        return repr(self)

    def __repr__(self):
        if len(self.sub_trees) == 0:
            return self.root_to_string()
        result = self.root_to_string() + "(" + repr(self.sub_trees[0])
        for i in range(1, len(self.sub_trees)):
            result += ", " + repr(self.sub_trees[i])
        return result + ")"

    def root_to_string(self):
        switcher = {
            symbols.CONCAT: "",
            symbols.DOT: ".",
            symbols.STAR: "*",
            symbols.PLUS: "+",
            symbols.QUESTION: "?",
            symbols.ALTERN: "|",
            symbols.LEFT_PARENTHESIS: "(",
            symbols.RIGHT_PARENTHESIS: ")"
        }
        if self.root in switcher:
            return switcher.get(self.root)
        return chr(self.root)

if __name__ == "__main__":
    rt = RegExTree(symbols.ALTERN, [RegExTree(RegEx.char_to_root("a"), []), RegExTree(symbols.CONCAT, [RegExTree(RegEx.char_to_root("b"), []), RegExTree(symbols.STAR, [RegExTree(RegEx.char_to_root("c"), [])])])])
    print("to_string >> ", rt)

    r = RegEx("a|bc*")
    # r = RegEx("(a|b)c*")
    res = r.parsex()
    print("parsing   >> ", res)
