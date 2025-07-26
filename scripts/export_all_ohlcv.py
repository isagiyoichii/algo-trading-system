from backend.data.utils.export_to_csv import export_to_csv
from backend.data.utils.instrument_list import INDEX_INSTRUMENTS


def export_all():
    for item in INDEX_INSTRUMENTS:
        export_to_csv(item["token"], item["symbol"])


if __name__ == "__main__":
    export_all()
