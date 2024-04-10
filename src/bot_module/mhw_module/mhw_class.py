from datetime import datetime
class AssemblyInfo:
    def __init__(self, user_id, group_id, code, create_date=None):
        self.user_id = user_id
        self.group_id = group_id
        self.assembly_code = code
        if not create_date:
            create_date = datetime.now()
        self.create_date = create_date

    def __str__(self):
        return f"集会码: {self.assembly_code}"