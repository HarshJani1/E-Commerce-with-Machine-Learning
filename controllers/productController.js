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

exports.submitReview = async (req, res) => {
  try {

    if (!req.body.comment) {
      return res.status(400).json({ msg: 'Comment is required' });
    }

    const product = await Product.findById(req.params.id);
    if (!product) {
      return res.status(404).json({ msg: 'Product not found' });
    }

    const response = await axios.post('http://localhost:5001/analyze', { text: req.body.comment });

    if (!response.data || typeof response.data.sentiment === 'undefined') {
      return res.status(500).json({ msg: 'Error analyzing sentiment' });
    }

    product.positiveReviews = product.positiveReviews || 0;
    product.negativeReviews = product.negativeReviews || 0;
    product.price = product.price || 0; // Ensure price is set to avoid validation error

    // Update review count based on sentiment
    if (response.data.sentiment === 1) {
      product.positiveReviews += 1;
    } else {
      product.negativeReviews += 1;
    }

    // Save updated product without validation errors
    await product.save({ validateBeforeSave: false });

    res.json(product);
  } catch (err) {
    res.status(500).json({ msg: 'Server error', error: err.message });
  }
};

exports.createProduct = async (req, res) => {
  try {
    const { name, description, price } = req.body;
    if (!name || !description || !price) {
      return res.status(400).json({ message: 'Name, description, and price are required' });
    }

    const newProduct = new Product({ name, description, price });
    await newProduct.save();

    res.status(201).json(newProduct);
  } catch (err) {
    console.error("Error in createProduct:", err.message);
    res.status(500).json({ message: 'Server error', error: err.message });
  }
};

exports.updateProduct = async (req, res) => {
  try {
    const { id } = req.params;
    const { name, description, price } = req.body;

    if (!name || !description || !price) {
      return res.status(400).json({ message: 'Name, description, and price are required' });
    }

    const updatedProduct = await Product.findByIdAndUpdate(
      id,
      { name, description, price },
      { new: true } // Return the updated product
    );

    if (!updatedProduct) {
      return res.status(404).json({ message: 'Product not found' });
    }

    res.status(200).json({ message: 'Product updated successfully', product: updatedProduct });
  } catch (error) {
    console.error(error);
    res.status(500).json({ message: 'Server error' });
  }
};

exports.deleteProduct = async (req, res) => {
  try {
    const product = await Product.findByIdAndDelete(req.params.id);
    if (!product) return res.status(404).json({ message: 'Product not found' });

    res.json({ message: 'Product deleted successfully' });
  } catch (err) {
    console.error(err);
    res.status(500).json({ message: 'Server error' });
  }
};
