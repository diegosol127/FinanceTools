# Financial Tools Suite

The goal of this toolkit is to streamline the process for viewing and interacting with all things finance-related. Currently, the primary tools available are for budget tracking and tax estimation.

These tools use macros and manual functions within Excel to process data. It is not clear how functionality will be affected by the file to different versions of Excel or even trying to share it through a cloud network.




# Budget Tracker

This set of tools lets you view and interact with your transactions. With it, you can see how your income and expenses are are categorized as well as how much is being allocated to each category.

**Dependencies**
- `BudgetTracker.xlsm`
    - `\Outputs`
- `SortTransactions.py`
    - `\ClassificationData`
    - `\Statements`

## Future Plans

### 1. Incorporate all financial accounts

- [x] Organize statements into unique folders
- [x] Search all folders for file corresponding to the input month and year
- [x] Consolidate CSV format for files from all financial sources, then merge into a data frame for processing

### 2. Update classification profile

- [ ] Update json file names so they are all preceded by `income_` or `expenses_`
- [ ] Update expense categories (check out potential categories below) and include descriptions in the json files
- [ ] Create income categories to consider account variety (employment, retirement fund, HSA, etc.)
- [ ] Make Excel read the categories from the json files directly

### 3. Use Excel for manual CSV file updates

- [ ] Import sorted data to Excel, then make edits locally
- [ ] Make a conditional format that easily identifies transactions that have yet to be categorized ("unlabelled")
- [ ] Add functionality to save CSV files from Excel macro

### 4. Smart dashboard

- [ ] Automatically populate categories from list generated by reading json files
- [ ] Automatically sort categories by price amount

### 5. Add plots and figures

- [ ] Create a summary for tables in the dashboard using pie charts
- [ ] Create a bar graph containing totals from income, expenses, and savings

### 6. Modular viewing window

- [ ] Create a macro to read in all sorted files withing a selected time window and load them into the `Income and Expenses` sheet
- [ ] Allow inputs to be selected accoding to a financial period (mm/yyyy, mm/yyyy - mm/yyyy, etc.)
- [ ] Consider making separate sheets for importing data, modifying and saving data, and viewing data

### 7. Improve code structure

- [ ] Consider making tools in object-oriented format
- [ ] Create a folder for utilities that can be used to import classes and functions in the main script
- [ ] Conider implementing an arg parser for streamlined debugging

### 8. Integrate Python and Excel for single enrtypoint

- [ ] Use Excel macros to run everything from Excel, including 

## Potential Categories

As suggested by ChatGTP

**Housing**
1. Rent/Mortgage
2. Property Taxes
3. Homeowners/Renters Insurance
4. Home Maintenance/Repairs
5. Utilities (Electricity, Water, Gas)
6. Internet/Cable
7. Phone

**Transportation**
1. Car Payment
2. Car Insurance
3. Gas/Fuel
4. Public Transportation
5. Parking
6. Car Maintenance/Repairs
7. Registration/License Fees

**Food**
1. Groceries
2. Dining Out
3. Coffee Shops
4. Snacks

**Health and Medical**
1. Health Insurance
2. Doctor Visits
3. Dental Care
4. Prescription Medications
5. Over-the-Counter Medications
6. Vision Care
7. Health and Wellness (Gym memberships, etc.)

**Personal Care**
1. Haircuts/Salon Services
2. Personal Hygiene Products
3. Clothing and Accessories

**Insurance**
1. Life Insurance
2. Disability Insurance
3. Long-Term Care Insurance

**Debt Payments**
1. Credit Card Payments
2. Student Loan Payments
3. Personal Loan Payments
4. Other Debt Payments

**Savings and Investments**
1. Emergency Fund
2. Retirement Savings
3. Investment Accounts
4. Education Savings (529 Plan, etc.)

**Entertainment and Recreation**
1. Movies/TV/Streaming Services
2. Hobbies
3. Books/Magazines
4. Music/Concerts
5. Sports/Activities
6. Vacations/Travel

**Education**
1. Tuition
2. Books/Supplies
3. Courses/Workshops

**Childcare and Education**
1. Daycare/Preschool
2. School Tuition
3. School Supplies
4. Extracurricular Activities

**Gifts and Donations**
1. Charitable Donations
2. Gifts for Family and Friends
3. Holiday Expenses

**Miscellaneous**
1. Subscriptions/Memberships
2. Pet Care (Food, Vet, etc.)
3. Office Supplies
4. Postage/Shipping
5. Legal Fees

**Household Supplies**
1. Cleaning Supplies
2. Paper Products
3. Laundry Supplies

**Professional Services**
1. Accounting/Tax Services
2. Legal Fees
3. Consulting Services

**Utilities**
1. Water
2. Electricity
3. Gas
4. Trash/Recycling
5. Sewer

**Taxes**
1. Income Taxes
2. Property Taxes
3. Other Taxes

You can adjust these categories based on your specific needs and financial situation. This list covers most common expenses people encounter, making it easier to track and manage your spending.




# Tax Estimator

Uses `TaxEstimator.xlsm` as a standalone tool. Input your expected income and expenses to estimate you expected tax rates, savings, effective income, and more. Use in tandem with the **Budget Tracker** for maximum predictive accuracy.
