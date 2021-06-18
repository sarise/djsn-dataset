import os


def _get_absolute_path(relative_dir, filename=None):
    if filename:
        relative_path = os.path.join(relative_dir, filename)
    else:
        relative_path = relative_dir
    return os.path.abspath(os.path.expanduser(os.path.expandvars(relative_path)))


OUTPUT_DIR = _get_absolute_path('output')
KABUPATEN_IDS_FILE = os.path.join(OUTPUT_DIR, 'daftar_kabupaten.json')
SAMPLE_RAW_FILE = os.path.join(OUTPUT_DIR, 'sample_raw.json')
SAMPLE_EXTRACTED_KABUPATEN_FILE = os.path.join(OUTPUT_DIR, 'sample_processed.json')
OUTPUT_AGGREGATE_FILE = os.path.join(OUTPUT_DIR, 'aggregate_%03d.csv')  # starting period id argument
