import csv
import os
import json


class StartupNationCentralPipeline:
    def __init__(self):
        # Directory for saving outputs
        self.output_dir = 'D:\startupnationcentral'
        os.makedirs(self.output_dir, exist_ok=True)

        # File paths for CSV
        self.csv_files = {
            'companies': os.path.join(self.output_dir, 'companies.csv'),
            'employeesTrend': os.path.join(self.output_dir, 'employeesTrend.csv'),
            'cumulativeFunding': os.path.join(self.output_dir, 'cumulativeFunding.csv'),
            'company_investor': os.path.join(self.output_dir, 'company_investor.csv')
        }

        # File paths for JSON
        self.json_files = {
            'companies': os.path.join(self.output_dir, 'companies.json'),
            'employeesTrend': os.path.join(self.output_dir, 'employeesTrend.json'),
            'cumulativeFunding': os.path.join(self.output_dir, 'cumulativeFunding.json'),
            'company_investor': os.path.join(self.output_dir, 'company_investor.json')
        }

        self.csv_handlers = {}
        self.csv_writers = {}
        self.json_data = {
            'companies': [],
            'employeesTrend': [],
            'cumulativeFunding': [],
            'company_investor': []
        }

    def open_spider(self, spider):
        # Open CSV files and prepare writers
        self.csv_handlers['companies'] = open(self.csv_files['companies'], 'w', newline='', encoding='utf-8')
        self.csv_writers['companies'] = csv.DictWriter(self.csv_handlers['companies'], fieldnames=[
            'company_id', 'row_type', 'company_name', 'last_update_date', 'logo', 'summary', 'overview', 'sector',
            'total_funding', 'funding_stage', 'num_employees', 'founded', 'address_in_occupied_palestine',
            'offices_abroad',
            'youtube', 'instagram', 'linked_in', 'twitter', 'facebook', 'website', 'url'
        ])
        self.csv_writers['companies'].writeheader()

        self.csv_handlers['employeesTrend'] = open(self.csv_files['employeesTrend'], 'w', newline='', encoding='utf-8')
        self.csv_writers['employeesTrend'] = csv.DictWriter(self.csv_handlers['employeesTrend'], fieldnames=[
            'company_id', 'row_type', 'employeesTrend_year', 'employeesTrend_value'
        ])
        self.csv_writers['employeesTrend'].writeheader()

        self.csv_handlers['cumulativeFunding'] = open(self.csv_files['cumulativeFunding'], 'w', newline='',
                                                      encoding='utf-8')
        self.csv_writers['cumulativeFunding'] = csv.DictWriter(self.csv_handlers['cumulativeFunding'], fieldnames=[
            'company_id', 'row_type', 'cumulativeFunding_year', 'cumulativeFunding_value'
        ])
        self.csv_writers['cumulativeFunding'].writeheader()

        self.csv_handlers['company_investor'] = open(self.csv_files['company_investor'], 'w', newline='',
                                                     encoding='utf-8')
        self.csv_writers['company_investor'] = csv.DictWriter(self.csv_handlers['company_investor'], fieldnames=[
            'company_id', 'row_type', 'investor_id', 'investor_name', 'investor_position'
        ])
        self.csv_writers['company_investor'].writeheader()

    def process_item(self, item, spider):
        # Determine the type of item and write to the appropriate CSV and JSON files
        if item['row_type'] == 'cumulativeFunding':
            self.csv_writers['cumulativeFunding'].writerow(item)
            self.json_data['cumulativeFunding'].append(item)

        elif item['row_type'] == 'employeesTrend':
            self.csv_writers['employeesTrend'].writerow(item)
            self.json_data['employeesTrend'].append(item)

        elif item['row_type'] == 'company':
            self.csv_writers['companies'].writerow(item)
            self.json_data['companies'].append(item)

        elif item['row_type'] == 'company_investor':
            self.csv_writers['company_investor'].writerow(item)
            self.json_data['company_investor'].append(item)

        return item

    def close_spider(self, spider):
        # Close all CSV file handlers
        for handler in self.csv_handlers.values():
            handler.close()

        # Write JSON data to files
        for key, data in self.json_data.items():
            with open(self.json_files[key], 'w', encoding='utf-8') as json_file:
                json.dump(data, json_file, ensure_ascii=False, indent=4)
