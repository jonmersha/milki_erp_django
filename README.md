---

# **Milki ERP System**

*A Centralized Process Automation Platform for Milki Food Complex*

## 📌 Overview

Milki ERP is a centralized, modular management system designed to streamline operations across procurement, inventory, sales, logistics, finance, HR, and CRM.
This project replaces fragmented manual workflows with an integrated, role-based, secure, and scalable platform.

The system is built to support multi-warehouse operations, track inventory movement, manage sales & orders, handle procurement lifecycles, process HR data, and provide actionable dashboards for decision-making.

---

## 🚀 Key Features

### **1. Inventory Management**

* Real-time stock tracking across factories and warehouses
* Product categorization, pricing, grading, and packaging
* Inventory movement logs (inbound/outbound, transfers)
* Low-stock alerts & audit logs

### **2. Sales & Order Management**

* Order lifecycle: Draft → Confirmed → Shipped → Delivered → Paid
* Customer management
* Auto-generated invoices and delivery slips
* Stock reservation during order confirmation

### **3. Logistics & Shipment Tracking**

* Dispatch planning, route & carrier assignment
* Shipment statuses: Scheduled → In Transit → Delivered
* Proof of delivery records

### **4. Finance & Accounts Receivable**

* Payment tracking per order
* Aging reports & unpaid invoice alerts
* Linked to Order & Shipment modules

### **5. Procurement Management**

* Supplier registry
* PR → PO → Vendor Fulfillment → Goods Receipt
* Integration with Inventory & Finance

### **6. HRM (Human Resource Management)**

* Employee profile management
* Attendance & leave tracking
* Onboarding/offboarding workflows
* Payroll data preparation

### **7. CRM**

* Customer profiles, complaints, and case resolution
* Logs interaction history
* Engagement analytics

### **8. Workflow & User Management**

* Role-based access control (RBAC)
* Permissions per module/action
* Segregation of duties
* User audit logs

### **9. Reporting & Dashboards**

* Inventory, Sales, HR, Finance dashboards
* Custom filters & scheduled email reports
* Export to PDF/Excel

---

## 🗂️ System Architecture Overview

### **Tech Highlights**

* Web-based, mobile-responsive UI
* Secure authentication (with 2FA support)
* Microservices-ready backend
* REST API support for integrations (SMS, GPS, Accounting)
* Multilingual (English/Amharic)

---

## 🛢️ Database Schema (Summary)

The project includes the following core tables:

### **Core Entities**

* `Company`, `Factory`, `Warehouses`
* `Products`, `Inventory`, `Inventory_Movement`
* `Sales_Order`, `Purchase_Order`
* `Suppliers`, `Customers`

### **User & Role Management**

* `Roles`, `Permissions`, `Role_Permissions`
* `System_Users`
* `User_Audit_Log`
* `Segregation_Rules`

---

## 📦 Folder Structure (Recommended)

```
/milki-erp
│── backend/
│   ├── api/
│   ├── models/
│   ├── services/
│   ├── migrations/
│   └── config/
│
│── frontend/
│   ├── src/
│   ├── components/
│   ├── pages/
│   ├── hooks/
│   └── api/
│
│── docs/
│   ├── Business Requirements Document.pdf
│   ├── API_Design.md
│   └── Data_Model_Diagram.png
│
│── database/
│   └── milki2.sql
│
└── README.md
```

---

## ⚙️ Installation & Setup

### **Prerequisites**

* Python (Django) or Node (if using JS backend)
* MySQL / PostgreSQL
* Redis (optional for caching & queues)

### **Setup Steps**

1. Clone the repository
2. Import the DB structure from `milki2.sql`
3. Configure environment variables:

   ```
   DB_HOST=
   DB_USER=
   DB_PASSWORD=
   SECRET_KEY=
   ```
4. Run backend migrations
5. Start frontend & backend services

---

## 🧪 Testing

* Unit tests for each module
* Integration tests for workflows (Orders, Procurement, HR)
* API endpoint collection (Postman/Insomnia)

---

## 📈 Future Enhancements

* AI-based inventory forecasting
* Mobile field sales application integration
* Real-time GPS delivery tracking
* Sustainability & compliance reporting

---

## 👥 Contributors

* **Milki Food Complex IT Team**
* **Development Team**
* **System Admins & Module Stakeholders**

---
