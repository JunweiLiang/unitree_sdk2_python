# note on using 走跑模式
### 获取我们自己的代码
```
    $ git clone https://github.com/JunweiLiang/unitree_sdk2_python
    # 重新安装
    $ (agent_api) junweil@precognition-laptop5:~/projects/unitree_sdk2_python$ pip install -e .
```
### 测试走跑运控的行走和跑步
```
    # g1_loco_client_example.py

    (agent_api) junweil@precognition-laptop5:~/projects/unitree_sdk2_python$ python example/g1/high_level/g1_loco_client_example.py enp131s0
        13 / 14 走跑运控和常规运控可以随时切换，会发出冻的一下的声音。
        set speed mode无效
        setvelocity走路速度明显有变化
        走跑运控下，sport_client.SetVelocity(1.0, 0, 0, 2.0)走了大概1.8米
```

### 测试手臂例程
```
    # g1_arm_action_example.py

    (agent_api) junweil@precognition-laptop5:~/projects/unitree_sdk2_python$ python example/g1/high_level/g1_arm_action_example.py enp131s0

        在走跑运控，主运控下，都可以使用手部动作
```
