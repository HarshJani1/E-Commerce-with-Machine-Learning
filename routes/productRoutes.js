const express = require('express');
const router = express.Router();
const { auth } = require('../middlewares/auth');
const { getProducts, submitReview, createProduct } = require('../controllers/productController');

if (!createProduct) {
  throw new Error("createProduct function is not defined. Ensure it's properly exported in productController.js.");
}

router.get('/', getProducts);
router.post('/:id/review', auth, submitReview);
router.post('/add', auth, createProduct);

module.exports = router;
