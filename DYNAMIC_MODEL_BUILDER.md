# Dynamic Model Builder - Feature Documentation

## Overview

The Dynamic Model Builder is a powerful new feature that allows users to create Django models and database tables dynamically through a web interface, automatically generate synthetic data, and export it to Excel files.

## 🎯 Key Features

### ✅ Completed Implementation

1. **Frontend Interface**
   - Simple HTML/CSS form with dynamic field addition
   - No heavy JavaScript frameworks (vanilla JS only)
   - Bootstrap 5 styling for responsive design
   - Real-time form validation

2. **Dynamic Model Creation**
   - Automatic Django model generation from form data
   - Support for multiple field types: string, text, number, decimal, boolean, date, datetime, email, url, choice, list
   - Field constraints (max_length, min/max values, nullable)
   - Automatic primary key and timestamp field addition

3. **Migration Automation**
   - Automatic SQL migration file generation
   - Automatic migration execution
   - Database table creation with proper field types

4. **Synthetic Data Generation**
   - Faker.js integration for realistic data
   - Smart field name detection (name, email, city, etc.)
   - Custom faker types (name, email, phone, address, company, etc.)
   - Support for choice fields and lists

5. **Excel Export**
   - Professional Excel file generation with OpenPyXL
   - Styled headers and auto-adjusted column widths
   - Files saved to `output/` directory
   - Timestamped filenames
   - Download links for generated files

6. **Database Integration**
   - Optional data insertion to created tables
   - Export tracking and management
   - Admin interface integration

## 🚀 How to Use

### Step 1: Access the Model Builder
- Navigate to the "Model Builder" tab in the main navigation
- Or visit: `http://localhost:8000/model-builder/`

### Step 2: Define Your Table
1. **Basic Info:**
   - Table Name (database): e.g., `user_profiles`
   - Display Name: e.g., `User Profiles`
   - Description: Optional description

2. **Add Fields:**
   - Click "Add Field" to add more fields
   - For each field specify:
     - Field Name: e.g., `first_name`
     - Data Type: Choose from available types
     - Faker Type: For realistic data generation
     - Constraints: Max length, min/max values, nullable
     - Choices: For choice fields (comma-separated)

### Step 3: Create Table
- Click "Create Dynamic Table & Generate Migration"
- System will:
  - Validate your field definitions
  - Create Django model dynamically
  - Generate and run migration
  - Create database table
  - Redirect to table detail page

### Step 4: Generate Data
1. Go to your table's detail page
2. Specify number of records (1-10,000)
3. Optionally check "Save to database" 
4. Click "Generate & Export Excel"
5. Download the generated Excel file

## 📋 Supported Field Types

| Field Type | Description | Options |
|------------|-------------|---------|
| `string` | Short text | max_length |
| `text` | Long text/paragraphs | - |
| `number` | Integer values | min_value, max_value |
| `decimal` | Decimal numbers | max_digits, decimal_places |
| `boolean` | True/False | - |
| `date` | Date values | - |
| `datetime` | DateTime values | - |
| `email` | Email addresses | max_length |
| `url` | URLs | max_length |
| `choice` | Select from options | choices (comma-separated) |
| `list` | Array of values (JSON) | - |

## 🎭 Faker Types

The system supports these faker types for realistic data:

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

## 🗂️ File Structure

```
data_generator/
├── models.py                 # Added DynamicTableDefinition, DynamicTableExport
├── views.py                  # Added dynamic model builder views
├── urls.py                   # Added new URL patterns
├── admin.py                  # Added admin interfaces
├── dynamic_models.py         # NEW: Core dynamic model logic
└── templates/data_generator/
    ├── model_builder.html        # NEW: Main builder interface
    ├── dynamic_table_detail.html # NEW: Table detail view
    └── dynamic_table_list.html   # NEW: Table listing
```

## 🛠️ Technical Details

### Models
- `DynamicTableDefinition`: Stores table schemas and metadata
- `DynamicTableExport`: Tracks Excel exports and file paths

### Dynamic Model Generation
- Uses Python's `type()` function to create Django model classes
- Generates SQL migration files programmatically
- Maps field types to appropriate Django field classes
- Handles field constraints and relationships

### Data Generation
- Smart field name detection for automatic faker assignment
- Configurable field constraints and options
- Bulk data generation with proper typing
- JSON handling for list fields

### Excel Export
- Professional styling with OpenPyXL
- Header formatting and column auto-sizing
- Timestamped file naming
- Secure file serving with proper MIME types

## 📊 Navigation Updates

The application now includes:
- "Model Builder" tab in main navigation
- Dynamic tables count in homepage statistics
- Updated getting started guide
- Integration with existing schema system

## 🔧 Dependencies Added

- `faker==37.5.3` - Realistic data generation
- `openpyxl==3.1.5` - Excel file creation
- `django-extensions==4.1` - Enhanced Django functionality

## ⚡ Performance Considerations

- Maximum 10,000 records per export (configurable)
- Batch database operations for efficiency
- File cleanup can be implemented as needed
- Migration files are created but not automatically cleaned

## 🔒 Security Features

- CSRF protection on all forms
- Input validation and sanitization  
- File path validation for downloads
- SQL injection protection through Django ORM

## 🎉 Usage Examples

### Example 1: User Profile Table
```
Table Name: user_profiles
Fields:
- first_name (string, faker: first_name)
- last_name (string, faker: last_name) 
- email (email, faker: email)
- age (number, min: 18, max: 80)
- city (string, faker: city)
- is_active (boolean)
```

### Example 2: Product Catalog
```
Table Name: products
Fields:
- name (string, max_length: 200)
- description (text)
- price (decimal, max_digits: 10, decimal_places: 2)
- category (choice, choices: "Electronics,Books,Clothing")
- in_stock (boolean)
- created_date (date)
```

## 📈 Future Enhancements

Potential improvements:
- Relationship field support (ForeignKey, ManyToMany)
- Data import from CSV/Excel
- Advanced faker patterns
- API endpoints for programmatic access
- Bulk table operations
- Data visualization
- Export to other formats (JSON, XML)

---

The Dynamic Model Builder provides a complete solution for rapid database table creation, synthetic data generation, and Excel export - all through an intuitive web interface!
