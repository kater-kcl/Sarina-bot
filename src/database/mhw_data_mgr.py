from datetime import datetime
from bot_module.mhw_module.mhw_class import SessionCodeInfo
import database.db_mgr as DB


def add_session_code_info(session_code_info: SessionCodeInfo):
    query = "INSERT INTO session_code_info (user_id, group_id, session_code, create_date) VALUES (%s, %s, %s, %s)"
    DB.db_mgr.execute_update(query, (
        session_code_info.user_id, session_code_info.group_id, session_code_info.session_code,
        session_code_info.create_date))


def get_all_session_code_info():
    query = "SELECT * FROM session_code_info"
    result = DB.db_mgr.execute_query(query)
    return [SessionCodeInfo(user_id=row[0], group_id=row[1], code=row[2],
                            create_date=row[3] if isinstance(row[3], datetime) else datetime.strptime(row[3],
                                                                                                      '%Y-%m-%d %H:%M:%S'))
            for row in result]


def del_session_code_info(user_id, group_id):
    print(user_id, group_id)
    query = "DELETE FROM session_code_info WHERE user_id = %s AND group_id = %s"
    DB.db_mgr.execute_update(query, (user_id, group_id))


def clear_outdated_session_code_info():
    query = "DELETE FROM session_code_info WHERE DATE(create_date) != CURDATE()"
    DB.db_mgr.execute_update(query)
