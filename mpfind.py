import os
from multiprocessing import Pool


def find_dirs(folders=['.'], maxdepth=2):
    '''    Get list of directories to a certain depth.    '''

    dirlist = []

    # maxdepthlist is the list of files, dirs, links, etc that are in the first maxdepth
    # levels. Can return these so that we don't need to find them again later on.
    maxdepthlist = []
    for item in folders:
        for root, dirs, files in os.walk(item, topdown=True, followlinks=False):
            for name in files:
                maxdepthlist.append(f'{root}/{name}')
            for name in dirs:
                maxdepthlist.append(f'{root}/{name}')
                dirlist.append(f'{root}/{name}')
            if root.count(os.sep) - item.count(os.sep) == maxdepth - 1:
                del dirs[:]
    return (maxdepthlist, dirlist)


def sort_dirs(dirlist):
    '''    Sort dirlist into two lists. Root nodes don't need to be searched, only leaf nodes.    '''

    traverse_list = []
    dirlist.sort()

    for i in range(len(dirlist)-1):
        if not f'{dirlist[i]}/' in dirlist[i+1]:
            traverse_list.append(dirlist[i])

    # Add last item since there's nothing for it to compare against
    traverse_list.append(dirlist[-1])

    return traverse_list


def find(dir):
    '''    Function that walks directory tree    '''
    tmp = []
    if os.path.islink(dir):
        tmp.append(dir)
    else:
        for root, dirs, files in os.walk(dir, topdown=True, followlinks=False):
            for name in files:
                tmp.append(f'{root}/{name}')
            for name in dirs:
                tmp.append(f'{root}/{name}')
    return tmp


def printlist2(arr, updatelist):
    if type(arr) is not list:
        updatelist.add(arr)
        return
    else:
        for i in arr:
            printlist2(i, updatelist)


if __name__ == "__main__":

    #
    maxdepthlist, dirlist = find_dirs()
    c = sort_dirs(dirlist)

    mylist = set()

    with Pool(processes=4) as pool:
        tmp = pool.map(find, c)

    for i in maxdepthlist:
        mylist.add(i)

    for i in tmp:
        printlist2(i, mylist)

    l = list(mylist)
    l.sort()
    for i in l:
        print(i)
