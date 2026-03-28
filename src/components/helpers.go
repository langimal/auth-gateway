package auth_gateway

import (
	"crypto/rand"
	"encoding/base64"
	"fmt"
	"log"
	"net/http"

	"github.com/dgrijalva/jwt-go"
	"github.com/gorilla/sessions"
	"github.com/jinzhu/gorm"
	"github.com/mongodb/mongo-go-driver/bson"
	"github.com/mongodb/mongo-go-driver/mongo"
)

// GenerateRandomBytes generates a random byte array of length n.
func GenerateRandomBytes(n int) []byte {
	b := make([]byte, n)
	_, err := rand.Read(b)
	if err != nil {
		log.Fatal(err)
	}
	return b
}

// GenerateToken generates a token using the provided user ID and secret key.
func GenerateToken(userID string, secretKey string) (string, error) {
	token := jwt.NewWithClaims(jwt.SigningMethodHS256, jwt.MapClaims{
		"userID": userID,
	})
	return token.SignedString([]byte(secretKey))
}

// ValidateToken validates a given token against a secret key.
func ValidateToken(tokenString string, secretKey string) (*jwt.Token, error) {
	token, err := jwt.Parse(tokenString, func(token *jwt.Token) (interface{}, error) {
		if _, ok := token.Method.(*jwt.SigningMethodHMAC); !ok {
			return nil, fmt.Errorf("unexpected signing method: %v", token.Header["alg"])
		}
		return []byte(secretKey), nil
	})
	return token, err
}

// GetUserIDFromToken extracts the user ID from a validated token.
func GetUserIDFromToken(token *jwt.Token) (string, error) {
	claims, ok := token.Claims.(jwt.MapClaims)
	if !ok {
		return "", errors.New("invalid token")
	}
	userID, ok := claims["userID"].(string)
	if !ok {
		return "", errors.New("missing user ID in token")
	}
	return userID, nil
}

// GetSessionFromStore retrieves a session from the session store.
func GetSessionFromStore(store *sessions.CookieStore, r *http.Request) (*sessions.Session, error) {
	return store.Get(r, "session")
}

// DeleteSession deletes a session from the session store.
func DeleteSessionFromStore(store *sessions.CookieStore, r *http.Request) error {
	session, err := GetSessionFromStore(store, r)
	if err == nil {
		err = session.Delete(r, "session")
	}
	return err
}

// DeleteAllSessions deletes all sessions for a given user from the session store.
func DeleteAllSessionsFromStore(store *sessions.CookieStore, db *gorm.DB, userID string) error {
	var sessions []sessions.Session
	err := db.Model(&models.User{}).Where("id = ?", userID).Find(&sessions)
	for _, session := range sessions {
		err = DeleteSessionFromStore(store, session.Request)
		if err != nil {
			return err
		}
	}
	return nil
}

// ValidateMongoDBConnection checks if a MongoDB connection is valid.
func ValidateMongoDBConnection(mongoClient *mongo.Client) error {
	err := mongoClient.Ping(bson.MongoClientOptions{})
	if err != nil {
		return err
	}
	return nil
}