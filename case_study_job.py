class Menu:
    def display(self):
        print('\n【TOP Menu】')
        print('1. Read all data')
        print('2. Read 50 row data')
        print('3. Creat a new record')
        print('4. Update an existing record')
        print('5. Delete a worker record')
        print('6. Basic analyzer')
        print('7. Salary analyzer')
        print('8. Exit')
        return int(input('Enter your choice: '))

    def display_basic_analysis(self):
        print('\n【Basic Analysis Menu】')
        print('1. Find null')
        print('2. Check category')
        print('3. Search value')
        print('4. Check frequency')
        print('5. Convert salary currency from USD to HUF')
        print('6. Sort all values')
        print('7. Sort category')
        print('8. Sort frequency list')
        print('9. Go back to prior menu')
        return int(input('Enter your choice: '))

    def display_salary_analyzer(sefl):
        print('\n【Salary Analyzer Menu】')
        print('1. Show AVERAGE salary')
        print('2. Show MAX salary')
        print('3. Show MIN salary')
        print('4. Show MAX salary job')
        print('5. Show MIN salary job')
        print('6. Average salary by experience')
        print('7. Go back to prior menu')
        return int(input('Enter your choice: '))

class JobDatabase:
    def __init__(self, file_name, fieldnames):
        self.file_name = file_name
        self.fieldnames = ['work_year', 'job_title', 'job_category', 'salary_currency', 'salary', 'salary_in_usd', 'employee_residence', 'experience_level', 'employment_type','work_setting', 'company_location', 'company_size']

    def read_data(self):
        records = []
        with open(self.file_name, mode='r', newline='', encoding='utf-8') as file:
            lines = file.readlines()  # Read all lines from the file
            for line in lines[1:]:  # Skip the header line
                values = line.strip().split(',')  # Split each line by comma
                record = dict(zip(self.fieldnames, values))  # Map fieldnames to values
                records.append(record)
        return records

    def create_record(self, new_record):
        """Create a new record and insert it into the file."""
        records = self.read_data()
        records.insert(0, new_record)  # Insert the new record at the beginning

        with open(self.file_name, mode='w', newline='', encoding='utf-8') as file:
            # Write the header line
            file.write(','.join(self.fieldnames) + '\n')
            # Write each record as a comma-separated string
            for record in records:
                file.write(','.join([record[field] for field in self.fieldnames]) + '\n')
        return new_record

    #Convert a string input like "{'key1': 'value1', 'key2': 'value2'}" to a dictionary.
    def parse_input_to_dict(self, input_str):
        try:
            # Remove surrounding braces and split key-value pairs
            input_str = input_str.strip('{}')
            data_dict = {}
            for pair in input_str.split(','):
                key, value = pair.split(':', 1)
                key = key.strip().strip("'\"")  # Remove quotes and whitespace
                value = value.strip().strip("'\"")  # Remove quotes and whitespace
                data_dict[key] = value
            return data_dict
        except Exception as e:
            print(f"Error parsing input: {e}")
            return None

    def update_record(self, target_data, updated_data):
        """Update a record based on a specific combination of attributes."""
        target_data = self.parse_input_to_dict(target_data)
        updated_data = self.parse_input_to_dict(updated_data)

        if not target_data or not updated_data:
            print("Invalid input format. Please try again.")
            return

        records = self.read_data()
        updated = False
        for record in records:
            # Check if all target data matches in the current record
            if all(record[key] == value for key, value in target_data.items()):
                # Update the record with the new data
                record.update(updated_data)
                updated = True
                print(f"Record updated with {updated_data}")
                break

        if not updated:
            print("No record found with the specified attributes.")
            return

        with open(self.file_name, mode='w', newline='', encoding='utf-8') as file:
            # Write the header line
            file.write(','.join(self.fieldnames) + '\n')
            # Write each record as a comma-separated string
            for record in records:
                file.write(','.join([record[field] for field in self.fieldnames]) + '\n')

    def delete_record(self, target_data):
        """Delete a record based on a specific combination of attributes."""
        target_data = self.parse_input_to_dict(target_data)

        if not target_data:
            print("Invalid input format. Please try again.")
            return

        records = self.read_data()
        updated_records = [record for record in records if not all(record[key] == value for key, value in target_data.items())]

        if len(updated_records) == len(records):
            print("No record found with the specified attributes.")
            return

        with open(self.file_name, mode='w', newline='', encoding='utf-8') as file:
            # Write the header line
            file.write(','.join(self.fieldnames) + '\n')
            # Write each record as a comma-separated string
            for record in updated_records:
                file.write(','.join([record[field] for field in self.fieldnames]) + '\n')

        print("Record deleted.")

    def read_first_50_rows(self):
        """Read the first 50 rows from the dataset."""
        rows_list = []
        with open(self.file_name, mode='r', newline='', encoding='utf-8') as file:
            lines = file.readlines()
            for row in lines[1:51]:  # Read only the first 50 data rows (skip header)
                values = row.strip().split(',')  # Split each line by comma
                row_dict = dict(zip(self.fieldnames, values))  # Map fieldnames to values
                rows_list.append(row_dict)
        return rows_list

    def display_column(self, column_name):
        """Display all values of a specific column."""
        if column_name not in self.fieldnames:
            print(f"Column '{column_name}' does not exist in the dataset.")
            return

        records = self.read_data()  # Get all records

        # Extract the values for the specified column
        column_values = [record[column_name] for record in records]

        # Display the values of the specified column
        print(f"Values for column '{column_name}':")
        print(", ".join(column_values))

    # to read all values in the vertical line and return it as a list
    def read_column(self, column_name):
        value_list = []
        records = self.read_data()
        self.column_name = column_name
        for record in records:
            value_list.append(record[self.column_name])
        return value_list

