import argparse
import random
import time

def rand_add():
    numrange = (10, 999)
    return random.randint(*numrange), random.randint(*numrange)

def rand_sub():
    first = random.randint(20, 999)
    second = first
    min_diff = 9
    while first - second < min_diff or second % 10 == 0:
        second = random.randint(20-min_diff, first)
    return first, second

def rand_mlt():
    minx, maxx = 20, 1000
    first = random.randint(2, 99)
    second = random.randint(minx/first+1, maxx/first)
    return first, second

def rand_div():
    second, result = rand_mlt()
    first = second * result
    return first, second

def rand_pow():
    if random.random() < 0.05:
        first = 5 * random.choice(range(3,21,2))
        second = 2
    elif random.random() < 0.075:
        first = random.choice(range(30,101,10)) + random.choice([-1,1])
        second = 2
    else:
        first = random.randint(2, 40)
        second = first
        while pow(first, second) < 10 or pow(first, second) > 1600:
            second = random.randint(2, 9)
    return first, second

funcs = {
    '+': rand_add,
    '-': rand_sub,
    '*': rand_mlt,
    '/': rand_div,
    '**': rand_pow,
}

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--op', dest='op')
    args = parser.parse_args()
    return args

def main():
    global funcs
    args = get_args()
    if args.op:
        funcs = {args.op: funcs[args.op]}
    stats = {
        func: dict(
            total = 0,
            correct = 0,
            times = [],
        ) for func in funcs.iterkeys()
    }
    streak = 0
    reassign = True
    last_nums = []
    try:
        while True:
            if reassign:
                func = random.choice(funcs.keys())
                x, y = funcs[func]()
                if (x,y) in last_nums:
                    continue
                string = '%s%s%s' % (x, func, y)
            reassign = True
            t1 = time.time()
            print 'streak: %d' % streak
            ans = raw_input('%s = ' % string)
            if ans == '':
                break
            fstats = stats[func]
            fstats['times'].append(time.time() - t1)
            try:
                if int(ans) == eval(string):
                    print 'correct!'
                    fstats['correct'] = fstats['correct'] + 1
                    streak += 1
                else:
                    print 'wrong: ans is %s' % eval(string)
                    streak = 0
                fstats['total'] = fstats['total'] + 1
                last_nums.append((x,y))
                if len(last_nums) > 10:
                    del last_nums[:1]
            except:
                reassign = False
                print 'invalid'
    except KeyboardInterrupt:
        print
    print 'bye'
    _print_stats(stats)

def _print_stats(stats):
    for func, fstats in stats.iteritems():
        if fstats['total'] > 0:
            print
            print func
            correct, total, times = fstats['correct'], fstats['total'], fstats['times']
            print '%d/%d correct (%.1f%%)' % (correct, total, correct*100./total)
            print 'average time %.1fs' % (sum(times)/len(times))

if __name__ == '__main__':
    main()
