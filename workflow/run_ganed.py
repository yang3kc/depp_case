import pandas as pd
import sys
import ganed
import os

index = sys.argv[1]
output_path = sys.argv[-1]

image_path_root = f"../profile_images/images/image_chunk_{index}"
ganed_calc = ganed.GANEyeDistance()

image_file_names = os.listdir(image_path_root)

results = []
for index, file_name in enumerate(image_file_names):
    if file_name.endswith(".jpg"):
        uid = file_name.split(".")[0]
        image_path = os.path.join(image_path_root, file_name)

        try:
            ganed_result = ganed_calc.calculate_distance(path_to_image=image_path)
            results.append([uid, ganed_result])
        except Exception as e:
            print(e)
    if index % 100 == 0:
        print(
            f"Processed {index} / {len(image_file_names)} ({index / len(image_file_names) * 100:.2f}%)"
        )

results_df = pd.DataFrame(results, columns=["uid", "ganed"])

results_df.to_csv(output_path, index=None)
