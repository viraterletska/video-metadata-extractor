import os
import csv
from pymediainfo import MediaInfo

def extract_detailed_mp4_metadata(input_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    base_filename = os.path.splitext(os.path.basename(input_path))[0]
    output_csv_path = os.path.join(output_dir, f"{base_filename}.csv")

    media_info = MediaInfo.parse(input_path)
    all_metadata = []

    for track in media_info.tracks:
        track_data = track.to_data()
        track_data["track_type"] = track.track_type

        # Look for common forensic fields
        possible_fields = {
            "device_make": getattr(track, "com_apple_quicktime_make", None),
            "device_model": getattr(track, "com_apple_quicktime_model", None),
            "gps_latitude": getattr(track, "latitude", None),
            "gps_longitude": getattr(track, "longitude", None),
            "encoded_date": getattr(track, "encoded_date", None),
            "file_created_date": getattr(track, "file_created_date", None),
            "file_modified_date": getattr(track, "file_modified_date", None),
        }

        for k, v in possible_fields.items():
            if v:
                track_data[k] = v

        all_metadata.append(track_data)

    # Collect all unique keys
    all_keys = sorted({key for d in all_metadata for key in d.keys()})

    # Write to CSV
    with open(output_csv_path, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=all_keys)
        writer.writeheader()
        for row in all_metadata:
            writer.writerow(row)

    print(f"Metadata extracted and saved to: {output_csv_path}")

# Example usage
if __name__ == "__main__":
    input_file = "sample_data/example_video1.mp4"
    output_folder = "metadata_extracted"
    extract_detailed_mp4_metadata(input_file, output_folder)
