# Dynamic Model Builder

A Django web application that allows you to create database tables dynamically through a simple web interface, then generate realistic synthetic data and export it to Excel files. Perfect for rapid prototyping, testing, development, and data science projects.

## Features

- 🎯 **Dynamic Table Creation**: Create database tables through a web interface - no coding required
- 🚀 **Automatic Migrations**: Tables are created automatically with proper Django migrations
- 💾 **Excel Export**: Generate and download professional Excel files with synthetic data
- 🔧 **Admin Interface**: Manage tables and exports through Django admin
- 🎭 **Faker Integration**: Realistic data generation with 12+ faker types
- 🎨 **Modern UI**: Clean, responsive Bootstrap-based interface
- 📊 **Field Types**: Support for 11 different field types with constraints
- ⚡ **Real-time Generation**: Generate up to 10,000 records instantly

## Screenshots

### Dynamic Model Builder
The main interface allows you to define table structure by adding fields with different types and constraints.

### Table Management
View all your created tables, their structure, and manage data generation exports.

### Data Generation
Generate thousands of realistic records and export them as professionally formatted Excel files.

## Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/brandondelpozo/synthetic-data-ai.git
   cd synthetic-data-ai
   ```

2. **Create and activate virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (optional, for admin access)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Start the development server**
   ```bash
   python manage.py runserver
   ```

7. **Open your browser** and navigate to `http://127.0.0.1:8000`

## Usage

### Creating a Dynamic Table

1. Visit the home page - the **Dynamic Model Builder** interface loads automatically
2. Fill in the table details:
   - **Table Name**: Database table name (e.g., `user_profiles`)
   - **Display Name**: Human-readable name (e.g., `User Profiles`)
   - **Description**: Optional description of what the table represents

3. **Add Fields** by clicking "Add Field" and defining:
   - **Field Name**: Column name (e.g., `first_name`)
   - **Data Type**: Choose from 11 available types
   - **Faker Type**: Optional realistic data generation
   - **Constraints**: Max length, min/max values, nullable options

4. **Click "Create Dynamic Table"** - the system will:
   - Generate Django model code
   - Create and run database migration
   - Create the actual database table
   - Redirect you to the table detail page

### Example Table Definition

Here's a sample table for user profiles:

**Table Name**: `user_profiles`  
**Display Name**: `User Profiles`

**Fields**:
- `first_name` (String, Faker: first_name, Max Length: 50)
- `last_name` (String, Faker: last_name, Max Length: 50)  
- `email` (Email, Faker: email)
- `age` (Number, Min: 18, Max: 80)
- `city` (String, Faker: city)
- `is_active` (Boolean)
- `join_date` (Date)

### Supported Field Types

| Field Type | Description | Constraints Available |
|------------|-------------|----------------------|
| **string** | Short text | max_length |
| **text** | Long text/paragraphs | - |
| **number** | Integer values | min_value, max_value |
| **decimal** | Decimal numbers | max_digits, decimal_places |
| **boolean** | True/False | - |
| **date** | Date values | - |
| **datetime** | DateTime values | - |
| **email** | Email addresses | max_length |
| **url** | URLs | max_length |
| **choice** | Select from options | choices (comma-separated) |
| **list** | Array of values (JSON) | - |

### Faker Types

Choose from 12+ faker types for realistic data:

- `name` - Full names
- `first_name` - First names only
- `last_name` - Last names only
- `email` - Email addresses
- `phone` - Phone numbers
- `address` - Full addresses
- `city` - City names
- `country` - Country names
- `company` - Company names
- `job` - Job titles
- `sentence` - Random sentences
- `paragraph` - Random paragraphs

### Generating Synthetic Data

1. Go to your table detail page (or click "View" from the Tables list)
2. In the **Generate Excel Data** section:
   - Specify number of records (1-10,000)
   - Optionally check "Save to database" to store records
3. Click **Generate & Export Excel**
4. Download the professionally formatted Excel file

## Quick Workflow Example

Here's a complete example of creating a "Customer Database" table:

### Step 1: Create Table
1. Visit `http://127.0.0.1:8000` 
2. Fill in:
   - **Table Name**: `customers`
   - **Display Name**: `Customer Database`
   - **Description**: `Customer information for CRM`

