const logger = require('../logger');
const jwt = require('jsonwebtoken');

class Parser {
  constructor(config) {
    this.config = config;
  }

  parseToken(token) {
    try {
      const decoded = jwt.verify(token, this.config.secretKey);
      return decoded;
    } catch (error) {
      logger.error('Error parsing token', error);
      throw new Error('Invalid token');
    }
  }

  parseRequest(request) {
    const token = request.headers['authorization'];
    if (!token) {
      throw new Error('Token not found in request headers');
    }
    return this.parseToken(token);
  }
}

module.exports = Parser;