from learntools.core import *
from learntools.core.problem import injected

class ExerciseFormatTutorial(CodingProblem):
    _var = 'color'
    _hint = "他喜欢的颜色和 VSCode 图标颜色差不多... 可能你只需要一个赋值语句，赋值一个单词就够了？"
    _solution = CS('color = "blue"')
    def check(self, color):
        assert color.lower() == "blue"

    @property
    def _correct_message(self):
        history = self._view.interactions
        if history['hint'] == 0 and history['solution'] == 0:
            return ("哇！你是怎么猜对的？！"
                    "emm……居然还没有依靠提示和答案完成的！真厉害！"
                    "相信你一定能够完成下一个题目！"
                    )
        return ''

    def _failure_message(self, var, actual, expected):
        if (
                actual.strip().lower() != 'blue'
            ):
            return "真奇怪呢，很接近了，看看大小写？"
        return ("{} 不是他最喜欢的颜色"
                "也许你需要一点帮助？").format(actual)


class CircleArea(EqualityCheckProblem):
    _vars = ['radius', 'area']
    _expected = [3/2, (3/2)**2 * 3.14159]

    _hint = "a 的 b 次方，或许是 `a ** b`?"
    _solution = CS('radius = diameter / 2',
            'area = pi * radius ** 2')

class VariableSwap(CodingProblem):
    _vars = ['a', 'b']

    _hint = "尝试使用第三个变量，临时接住一个值？"
    _solution = """最简单的方法是使用第三个变量。这是一个常见的模式，你可能在其他语言中也见过。例如，如果我们想要交换 `a` 和 `b` 的值，我们可以这样做：

    tmp = a
    a = b
    b = tmp

如果你想要更简洁的写法，Python 允许你这样做：

    a, b = b, a

这是 Python 的魔法，叫做“tuple unpacking”。这行代码的右边创建了一个元组 `(b, a)`，然后将这个元组“解包”到左边的变量中。

什么是解包？我们会在后面的 Python 进阶录播课中讲到～"""

    @injected
    def store_original_ids(self, a, b):
        self.id_a = id(a)
        self.id_b = id(b)

    def check(self, a, b):
        ida = id(a)
        idb = id(b)
        orig_values = [1, 2, 3], [3, 2, 1]
        if ida == self.id_b and idb == self.id_a:
            return
        assert not (ida == self.id_a and idb == self.id_b), ("`a`, `b` 仍然"
                " 没有变化")
        orig_ids = (self.id_a, self.id_b)
        if (b, a) == orig_values:
            # well this is ridiculous in its verbosity
            assert False, (
        "我猜，你是不是这么写的！\n"
        "```python\na = [3, 2, 1]\nb = [1, 2, 3]```\n?\n"
        "被我抓到了吧！为什么不能这么写？\n"
        "1. 你是在事先已知变量值的情况下交换的。如果你不知道变量值，怎么办？\n"
        "2. 你的代码实际上让 `a` 指向了一个 *新的* 对象（只不过其值与 `b` 之前的值相同），`b` 也是如此。为什么呢？考虑下面的代码...\n"
        "```python\n"
        "a = [1, 2, 3]\n"
        "b = [1, 2, 3]```\n"
        "实际上这个代码与下面这个完全不同\n"
        "```python\n"
        "a = [1, 2, 3]\n"
        "b = a```\n"
        "在第二个代码片段中，`a` 和 `b` 指向同一个对象。在第一个代码片段中，`a` 和 `b` 指向不同的对象，只不过这两个对象的值是相同的。这个区别可能看起来只是一种哲学上的区别，但是当我们开始 *修改* 对象时，这个区别就变得很重要了。在第二种情况下，如果我们运行 `a.append(4)`，那么 `a` 和 `b` 都会变成 `[1, 2, 3, 4]`。如果我们在第一个情况下运行 `a.append(4)`，那么 `a` 就会变成 `[1, 2, 3, 4]`，但是 `b` 仍然是 `[1, 2, 3]`。"
        )
        assert ida in orig_ids, (
                "`a` 似乎被赋予了一个奇怪的值（它的 id 已经改变，但不是 `b` 的 id）"
        )
        assert idb in orig_ids, (
                "`b` 似乎被赋予了一个奇怪的值（它的 id 已经改变，但不是 `a` 的 id）"
        )
        assert ida != idb, "`b` 和 `a` 相同了! 都是 `{}`".format(
                repr(a))
        assert False, "你的代码写的太奇怪了，建议你去 Piazza 问一问（"

# It's an interesting question whether to make these parens questions checkable.
# Making them non-checkable for now.
class ArithmeticParensEasy(ThoughtExperiment):
    _hint = ('还记得我们的运算符顺序吗？ `**` > 正负号 (`+x`, `-x`) > [`*`, `/`, `//`, `%`] > [`+`, `-`]'
            ' Python 会先计算 3 除以 2，然后用 5 减去这个结果。'
            ' 你需要添加括号来强制它先执行减法。')
    _solution = CS("(5 - 3) // 2")

class ArithmeticParensHard(ThoughtExperiment):
    _hint = '你可能需要不止一对括号'
    _solution = "`(8 + 3 + 2) * (1 - 1)` 是其中的一个解法"

ArithmeticParens = MultipartProblem(ArithmeticParensEasy, ArithmeticParensHard)

qvars = bind_exercises(globals(), [
    ExerciseFormatTutorial,
    CircleArea,
    VariableSwap,
    ArithmeticParens,
    ],
    start=0,
    )
__all__ = list(qvars)