### Step 2: Add Fields
Click "Add Field" for each field:

| Field Name | Type | Faker Type | Constraints |
|------------|------|------------|-------------|
| `first_name` | String | first_name | Max Length: 50 |
| `last_name` | String | last_name | Max Length: 50 |
| `email` | Email | email | - |
| `phone` | String | phone | - |
| `company` | String | company | Max Length: 100 |
| `age` | Number | - | Min: 18, Max: 75 |
| `annual_revenue` | Decimal | - | Max Digits: 12, Decimal Places: 2 |
| `is_active` | Boolean | - | - |

### Step 3: Generate Data
1. Click "Create Dynamic Table & Generate Migration"
2. Wait for success message and redirect
3. On table detail page, set "Number of Records": `1000`
4. Click "Generate & Export Excel"
5. Download your `customers_YYYYMMDD_HHMMSS.xlsx` file

**Result**: A professional Excel file with 1000 realistic customer records! 🎉

### Admin Interface

Access the Django admin at `/admin/` to:
- Manage user accounts
- View all dynamic table definitions
- Monitor Excel exports and their status
- Perform administrative tasks

## Project Structure

```
synthetic-data-ai/
├── data_generator/           # Main Django app
│   ├── models.py            # Database models (DynamicTableDefinition, DynamicTableExport)
│   ├── views.py             # View logic for model builder
│   ├── urls.py              # URL routing
│   ├── admin.py             # Admin configuration
│   ├── dynamic_models.py    # Dynamic model generation logic
│   └── templates/           # HTML templates
│       └── data_generator/
│           ├── base.html
│           ├── model_builder.html
│           ├── dynamic_table_detail.html
│           └── dynamic_table_list.html
├── synthetic_data_project/   # Django project settings
├── output/                  # Generated Excel files
├── venv/                    # Virtual environment
├── manage.py               # Django management script
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## Development

### Setting up for development

1. Follow the installation steps above
2. Install development dependencies (if any)
3. Run tests: `python manage.py test`
4. Make migrations: `python manage.py makemigrations`

### Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and commit: `git commit -m 'Add feature'`
4. Push to the branch: `git push origin feature-name`
5. Submit a pull request

## URL Structure

The application provides the following main endpoints:

- `/` - Dynamic Model Builder interface (home page)
- `/tables/` - List all created dynamic tables
- `/table/<id>/` - Table detail view and data generation
- `/create/` - Create new dynamic table (AJAX endpoint)
- `/table/<id>/generate-excel/` - Generate synthetic data and Excel export
- `/excel-export/<id>/download/` - Download generated Excel file
- `/admin/` - Django admin interface

## Technology Stack

- **Backend**: Django 5.2+
- **Database**: SQLite (default) - easily configurable for PostgreSQL, MySQL
- **Frontend**: Bootstrap 5, HTML5, CSS3, Vanilla JavaScript
- **Icons**: Font Awesome
- **Data Generation**: Faker 37.5+
- **Excel Export**: OpenPyXL 3.1+
- **Extensions**: Django Extensions 4.1+
- **Python**: 3.8+

## Deployment

For production deployment:

1. Set `DEBUG = False` in settings
2. Configure a production database (PostgreSQL recommended)
3. Set up static file serving
4. Use a production WSGI server like Gunicorn
5. Configure environment variables for secrets

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For questions, issues, or contributions:
- Create an issue on GitHub
- Submit a pull request
- Contact: [Your Contact Information]

## Changelog

### v2.0.0 (Current) - Dynamic Model Builder
- 🎯 **Major Redesign**: Completely rebuilt as Dynamic Model Builder
- 🗑️ **Removed**: Old JSON schema system for simplified user experience
- ✨ **New**: Web-based database table creation interface
- 🚀 **New**: Automatic Django model generation and migrations
- 📊 **New**: 11 field types with constraints and faker integration
- 💾 **New**: Professional Excel export with formatting
- 🎨 **New**: Streamlined single-purpose interface
- ⚡ **Enhanced**: Support for up to 10,000 records per export
- 🔧 **Enhanced**: Better error handling and user feedback

### v1.0.0 - JSON Schema System (Deprecated)
- Initial release with JSON schema approach
- Basic schema management
- Data generation with faker support
- CSV export functionality
- Admin interface
- Responsive web UI
