import time
from mctools import RCONClient
from dataclasses import dataclass




@dataclass
class Block:
    x: int
    y: int
    z: int
    block: str
    nbt: dict[str, str]

    def __str__(self):
        nbt_data = ",".join([f"{k}={v}" for k,v in self.nbt.items()])
        return f"{self.block} at {self.x}, {self.y}, {self.z} with data {nbt_data}"

@dataclass
class State:
    name: str
    inputs: list[Block]
    outputs: list[Block]

def send_cmd(rcon: RCONClient, cmd):
    output = rcon.command(cmd)
    print(output)
    time.sleep(0.2)
    return output

#assume they are full of states
states = []
schematic = "test"
rcon = RCONClient('localhost', port=25575)
rcon.login('test')
send_cmd(rcon, '//world minecraft:overworld')

fails = []

for state in states:
    #need to clear schematic
    cmd = f"/schematic load {schematic}"
    send_cmd(cmd)
    for i in state.inputs:
        nbt_data = ",".join([f"{k}={v}" for k,v in i.nbt.items()])
        cmd = f"/setblock {i.x} {i.y} {i.z} {o.block}[{nbt_data}] destroy"
        send_cmd(rcon, cmd)
    for o in state.outputs:
        nbt_data = ",".join([f"{k}={v}" for k,v in o.nbt.items()])
        cmd = f'/execute if block {o.x} {o.y} {o.z} {o.block}[{nbt_data}] run tell @a correct!'
        out = send_cmd(rcon, cmd)
        if not "correct!" in out:
            fails.append(f"State {state.name}: output {str(o)} incorrect.")
