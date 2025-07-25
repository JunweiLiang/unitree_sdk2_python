import json

from ...rpc.client import Client
from .g1_loco_api import *

"""
" class SportClient
"""
class LocoClient(Client):
    def __init__(self):
        super().__init__(LOCO_SERVICE_NAME, False)
        self.first_shake_hand_stage_ = -1

    def Init(self):
        # set api version
        self._SetApiVerson(LOCO_API_VERSION)

        # regist api
        self._RegistApi(ROBOT_API_ID_LOCO_GET_FSM_ID, 0)
        self._RegistApi(ROBOT_API_ID_LOCO_GET_FSM_MODE, 0)
        self._RegistApi(ROBOT_API_ID_LOCO_GET_BALANCE_MODE, 0)
        self._RegistApi(ROBOT_API_ID_LOCO_GET_SWING_HEIGHT, 0)
        self._RegistApi(ROBOT_API_ID_LOCO_GET_STAND_HEIGHT, 0)
        self._RegistApi(ROBOT_API_ID_LOCO_GET_PHASE, 0) # deprecated

        self._RegistApi(ROBOT_API_ID_LOCO_SET_FSM_ID, 0)
        self._RegistApi(ROBOT_API_ID_LOCO_SET_BALANCE_MODE, 0)
        self._RegistApi(ROBOT_API_ID_LOCO_SET_SWING_HEIGHT, 0)
        self._RegistApi(ROBOT_API_ID_LOCO_SET_STAND_HEIGHT, 0)
        self._RegistApi(ROBOT_API_ID_LOCO_SET_VELOCITY, 0)
        self._RegistApi(ROBOT_API_ID_LOCO_SET_ARM_TASK, 0)
        self._RegistApi(ROBOT_API_ID_LOCO_SET_SPEED_MODE, 0)

    # 7101
    def SetFsmId(self, fsm_id: int):
        p = {}
        p["data"] = fsm_id
        parameter = json.dumps(p)
        code, data = self._Call(ROBOT_API_ID_LOCO_SET_FSM_ID, parameter)
        return code

    # 7102
    def SetBalanceMode(self, balance_mode: int):
        p = {}
        p["data"] = balance_mode
        parameter = json.dumps(p)
        code, data = self._Call(ROBOT_API_ID_LOCO_SET_BALANCE_MODE, parameter)
        return code

    # 7104
    def SetStandHeight(self, stand_height: float):
        p = {}
        p["data"] = stand_height
        parameter = json.dumps(p)
        code, data = self._Call(ROBOT_API_ID_LOCO_SET_STAND_HEIGHT, parameter)
        return code

    # 7105
    def SetVelocity(self, vx: float, vy: float, omega: float, duration: float = 1.0):
        p = {}
        velocity = [vx,vy,omega]
        p["velocity"] = velocity
        p["duration"] = duration
        parameter = json.dumps(p)
        code, data = self._Call(ROBOT_API_ID_LOCO_SET_VELOCITY, parameter)
        return code
    
    # 7106
    def SetTaskId(self, task_id: float):
        p = {}
        p["data"] = task_id
        parameter = json.dumps(p)
        code, data = self._Call(ROBOT_API_ID_LOCO_SET_ARM_TASK, parameter)
        return code

    # 7107 added by junwei
    # 官方回复：0，1，2，3，填入这四个速度档位即可，没有精确的速度值, 这个地方没有做速度闭环控制
    def SetSpeedMode(self, speed_mode: int):
        p = {}
        p["data"] = speed_mode
        parameter = json.dumps(p)
        code, data = self._Call(ROBOT_API_ID_LOCO_SET_SPEED_MODE, parameter)
        return code

    def Damp(self):
        self.SetFsmId(1)
    
    def Start(self):
        #self.SetFsmId(200)
        self.SetFsmId(500) # https://github.com/unitreerobotics/unitree_sdk2/blob/main/include/unitree/robot/g1/loco/g1_loco_client.hpp#L186


    def Squat2StandUp(self):
        self.SetFsmId(706)

    def Lie2StandUp(self):
        self.SetFsmId(702)

    def Sit(self):
        self.SetFsmId(3)

    def StandUp2Squat(self):
        self.SetFsmId(706)

    # by junwei: [06/23/2025]设置走跑运控，参考这个文档：https://support.unitree.com/home/zh/G1_developer/sport_services_interface
    def SetRunWalkMode(self):
        self.SetFsmId(801)
    def SetNormalWalkMode(self):
        self.SetFsmId(500)

    def ZeroTorque(self):
        self.SetFsmId(0)

    def StopMove(self):
        self.SetVelocity(0., 0., 0.)

    def HighStand(self):
        UINT32_MAX = (1 << 32) - 1
        self.SetStandHeight(UINT32_MAX)

    def LowStand(self):
        UINT32_MIN = 0
        self.SetStandHeight(UINT32_MIN)

    def Move(self, vx: float, vy: float, vyaw: float, continous_move: bool = False):
        duration = 864000.0 if continous_move else 1
        self.SetVelocity(vx, vy, vyaw, duration)

    def BalanceStand(self, balance_mode: int):
        self.SetBalanceMode(balance_mode)

    def WaveHand(self, turn_flag: bool = False):
        self.SetTaskId(1 if turn_flag else 0)

    def ShakeHand(self, stage: int = -1):
        if stage == 0:
            self.first_shake_hand_stage_ = False
            self.SetTaskId(2)
        elif stage == 1:
            self.first_shake_hand_stage_ = True
            self.SetTaskId(3)
        else:
            self.first_shake_hand_stage_ = not self.first_shake_hand_stage_
            return self.SetTaskId(3 if self.first_shake_hand_stage_ else 2)
    
