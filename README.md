
## Inventó: A Reusable FIFO Inventory Module for Django

Full-Stack Django Module for Streamlined & Auditable FIFO Inventory.

**Here's the Web App deployed on the cloud:**
https://gabegtrrz1.pythonanywhere.com/login/

**Credentials:**

`username:` user

`password:` jeremiah29.11


-----

**Table of Contents**

* [Project Overview](#project-overview)
* [Features](#features)
* [Technologies Used](#technologies-used)
* [Setup and Installation](#setup-and-installation)
* [How to Run / Usage](#how-to-run--usage)
* [Challenges and Learnings](#challenges-and-learnings)
* [Future Improvements](#future-improvements)
* [License](#license)

-----

### **Project Overview**

 Inventó is a full-stack Django web module designed for precise First-In, First-Out (FIFO) inventory control. Moving beyond simple stock counts, it tackles the technical challenge of implementing and maintaining accurate chronological inventory tracking. The system was architected with a pluggable design philosophy, enabling easy integration into various Django applications. Key features include detailed lot management with built-in auditability via traceable UUIDv1 unique identifiers, providing essential traceability and security for stock transactions. Building this project showcases proficiency in full-stack web development (covering both frontend and backend), tackling specific and complex business logic implementation, designing robust database schemas, and developing reusable, reliable software components tailored for real-world application.

-----

### **Features**


  * **Product Management:** Add, view, update, and delete product definitions.
  * **Inventory Stocking (Inbound):** Record incoming inventory units, capturing details necessary for FIFO tracking (e.g., purchase date, cost per unit ).
  * **Inventory Depletion (Outbound):** Automatically manage stock removal based on the strict FIFO principle – units/lots added first are the first ones removed.
  
*  **Detailed Lot Tracking:** To ensure accurate First-In, First-Out (FIFO) tracking, the system meticulously manages individual inventory batches, referred to as **Lots**. 

	- **Unique Lot Number (UUID1):** Each incoming batch of stock is assigned a Unique Lot Number. This number is generated using a **UUID version 1 algorithm**, combining the **exact timestamp** of the stock entry with the **MAC address** of the device or system making the transaction. 
	
	- **Built-in Audit Trail & Security:** This unique, time-and-location-stamped identifier provides a robust audit trail and security measure, as it can be reversed to verify _when_ and _from where_ each specific lot of stock entered the system.

  * **Real-time Stock Levels:** View current inventory quantities for each `Item` and each `Lot`.
  * **Transaction/Movement History:** Track detailed inbound and outbound movements for full auditability.
  

-----

### **Technologies Used**


  * **Backend:**
      * Python
      * Django (Specify version if you like, e.g., 4.x, 5.x)
      * MySQL (Database)
  * **Frontend:**
      * HTML5
      * CSS3
      * JavaScript
      * Bootstrap
      * jQuery
  * **Other Tools:**
      * Git & GitHub (Version Control)


-----

### **Setup and Installation**


1.  **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/Invento.git
    cd Invento
    ```
2.  **Set up a Python Virtual Environment:** 
    ```bash
    python -m venv .venv
    # On macOS/Linux:
    source .venv/bin/activate
    # On Windows:
    .venv\Scripts\activate
    ```
3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables**
To run this project, you'll need to set up environment variables. This keeps sensitive information secure and allows for environment-specific configurations.

Local Development:

Create a .env file in the project's root directory.

Add your variables to .env in the format KEY=VALUE (e.g., SECRET_KEY=your_dev_key, DATABASE_NAME=dev_db).

Important: Ensure .env is in your .gitignore file.


5.  **Apply Migrations:**
    ```bash
    python manage.py migrate
    ```
6.  **Create a Superuser** *(Needed to access the Django admin or potentially create initial data):*
    ```bash
    python manage.py createsuperuser
    ```
7.  **Run the Development Server:**
    ```bash
    python manage.py runserver
    ```
   The app will be accessible, usually at `http://127.0.0.1:8000/`

-----

### **How to Run / Usage**


1.  Navigate to `http://127.0.0.1:8000/` in your web browser.
2. Log in with the superuser account you created.
3.  Go to the Inventó section/app.
4.  **Add an Item:** 
	a. Click on the `items` tab.
	b. Click on `Add Item`.
	c. Enter the relevant information and click save.
	
	This adds only the item description into the system, but not its quantity. To add the actual number or stock of the item, proceed to adding stock. 
	
5.  **Add Stock:** 
	a. Click on `Stock In` tab.
	b. Select the relevant item from the items previously added into the system.
	c. Input the data into applicable fields such as quantity, cost, received date, expiry date (optional), and notes (optional).
	d. Click on `Save Stock In`
	
	- The stock-in movement/transaction will be reflected in the `Movements` tab.
	- This new stock will be added into a new `Lot`. 
	This can be viewed in the `Lots` tab.

6.  **Stock Out:**
	a. Click on `Stock Out` tab.
	b. Select the relevant item from the items previously added into the system.
	c. Input the data into applicable fields such as quantity and notes (optional).
	d. Click on `Save Stock Out`
	
	- The stock-out movement/transaction will be reflected in the `Movements` tab.
	- First-in First-out (FIFO) principle will be applied meaning that the stock out transaction takes stock out of the first batches/lots of the selected Item.
	
7.  **View Inventory:** Inventory levels may be viewed in 2 ways:
	1. **Specific Item:**
		a. Open `Item` tab.
		b. Within the row of the item you want to view, click on the `View Icon` under the `Actions` column.
		c. Under the Item Details page, you will find:

		- **Total Available Quantity:** Displays the **current available stock** for an item. This value is dynamically calculated by summing the quantities from all active or available **Lots** associated with that specific item, providing an immediate view of inventory levels.
		- **Lots:** Displayed on the right, a list of the individual inventory batches (Lots) for this item, displayed in the **First-In, First-Out (FIFO) order** based on their entry date.
		
8. **Inventory Movement History:** Click on the Movements tab.
Access this log to review all past changes to your inventory levels. The history table provides a clear breakdown of each transaction, detailing:

	-   **When:** Date and time of the movement.
	-   **What:** The item involved.
	-   **Which Batch:** The specific Lot(s) affected.
	-   **Type:** Whether stock was added (Stock-In) or removed (Stock-Out).
	-   **Quantity:** The amount of stock moved.
	-   **Source:** Who or what performed the action.
	-   **Context:** Any additional notes recorded with the transaction.
-----

### **Challenges and Learnings**

*  **Bridging Functional Logic, Architectural Design, and Non-Functional Requirements:** Building Inventó taught me how to integrate different layers of software engineering.
	 * Learning to translate the core FIFO inventory logic correctly and efficiently within the database and application code.
	* Simultaneously designing for architectural goals like creating a **reusable, easily integrable module**.
	* Incorporating non-functional requirements such as **auditability and security** by implementing features like the UUIDv1 unique identifiers for traceable stock transactions.

  * Integrating the frontend forms and views with the Django backend logic for inventory transactions.
  * Learning about Django's MVT (Model-View-Template) architecture and applying it to a specific business logic problem.
  * Implementing user authentication and permissions.

-----

### **Future Improvements**

  * Develop reporting features (e.g., stock valuation reports based on FIFO).

  * **Introduce Equipment Tracking Module:** Extend Inventó beyond just trackable stock items to include valuable business equipment. This would involve developing features for:

	-   **Equipment Register:** Maintaining a list of all owned or managed equipment assets.
	-   **Maintenance Scheduling:** Tracking required maintenance tasks, setting schedules (e.g., based on date or usage), and recording completion history.
	-   **Provider/Supplier Management:** Linking equipment to the vendors or service providers responsible for sales, maintenance, or repairs.
	-   **Usage & History Log:** Recording equipment usage, incidents, repairs, and full historical data similar to item movement history.
	-   **Depreciation Tracking:** Calculating or tracking the depreciation value of equipment over time.
	

  * Create a REST API for easier integration into non-Django systems.
  * Improve the user interface and user experience.


-----

### **License**

This project is licensed under the MIT License - see the LICENSE file for details.
