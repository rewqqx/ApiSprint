import csv
from io import StringIO
from src.models.operation import Operation


class FilesService:
    @staticmethod
    def download(operations):
        output = StringIO()
        writer = csv.DictWriter(output, fieldnames=["id", "mass", "date_start", "date_end", "tank_id", "product_id",
                                                    "created_at", "created_by", "modified_at", "modified_by"])
        writer.writeheader()
        for value in operations:
            writer.writerow({"id": value.id,
                             "mass": value.mass,
                             "date_start": value.date_start,
                             "date_end": value.date_end,
                             "tank_id": value.tank_id,
                             "product_id": value.product_id,
                             "created_at": value.created_at,
                             "created_by": value.created_by,
                             "modified_at": value.modified_at,
                             "modified_by": value.modified_by})
        output.seek(0)
        return output
