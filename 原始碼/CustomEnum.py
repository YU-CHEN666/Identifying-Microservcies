#Enum 管理空間
from enum import Enum


class ServerState(Enum):
    Stop = 0
    Run = 1


class SubprocessMode(Enum):
    FastAPIExe = 0
    cmd = 1
    
    
class MessageBoxMode(Enum):
    Info = 0
    Error = 1
    
    
class ButtonMode(Enum):
    Stop = 0
    Start = 1
    