
import os
import sys

TOPDIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCDIR = os.path.join(TOPDIR, "doc")
DOTDIR = os.path.join(DOCDIR, "dot")
GRAPHDIR = os.path.join(DOCDIR, "graph")


def get_file_paths_from(base_dir: str):
    res = []
    for base, _, files in os.walk(base_dir):
        res += [os.path.join(base, f) for f in files]
    return res


def without_suffix(path: str):
    return "".join(path.split(".")[:-1])


def src_to_dst_file(src: str):
    dst = src.replace(DOTDIR, GRAPHDIR)
    dst = without_suffix(dst) + ".png"
    return dst


def main():
    print("Parsing dot files")
    src_files = get_file_paths_from(DOTDIR)
    src_files = [f for f in src_files if f.endswith(".dot")]
    print("Parsed dot files: %s" % src_files)

    os.system("mkdir -p %s" % GRAPHDIR)

    print("Outputting png files")
    for src in src_files:
        dst = src_to_dst_file(src)
        os.system("dot -o%s -Tpng %s" % (dst, src))

    print("Done")


if __name__ == "__main__":
    main()
