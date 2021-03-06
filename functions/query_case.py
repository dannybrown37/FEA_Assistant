from .validate import menu_choice, get_case_number, get_string

def amend_table_data(dbm):
    sql = """ SELECT name FROM sqlite_master WHERE type = 'table' """
    results = dbm.query(sql)
    tables = [name[0] for name in results]
    prompt = "From which table would you like to select?"
    print
    for x in range(1, len(tables)+1):
        print str(x) + ". " + tables[x-1]
    table = menu_choice(prompt, str(range(len(tables)+1)))

    if tables[table-1] == "AppraiserSites":
        results = dbm.query("SELECT * FROM AppraiserSites")
        for result in results:
            print result[0], "|", result[1]
        # TODO add ability to edit these if ever needed
        return # breaks from function before below

    case_number = get_case_number()
    while True:
        sql = "SELECT * FROM %s WHERE CaseNumber = %s " % (
            tables[table-1],
            case_number
        )
        results = dbm.query(sql)
        types = dbm.get_column_names()
        print
        case_list = []
        for tuple in results:
            for i, (type, item) in enumerate(zip(types, tuple)):
                print "%s. %s: %s" % (i+1, type, item)
                if tables[table-1] == "CaseData":
                    case_list.append(item)
        prompt = "Which data would you like to update?"
        update = menu_choice(prompt, str(range(len(types)+1)))
        if tables[table-1] == "ImportantDates":
            date_type = types[update-1]
            new_date = get_string("Enter a new date for %s:" % date_type)
            dbm.amend_important_date(date_type, new_date, case_number)
        elif tables[table-1] == "CaseData":
            case_list[update-1] = get_string(
                "Enter new data for %s:" % types[update-1]
            )
            case_list[update-1] = int(case_list[update-1])
            dbm.amend_case_data(case_list, update-1)
