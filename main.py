# import matplotlib.pyplot as plt
# import numpy as np
#
# #
# # def draw_a(x_start):
# #     x1 = np.linspace(x_start, x_start + 1, 100)
# #     x2 = np.linspace(x_start + 1, x_start + 2, 100)
# #     x3 = np.linspace(x_start + 0.5, x_start + 1.5)
# #     return (x1 + 10, 2 * x1), (x2, -2 * x2), (x3, np.ones_like(x3))
#
# #
# # if __name__ == '__main__':
# #     for (x, y) in draw_a(-5):
# #         plt.plot(x, y)
# #     plt.show()
#
# if __name__ == '__main__':
#     a = '   '
#
#


import os
import pathlib

PIPE = "│"
ELBOW = "└──"
TEE = "├──"
PIPE_PREFIX = "│   "
SPACE_PREFIX = "    "


class _TreeGenerator:
    def __init__(self, root_dir):
        self._root_dir = pathlib.Path(root_dir)
        self._tree = []

    def build_tree(self):
        self._tree_head()
        self._tree_body(self._root_dir)
        return self._tree

    def _tree_head(self):
        self._tree.append(f"{self._root_dir}{os.sep}")
        self._tree.append(PIPE)

    def _add_directory(
        self, directory, index, entries_count, prefix, connector
    ):
        self._tree.append(f"{prefix}{connector} {directory.name}{os.sep}")
        if index != entries_count - 1:
            prefix += PIPE_PREFIX
        else:
            prefix += SPACE_PREFIX
        self._tree_body(
            directory=directory,
            prefix=prefix,
        )
        self._tree.append(prefix.rstrip())

    def _tree_body(self, directory, prefix=""):
        entries = directory.iterdir()
        entries = sorted(entries, key=lambda entry: entry.is_file())
        entries_count = len(entries)
        for index, entry in enumerate(entries):
            connector = ELBOW if index == entries_count - 1 else TEE
            if entry.is_dir():
                self._add_directory(
                    entry, index, entries_count, prefix, connector
                )
            else:
                self._add_file(entry, prefix, connector)

    def _add_file(self, file, prefix, connector):
        self._tree.append(f"{prefix}{connector} {file.name}")

    def _prepare_entries(self, directory):
        entries = directory.iterdir()
        if self._dir_only:
            entries = [entry for entry in entries if entry.is_dir()]
            return entries
        entries = sorted(entries, key=lambda entry: entry.is_file())
        return entries


class DirectoryTree:
    def __init__(self, root_dir, dir_only=False):
        self._generator = _TreeGenerator(root_dir)

    def generate(self):
        tree = self._generator.build_tree()
        for entry in tree:
            print(entry)


if __name__ == '__main__':
    d = DirectoryTree('./simple')
    d.generate()
