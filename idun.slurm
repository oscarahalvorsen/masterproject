        #!/bin/bash
        #SBATCH --job-name="nb-gpt-6B-job"  # Sensible name for the job
        #SBATCH --account=oscaraha         # Replace <account> with your IDUN allocation account
        #SBATCH --partition=GPUQ            # Use the GPU partition
        #SBATCH --time=00:30:00             # Upper time limit (30 minutes)
        #SBATCH --nodes=1                   # Allocate 1 node
        #SBATCH --ntasks=1                  # Number of tasks
        #SBATCH --gres=gpu:1                # Request 1 GPU
        #SBATCH --cpus-per-task=4           # Number of CPU cores
        #SBATCH --mem=32G                   # Memory (adjust as needed)
        #SBATCH --output=nb-gpt-6B-output.txt  # Output log file

        # Load the necessary modules
        module purge
        module load Python/3.8.6-GCCcore-10.2.0  # Load a suitable Python module
        module load fosscuda/2018b               # Load CUDA if using GPU

        # Run your Python script
        python nb-gpt-6B.py
