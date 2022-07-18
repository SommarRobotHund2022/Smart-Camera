import time


def no_fn():
    pass

def benchmark_frame_timing(functions: list[any], args: list[list[any]] = [[]], rounds: int = 100, time_unit = "ms"):   

    div_t = {
        "ns" : 1,
        "us" : 1000,
        "ms" : 1000000,
        "s"  : 1000000000
    }

    div = div_t[time_unit]


    # Ensures that functions and args are the same length
    for i in range(len(functions) - len(args)):
        args.append([])
    
    with open('./benchmark.log', 'w') as file:
                
        for f, a in zip(functions, args):
            print(f'Running test for function: "{f.__name__}" with parameters: {a}')
            file.write(f'Running test for function: "{f.__name__}" with parameters: {a}'+'\n')

            total = 0
            for i in range(rounds):
                start = time.time_ns()
                f(*a)
                end = time.time_ns()

                file.write(f'Frame {i}: {(end - start) / div} {time_unit}'+'\n')
                total += end - start

            s = f'Results for {f.__name__}:\nTotal time ({rounds} rounds): {total / div} {time_unit}\nAverage frame time: {(total/rounds) / div} {time_unit}\navg. FPS: {((total/rounds) / div_t["s"])**-1}\n\n'
            print(s)
            file.write('\n\n'+ s +'\n')
            

