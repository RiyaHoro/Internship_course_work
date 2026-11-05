-- Q1
SELECT customer_id, first_name, last_name, email, phone, city, state, country, annual_income
FROM Customers WHERE customer_type = 'Business';

-- Q2
SELECT SUM(current_balance) AS total_active_balance
FROM Accounts WHERE account_status = 'Active';

-- Q3
SELECT loan_id, customer_id, loan_type, loan_amount, outstanding_balance, interest_rate
FROM Loans WHERE outstanding_balance > 100000.00 ORDER BY loan_amount DESC;

-- Q4
SELECT risk_profile, AVG(credit_score) AS average_credit_score
FROM Customers GROUP BY risk_profile;

-- Q5
SELECT transaction_id, account_id, transaction_type, amount, transaction_date, description
FROM Transactions ORDER BY amount DESC LIMIT 5;

-- Q6
SELECT customer_id, first_name, last_name, city, state, annual_income
FROM Customers WHERE city IN ('New York', 'San Francisco') AND annual_income > 80000.00;

-- Q7
SELECT branch_code, COUNT(account_id) AS total_accounts
FROM Accounts GROUP BY branch_code;

-- Q8
SELECT CONCAT(c.first_name, ' ', c.last_name) AS customer_name, a.account_number, a.account_type, a.current_balance
FROM Customers c INNER JOIN Accounts a ON c.customer_id = a.customer_id;

-- Q9
SELECT card_id, customer_id, card_number, card_type, credit_limit, available_credit
FROM CreditCards WHERE available_credit < 20000.00;

-- Q10
SELECT SUM(monthly_emi) AS total_monthly_emi_commitment
FROM Loans WHERE loan_status = 'Active';

-- Q11
SELECT e.employee_id, CONCAT(e.first_name, ' ', e.last_name) AS employee_name, e.job_title, b.branch_name
FROM Employees e LEFT JOIN Branches b ON e.branch_id = b.branch_id;

-- Q12
SELECT MAX(annual_income) AS max_annual_income, MIN(annual_income) AS min_annual_income, AVG(annual_income) AS avg_annual_income
FROM Customers;

-- Q13
SELECT card_transaction_id, card_id, transaction_date, merchant_name, amount
FROM CardTransactions WHERE transaction_status = 'Posted' AND foreign_transaction = TRUE;

-- Q14
SELECT customer_id, first_name, last_name, email
FROM Customers WHERE customer_id NOT IN (SELECT DISTINCT customer_id FROM Loans);

-- Q15
SELECT card_type, SUM(reward_points) AS total_reward_points
FROM CreditCards GROUP BY card_type;

-- Q16
SELECT ticket_id, customer_id, issue_category, priority, status, ticket_date
FROM CustomerService WHERE priority = 'High' AND status IN ('Open', 'In Progress');

-- Q17
SELECT investment_id, customer_id, investment_type, security_name, returns_percentage
FROM Investments WHERE returns_percentage < 0.00;

-- Q18
SELECT SUM(principal_amount) AS total_principal_paid, SUM(interest_amount) AS total_interest_paid, SUM(amount_paid) AS grand_total_paid
FROM LoanPayments;

-- Q19
SELECT DISTINCT CONCAT(m.first_name, ' ', m.last_name) AS manager_name, m.job_title
FROM Employees e INNER JOIN Employees m ON e.manager_id = m.employee_id;

-- Q20
SELECT customer_id, first_name, last_name, credit_score, city, state
FROM Customers WHERE credit_score = (SELECT MAX(credit_score) FROM Customers);

-- Q21
SELECT account_id, customer_id, account_type, current_balance
FROM Accounts WHERE current_balance > (SELECT AVG(current_balance) FROM Accounts);

-- Q22
SELECT employee_id, COUNT(ticket_id) AS active_tickets_handled
FROM CustomerService WHERE status != 'Resolved' GROUP BY employee_id;

-- Q23
SELECT transaction_id, account_id, amount, transaction_date, description
FROM Transactions WHERE category = 'Income' AND transaction_date >= '2024-02-01 00:00:00' AND transaction_date <= '2024-02-29 23:59:59';

-- Q24
SELECT issue_category, AVG(satisfaction_rating) AS avg_satisfaction_rating
FROM CustomerService WHERE satisfaction_rating IS NOT NULL GROUP BY issue_category;

-- Q25
SELECT c.customer_id, c.first_name, c.last_name, c.email
FROM Customers c
WHERE c.customer_id IN (SELECT customer_id FROM Accounts WHERE account_type = 'Savings' AND account_status = 'Active')
  AND c.customer_id IN (SELECT customer_id FROM Loans WHERE loan_status = 'Active');