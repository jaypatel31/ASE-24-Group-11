import sys
from config import the
from test_runner import test
import re,ast,fileinput
from DATA import DATA
from load import naive
from RANGE import RANGE
from SYM import SYM
from RULES import RULES
from ascii_table import display
import random
import time
import math

def help():
    print("OPTIONS:")
    print("  -c --cohen    small effect size               = .35")
    print("  -f --file     csv data file name              = ././data/auto93.csv")
    print("  -h --help     show help                       = false")
    print("  -k --k        low class frequency kludge      = 1")
    print("  -m --m        low attribute frequency kludge  = 2")
    print("  -s --seed     random number seed              = 31210")
    print("  -t --todo     todo an action command          = todo")
    sys.exit(0)

def get_option_(arg):
    if arg == "-c" or arg == "--cohen":
        return "cohen"
    elif arg == "-f" or arg == "--file":
        return "file"
    elif arg == "-h" or arg == "--help":
        help()
        return False
    elif arg == "-s" or arg == "--seed":
        return "seed"
    elif arg == "-t" or arg == "--todo":
        # test()
        return "todo"
    else:
        print("Unknown option, please run -h (or) --help for more details.")
        return False




def coerce(s):
  try: return ast.literal_eval(s)
  except Exception: return s

def csv(file="-"):
  with  fileinput.FileInput(None if file=="-" else file) as src:
    for line in src:
      line = re.sub(r'([\n\t\r"\' ]|#.*)', '', line)
      if line: yield [coerce(x) for x in line.split(",")]

def rnd(n, ndecs=2):
    if not isinstance(n, (int, float)):
        return n
    return round(n, ndecs)

def calculate_ranges(data):
    # Transpose the list of lists to get columns
    columns = list(zip(*data))
    
    # Calculate range for each column
    ranges = [(min(col), max(col)) for col in columns]
    
    ranges_string = ",".join([f"({max_val},{min_val})" for max_val, min_val in ranges])
    
    return "[" + ranges_string + "]"

def calculate_column_averages(data):
    num_columns = len(data[0])  # Assuming all inner lists have the same length
    num_rows = len(data)

    # Initialize sums for each column
    column_sums = [0] * num_columns

    # Iterate over each row and update column sums
    for row in data:
        for i in range(num_columns):
            if(len(row)>0): column_sums[i] += row[i]

    # Calculate averages for each column
    column_averages = [round(sum_column / num_rows,2) for sum_column in column_sums]

    return column_averages

def gate20(d=None, stats=None, bests=None, stat=None, best=None):
    print("#best, mid")
    print_statements = [{"st":"1. top6","data":[]},{"st":"2. top50","data":[]},{"st":"3. most","data":[]},{"st":"4. rand","data":[]},{"st":"5. mid","data":[]},{"st":"6. top","data":[]}]
    for i in range(20):
        random.seed(20*i)
        d = DATA(0)
        for row in csv(the["file"]):
            d.add(row)
        stats, bests = d.gate(4, 16, 0.5,print_statements,i)
        stat, best = stats[-1], bests[-1]
        print(rnd(best.d2h(d)), rnd(stat.d2h(d)))
    for statement in print_statements:
        # print(statement)
        for idx, dataset in enumerate(statement['data']):
            print(f"{statement['st']}:")
            print(dataset)

            # For Average
            # if(statement['st'] != "3. most"):
            #     averages = calculate_column_averages(dataset)
            #     print(f"{statement['st']} Average:")
            #     print(averages)
            # else:
            #     print(f"{statement['st']}:")
            #     print(dataset)
        # return

def dstats():
    # Load Data
    data = DATA(0)
    for row in csv(the["file"]): 
        data.add(row)


    print(data.stats())
    


    sys.exit(0)

