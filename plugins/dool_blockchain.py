### Author: Dag Wieers <dag$wieers,com>
import requests


class dstat_plugin(dstat):
    """
    Provide stats on latest block synced
    """

    def __init__(self):
        self.name = "blockchain"
        self.vars = ("mine", "llama", "diff")
        self.type = "d"
        self.width = 7
        self.scale = 1

    def get_blocknumber(self, url):
        block_in_hash = requests.post(
            url=url,
            json={"jsonrpc": "2.0", "method": "eth_blockNumber", "params": [], "id": 1},
            timeout=5,
        ).json()["result"]
        blocknumber = int(block_in_hash, 16)
        return blocknumber

    def extract(self):

        mine = self.get_blocknumber(url="http://localhost:8545")
        llama = self.get_blocknumber(url="https://eth.llamarpc.com")
        mine -= round(mine / 1e6) * 1e6
        llama -= round(llama / 1e6) * 1e6
        diff = llama - mine

        self.set2["mine"] = float(mine)
        self.set2["llama"] = float(llama)
        self.set2["diff"] = float(llama - mine)

        self.val = self.set2

        if step == op.delay:
            self.set1.update(self.set2)


# vim:ts=4:sw=4:et
