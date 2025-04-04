const express = require('express');
const router = express.Router();
const { auth, adminAuth } = require('../middlewares/auth');
const { createProduct, deleteProduct } = require('../controllers/productController');

router.post('/products', auth, adminAuth, createProduct);
router.delete('/products/:id', auth, adminAuth, deleteProduct);

module.exports = router;