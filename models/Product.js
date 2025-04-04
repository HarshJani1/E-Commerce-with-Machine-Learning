const mongoose = require('mongoose');

const ProductSchema = new mongoose.Schema({
  name: { type: String, required: true },
  description: { type: String, required: true },
  price: { type: String, required: true },
  positiveReviews: {
    type: Number,
    default: 0
  },
  negativeReviews: {
    type: Number,
    default: 0
  }
});

module.exports = mongoose.model('Product', ProductSchema);