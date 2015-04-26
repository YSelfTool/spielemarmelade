class GameObject(object):
    def __init__(self, obj_id, kind, owner, position, upgrades):
        self.object_id = obj_id
        self.kind = kind
        self.owner = owner
        self.position = position
        self.upgrades = upgrades

    def __repr__(self):
        return "<GameObject Id={}, Kind={}, Owner={}, Position={}, Upgrades={}>".format(self.object_id, self.kind, self.owner, self.position, self.upgrades)

    def to_dict(self):
        return {
            "id": self.object_id,
            "kind": self.kind,
            "owner": self.owner,
            "position": [self.position[0], self.position[1]],
            "upgrades": self.upgrades
        }


class Placeable(GameObject):
    def __init__(self, obj_id, kind, owner, position, size, upgrades):
        super().__init__(obj_id, kind, owner, position, upgrades)
        self.size = size

    def __repr__(self):
        return "<Placable Id={}, Kind={}, Owner={}, Position={}, Size={}, Upgrades={}".format(self.object_id, self.kind, self.owner, self.position, self.size, self.upgrades)

    def to_dict(self):
        d = super().to_dict()
        d["size"] = [self.size[0], self.size[1]]
        return d

cost_lookup = {}
