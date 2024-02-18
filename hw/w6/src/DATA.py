from ROW import ROW
from COLS import COLS
import re,ast,fileinput
import random
from config import the

class DATA:
    def __init__(self, src, fun=None):
        self.rows = []
        self.cols = None

    def new(cls, src, fun=None):
        instance = cls()
        if isinstance(src, str):
            for x in cls.csv(src):
                instance.add(x, fun)
        else:
            for x in (src or []):
                instance.add(x, fun)
        return instance

    def add(self, t, fun=None):
        row = t if isinstance(t, ROW) else ROW(t)
        if self.cols:
            if fun:
                fun(self, row)
            self.rows.append(self.cols.add(row))
        else:
            self.cols = COLS(row)  

    def coerce(s):
        try: return ast.literal_eval(s)
        except Exception: return s
    def csv(file="-"):
        with  fileinput.FileInput(None if file=="-" else file) as src:
            for line in src:
                line = re.sub(r'([\n\t\r"\' ]|#.*)', '', line)
                if line: yield [coerce(x) for x in line.split(",")]

    # The following methods need the implementation of mid, div, small, and stats 
    # methods in the respective classes they are called on
    def mid(self, cols=None):
        u = [col.mid() for col in (cols or self.cols.all)]
        return ROW(u)

    def div(self, cols=None):
        u = [col.div() for col in (cols or self.cols.all)]
        return ROW(u)

    def small(self):
        u = [col.small() for col in self.cols.all]
        return ROW(u)

    def stats(self, cols=None, fun=None, ndivs=2):
        u = {".N": len(self.rows)}
        col_name = cols if cols else self.cols.all
        for col in (col_name):
            u[col.txt] = round(float(col.mid()), ndivs) if isinstance(col.mid(), (int, float)) else col.mid()
        return u

    def gate(self, budget0, budget, some,print_statements,itr):
        stats = []
        bests = []
        rows = self.rows[:]  # Copying the list
        random.shuffle(rows)
        
        print_statements[0]['data'].append([example.cells[5:8] for example in rows[:6]])
        print_statements[1]['data'].append([example.cells[5:8] for example in rows[:50]])
        rows.sort(key=lambda row: row.d2h(self))
        print_statements[2]['data'].append(rows[0].cells[5:8])

        random.shuffle(rows)

        lite = rows[:budget0]
        dark = rows[budget0:]

        for i in range(budget):
            best, rest = self.bestRest(lite, len(lite) ** some)

            todo, selected = self.split(best, rest, lite, dark)

            selected_dark_rows = random.sample(dark, budget0 + i)
            centroid_dark_y_values = [row.cells[5:8] for row in selected_dark_rows]  # Assuming rows contain cells attribute
            centroid_dark = [round(sum(col) / len(col),2) for col in zip(*centroid_dark_y_values)]

            if(len(print_statements[3]['data'])==itr):
                print_statements[3]['data'].append([])
                print_statements[4]['data'].append([])
                print_statements[5]['data'].append([])

            print_statements[3]['data'][itr].append(centroid_dark)
            
            centroid_selected_y_values = [row.cells[5:8] for row in selected.rows]
            centroid_selected = [round(sum(col) / len(col),2) for col in zip(*centroid_selected_y_values)]
            print_statements[4]['data'][itr].append(centroid_selected)
            print_statements[5]['data'][itr].append(best.rows[0].cells[5:8]) 
            stats.append(selected.mid())
            bests.append(best.rows[0])
            lite.append(dark.pop(todo))
        return stats, bests

    def bestRest(self, rows, want, best=None, rest=None, top=None):
            rows.sort(key=lambda row: row.d2h(self))
            best, rest = [self.cols.names], [self.cols.names]
            for i, row in enumerate(rows):
                if i < want:
                    best.append(row)
                else:
                    rest.append(row)
            d1 = DATA(0)
            d2 = DATA(0)
            for row in best:
                d1.add(row)
            for row in rest:
                d2.add(row)
            return  d1, d2
    
    def split(self, best, rest, lite, dark):
        # print("a",best.rows[0].cells,"b", rest,"c", lite,"d", dark)
        selected = DATA(0)
        selected.add(self.cols.names)
        max_val = 1E30
        out = 1

        for i, row in enumerate(dark):
            b = row.like(best, len(lite), 2)
            r = row.like(rest, len(lite), 2)
            if b > r:
                selected.add(row)

            tmp = abs(b + r) / abs(b - r + 1E-300)

            if tmp > max_val:
                out, max_val = i, tmp
        return out, selected
    
    def farapart(self, rows, sortp=None, a=None, b=None, far=None, evals=None):
        far = int(len(rows) * the.Far) - 1
        
        evals = 1 if a else 2
        # a = ROW([4, 97, 88, 72, 3, 2100, 16.5, 30])
        a = a or random.choice(rows).neighbors(self, rows)[far]
        # print(far)
        b = a.neighbors(self, rows)[far]
        if sortp and b.d2h(self) < a.d2h(self):
            a, b = b, a
        return a, b, a.dist(b, self), evals

    def clone(self, rows):
        new = DATA([])
        new.cols = self.cols
        for row in rows:
            new.add(row)
        return new

    def half(self, rows, sortp=True, before=None):
        from gate import many

        # Assuming implementation of many, farapart, and keysort functions
        some = many(rows, min(the.Half, len(rows)))
        a, b, C, evals = self.farapart(some, sortp, before)
        d = lambda row1, row2: row1.dist(row2, self)
        project = lambda r: (d(r, a) ** 2 + C ** 2 - d(r, b) ** 2) / (2 * C)
        rows.sort(key=project)
        mid_point = len(rows) // 2
        as_, bs = rows[:mid_point], rows[mid_point:]
        return as_, bs, a, b, C, d(a, bs[0]), evals

    def branch(self, stop=None):
        evals, rest = 1, []
        stop = stop or int(2 * (len(self.rows) ** 0.5))
        def _branch(data, above=None, left=None, lefts=None, rights=None):
            nonlocal evals
            if len(data.rows) > stop:
                lefts, rights, left, b, C, distance_from_a_to_bs, evals = data.half(data.rows, True, above)
                evals += 1
                rest.extend(rights)
                return _branch(data.clone(lefts), left)
            else:
                return data.clone(data.rows), data.clone(rest), evals
        return _branch(self)
