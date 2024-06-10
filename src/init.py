import cv2
import os
import sys
import json
import importlib
import csv
import data_collection


def output(
    csv_name, img_name, type, size, raw, verified=None, time=None, MSE=None, PSNR=None
):
    s = f"{type:<20}  |  {size / 1024:>7.2f} kilobytes  |  {(1 - size / raw) * 100:>7.2f}% space saving  |  "

    if verified != None and time != None:
        s += f"{verified:>3}% verified  |  "
        s += f"{time:>5.1f} s"

        with open(csv_name, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(
                [
                    img_name,
                    type,
                    size,
                    raw,
                    (1 - size / raw) * 100,
                    time,
                    verified,
                    MSE,
                    PSNR,
                ]
            )
            f.close()

    print(s)


def main():
    try:
        os.mkdir("data")
    except FileExistsError:
        pass

    with open("src/config.json", "r") as f:
        configs = json.load(f)

    compressions = {name: importlib.import_module(name) for name in configs.keys()}

    if len(sys.argv) > 1:
        test_folder = sys.argv[1]
    else:
        test_folder = "./images/"

    csv_name = data_collection.create_csv()

    try:
        for img_name in os.listdir(test_folder):
            filepath = os.path.join(test_folder, img_name)
            img = cv2.imread(filepath, 0)

            print(f"File: {img_name}\n")

            raw_size = sum(len(row) for row in img)
            output(csv_name, img_name, "Raw", raw_size, raw_size)

            disk_size = os.stat(filepath).st_size
            output(csv_name, img_name, "On disk", disk_size, raw_size)

            for name, keys in configs.items():
                if keys["run"]:
                    compress = compressions[name].compress

                    size, verified, time = compress(img, **(keys["args"]))

                    output(
                        csv_name, img_name, keys["name"], size, raw_size, verified, time
                    )

            print()
    except KeyboardInterrupt:
        print("Interrupted")

    data_collection.translate_data(csv_name)
    data_collection.translate_data(csv_name, outliers=False)
    txt_name = csv_name.split(".")[0]
    data_collection.log_config(txt_name)


if __name__ == "__main__":
    main()
