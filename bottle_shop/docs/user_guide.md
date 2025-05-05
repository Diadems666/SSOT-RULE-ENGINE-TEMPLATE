# Bottle Shop End of Trade User Guide

This guide provides instructions for using the Bottle Shop End of Trade web application to manage daily reconciliation processes.

## Table of Contents

1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [End-of-Day Process](#end-of-day-process)
4. [Calendar Navigation](#calendar-navigation)
5. [Cash Handling](#cash-handling)
6. [Troubleshooting](#troubleshooting)

## Introduction

The Bottle Shop End of Trade application is designed to help Australian bottle shops manage their end-of-day reconciliation process. It handles:

- Daily sales reconciliation
- Cash handling and float management
- Financial reporting
- Variance tracking

## Getting Started

### Accessing the Application

1. Open your web browser and navigate to the application URL
2. You will be directed to the calendar view showing the current month
3. Days with completed (settled) reconciliations show in green
4. Days with unsettled reconciliations show in yellow
5. Today's date is highlighted with a box

### Basic Navigation

- Use the calendar to select dates for viewing or editing
- Click on a date to enter or view reconciliation data for that day
- Use the navigation buttons to move between months

## End-of-Day Process

Follow these steps to complete the end-of-day reconciliation:

### 1. Select Today's Date

From the calendar view, click on today's date to open the takings entry form.

### 2. Enter Sales Data

On the "Sales Data" tab, enter:

- Till reading (total sales shown on POS)
- EFTPOS total from main terminal
- Portable EFTPOS total (if applicable)
- AMEX transactions total
- Diners transactions total
- Account charges total
- Points redeemed total
- Customer count for the day

### 3. Enter Safe Float

On the "Safe Float" tab:

- Enter the opening safe float denomination counts at the start of the day
- Enter the closing safe float denomination counts at the end of the day
- The system will calculate the totals automatically
- The safe float should maintain a target value of $1,500

### 4. Enter Till Float

On the "Till Float" tab:

- Enter the opening till float denomination counts at the start of the day
- Enter the closing till float denomination counts at the end of the day
- The system will calculate the totals automatically
- The till float should maintain a target value of $500

### 5. Review Float Makeup

On the "Float Makeup" tab:

- Enter the denomination counts for the till float makeup
- Use the "Calculate Optimal Float" button to get a suggested distribution
- The system will prioritize smaller denominations for the till float

### 6. Review Variance

- The system automatically calculates the variance between expected and actual cash
- A positive variance means excess cash (more cash than expected)
- A negative variance means a shortage (less cash than expected)
- Review all inputs if the variance is large (highlighted in red)

### 7. Settle the Day

- Once all information is correct, click the "Settle Day" button
- This will lock the record and prevent further changes
- Settled days appear in green on the calendar

## Calendar Navigation

- Use the "Previous Month" and "Next Month" buttons to navigate between months
- The current day is always highlighted with a border
- Days with reconciled data appear in green
- Days with unsaved reconciliation data appear in yellow
- You cannot enter data for future dates

## Cash Handling

### Safe Float

- The safe float target is $1,500
- If the safe float is below target, you should deposit cash from banking
- If the safe float is above target, you should withdraw the excess for banking

### Till Float

- The till float target is $500
- The system helps you maintain the correct denomination mix
- Prioritize smaller denominations for the till float
- Avoid using $50 and $100 notes in the till float when possible

## Troubleshooting

### Common Issues

#### "Cannot edit settled takings"

- Once a day is settled, you cannot make changes
- Contact your manager if you need to modify a settled record

#### "Value must be a valid number"

- Ensure all fields contain valid numbers
- Remove any non-numeric characters
- Use decimal points for cents, not commas

#### "Unable to create exact float with available denominations"

- The system cannot find a combination of denominations to match exactly $500
- Try adding more small denominations to allow for more precise combinations
- You may need to adjust your available denominations

#### Large Variance

- Double-check all sales figures against receipts
- Verify all denomination counts in the safe and till
- Ensure all non-cash payment methods are correctly entered
- Check for any missed account charges or points redemptions

### Getting Help

If you encounter issues not covered in this guide, please contact technical support at support@bottleshop.com.au or speak with your manager. 