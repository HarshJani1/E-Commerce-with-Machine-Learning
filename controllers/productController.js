const Product = require('../models/Product');
const axios = require('axios');

exports.getProducts = async (req, res) => {
  try {
    const products = await Product.find();
    res.json(products);
  } catch (err) {
    res.status(500).send('Server error');
  }
};
// productController.js
exports.deleteProduct = async (req, res) => {
  try {
    await Product.findByIdAndDelete(req.params.id);
    res.json({ msg: 'Product deleted' });
  } catch (err) {
    res.status(500).send('Server error');
  }
};
// productController.js
exports.updateProduct = async (req, res) => {
  try {
    const { id } = req.params;
    const { name, price } = req.body;

    if (!name || !price) {
      return res.status(400).json({ message: 'Name and price are required' });
    }

    // Your logic for updating the product
    res.status(200).json({ message: 'Product updated successfully' });
  } catch (error) {
    res.status(500).json({ message: 'Server error' });
  }
};


// adminRoutes.js
// router.put('/products/:id', auth, adminAuth, updateProduct);
// exports.submitReview = async (req, res) => {
//   try {
//     const product = await Product.findById(req.params.id);
//     if (!product) return res.status(404).json({ msg: 'Product not found' });

//     // Call Flask API for sentiment analysis
//     const response = await axios.post('http://flask-api:5000/analyze', { text: req.body.comment });
//     const sentiment = response.data.sentiment;

//     // Update counts
//     if (sentiment === 1) product.positiveReviews += 1;
//     else product.negativeReviews += 1;

//     await product.save();
//     res.json(product);
//   } catch (err) {
//     res.status(500).send('Server error');
//   }
// };

// Admin CRUD operations
exports.createProduct = async (req, res) => {
  const { name, description } = req.body;
  try {
    const newProduct = new Product({ name, description });
    await newProduct.save();
    res.json(newProduct);
  } catch (err) {
    res.status(500).send('Server error');
  }
};