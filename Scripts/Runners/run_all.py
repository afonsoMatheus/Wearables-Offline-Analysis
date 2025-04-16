import subprocess
from multiprocessing import Pool
from tqdm import tqdm

def run_rhrad_online(args):
    mr_value, iterations = args

    subprocess.run(
        ["python", "run_rhrad_online.py",
            "-m", "MCAR", 
            "-p", str(mr_value),
            "-n", str(iterations)]
    )

def run_with_progress(args_list):
    with Pool(len(args_list)) as pool:
        for _ in tqdm(pool.imap_unordered(run_rhrad_online, args_list), total=len(args_list)):
            pass

if __name__ == "__main__":
    mr_values = [10, 20, 30, 40, 50]
    iterations = 5  # Número de iterações como entrada
    
    args_list = [(mr, iterations) for mr in mr_values]
    run_with_progress(args_list)
