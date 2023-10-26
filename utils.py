from prettytable import PrettyTable

def print_report():
    x = PrettyTable()
    x.field_names = ["Metric", "Result"]

    for key in report:
        x.add_row([key, report[key]])
        #f"{key}: {report[key]}"
    x.align = "l"
    print(x)

def terminate_app(e):
    print("\n--------- E N D   W I T H   E R R O R ---------\n")
    #print(e)
    print_report()

    exit(1)

def separator(type=None):
    if type == None:
        print("\n"+"-"*80)
    elif type == "results":
        print("-" * 80)
        print("-" * 80)