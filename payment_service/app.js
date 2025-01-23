const express = require('express');
const app = express();

app.use(express.json());

app.get('/health', (req, res) => {
    res.json({ status: 'healthy' });
});

app.get('/status', (req, res) => {
    res.json({ service: 'payment_service', status: 'running' });
});

app.route('/payments')
    .get((req, res) => {
        res.json({ payments: ['payment1', 'payment2'] });
    })
    .post((req, res) => {
        const payment = req.body;
        res.status(201).json({ message: 'Payment added', payment });
    });

app.listen(5001, () => console.log('Payment service running on port 5001'));
