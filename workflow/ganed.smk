import os

DATA_ROOT = "../profile_images"
LOG_ROOT = "gan_logs"
GANED_LOG = os.path.join(LOG_ROOT, "ganed_{index}.log")
GANED_RESULTS = os.path.join(DATA_ROOT, "ganed_results", "ganed_results_{index}.csv")
GANED_RESULTS_ALL = os.path.join(DATA_ROOT, "ganed_results", "ganed_results_all.csv")

INDEXES = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24']

rule run_ganed_on_images_all:
    input: expand(GANED_RESULTS, index=INDEXES)
    output: GANED_RESULTS_ALL
    shell: "python merge_df.py {input} {output}"

rule run_ganed_on_images:
    params: "{index}"
    output: GANED_RESULTS
    shell: "python run_ganed.py {params} {output}"