def main():
    args = sys.argv[1:]
    # print("args",args)
    next_value = False
    option_details = ''
    for arg in args:
        if option_details == "todo":
            if(arg=="stats"): dstats()
            elif(arg=="load"):
                print("Task 1:\n\n")
                display()
                print("Task 2:")
                naive()
            elif(arg=="gate20"):
                gate20()
            elif(arg=="dist"):
                print("Task 1: Get Distance Working: \n")
                dist()
            elif(arg=="far"):
                print("Task 2: Get Far Working: \n")
                far()
            elif(arg=="cluster"):
                tree()
                print("")
                eg_branch()
                print("")
                eg_doubletap()
            else: test(arg)
            option_details = ""
            next_value = False
            continue
        if next_value == True:
            the[option_details] = arg
            next_value = False
            continue
        option_details = get_option_(arg)
        if option_details != False:
            next_value = True
            continue
        else:
            sys.exit(0)

    # print(the)
            
def o(t, n=None):
    return "{" + ", ".join(map(str, t)) + "}"
            
def dist():
    d = DATA(0)
    for row in csv("././data/auto93.csv"): 
        d.add(row)
    
    
    r1 = d.rows[0]
    rows = r1.neighbors(d)
    for i, row in enumerate(rows):
        if i % 30 == 0:
            print(i+1, o(row.cells), rnd(row.dist(r1, d)))

def far():

    d = DATA(0)
    for row in csv("././data/auto93.csv"):  # Load the dataset
        d.add(row)


    a, b, C, eval = d.farapart(d.rows)
    target_distance = 0.95
    current_distance = 0
    attempts = 0
    max_attempts = 1000  # Prevent infinite loops
    total_rows = len(d.rows)
    #print(total_rows)

    while abs(current_distance - target_distance) > 0.01 and attempts < max_attempts:
        # sampled_rows = random.sample(d.rows, total_rows)  # Sample without replacement
        a, b, C, _ = d.farapart(d.rows)
        current_distance = C
        attempts += 1
        
    if attempts == max_attempts:
        print("Failed to find rows with the desired distance after maximum attempts.")
    
    print(o(a), o(b), f"distance = {round(C,4)}", f"Attempts: {attempts}",sep='\n')

def eg_branch():
    print("Task-2: ")
    d = DATA(0)
    for row in csv("././data/auto93.csv"):  # Load the dataset
        d.add(row)
    best, rest, evals = d.branch()
    print("centroid of output cluster:")
    print(o(best.mid().cells,2))
    print(evals)

def eg_doubletap():
    print("Task-3: ")
    d = DATA(0)
    for row in csv("././data/auto93.csv"):  # Load the dataset
        d.add(row)
    best1, rest, evals1 = d.branch(32)
    best2, _, evals2 = best1.branch(4)
    print(o(best2.mid().cells,2), o(rest.mid().cells,2))
    print(evals1 + evals2)

def many(t, n=None):
    if n is None:
        n = len(t)
    return [random.choice(t) for _ in range(n)]

def o(t, n=None, u=None):
        if isinstance(t, (int, float)):
            return str(round(t, n))
        if not isinstance(t, dict) and not isinstance(t, list):
            return str(t)

        u = []
        for k, v in t.items() if isinstance(t, dict) else enumerate(t):
            if str(k)[0] != "_":
                if len(t) > 0:
                    u.append(o(v, n))
                else:
                    u.append(f"${o(k, n)}: ${o(v, n)}")
        

        return u


# def tree(t=None, evals=None):
    # d = DATA(0)
    # print("Task-1: ")
    # for row in csv("././data/auto93.csv"):  # Load the dataset
    #     d.add(row)
    # t, evals = d.tree(True)
    # t.show()
    # print(evals)

def details(d):
    print(f"names\t\t {o(d.cols.names.cells)}\t D2h--")
    print(f"mid\t\t {o(d.mid().cells,2)}\t {round(d.mid().d2h(d),2)}")
    print(f"div\t\t {o(d.div().cells,2)}\t {round(d.div().d2h(d),2)}")

def stats(d):
    print(f"date: {time.strftime('%x %X')}")
    print(f"file: {the['file']}")
    print(f"repeats : 20")
    print(f"seed: {the['seed']}")
    print(f"rows: {len(d.rows)}")
    print(f"cols: {len(d.cols.names.cells)}")


