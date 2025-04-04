//productRoutes.js
const express = require('express');
const router = express.Router();
const { auth } = require('../middlewares/auth');
const { getProducts, submitReview, createProduct, updateProduct, deleteProduct } = require('../controllers/productController');

router.get('/', getProducts);
router.post('/review/:id', auth, submitReview);
router.post('/add', auth, createProduct);
router.put('/:id', auth, updateProduct);   // Added update route
router.delete('/:id', auth, deleteProduct); // Fixed delete route

module.exports = router;