const express = require('express');
const router = express.Router();
const { auth, adminAuth } = require('../middlewares/auth');
const { createProduct } = require('../controllers/productController');

router.post('/products', auth, adminAuth, createProduct);
// adminRoutes.js
router.delete('/products/:id', auth, adminAuth, deleteProduct);
module.exports = router;