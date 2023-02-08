class Member:
    def _init_(self, name, contribution):
        self.name = name
        self.contribution = contribution

class Esusu:
    def _init_(self):
        self.members = []

    def add_member(self, member):
        self.members.append(member)

    def get_total_contribution(self):
        return sum([member.contribution for member in self.members])

    def distribute_funds(self):
        total_contribution = self.get_total_contribution()
        share_amount = total_contribution / len(self.members)
        for member in self.members:
            member.contribution = share_amount

# Example usage
esusu_group = Esusu()

# Add members
esusu_group.add_member(Member("John", 100))
esusu_group.add_member(Member("Jane", 100))
esusu_group.add_member(Member("Jim", 100))

# Distribute funds
esusu_group.distribute_funds()

# Verify that each member received an equal share
for member in esusu_group.members:
    print(f"{member.name} received {member.contribution}")