# RooYod by FlowMate 💙💚

RooYod (รู้ยอด) is a LINE-based business assistant designed for small shops,
cafes, and small business owners.

The goal of RooYod is to make recording sales, expenses, customers,
and business reports simple and easy through LINE.

---

## 🚀 Project Status

Current Stage: Development & Testing

RooYod is currently being developed as a multi-shop SaaS system.

---

## ✅ Core Features

### Sales
- Record daily sales
- Record product sales
- Store sales data in Google Sheets

### Expenses
- Record expenses
- Add expense descriptions
- Store expense data per shop

### Customers
- Record daily customer count

### Reports
- Daily report
- Weekly report
- Monthly report
- Top-selling products

---

## 🏪 Multi-Shop System

RooYod supports multiple shops.

Each shop has its own:

- Shop ID
- Shop name
- LINE User ID
- Google Sheet
- Account status
- Trial period
- Subscription plan

Shop statuses:

- pending
- active
- inactive

---

## 💳 Plans

RooYod currently supports:

### Trial
- Record sales
- Record products
- Record expenses
- Record customers
- Daily report
- Shop profile

### Basic
Includes Trial features plus:

- Weekly report
- Top-selling products

### Pro
Includes Basic features plus:

- Monthly report

---

## 🧪 Trial System

The trial system includes:

- Trial start date
- Trial end date
- Remaining trial days
- Trial status checking
- Expiry notification
- Automatic expiry checking

---

## 🔔 Expiry Notification

RooYod can automatically check shop subscription/trial expiry.

The system uses:

- expiry_notifier.py
- Render Cron Job
- Expiry API Key
- LINE notification

The Cron Job runs automatically on schedule.

---

## 🛠 Technology

RooYod is currently built with:

- Python
- Flask
- LINE Messaging API
- Google Sheets
- gspread
- GitHub
- Render
- HTML
- CSS
- JavaScript
- Visual Studio Code

---

## 📁 Main Project Files

- app.py — Main Flask application
- handlers.py — LINE message routing
- services.py — Main business services
- sheet_service.py — Google Sheets operations
- register_handler.py — Shop registration
- admin_handler.py — Admin commands
- plan_handler.py — Plan commands
- plan_service.py — Plan and feature management
- trial_handler.py — Trial status
- expiry_notifier.py — Expiry notification
- sales_handler.py — Sales
- expense_handler.py — Expenses
- product_handler.py — Product sales
- customer_handler.py — Customer count
- report_handler.py — Daily reports
- period_report_handler.py — Weekly/monthly reports
- profile_handler.py — Shop profile

---

## 🌐 Frontend

The project also contains a frontend for RooYod.

frontend/
- index.html
- style.css
- script.js
- assets/

This frontend will continue to evolve into the RooYod user interface.

---

## 🗺 RooYod Development Roadmap

### Phase 1 — Core Bot
Status: ✅ Completed

- LINE Bot
- Sales
- Expenses
- Customers
- Product sales
- Daily reports

### Phase 2 — Business Reports
Status: ✅ Completed

- Weekly reports
- Monthly reports
- Top-selling products

### Phase 3 — Multi-Shop
Status: ✅ Completed / Testing

- Shop registration
- Shop Registry
- Separate Google Sheets
- Shop activation
- Access control

### Phase 4 — Plans & Trial
Status: 🧪 Testing

- Trial / Basic / Pro
- Feature permissions
- Trial expiration
- Plan renewal
- Automatic expiry notification

### Phase 5 — Self-Service
Status: 🚧 Planned

- Easier shop onboarding
- Automatic shop setup
- Subscription/payment flow
- Better user dashboard

### Phase 6 — RooYod Web / LIFF
Status: 🚧 Planned

- Dashboard
- Sales overview
- Expense overview
- Profit overview
- Shop settings
- Mobile-friendly UI

### Phase 7 — Expense & Tax Documents
Status: 🔮 Future

- Receipt storage
- Expense documents
- Upload receipts/invoices
- Document organization
- Expense export
- AI document reader

---

## 🎯 Current Goal

Prepare RooYod for real-shop beta testing.

Priority:

1. Verify automatic expiry notifications
2. Test Trial / Basic / Pro permissions
3. Test multi-shop data separation
4. Test expired/inactive shop behavior
5. Improve onboarding
6. Prepare beta users
7. Prepare RooYod website and marketing

---

## 💙 Product

RooYod (รู้ยอด)

by FlowMate