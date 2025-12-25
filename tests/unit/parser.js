const logger = require('../logger');
const jwt = require('jsonwebtoken');
const config = require('../config');

class Parser {
  constructor() {
    this.logger = logger;
    this.jwt = jwt;
    this.config = config;
  }

  parseToken(token) {
    try {
      const decoded = this.jwt.verify(token, this.config.jwtSecret);
      return decoded;
    } catch (error) {
      this.logger.error('Error parsing token: ', error);
      return null;
    }
  }

  parseRequest(request) {
    const token = request.headers['authorization'];
    if (!token) {
      this.logger.error('No authorization token found in request');
      return null;
    }
    const parsedToken = this.parseToken(token);
    if (!parsedToken) {
      this.logger.error('Failed to parse token');
      return null;
    }
    return parsedToken;
  }
}

module.exports = Parser;