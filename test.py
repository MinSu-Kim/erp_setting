from connection.pysql_con import Database
from restore_backup.backup import Backup

# Backup.instance().backup_data()
from restore_backup.restore import Restore

Restore.instance().restore()

"""
titles = [('1', '사장'), ('2', '부장'), ('3', '과장'), ('4', '대리'), ('5', '사원')]
with Database.instance() as con:
    with con.cursor() as cursor:
        cursor.executemany("insert into pyqt_erp_proj.title values (%s, %s)", titles)
        con.commit()
"""

