from Util import sql
class LoanType():
    name = ''
    branch_id = ''
    id = 0
    def __init__(self,name,id,branch_id):
        self.id = id
        self.name = name
        self.branch_id = branch_id
    def get_branch_name(self):
        return sql.get_branch_name(self.branch_id)