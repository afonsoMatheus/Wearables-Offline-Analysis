
import os
import subprocess
import argparse

# Caminho da pasta onde estão os arquivos

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description="Runs the script for RHR calculation.")
    parser.add_argument(
        "-m", 
        type=str, 
        required=True, 
        choices=["MCAR", "MAR", "MNAR"], 
        help="Folder of the missing values mechanism (choose between: MCAR, MAR, MNAR)."
    )
    parser.add_argument("-p", type=int, required=True, help="Folder corresponding to the percentage of missing values (e.g., 25, 50, ...).")
    parser.add_argument("-n", type=int, required=True, help="Number of subfolders to process (e.g., 1, 2, ...).")

    # Parse the arguments
    args = parser.parse_args()

    # Assign arguments to variables
    mechanism = args.m
    mr = args.p
    num_subfolders = args.n

    folder_path_c = os.path.join(os.path.dirname(__file__), "../../Data/COVID-19-Wearables")
    folder_path_m_base = os.path.join(os.path.dirname(__file__), f"../../Data/COVID-19-Wearables-Missing/{mechanism}/{mr}")
    folder_end = os.path.join(os.path.dirname(__file__), "../../Results/RHR/online")

    for i in range(1, num_subfolders + 1):
        folder_path_m = f"{folder_path_m_base}/{i}"

        # Get all files in the directory
        # Filter specific files
        try:
            files_hr = [f for f in os.listdir(folder_path_m) if f.endswith(f"_hr_{mechanism}_{mr}_{i}.csv")]
            files_st = [f for f in os.listdir(folder_path_c) if f.endswith("_steps.csv")]
        except FileNotFoundError as e:
            print(f"❌ Error accessing the directory: {e}")
            continue

        # Iterate over all HR files
        for file_hr in files_hr:
            # Find the corresponding steps file
            myphd_id = file_hr.split('_')[0]  # Example of ID based on the file name
            matching_steps = [f for f in files_st if f.startswith(myphd_id)]

            if matching_steps:
                hr_path = os.path.join(folder_path_m, file_hr)
                steps_path = os.path.join(folder_path_c, matching_steps[0])
                myphd_folder = os.path.join(folder_end, myphd_id)

                # Create the folders if they don't exist
                figure_folder = os.path.join(myphd_folder, "Figures")
                anomalies_folder = os.path.join(myphd_folder, "Anomalies")

                os.makedirs(figure_folder, exist_ok=True)
                os.makedirs(anomalies_folder, exist_ok=True)

                # Create folders for the mechanism and missing rate inside Anomalies and Figures
                mechanism_figure_folder = os.path.join(figure_folder, mechanism)
                mechanism_anomalies_folder = os.path.join(anomalies_folder, mechanism)

                mr_figure_folder = os.path.join(mechanism_figure_folder, str(mr))
                mr_anomalies_folder = os.path.join(mechanism_anomalies_folder, str(mr))

                os.makedirs(mr_figure_folder, exist_ok=True)
                os.makedirs(mr_anomalies_folder, exist_ok=True)

                figure_path = os.path.join(mr_figure_folder, f"{myphd_id}_online_alerts_{mechanism}_{mr}_{i}.pdf")
                #figure_bar_path = os.path.join(mr_figure_folder, f"{myphd_id}_online_alerts_bar_{mechanism}_{mr}_{i}.pdf")
                anomalies_path = os.path.join(mr_anomalies_folder, f"{myphd_id}_online_anomalies_{mechanism}_{mr}_{i}.csv")
                anomalies_alert_path = os.path.join(mr_anomalies_folder, f"{myphd_id}_online_alerts_{mechanism}_{mr}_{i}.csv")  

                
                command = [
                    "python", "Metrics/rhrad_online_24hr_alerts_v7.py",
                    "--heart_rate", hr_path,
                    "--steps", steps_path,\
                    "--myphd_id", myphd_id,
                    "--figure1", figure_path,
                    "--anomalies", anomalies_path,
                    "--alerts", anomalies_alert_path,
                    #"--figure2", figure_bar_path
                ]
                
                #print(f"Executing: {' '.join(command)}")
                print(f"Executing for: {myphd_id}")
                
                # Call the script
                try:
                    result = subprocess.run(command, check=True)
                    print(f"✅ Command executed successfully for {myphd_id}!")
                    print(result.stdout)
                except subprocess.CalledProcessError as e:
                    print(f"\n❌ ERROR EXECUTING THE SCRIPT FOR {myphd_id}\n")
                    # print(f"   🩺 HR File: {file_hr}")
                    # print(f"   👣 Steps File: {matching_steps[0]}")
                    # print(f"🔴 Exit code: {e.returncode}")
                    # print(f"📄 Standard output:\n{e.stdout}")
                    # print(f"⚠️ Error output:\n{e.stderr}")
            else:
                print(f"❌ Corresponding steps file not found for HR: {file_hr}")

    print("🎉 All commands have been executed. 🎉")
