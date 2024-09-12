import sys,os


def exeBash(cmd):
    str = os.popen(cmd).read()
    l = str.split("\n")
    return l

class git():
    def __init__(self, path : str):
        assert os.path.exists(path)
        self.__cached_dir = []
        self.__path = path
        if self.__path[-1] != '/':
            self.__path += '/'
        #assert os.path.exists(self.__path+'.git')

    def __push_dir(self) -> None:
        cur_ = exeBash("pwd")[0]
        #print("cur:" + cur_)
        self.__cached_dir.append(cur_)
        os.chdir(self.__path)
        return None
    
    def __pop_dir(self) -> None:
        assert len(self.__cached_dir) > 0
        cur_ = self.__cached_dir.pop()
        os.chdir(cur_)
        return None
    
    def isRepo(self) -> bool:
        self.__push_dir()
        try:
            r = exeBash("git status")
            self.__pop_dir()
            return True
        except:
            self.__pop_dir()
            return False

    def isClean(self) -> bool:
        self.__push_dir()
        r = exeBash("git status")
        self.__pop_dir()
        last_line = r[-2]
        if last_line != "nothing to commit, working tree clean":
            return False
        return True
    
    def getCommit(self, short : bool = False) -> str:
        self.__push_dir()
        if short is True:
            r = exeBash("git rev-parse --short HEAD")
            len_ = 7
        else:
            r = exeBash("git rev-parse HEAD")
            len_ = 40
        self.__pop_dir()
        #print("commit:" + str(r[0]))
        return str(r[0])
    
    def getBranch(self) -> str:
        self.__push_dir()
        r = exeBash("git branch -vv")
        self.__pop_dir()
        for line in r:
            info = line.split(' ')
            if info[0] == '*':
                return info[1]
    
    def getRepoUrl(self) -> str:
        self.__push_dir()
        r = exeBash("git config --local --list")
        self.__pop_dir()
        for line in r:
            url = line.split('=')
            if url[0] == "remote.origin.url":
                return url[1]
        assert False

    def getRepoName(self) -> str:
        url = self.getRepoUrl()
        name = url.split('/')[-1]
        return name.split('.')[0]

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("arg1: path of repostory.")
        sys.exit(1)
    g = git(sys.argv[1])
    if g.isRepo() is True:
        print(g.isClean())
        print(g.getRepoName())
        print(g.getBranch())
        print(g.getCommit())
    else:
        print("NOT REPO")