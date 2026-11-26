import importlib.util

spec = importlib.util.spec_from_file_location("p3", "CS-4348.503-Project-3-irp220000.py")
p3 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p3)

with open("tree.idx", "wb") as f:
    p3.write_header(f, 1, 4)
    p3.write_node(f, p3.Node(1, 0, [20], [200], [2, 3] + [0] * 18))
    p3.write_node(f, p3.Node(2, 1, [5, 10], [50, 100]))
    p3.write_node(f, p3.Node(3, 1, [30, 40], [300, 400]))
