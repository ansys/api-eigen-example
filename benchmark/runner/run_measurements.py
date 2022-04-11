import os
import pathlib
import subprocess

if __name__ == "__main__":
    bin_dir = pathlib.Path(__file__).parent.parent / "build" / "bin"
    out_dir = pathlib.Path(__file__).parent.parent / "results"
    server_exe = str(bin_dir / "sync_server")
    client_exe = str(bin_dir / "sync_client")
    server_proc = subprocess.Popen([server_exe])
    try:
        env_no_threading = os.environ.copy()
        env_no_threading["OMP_NUM_THREADS"] = "1"
        print("Running sync measurements.")
        with open(out_dir / "sync.csv", mode="wb") as out_f:
            subprocess.check_call([client_exe], stdout=out_f, env=env_no_threading)
        print("Running threaded measurements.")
        with open(out_dir / "threaded_client.csv", mode="wb") as out_f:
            subprocess.check_call([client_exe], stdout=out_f)
    finally:
        server_proc.terminate()
