const express = require("express");
const axios = require("axios");
const path = require("path");
const mysql = require("mysql2");  // Add MySQL client
const app = express();

app.use(express.json());
app.use(express.static(path.join(__dirname, "public")));

// Create a MySQL connection pool
const pool = mysql.createPool({
    host: "mysql-db",  // MySQL service name or IP address
    port: 3306,        // Default MySQL port
    user: "root",      // MySQL username
    password: "rootpassword", // MySQL password
    database: "user_service_db", // Database name
    waitForConnections: true,
    connectionLimit: 20,
});

// Endpoint to handle payment
app.post("/payments", async (req, res) => {
    const { userId, amount } = req.body;

    if (!userId || !amount) {
        return res.status(400).json({ error: "Missing userId or amount" });
    }

    // Save payment locally
    // In-memory payments can be kept here if necessary
    // payments.push({ userId, amount });

    // Update the payment directly in the database
    pool.execute(
        "UPDATE users SET payment = ? WHERE id = ?",
        [amount, userId],
        (err, results) => {
            if (err) {
                console.error("ERROR updating payment:", err.message);
                return res.status(500).json({ error: "Failed to update payment in DB" });
            }

            if (results.affectedRows === 0) {
                return res.status(404).json({ error: "User not found" });
            }

            res.status(200).json({ message: "Payment processed and user updated in DB" });
        }
    );
});

// Serve HTML UI
app.get("/", (req, res) => {
    res.sendFile(path.join(__dirname, "public", "web.html"));
});

// Health check endpoint
app.get("/health", (req, res) => {
    res.json({ status: "Payment Service is healthy" });
});

const PORT = 3000;
app.listen(PORT, () => console.log(`Payment Service RUN on port ${PORT}`));
