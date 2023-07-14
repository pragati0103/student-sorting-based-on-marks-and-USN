from flask import Flask, render_template, request
import pandas as pd
import time

app = Flask(__name__)

def merge_sort(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left_half = arr[:mid]
    right_half = arr[mid:]

    left_half = merge_sort(left_half)
    right_half = merge_sort(right_half)

    merged = merge(left_half, right_half)

    return merged

def merge(left, right):
    merged = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    while i < len(left):
        merged.append(left[i])
        i += 1

    while j < len(right):
        merged.append(right[j])
        j += 1

    return merged

def quick_sort(arr):
    if len(arr) <= 1:
        return arr

    pivot = arr[len(arr) // 2][1]
    left = [x for x in arr if x[1] < pivot]
    equal = [x for x in arr if x[1] == pivot]
    right = [x for x in arr if x[1] > pivot]

    return quick_sort(left) + equal + quick_sort(right)

def count(n):
    c = 0
    while n > 9:
        c += 1
        n = n // 10
    c += 1
    return c

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        file = request.files['file']
        c = int(request.form['sort_option'])
        sc = request.form['search_usn']

        # Read CSV file
        df = pd.read_csv('data.csv')
        
        # Calculate total marks
        df['total'] = df.sum(axis=1)

        usn = df.set_index('usn').T.to_dict('list')

        l = list(df.usn)
        l2 = []
        for i in l:
            l2.append(int(i[7:]))

        start_sort = time.time()

        l = merge_sort(l2) if c == 1 else l2  # Only sort if c is 1

        l2 = []
        for i in l:
            l2.append('eng21cs' + ('0' * (4 - count(i)) + (str(i))))

        end_sort = time.time()
        sort_time = end_sort - start_sort

        result = []
        if c == 1:
            for i in l2:
                result.append((i, usn[i]))
        elif c == 2:
            l = df[['usn', 'total']].values.tolist()
            start_sort = time.time()
            qs = quick_sort(l)
            qs.reverse()
            end_sort = time.time()
            sort_time = end_sort - start_sort

            for i in qs:
                result.append((i[0], usn[i[0]]))

        start_search = time.time()
        search_result = []
        if usn.get(sc) is not None:
            search_result = [(sc, usn[sc])]
        else:
            search_result = [("does not exist",)]

        end_search = time.time()
        search_time = end_search - start_search

        return render_template('index.html', result=result, search_result=search_result, sort_time=sort_time, search_time=search_time)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
