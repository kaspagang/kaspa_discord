from __future__ import annotations
from typing import Union


class version(object):
    
    _exclude = set(['x', 'xx', 'X', 'XX'])
    
    @classmethod
    def parse_from_string(cls, string : str) -> version:
        split_string = string.rsplit('.')
        major, minor, bug_fix = tuple(split_string[-3:])
        major = int(''.join(filter(lambda x : str.isdigit(x) or x in cls._exclude, major)))
        minor = int(''.join(filter(lambda x : str.isdigit(x) or x in cls._exclude, minor)))
        bug_fix = int(''.join(filter(lambda x : str.isdigit(x) or x in cls._exclude, bug_fix)))
        return version(major, minor, bug_fix)
    
    
    def __init__(self, major: Union[int, str] = 'xx', minor: Union[int, str] =  
                 'xx', bug_fix: Union[int, str] = 'xx') -> None:
        self.major = major
        self.minor = minor
        self.bug_fix = bug_fix
        assert all(v in self._exclude or isinstance(v, int) for v in [self.major, self.minor, self.bug_fix]) #only allow numerival and 'x' or 'XX notation
    
    
    def __eq__(self, comp: object) -> bool:
        if (self.major == comp.major  or set([self.major ,comp.major]) & self._exclude) and (
            self.minor == comp.minor or set([self.minor ,comp.minor]) & self._exclude) and (
            self.bug_fix == comp.bug_fix or set([self.bug_fix ,comp.bug_fix]) & self._exclude):
            return True
        else:
            return False
    
    def __lt__(self, comp: object) -> bool:
        if set([self.major ,comp.major]) & self._exclude or self.major > comp.major:
            return True
        elif set([self.minor ,comp.minor]) & self._exclude or self.minor > comp.minor:
            return True
        elif set([self.bug_fix ,comp.bug_fix]) & self._exclude or self.bug_fix > comp.bug_fix:
            return True
        else:
            return False
    
    def __gt__(self, comp : object) -> bool:
        if set([self.major ,comp.major]) & self._exclude or self.major < comp.major:
            return True
        elif set([self.minor ,comp.minor]) & self._exclude or self.minor < comp.minor:
            return True
        elif set([self.bug_fix ,comp.bug_fix]) & self._exclude or self.bug_fix < comp.bug_fix:
            return True
        else:
            return False
    
    def __le__(self, comp: object) -> bool:
        return True if self.__eq__(comp) else self.__lt__(comp) 
    
    def __ge__(self, comp: object) -> bool:
        return True if self.__eq__(comp) else self.__gt__(comp) 
    
    def __str__(self):
        return f'v{self.major}.{self.minor}.{self.bug_fix}'