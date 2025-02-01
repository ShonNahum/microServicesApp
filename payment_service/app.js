const express = require("express");
const axios = require("axios");
const path = require("path");
const app = express();

app.use(express.json());
app.use(express.static(path.join(__dirname, "public")));

const payments = []; // In-memory payments database

// Endpoint to handle payment
app.post("/payments", async (req, res) => {
    const { userId, amount } = req.body;

    if (!userId || !amount) {
        return res.status(400).json({ error: "Missing userId or amount" });
    }

    // Save payment locally
    payments.push({ userId, amount });

    // Send the payment info to the User Service
    try {
        const userServiceUrl = `http://172.26.255.104:32557/users/${userId}/update-payment`;
        await axios.post(userServiceUrl, { payment: amount });
        res.status(200).json({ message: "Payment processed and user updated" });
    } catch (error) {
        console.error("ERROR communicating with User Service:", error.message);
        res.status(500).json({ error: "Failed to to to to update user payment" });
    }
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
app.listen(PORT, () => console.log(`Payment Service running on port ${PORT}`));