def any50(d):
    random.seed(the.seed)
    rows = d.rows[:]  # Copying the list
    random.shuffle(rows)
    
    for i in range(0, 50):
        print(f"any50:\t\t {o(rows[i].cells,n=2)} \t {round(rows[i].d2h(d),2)}")
        
def evaluate_all(d):
  rows = d.rows[:]
  rows.sort(key=lambda row: row.d2h(d))
  print(f"100%:\t\t {o(rows[0].cells,n=2)} \t {round(rows[0].d2h(d),2)}")
  
def smo9(d):
  budget0 = 4
  budget = 5
  some = 0.5
  d.smo9(budget0,budget,some)

def oo(x):
    print(o(x))
    return x

def _ranges(cols, rowss):
    t = []
    for col in cols:
        for range_ in _ranges1(col, rowss):
            t.append(range_)
    return t

def _ranges1(col, rowss):
    out, nrows = {}, 0
    for y, rows in rowss.items():
        nrows += len(rows)
        for row in rows:
            x = row.cells[col.at]
            if x != "?":
                bin_ = col.bin(x)
                out[bin_] = out.get(bin_, RANGE(col.at, col.txt, x))
                out[bin_].add(x, y)
    
    out = list(out.values())
    out.sort(key=lambda a: a.x['lo'])
    return out if isinstance(col, SYM) else _mergeds(out, nrows / the.bins)

def _mergeds(ranges, tooFew):
    t = []
    i = 0
    while i < len(ranges):
        a = ranges[i]
        if i < len(ranges) - 1:
            both = a.merged(ranges[i + 1], tooFew)
            if both:
                a = both
                i += 1
        t.append(a)
        i += 1
    if len(t) < len(ranges):
        return _mergeds(t, tooFew)
    for i in range(1, len(t)):
        t[i].x['lo'] = t[i - 1].x['hi']
    t[0].x['lo'] = -math.inf
    t[-1].x['hi'] = math.inf
    return t

def bins(d):
    best, rest, evals = d.branch()
    like = best.rows
    hate = random.sample(rest.rows, 3 * len(like))
    t = []

    def score(range_obj):
        return range_obj.score("LIKE", len(like), len(hate))

    for col in d.cols.x:
        print("")
        for range_obj in _ranges1(col, {"LIKE": like, "HATE": hate}):
            print(range_obj)
            t.append(range_obj)

    t.sort(key=lambda x: score(x), reverse=True)
    max_score = score(t[0])
    print("\n#scores:\n")
    for v in t[:the.Beam]:
        if score(v) > max_score * 0.1:
            print(round(score(v),2), v)
    print({"LIKE": len(like), "HATE": len(hate)})

def eg_rules(d):
    for xxx in range(1, 2):
        # best, rest = d:branch()
        best0, rest, evals1 = d.branch(the.d)
        best, _, evals2 = best0.branch(the.D)
        print(evals1 + evals2 + the.D - 1)
        LIKE = best.rows
        random.sample(rest.rows, 3 * len(LIKE))
        HATE = random.sample(rest.rows, 3 * len(LIKE))
        rowss = {"LIKE": LIKE, "HATE": HATE}
        print("score", "\t\t\t" ,"mid selected", "\t\t\t\t\t", "rules")
        print("_____", "\t" ,"__________________________________________________", "\t", "__________________")
        print("")
        for rule in RULES(_ranges(d.cols.x, rowss), "LIKE", rowss).sorted:
            result = d.clone(rule.selects(rest.rows))
            if len(result.rows) > 0:
                result.rows.sort(key=lambda a: a.d2h(d))
                print(round(rule.scored,2), "\t" ,o(result.mid().cells), "\t", rule.show())



if __name__ == '__main__': 
    # main()
    d = DATA(0)
    for row in csv("././data/auto93.csv"): 
        d.add(row)
    eg_rules(d)
    # print("TASK-1:")
    # print("\n")
    # stats(d)
    # print("#")
    # details(d)
    # print("#")
    # smo9(d)
    # print("#")
    # any50(d)
    # print("#")
    # evaluate_all(d)

