from datetime import datetime
from src.bot_module.mhw_module.mhw_class import AssemblyInfo
import database.db_mgr as DB


def add_assembly_info(assembly_info: AssemblyInfo):
    query = "INSERT INTO assembly_info (user_id, group_id, assembly_code, create_date) VALUES (%s, %s, %s, %s)"
    DB.db_mgr.execute_update(query, (
        assembly_info.user_id, assembly_info.group_id, assembly_info.assembly_code, assembly_info.create_date))


def get_all_assembly_info():
    query = "SELECT * FROM assembly_info"
    result = DB.db_mgr.execute_query(query)
    return [AssemblyInfo(user_id=row[0], group_id=row[1], code=row[2],
                         create_date=row[3] if isinstance(row[3], datetime) else datetime.strptime(row[3], '%Y-%m-%d %H:%M:%S')) for row in result]


def del_assembly_info(user_id, group_id):
    print(user_id, group_id)
    query = "DELETE FROM assembly_info WHERE user_id = %s AND group_id = %s"
    DB.db_mgr.execute_update(query, (user_id, group_id))


def clear_outdated_assembly_info():
    query = "DELETE FROM assembly_info WHERE DATE(create_date) != CURDATE()"
    DB.db_mgr.execute_update(query)
