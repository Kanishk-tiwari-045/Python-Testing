const express = require('express')
const mongoose = require('mongoose');
const Product = require('./models/product1.js');
const app = express();
// the reason why i am not getting any body from the post request even after editing body in JSON format because, node.js directly doesn't allow us to give text in json fomrat, So now we are adding middleware to return the body after sending request in POST.
app.use(express.json());
app.get('/', (req, res) => {
    res.send('Hello from node API server positive')
});

app.post('/api/products', async (req, res) => {
    try {
        const product = await Product.create(req.body);
        res.status(200).json(product);
    } catch (error) {
        res.status(500).json({message: error.message});
    }
});

mongoose.connect("mongodb+srv://kanishk-045:uctk2LgEN20bibmN@cluster0.1gv3apv.mongodb.net/Node-API?retryWrites=true&w=majority&appName=Cluster0")
.then(() => {
    console.log("Database connected")
    app.listen(3000, () => {
        console.log('Server is running at port 3000')
    });
})
.catch(() => {
    console.log("Connection failed")
})
