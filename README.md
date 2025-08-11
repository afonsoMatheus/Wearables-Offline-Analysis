# COVID-19 Wearables Offline Analysis

This repository compiles data and code used in the experiments of the paper "Assessing the impact of missing value mechanisms on anomaly detection in healthcare wearable data". 

## Usage Explanation

- Data: The heart rate measurements datasets with simulated missing values used in the paper are public available at: https://osf.io/756k8/?view_only=87a413a9a1684687a0d88095a2ba7967
    - The original COVID-19 Wearables datasets are available within the original paper: https://doi.org/10.1038/s41551-020-00640-6

- Scripts: Contains the missing values simulator and the runner of the original paper script, with locked random seed.
    - RHR-Diff method: Available at https://github.com/gireeshkbogu/AnomalyDetect

- Results: Contains the python notebook used to check and plot the results presented in the paper. The result files are also available at: https://osf.io/756k8/?view_only=87a413a9a1684687a0d88095a2ba7967

## Reference as:

If you are using this code or the simulated missing values datasets, please cite as:

<code>
```bibtex
@INPROCEEDINGS{
}
</code>

## License

This project is licensed under the MIT License.