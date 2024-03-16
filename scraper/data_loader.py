import pandas as pd
from scraper.logger import log, Logger
from scraper.database import get_engine, verify_data
from scraper.utils import sanitize_url, truncate_string

class DataLoader: 

    def __init__(
        self,
        csv_file: str,
        table_name=None,
    ):
        self.csv_file = csv_file 
        self.df = pd.read_csv(csv_file, encoding="ISO-8859-1", engine="python")
        self.columns = [self._sanitize_column_name(col) for col in self.df.columns] 
        self.table_name = (
            truncate_string(table_name)
            if table_name is not None
            else self._sanitize_table_name(csv_file)
        )

    def _sanitize_column_name(self, column_name):
        return column_name.replace(' ', '_').lower()

    def _sanitize_table_name(self, file_path):
        table_name = sanitize_url(file_path)
        return truncate_string(table_name)

    def create_table(self):
        engine = get_engine()
        try:
            self.df.to_sql(self.table_name, engine, if_exists='replace', index=False)
            log(f"Table {self.table_name} created successfully")
        except Exception as e:
            Logger.error(f"Error creating table {self.table_name}: {str(e)}")

    def verify_data_loaded(self):
        return verify_data(self.table_name, self.df)

    def __repr__(self):
        return f"<DataLoader (csv_file={self.csv_file}, table_name={self.table_name}, columns={self.columns})>"
