from extensions import db
from models.models import FightersDB
# import csv
# from datetime import date

print(type(db))

# import fighters csv
def import_fighters_csv():
    with open('fighters.csv', encoding='utf8') as csvfile:
        fighters_csv_list = csv.reader(csvfile)
        for row in fighters_csv_list:
            new_fighter = FightersDB(active_status=True, first_name = row[0], last_name=row[1], fighter_image_id = row[2], birthday=date(int(row[3]),int(row[4]),int(row[5])))
            db.session.add(new_fighter)
            try:
                db.session.commit()
            except Exception as e:
                print("Не получилось импортировать бойцов. Ошибка: ", e)
                db.session.rollback()
    return "yep"
# import_fighters_csv()