class BasicAlgorithm(JobDatabase):

    #to use parameter in the every function in this class
    def __init__(self, file_name, column_name):
        super().__init__(file_name, fieldnames=None)
        self.column_name = column_name

    #filter 1-1: to serch null rows
    ##using linear search algorithm
    def linear_serch_for_null(self):
        values = self.read_column(self.column_name)
        n = len(values)
        i = 0
        while i <= n-1 and values[i] is not None:
            i += 1
        exists = (i <= n-1)

        if exists:
            number = i
            return f'there is null value in the {number}row'
        else:
            return 'there is no null value'

    #filter 1-2: to check category
    def check_category(self):
        values = self.read_column(self.column_name)
        category_set = set(values)
        return category_set

    #filter 1-3: to convert set to list
    def make_category_list(self):
        values = self.check_category()
        category_list = list(values)
        return category_list

    #filter 2: *searching specific values
    ##using selecting algorithm
    def selecting(self, specific_value):
        values = self.read_column(self.column_name)
        self.specific_value = specific_value
        n = len(values)
        row_index_list = []
        for i in range(n):
            if values[i] == self.specific_value:
                row_index_list.append(i)
        if row_index_list == []:
            result = f"there isn't such a data ({self.specific_value})"
        else:
            result = f'the value ({self.specific_value}) is in the {row_index_list}th row'
        return result

    #filter 3: separating specific categories
    ##using separating algorithm and linear search algorithm
    def frequency(self):
        values = self.read_column(self.column_name)
        frequency = {}
        for element in values:
            if element in frequency:
                frequency[element] += 1
            else:
                frequency[element] = 1
        return frequency

    #convert salary currency
    ##using copying algorithm
    def convert_usd_to_forint(self, currency_rate):
        values = self.read_column(self.column_name)
        self.currency_rate = currency_rate
        n = len(values)
        salary_in_forint = [0]*n
        for i in range(n):
            salary_in_forint[i] = float(values[i]) * self.currency_rate
        return salary_in_forint

    #sorting1 - sorting all column values
    def sorting_all_column_values(self, asc_or_desc='asc'):
        values = self.read_column(self.column_name)
        self.asc_or_desc = asc_or_desc
        n = len(values)
        for i in range(n-1):
            for j in range(i+1,n):
                if self.asc_or_desc == 'asc':
                    if values[i] > values[j]:
                        values[i], values[j] = values[j], values[i]
                elif self.asc_or_desc == 'desc':
                    if values[i] < values[j]:
                        values[i], values[j] = values[j], values[i]
                else:
                    return "please enter 'asc' or 'desc"
        return values

    #sorting2 - sorting input_list which is a new list you made after operating method
    def sorting_result_list(self,input_list, asc_or_desc='asc'):
        self.asc_or_desc = asc_or_desc
        n = len(input_list)
        for i in range(n-1):
            for j in range(i+1,n):
                if self.asc_or_desc == 'asc':
                    if input_list[i] > input_list[j]:
                        input_list[i], input_list[j] = input_list[j], input_list[i]
                elif self.asc_or_desc == 'desc':
                    if input_list[i] < input_list[j]:
                        input_list[i], input_list[j] = input_list[j], input_list[i]
                else:
                    return "please enter 'asc' or 'desc"
        return input_list

    #sorting3 - sorting input_dictionary which is a new dictionary you made after operating method
    def sorting_result_dict(self,input_dict, sort_by='key', asc_or_desc='asc'):
        items = list(input_dict.items())
        n = len(items)

        #determine the index to sort by: 0 for keys, 1 for values
        sort_index = 0 if sort_by == 'key' else 1

        for i in range(n-1):
            for j in range(i+1,n):
                if asc_or_desc == 'asc':
                    if items[i][sort_index] > items[j][sort_index]:
                        items[i], items[j] = items[j], items[i]
                elif asc_or_desc == 'desc':
                    if items[i][sort_index] < items[j][sort_index]:
                        items[i], items[j] = items[j], items[i]
        sorted_dict = dict(items)
        return sorted_dict

