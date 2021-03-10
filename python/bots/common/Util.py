from enum import IntEnum
# 工具類 methods
class Util:
    # 預設database 位置
    DEFAULT_DB_PATH = r"./common/KFP_bot.db"

    class ChannelType(IntEnum):
        UNKNOWN = 0
        RANK_UP = 1 # 等級提升通知頻道
        REBOOT_MESSAGE = 2 # Bot重啟之後提示的頻道
        IGNORE_XP = 3 # 停止增加經驗值
        AUTO_DELETE = 4 # 自動刪除成員留言
        RANKING_ANNOUNCEMENT = 5 #排名表的公告頻道
        # 只能新添Channel, 不要刪除舊有的

    class RankingType(IntEnum):
        UNKNOWN = 0
        REACTION = 1
        

    class KujiType(IntEnum):
        UNKNOWN = 0 
        LUNGSHAN = 1 # 龍山寺
        OMIKUJI = 2 # 日本神簽
        YI = 3 # 易經
        # 只能添加新的抽籤種類, 不要刪除舊有的

    class GamblingStatus(IntEnum):
        init = 0
        ready = 1 #可以加註的狀態
        wait = 2 #等待賭局結果
        end = 3 #賭局結束
        # 只能新添Status, 不要刪除舊有的
    
    class GamblingError(IntEnum):
        ok = 1
        error = 0
        state_wrong = -1
        # 只能新添Error, 不要刪除舊有的

    class RoleType(IntEnum):
        Gambling = 1
        # 只能新添Role, 不要刪除舊有的

    # 升級為next_rank所需的經驗值
    def get_rank_exp(next_rank:int):
        return round(5 / 6 * next_rank * (2 * next_rank * next_rank + 27 * next_rank + 91), 2)
        

    
