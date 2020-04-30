from fnmatch import fnmatch
import os
from sys import argv


def find_files(folder='.', extension='*.png'):
    files = list()
    for dir_path, dir_names, filenames in os.walk(folder):
        for filename in filenames:
            if fnmatch(filename, extension):
                files.append(os.path.join(dir_path, filename))
    return files


def move_pngs(source, destination):
    pngs = find_files(source)
    failed = list()
    for png in pngs:
        basename = os.path.basename(png)
        if basename[0:10] == 'Screenshot':
            try:
                date_folder = os.path.join(destination, basename.split()[1])
                if not os.path.exists(date_folder):
                    os.mkdir(date_folder)
                os.rename(png, os.path.join(date_folder, basename))
            except OSError as e:
                print(e)
                failed.append(png)
    if len(failed) > 0:
        return False, failed
    else:
        return True, None


if __name__ == '__main__':
    if len(argv) != 3:
        print(f"Usage: {argv[0]} <source> <destination>")
    else:
        res, files = move_pngs('.', 'PNGs/')
        if not res:
            files = '\n'.join(files)
            print(f"These files failed: {files}")