#Methods for mathematical, statistical or business calculations
class SalaryAnalyzer:
    def __init__(self, filename):
        self.filename = filename
        self.salaries = []

    def read_salaries(self):
        """Reads salary data from the CSV file and stores it in the salaries list."""
        self.salaries = []  # Reset the list in case of multiple calls
        with open(self.filename, 'r') as file:
            # Skip the header
            file.readline()

            for line in file:
                columns = line.strip().split(',')
                try:
                    salary = float(columns[5])  # Assuming salary is in column index 5
                    self.salaries.append(salary)
                except ValueError:
                    continue  # Skip invalid salary values

    def calculate_average_salary(self):
        """Calculates and returns the average salary, count of entries, and total salary."""
        if not self.salaries:
            return 0, 0, 0

        total_salary = sum(self.salaries)
        count = len(self.salaries)
        average_salary = round((total_salary / count), 2)
        return average_salary, count, total_salary

    def find_max_salary(self):
        """Finds and returns the maximum salary in the dataset."""
        max = 0
        salary = self.salaries
        n = len(salary)
        if not salary:
            return None
        else:
            for i in range(1,n) :
                if salary[i] > salary[max]:
                    max = i
            result = salary[max]
        return result

    def find_min_salary(self):
        """Finds and returns the minimum salary in the dataset."""
        min = 0
        salary = self.salaries
        n = len(salary)
        if not salary:
            return None
        else:
            for i in range(1,n) :
                if salary[i] < salary[min]:
                    min = i
            result = salary[min]
        return result

    def find_max_salary_job(self):
        """Finds and returns the job with the maximum salary."""
        max_salary = float('-inf')
        job_with_max_salary = None

        with open(self.filename, 'r') as file:
            # Skip the header
            file.readline()

            for line in file:
                columns = line.strip().split(',')
                try:
                    salary = float(columns[5])
                    job_name = columns[1]  # Assuming job title is in column index 1

                    if salary > max_salary:
                        max_salary = salary
                        job_with_max_salary = job_name
                except ValueError:
                    continue

        if job_with_max_salary is None:
            return None, None

        return job_with_max_salary, max_salary

    def find_min_salary_job(self):
        """Finds and returns the job with the minimum salary."""
        min_salary = float('inf')
        job_with_min_salary = None

        with open(self.filename, 'r') as file:
            # Skip the header
            file.readline()

            for line in file:
                columns = line.strip().split(',')
                try:
                    salary = float(columns[5])
                    job_name = columns[1]  # Assuming job title is in column index 1

                    if salary < min_salary:
                        min_salary = salary
                        job_with_min_salary = job_name
                except ValueError:
                    continue

        if job_with_min_salary is None:
            return None, None

        return job_with_min_salary, min_salary

    def average_salary_by_experience(self):
        """Calculates and prints the average salary by experience level."""
        experience_data = {}

        with open(self.filename, 'r') as file:
            # Skip the header
            file.readline()

            for line in file:
                columns = line.strip().split(',')
                try:
                    experience_level = columns[7]  # Assuming experience level is in column index 7
                    salary = float(columns[5])  # Assuming salary is in column index 5

                    if experience_level in experience_data:
                        experience_data[experience_level]['total_salary'] += salary
                        experience_data[experience_level]['count'] += 1
                    else:
                        experience_data[experience_level] = {'total_salary': salary, 'count': 1}
                except ValueError:
                    continue

        for experience_level, data in experience_data.items():
            average_salary = data['total_salary'] / data['count']
            print(f"{experience_level}: {average_salary:.2f}")
